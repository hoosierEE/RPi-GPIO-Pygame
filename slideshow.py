# Cycle images (like a slideshow) using a rotary encoder.
import pygame
from pygame.color import Color
from RPi import GPIO  # Raspberry Pi only!

# hard-coded list of image pathnames (replace with your real image list)
slides = [ "../images/slide1.png", "../images/slide2.png", "../images/slide3.png" ]

# woo global variables!
state = 0
counter = 0
direction = 1
def rotate_event(pin):
        """
        Convert rotary encoder pulses into a new image index to be used
        by the main game loop.  This function occurs on a separate thread.
        """
	global state
	global counter
	global direction
	ra = GPIO.input(22)
	rb = GPIO.input(23)
        # some bit twiddling to turn quadrature into ordinal encoding
	ns = (ra ^ rb) | rb << 1
	if state == ns: # no change since last time
		return
	dt = (ns - state) % 4
	if dt == 3:
		direction = -1
	elif dt == 1:
		direction = 1
	counter = (counter + direction) % length(slides)
	state = ns

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
switch_pins = [22, 23]  # rotary encoder pins
for pin in switch_pins:
	GPIO.setup(pin, GPIO.IN, GPIO.PUD_UP)
	GPIO.add_event_detect(pin, GPIO.BOTH, rotate_event)

def render_output(path_to_image):
	img = pygame.image.load(path_to_image)
	screen.blit(img,(0,0))

pygame.init()
pygame.display.set_caption("RPi GPIO Slideshow")
screen = pygame.display.set_mode([1200,800])
clock = pygame.time.Clock()
done = False
while not done:
	screen.fill(Color('white'))  # TODO: is this required?
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
	render_output(slides[counter])
	clock.tick(33) # note: actual fps seems to top out around clock.tick(10)
	pygame.display.flip()
