import pygame as pg
from time import sleep
from Bevel import Bevel
from Map import Map
from Tile import Tile
from TiledMap import TiledMap
from SelectionPanel import SelectionPanel
from TileButtonArray import TileButtonArray
from threading import Thread, Event
from DrawTools import *
from ControlButton import *

# for Threading
def proccess_mouse_events():
	global mouse_events
	global tiled_screen
	global QUIT
	global screen
	global CHANGED_POSITIONS
	global slpan

	while(not QUIT):
		try:
			ev = mouse_events.pop(-1)
		except:
			sleep(0.01)
			continue

		if(ev == "Left"):
			tiled_screen.set_map_value(CHANGED_POSITIONS, slpan.get())
			CHANGED_POSITIONS = []
		elif(ev == "Right"):
			flood_list = flood_fill(tiled_screen, tupsum(tuple(get_grid_square(pg.mouse.get_pos())), tiled_screen.win_cord), slpan.get(), [])
			if(not flood_list):
				continue
			tiled_screen.set_map_value(flood_list, slpan.get())
			flood_list = []
		sleep(0.01)

def tupsum(tuple1, tuple2):
	return (tuple1[0]+tuple2[1], tuple1[1]+tuple2[0])

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
	global slpan
	global ctrlbtnarray
	global screen
	global LOCK
	global tiled_screen
	global HOLD_MCLICK
	global SELECTED_TILE

	# Scroll function
	if(ev.type == pg.MOUSEBUTTONDOWN and ev.button == 4):
		if(slpan.select(slpan.selected-1)):
			LOCK.clear()
			slpan.draw_selected(screen)
			LOCK.set()
	elif(ev.type == pg.MOUSEBUTTONDOWN and ev.button == 5):
		if(slpan.select(slpan.selected+1)):
			LOCK.clear()
			slpan.draw_selected(screen)
			LOCK.set()

	# Mid Click
	if(ev.type == pg.MOUSEBUTTONDOWN and ev.button == 2):
		HOLD_MCLICK = True
		SELECTED_TILE = get_grid_square(pg.mouse.get_pos())

	elif(ev.type == pg.MOUSEBUTTONUP and ev.button == 2 and HOLD_MCLICK):
		HOLD_MCLICK = False
		new_square = get_grid_square(pg.mouse.get_pos())
		dxy = (SELECTED_TILE[0] - new_square[0], SELECTED_TILE[1] - new_square[1])
		tiled_screen.win_move(dx= dxy[1], dy= dxy[0])

	if(ev.type == pg.MOUSEMOTION and HOLD_LCLICK): # Draw continuum
		CHANGED_POSITIONS.append(tupsum(get_grid_square(pg.mouse.get_pos()), tiled_screen.win_cord))

	elif(ev.type == pg.MOUSEBUTTONUP and ev.button == 1):
		HOLD_LCLICK = False	
		mouse_events.append("Left")

	elif(ev.type == pg.MOUSEBUTTONDOWN and ev.button == 1): # Left Click
		if(pg.mouse.get_pos()[1] <= 4*WIN_HEIGHT/5): # On TiledMap
			CHANGED_POSITIONS.append(tupsum(get_grid_square(pg.mouse.get_pos()), tiled_screen.win_cord))
			HOLD_LCLICK = True
		else:  # In panels
			for button in tbarray: # in Tiles Bevel
				if(button.click(pg.mouse.get_pos()) != None):
					slpan.update_selected(button.click(pg.mouse.get_pos()))
					slpan.draw_tiles(screen)
					return
			if(slpan.click(screen, pg.mouse.get_pos())): # Checks and handles Selection panel clicks
				LOCK.clear()
				slpan.draw_selected(screen)
				LOCK.set()
				return
			for but in ctrlbtnarray:
				if(but.click(pg.mouse.get_pos())):
					m, cord = but.action(tiled_screen)
					if(m != None):
						tiled_screen.load_map(m)
						tiled_screen.win_cord = cord
					return
	elif(ev.type == pg.MOUSEBUTTONDOWN and ev.button == 3): # Right Click
		mouse_events.append("Right")	

	elif(ev.type == pg.QUIT):
		QUIT = True

def handle_keyboard(ev):
	global QUIT
	global tiled_screen
	global DRAW_GRID
	global LOCK
	global tbarray
	global slpan
	global screen

	mods = pg.key.get_mods()
	if(pg.key.name(ev.key) == "escape"): # ESC
		QUIT = True
	elif(pg.key.name(ev.key) == "tab"): # Tab
		DRAW_GRID = not DRAW_GRID
		if(not DRAW_GRID):
			LOCK.clear()
			tiled_screen.clear_grid(screen)
			LOCK.set()

	# Number keys
	try:
		num = int(pg.key.name(ev.key))
		if(num != 0):
			if(slpan.select(int(pg.key.name(ev.key))-1)):
				LOCK.clear()
				slpan.draw_selected(screen)
				LOCK.set()
			return
	except:
		pass

	if(pg.key.name(ev.key) == "z" and mods & pg.KMOD_CTRL): # Ctrl + Z
		tiled_screen.undo_map()

	elif(pg.key.name(ev.key) == "a" and mods & pg.KMOD_SHIFT):
		tiled_screen.win_move(dx=-30)	
	elif(pg.key.name(ev.key) == "d" and mods & pg.KMOD_SHIFT):
		tiled_screen.win_move(dx=30)
	elif(pg.key.name(ev.key) == "s" and mods & pg.KMOD_SHIFT):
		tiled_screen.win_move(dy=30)
	elif(pg.key.name(ev.key) == "w" and mods & pg.KMOD_SHIFT):
		tiled_screen.win_move(dy=-30)

	elif(pg.key.name(ev.key) == "q"):
		tbarray.change_page(screen, forward=False)
	elif(pg.key.name(ev.key) == "e"):
		tbarray.change_page(screen)

	elif(pg.key.name(ev.key) == "a"):
		tiled_screen.win_move(dx=-1)
	elif(pg.key.name(ev.key) == "d"):
		tiled_screen.win_move(dx=1)
	elif(pg.key.name(ev.key) == "s"):
		tiled_screen.win_move(dy=1)
	elif(pg.key.name(ev.key) == "w"):
		tiled_screen.win_move(dy=-1)

mouse_events = []

pg.init()

screen = pg.display.set_mode((0,0), pg.FULLSCREEN | pg.HWSURFACE | pg.DOUBLEBUF) 
pg.display.set_caption("Chrono Quest")

FPS = 1/60
TICKRATE = 1/20
TILE_SIZE = 32
threads = []
QUIT = False
HOLD_LCLICK = False
HOLD_MCLICK = False
SELECTED_TILE = (0,0)
CHANGED_POSITIONS = []
DRAW_GRID = False
LOCK = Event()
LOCK.set()

info = pg.display.Info()
WIN_WIDTH = info.current_w
WIN_HEIGHT = info.current_h

m = Map([[-1]])

# Bevels
tiles_bev = Bevel(6*WIN_WIDTH/8, WIN_HEIGHT/5, pg.Color(200,200,200,255), (WIN_WIDTH/8,4*WIN_HEIGHT/5))
map_bev = Bevel(WIN_WIDTH, 4*WIN_HEIGHT/5, pg.Color(55,25,25,255), (0,0))
sel_bev = Bevel(WIN_WIDTH/8, WIN_HEIGHT/5, pg.Color(150,150,150,255), (0,4*WIN_HEIGHT/5))
but_bev = Bevel(WIN_WIDTH/8, WIN_HEIGHT/5, pg.Color(40,150,40,255), (7*WIN_WIDTH/8, 4*WIN_HEIGHT/5))

# Draw Bevels
tiles_bev.draw(screen)
sel_bev.draw(screen)
but_bev.draw(screen)

# Buttons
save_btn = SaveButton(screen, (7*WIN_WIDTH/8 + 30, 4*WIN_HEIGHT/5 + 12), "save_btn.png", saveas=False)
saveas_btn = SaveButton(screen, (7*WIN_WIDTH/8 + 30, 4*WIN_HEIGHT/5 + 76), "saveas_btn.png")
load_btn = LoadButton(screen, (7*WIN_WIDTH/8 + 30, 4*WIN_HEIGHT/5 + 140), "load_btn.png")
new_btn = NewButton(screen, (7*WIN_WIDTH/8 + 159, 4*WIN_HEIGHT/5 + 44), "new_btn.png")
ctrlbtnarray = [save_btn, saveas_btn, load_btn, new_btn]

# Tiled Display
tiled_screen = TiledMap(map_bev, m)

# TileButtonArray
tbarray = TileButtonArray(tiles_bev, [WIN_WIDTH/8 +40,4*WIN_HEIGHT/5])

# SelectionPanel
slpan = SelectionPanel(sel_bev, (8,4*WIN_HEIGHT/5))
slpan.draw_selected(screen)

threads.append(Thread(target=screen_refresh))
threads.append(Thread(target=proccess_mouse_events))

for th in threads:
	th.start()

pg.display.flip()
tbarray.draw_buttons(screen)

while(not QUIT):
	for ev in pg.event.get():
		LOCK.wait()
		if(ev.type in [pg.QUIT, pg.MOUSEBUTTONDOWN, pg.MOUSEMOTION, pg.MOUSEBUTTONUP]):
			handle_mouse(ev)
		elif(ev.type in [pg.KEYDOWN]):
			handle_keyboard(ev)
	sleep(FPS/3)
