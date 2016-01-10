
# Cycle images (like a slideshow) using a rotary encoder.

import pygame
from pygame.color import Color
from RPi import GPIO  # Raspberry Pi only!

# each of these contains a list of image pathnames, i.e.
# tops = [ "../images/top1.png", "../images/top2.png", ... ]
from tops import tops
from sides import sides
from backs import backs

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
	ns = (ra ^ rb) | rb << 1
	dt = (ns - state) % 4
	if state == ns:
		return
	if dt == 3:
		direction = -1
	elif dt == 1:
		direction = 1
	counter = (counter + direction) % 500
	state = ns

def render_output():
        """
        put the image (selected by counter) on the screen
        """
	img = pygame.image.load(tops[counter])
	screen.blit(img,(0,0))

# Raspberry Pi GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
sw_pins = [22, 23]  # rotary encoder
for pin in sw_pins:
	GPIO.setup(pin, GPIO.IN, GPIO.PUD_UP)
	GPIO.add_event_detect(pin, GPIO.BOTH, rotate_event)

pygame.init()
size = 1200,800 # TODO: fullscreen, fit images
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 25, True)
pygame.display.set_caption("RPi GPIO Slideshow")

done = False
while not done:
	# screen.fill(Color('white'))  # TODO: is this required?
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
	render_output()
	clock.tick(33) # note: with the image sizes I used, max refresh is ~12fps
	pygame.display.flip()
