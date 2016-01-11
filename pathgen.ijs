gp =: 4 :0"0 1  NB. generate pathnames
  NB. _3{.;(i.500)&gp each 'top'
  NB. "../assets/images/clipp/p497.png",
  NB. "../assets/images/clipp/p498.png",
  NB. "../assets/images/clipp/p499.png",
  pre =. '"../assets/images/clip'
  suf =. '.png",'
  pre,y,'/',y,(":x),suf
)

names =. ;((i.500)gp]) each 'top';'back';'side'
'vendor/lst.py' fwrites~ 'lst = [',(,names),']'