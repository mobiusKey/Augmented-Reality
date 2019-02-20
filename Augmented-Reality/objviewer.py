# Basic OBJ file viewer. needs objloader from:
#  http://www.pygame.org/wiki/OBJFileLoader
# LMB + move: rotate
# RMB + move: pan
# Scroll wheel: zoom in/out
import sys, pygame
from pygame.locals import *
from pygame.constants import *
from OpenGL.GL import *
from OpenGL.GLU import *

# IMPORT OBJECT LOADER
from objloader import *

pygame.init()
viewport = (800,600)
hx = viewport[0]/2
hy = viewport[1]/2
srf = pygame.display.set_mode(viewport, OPENGL | DOUBLEBUF)

glLightfv(GL_LIGHT0, GL_POSITION,  (-40, 200, 100, 0.0))
glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
glEnable(GL_LIGHT0)
glEnable(GL_LIGHTING)
glEnable(GL_COLOR_MATERIAL)
glEnable(GL_DEPTH_TEST)
#glShadeModel(GL_SMOOTH)		   # most obj files expect to be smooth-shaded

# LOAD OBJECT AFTER PYGAME INIT
obj = OBJ('./models/Dragon', swapyz=True)

clock = pygame.time.Clock()

glMatrixMode(GL_PROJECTION)
glLoadIdentity()
width, height = viewport
gluPerspective(90.0, width/float(height), 1, 100.0)
glEnable(GL_DEPTH_TEST)
glMatrixMode(GL_MODELVIEW)

rx, ry = (0,0)
tx, ty = (0,0)
zrot = 0
zpos = 5
rotate = move = False
while True:
	keys = pygame.key.get_pressed()
	
	for e in pygame.event.get():
		if e.type == QUIT:
			sys.exit()
		elif e.type == KEYDOWN and e.key == K_ESCAPE:
			sys.exit()
		elif e.type == MOUSEBUTTONDOWN:
			if e.button == 4: zpos = max(1, zpos-1)
			elif e.button == 5: zpos += 1
			elif e.button == 1: rotate = True
			elif e.button == 3: move = True
		elif e.type == MOUSEBUTTONUP:
			if e.button == 1: rotate = False
			elif e.button == 3: move = False 
		elif e.type == MOUSEMOTION:
			i, j = e.rel
			if rotate:
				rx += i
				ry += j
			if move:
				tx += i
				ty -= j
			
			
	if keys[pygame.K_w]:
		ty += 1
		print("w was pressed")
	if keys[pygame.K_a]:
		tx -= 1
		print("a was pressed")			
	if keys[pygame.K_s]:
		ty -= 1
		print("s was pressed")
	if keys[pygame.K_d]:
		tx += 1
		print("d was pressed")
		
	if keys[pygame.K_UP]:
		ry += 1
	if keys[pygame.K_DOWN]:
		ry -= 1
	if keys[pygame.K_LEFT]:
		rx -= 1
	if keys[pygame.K_RIGHT]:
		rx += 1
		
	if keys[pygame.K_SPACE]:
		zpos += 1
	if keys[pygame.K_LSHIFT]:
		zpos -= 1
	if keys[pygame.K_PERIOD]:
		zrot += 1
	if keys[pygame.K_COMMA]:
		zrot -= 1
		
	print("x:{} y:{} z:{}\nrx:{} ry:{}".format(tx, ty, zpos, rx, ry))

	clock.tick(30)

	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()

	# RENDER OBJECT
	#scaling seems to help with the dragon
	glScalef(0.5,0.5,0.5)
	
	glTranslate(tx/20., ty/20., - zpos)
	glRotate(ry, 1, 0, 0)
	glRotate(rx, 0, 1, 0)
	# need to add yaw gl rotate
	glRotate(zrot, 0, 0, 1)
	glCallList(obj.gl_list)
	

	pygame.display.flip()