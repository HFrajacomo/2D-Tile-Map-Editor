import pygame as pg
import sys
import os
from threading import Event
from time import sleep
from easygui import *

sys.path.append("ModelEditor\\")
from IntegerBox import IntegerBox
from Bevel import Bevel
from ControlButton import *

def update_model():
	global MODEL_SURFACE
	global r_box
	global g_box
	global b_box
	global a_box
	global EDITORMODE
	global screen
	global btnarray
	global FILTER_SURFACE

	FILTER_SURFACE.fill((0,0,0))
	FILTER_SURFACE.fill((r_box.get_value(),g_box.get_value(),b_box.get_value()), special_flags=pg.BLEND_ADD)
	FILTER_SURFACE.set_alpha(a_box.get_value())	
	if(not EDITORMODE): # Tile
		screen.blit(MODEL_SURFACE, (WIN_WIDTH/2-64, WIN_HEIGHT/2-64))
		screen.blit(FILTER_SURFACE, (WIN_WIDTH/2-64, WIN_HEIGHT/2-64))		
		pg.display.update(pg.Rect((WIN_WIDTH/2-64, WIN_HEIGHT/2-64), (128,128)))
	else: # Model
		screen.blit(MODEL_SURFACE, (WIN_WIDTH/2-256, WIN_HEIGHT/2-512))
		screen.blit(FILTER_SURFACE, (WIN_WIDTH/2-256, WIN_HEIGHT/2-512))		
		pg.display.update(pg.Rect((WIN_WIDTH/2-256, WIN_HEIGHT/2-512), (256*2,512*2)))	


def handle_mouse(ev):
	global MODEL_SURFACE
	global FILTER_SURFACE
	global screen
	global EDITORMODE

	if(ev.type == pg.MOUSEBUTTONDOWN and ev.button == 1): # Left Click
		for but in btnarray:
			if(but.click(pg.mouse.get_pos())):
				img, cod = but.action(screen, (WIN_WIDTH, WIN_HEIGHT), MODEL_SURFACE)	
				if(img != None):
					EDITORMODE = cod
					if(EDITORMODE == False):
						FILTER_SURFACE = pg.transform.scale(pg.image.load("ModelEditor\\Images\\none.png"), (128,128))
					else:
						FILTER_SURFACE = pg.transform.scale(pg.image.load("ModelEditor\\Images\\none.png"), (256*2,512*2))		
					MODEL_SURFACE = img
					r_box.reset(screen)
					g_box.reset(screen)
					b_box.reset(screen)
					a_box.reset(screen)
					update_model()
				elif(cod == "newtile"):
					EDITORMODE = False
					FILTER_SURFACE = pg.transform.scale(pg.image.load("ModelEditor\\Images\\none.png"), (128,128))
					r_box.reset(screen)
					g_box.reset(screen)
					b_box.reset(screen)
					a_box.reset(screen)
					update_model()	
				elif(cod == "newmodel"):	
					EDITORMODE = True
					FILTER_SURFACE = pg.transform.scale(pg.image.load("ModelEditor\\Images\\none.png"), (256,512))		
					r_box.reset(screen)
					g_box.reset(screen)
					b_box.reset(screen)
					a_box.reset(screen)
					update_model()	


def handle_keyboard(ev):
	global QUIT
	global r_box

	mods = pg.key.get_mods()

	# Shift
	if(pg.key.name(ev.key) == "w" and mods & pg.KMOD_SHIFT): 
		r_box.change_value(screen, 10)
		update_model()
	elif(pg.key.name(ev.key) == "q" and mods & pg.KMOD_SHIFT): 
		r_box.change_value(screen, -10)
		update_model()
	elif(pg.key.name(ev.key) == "s" and mods & pg.KMOD_SHIFT): 
		g_box.change_value(screen, 10)
		update_model()
	elif(pg.key.name(ev.key) == "a" and mods & pg.KMOD_SHIFT): 
		g_box.change_value(screen, -10)
		update_model()
	elif(pg.key.name(ev.key) == "x" and mods & pg.KMOD_SHIFT): 
		b_box.change_value(screen, 10)
		update_model()
	elif(pg.key.name(ev.key) == "z" and mods & pg.KMOD_SHIFT): 
		b_box.change_value(screen, -10)
		update_model()
	elif(pg.key.name(ev.key) == "2" and mods & pg.KMOD_SHIFT): 
		a_box.change_value(screen, 10)
		update_model()
	elif(pg.key.name(ev.key) == "1" and mods & pg.KMOD_SHIFT): 
		a_box.change_value(screen, -10)
		update_model()

	elif(pg.key.name(ev.key) == "w" and mods & pg.KMOD_CTRL): 
		r_box.change_value(screen, 100)
		update_model()
	elif(pg.key.name(ev.key) == "q" and mods & pg.KMOD_CTRL): 
		r_box.change_value(screen, -100)
		update_model()
	elif(pg.key.name(ev.key) == "s" and mods & pg.KMOD_CTRL): 
		g_box.change_value(screen, 100)
		update_model()
	elif(pg.key.name(ev.key) == "a" and mods & pg.KMOD_CTRL): 
		g_box.change_value(screen, -100)
		update_model()
	elif(pg.key.name(ev.key) == "x" and mods & pg.KMOD_CTRL): 
		b_box.change_value(screen, 100)
		update_model()
	elif(pg.key.name(ev.key) == "z" and mods & pg.KMOD_CTRL): 
		b_box.change_value(screen, -100)
		update_model()
	elif(pg.key.name(ev.key) == "2" and mods & pg.KMOD_CTRL): 
		a_box.change_value(screen, 100)
		update_model()
	elif(pg.key.name(ev.key) == "1" and mods & pg.KMOD_CTRL): 
		a_box.change_value(screen, -100)
		update_model()

	# Normal
	elif(pg.key.name(ev.key) == "w"):
		r_box.change_value(screen, 1)
		update_model()
	elif(pg.key.name(ev.key) == "q"): 
		r_box.change_value(screen, -1)
		update_model()
	elif(pg.key.name(ev.key) == "s"):
		g_box.change_value(screen, 1)
		update_model()
	elif(pg.key.name(ev.key) == "a"): 
		g_box.change_value(screen, -1)
		update_model()
	elif(pg.key.name(ev.key) == "x"):
		b_box.change_value(screen, 1)
		update_model()
	elif(pg.key.name(ev.key) == "z"): 
		b_box.change_value(screen, -1)
		update_model()
	elif(pg.key.name(ev.key) == "2"):
		a_box.change_value(screen, 1)
		update_model()
	elif(pg.key.name(ev.key) == "1"): 
		a_box.change_value(screen, -1)
		update_model()


	elif(pg.key.name(ev.key) == "escape"):
		QUIT = True

pg.init()
pg.font.init()

screen = pg.display.set_mode((0,0), pg.FULLSCREEN | pg.DOUBLEBUF | pg.HWSURFACE)

info = pg.display.Info()
WIN_WIDTH = info.current_w
WIN_HEIGHT = info.current_h

QUIT = False
LOCK = Event()
LOCK.set()
TILEMODE = True
SELECTED_TILE = None
TICKRATE = 1/20
EDITORMODE = False

# Bevels
btn_bvl = Bevel(WIN_WIDTH/8, WIN_HEIGHT/2, pg.Color(150,0,80), (7*WIN_WIDTH/8, WIN_HEIGHT/2))
clr_bvl = Bevel(WIN_WIDTH/8, WIN_HEIGHT/2, pg.Color(30,30,30), (7*WIN_WIDTH/8, 0))

btn_bvl.draw(screen)
clr_bvl.draw(screen)

# RGB Boxes
a_box = IntegerBox(32, (7*WIN_WIDTH/8 + 30, 30), (150,150,150))
a_box.change_value(screen, 0)
r_box = IntegerBox(32, (7*WIN_WIDTH/8 + 30, 70), (255,0,0))
r_box.change_value(screen, 0)
g_box = IntegerBox(32, (7*WIN_WIDTH/8 + 30, 110), (0,255,0))
g_box.change_value(screen, 0)
b_box = IntegerBox(32, (7*WIN_WIDTH/8 + 30, 150), (0,0,255))
b_box.change_value(screen, 0)

# Control Buttons
newtil_btn = NewButton(screen, (7*WIN_WIDTH/8 + 60, WIN_HEIGHT/2 + 20), "newtile_btn.png", False)
newmod_btn = NewButton(screen, (7*WIN_WIDTH/8 + 60, WIN_HEIGHT/2 + 100), "newmodel_btn.png", True)
loadtile_btn = LoadButton(screen, (7*WIN_WIDTH/8 + 60, WIN_HEIGHT/2 + 180), "loadtile_btn.png", False)
loadmodel_btn = LoadButton(screen, (7*WIN_WIDTH/8 + 60, WIN_HEIGHT/2 + 260), "loadmodel_btn.png", True)
save_btn = SaveButton(screen, (7*WIN_WIDTH/8 + 60, WIN_HEIGHT/2 + 340), "save_btn.png")
btnarray = [newtil_btn, newmod_btn, loadtile_btn, loadmodel_btn, save_btn]

# Model Surface
MODEL_SURFACE = pg.transform.scale(pg.image.load("ModelEditor\\Images\\none.png"), (128,128))
FILTER_SURFACE = pg.transform.scale(pg.image.load("ModelEditor\\Images\\none.png"), (128,128))
screen.blit(MODEL_SURFACE, (WIN_WIDTH/2-64, WIN_HEIGHT/2-64))

pg.display.flip()

while(not QUIT):
	for ev in pg.event.get():
		LOCK.wait()
		if(ev.type in [pg.QUIT, pg.MOUSEBUTTONDOWN, pg.MOUSEMOTION, pg.MOUSEBUTTONUP]):
			handle_mouse(ev)
		elif(ev.type in [pg.KEYDOWN]):
			handle_keyboard(ev)
	sleep(TICKRATE)

