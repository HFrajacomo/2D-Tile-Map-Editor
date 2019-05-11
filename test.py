import pygame as pg
from time import sleep
from Bevel import Bevel
from Map import Map
from Tile import Tile
from TiledMap import TiledMap
from TileButtonArray import TileButtonArray
from threading import Thread, Event
from DrawTools import *

# for Threading
def proccess_mouse_events():
	global mouse_events
	global tiled_screen
	global QUIT
	global screen
	global CHANGED_POSITIONS
	global SELECTED_TILE

	while(not QUIT):
		try:
			ev = mouse_events.pop(-1)
		except:
			sleep(0.01)
			continue

		if(ev == "Left"):
			tiled_screen.set_map_value(CHANGED_POSITIONS, SELECTED_TILE)
			CHANGED_POSITIONS = []
		elif(ev == "Right"):
			flood_list = flood_fill(tiled_screen, get_grid_square(list(pg.mouse.get_pos())), SELECTED_TILE, [])
			if(not flood_list):
				continue
			tiled_screen.set_map_value(flood_list, SELECTED_TILE)
			flood_list = []
		sleep(0.01)

# for Threading
def screen_refresh():
	global QUIT
	global DRAW_GRID
	global LOCK

	while(not QUIT):
		LOCK.clear()
		tiled_screen.update_tiles(screen, draw_grid=DRAW_GRID)
		LOCK.set()
		sleep(FPS)

def get_grid_square(pos):
	return [int(pos[1]/TILE_SIZE), int(pos[0]/TILE_SIZE)]


def handle_mouse(ev):
	global QUIT
	global HOLD_LCLICK
	global CHANGED_POSITIONS
	global tbarray
	global SELECTED_TILE

	if(ev.type == pg.MOUSEMOTION and HOLD_LCLICK): # Draw continuum
		CHANGED_POSITIONS.append(get_grid_square(list(pg.mouse.get_pos())))

	elif(ev.type == pg.MOUSEBUTTONUP and ev.button == 1):
		HOLD_LCLICK = False	
		mouse_events.append("Left")

	elif(ev.type == pg.MOUSEBUTTONDOWN and ev.button == 1): # Left Click
		if(pg.mouse.get_pos()[1] <= 4*WIN_HEIGHT/5): # On TiledMap
			CHANGED_POSITIONS.append(get_grid_square(list(pg.mouse.get_pos())))
			HOLD_LCLICK = True
		else:  # In button stream
			for button in tbarray:
				if(button.click(pg.mouse.get_pos()) != None):
					SELECTED_TILE = button.click(pg.mouse.get_pos())
					break

	elif(ev.type == pg.MOUSEBUTTONDOWN and ev.button == 3): # Right Click
		mouse_events.append("Right")	

	elif(ev.type == pg.QUIT):
		QUIT = True

def handle_keyboard(ev):
	global QUIT
	global tiled_screen
	global DRAW_GRID
	global LOCK

	mods = pg.key.get_mods()

	if(pg.key.name(ev.key) == "escape"): # ESC
		QUIT = True
	elif(pg.key.name(ev.key) == "tab"): # Tab
		DRAW_GRID = not DRAW_GRID
		if(not DRAW_GRID):
			LOCK.clear()
			tiled_screen.clear_grid(screen)
			LOCK.set()
	elif(pg.key.name(ev.key) == "z" and mods & pg.KMOD_CTRL): # Ctrl + Z
		tiled_screen.undo_map()


mouse_events = []

pg.init()
screen = pg.display.set_mode((0,0), pg.FULLSCREEN | pg.HWSURFACE)
pg.display.set_caption("Chrono Quest")
FPS = 1/60
TICKRATE = 1/20
TILE_SIZE = 32
threads = []
QUIT = False
HOLD_LCLICK = False
CHANGED_POSITIONS = []
DRAW_GRID = False
LOCK = Event()
LOCK.set()
SELECTED_TILE = 2

info = pg.display.Info()
WIN_WIDTH = info.current_w
WIN_HEIGHT = info.current_h

m = Map([[1,1,1,1,1,1,1,1,1,1,1],[1,0,1,0,1,0,1,0,1,0,1], [1,1,1,1,1,1,1,1,1,1,1]])

# Bevels
tiles_bev = Bevel(6*WIN_WIDTH/8, WIN_HEIGHT/5, pg.Color(200,200,200,255))
map_bev = Bevel(WIN_WIDTH, 4*WIN_HEIGHT/5, pg.Color(55,25,25,255))
sel_bev = Bevel(WIN_WIDTH/8, WIN_HEIGHT/5, pg.Color(150,150,150,255))
but_bev = Bevel(WIN_WIDTH/8, WIN_HEIGHT/5, pg.Color(40,150,40,255))

# Draw Bevels
tiles_bev.draw(screen, [WIN_WIDTH/8,4*WIN_HEIGHT/5])
sel_bev.draw(screen, [0,4*WIN_HEIGHT/5])
but_bev.draw(screen, [7*WIN_WIDTH/8, 4*WIN_HEIGHT/5])

tiled_screen = TiledMap(map_bev, m)

# TileButtonArray
tbarray = TileButtonArray(tiles_bev, [WIN_WIDTH/8 +40,4*WIN_HEIGHT/5])

threads.append(Thread(target=screen_refresh))
threads.append(Thread(target=proccess_mouse_events))

for th in threads:
	th.start()

pg.display.flip()
tbarray.draw_buttons(screen)

while(not QUIT):
	for ev in pg.event.get():
		if(ev.type in [pg.QUIT, pg.MOUSEBUTTONDOWN, pg.MOUSEMOTION, pg.MOUSEBUTTONUP]):
			handle_mouse(ev)
		elif(ev.type in [pg.KEYDOWN]):
			handle_keyboard(ev)
	sleep(FPS/3)
