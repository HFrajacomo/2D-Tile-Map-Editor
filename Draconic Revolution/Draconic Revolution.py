import pygame as pg
import sys
from time import sleep
from threading import Thread, Event

sys.path.append('src\\')

from Bevel import Bevel
from Map import Map
from Tile import Tile
from TiledMap import TiledMap
from Obj import Obj
from ServerHolder import *
from ScreenBevel import ScreenBevel
from CoordBox import CoordBox
from Entity import *


def handle_mouse(ev):
	if(dict_gamestate[GAMESTATE] == 1):
		pass

def handle_keyboard(ev):
	global QUIT
	global OFFSET_POS
	global DISC_POS
	global map_bev
	global movement

	clock.tick(FPS)

	if(pg.key.name(ev.key) == "escape"): # Quit test
		QUIT = True
	elif(pg.key.name(ev.key) == "w"):
		movement["up"] = True
	elif(pg.key.name(ev.key) == "s"):
		movement["down"] = True
	elif(pg.key.name(ev.key) == "a"):
		movement["left"] = True
	elif(pg.key.name(ev.key) == "d"):
		movement["right"] = True
	elif(pg.key.name(ev.key) == "y"):
		movement["kup"] = True
	elif(pg.key.name(ev.key) == "h"):
		movement["kdown"] = True
	elif(pg.key.name(ev.key) == "g"):
		movement["kleft"] = True
	elif(pg.key.name(ev.key) == "j"):
		movement["kright"] = True

def char_movement():
	global movement
	global clock
	global DISC_POS
	global OFFSET_POS
	global QUIT
	global LOCK

	while(not QUIT):
		clock.tick(60)

		LOCK.clear()
		if(movement["up"]):
			DISC_POS[1] -= 1
		if(movement["down"]):
			DISC_POS[1] += 1
		if(movement["left"]):
			DISC_POS[0] -= 1
		if(movement["right"]):
			DISC_POS[0] += 1
		if(movement["kup"]):
			OFFSET_POS = [OFFSET_POS[0], OFFSET_POS[1] -8]
		if(movement["kdown"]):
			OFFSET_POS = [OFFSET_POS[0], OFFSET_POS[1] +8]
		if(movement["kleft"]):
			OFFSET_POS = [OFFSET_POS[0] - 8, OFFSET_POS[1]]
		if(movement["kright"]):
			OFFSET_POS = [OFFSET_POS[0] + 8, OFFSET_POS[1]]
		calculate_player_pos()
		LOCK.set()

def handle_keyups(ev):
	global clock

	clock.tick(FPS)

	if(pg.key.name(ev.key) == "escape"): # Quit test
		QUIT = True
	elif(pg.key.name(ev.key) == "w"):
		movement["up"] = False
	elif(pg.key.name(ev.key) == "s"):
		movement["down"] = False
	elif(pg.key.name(ev.key) == "a"):
		movement["left"] = False
	elif(pg.key.name(ev.key) == "d"):
		movement["right"] = False
	elif(pg.key.name(ev.key) == "y"):
		movement["kup"] = False
	elif(pg.key.name(ev.key) == "h"):
		movement["kdown"] = False
	elif(pg.key.name(ev.key) == "g"):
		movement["kleft"] = False
	elif(pg.key.name(ev.key) == "j"):
		movement["kright"] = False


def calculate_player_pos():
	global DISC_POS
	global OFFSET_POS
	global tiled_map
	global coordbox

	mapsize = tiled_map.map_.get_size()

	if(OFFSET_POS[0]>64):
		DISC_POS[0] += 1
		OFFSET_POS[0] -= 64
	elif(OFFSET_POS[1]>64):
		DISC_POS[1] += 1
		OFFSET_POS[1] -= 64
	if(OFFSET_POS[0]<0):
		DISC_POS[0] -= 1
		OFFSET_POS[0] += 64
	elif(OFFSET_POS[1]<0):
		DISC_POS[1] -= 1
		OFFSET_POS[1] += 64

	if(DISC_POS[0] >= mapsize[0]):
		DISC_POS[0] = 0
	if(DISC_POS[0] < 0):
		DISC_POS[0] = mapsize[0] - 1
	if(DISC_POS[1] >= mapsize[1]):
		DISC_POS[1] = 0
	if(DISC_POS[1] < 0):
		DISC_POS[1] = mapsize[1] - 1

	coordbox.change_value(screen, DISC_POS, tiled_map)

def game_refresher():
	global screen
	global map_bev
	global DISC_POS
	global OFFSET_POS
	global QUIT
	global clock
	global tiled_map
	global inter_map

	while(not QUIT):
		clock.tick(120)
		map_bev.get_window(screen, DISC_POS, OFFSET_POS, player, tiled_map.map_.get_pixel_size(), inter_map)

pg.init()

dict_gamestate = {0:"LOADING", 1:"INGAME"}

screen = pg.display.set_mode((0,0), pg.FULLSCREEN | pg.HWSURFACE | pg.DOUBLEBUF) 
pg.display.set_caption("Draconic Revolution")

FPS = 30
threads = []
QUIT = False
GAMESTATE = 1
OFFSET_POS = [0,0]
DISC_POS = [100,120]
# Map
m, inter_map = loadmap("map\\draconis") # 21x15

# Bevels
map_bev = ScreenBevel(1344, 960, (55,25,25,255), (0,0))  # Sobra x = 96 e y = 120
side_bev = Bevel(480, 1080, (155,155,155), (1440, 0))
minimap_bev = Bevel(300, 300, (200,0,0), (1440,0))
dynamicbuttons_bev = Bevel(180, 300, (200,200,0), (1740,0))
dynamicwindow_bev = Bevel(480, 360, (155,0,255), (1440, 300))
equipment_bev = Bevel(480,270,(80,80,80), (1440, 660))
hotkeys_bev = Bevel(480, 150, (255,255,255), (1440, 930))
lifebar_bev = Bevel(1440,20,(255,0,0),(0,960))
magicbar_bev = Bevel(1440,20,(0,0,255),(0,980))
apbar_bev = Bevel(1440,20,(0,255,0),(0,1000))
guardbar_bev = Bevel(1440,20,(180,0,180),(0,1020))
hungerbar_bev = Bevel(1440,20,(200,120,0),(0,1040))
sleepbar_bev = Bevel(1440,20,(200,200,200),(0,1060))
buttons_bev = Bevel(96,960,(0,50,200),(1344,0))

# Draw Bevels
map_bev.draw(screen)
side_bev.draw(screen)
minimap_bev.draw(screen)
dynamicbuttons_bev.draw(screen)
dynamicwindow_bev.draw(screen)
equipment_bev.draw(screen)
lifebar_bev.draw(screen)
magicbar_bev.draw(screen)
apbar_bev.draw(screen)
guardbar_bev.draw(screen)
hungerbar_bev.draw(screen)
sleepbar_bev.draw(screen)
buttons_bev.draw(screen)

# TiledMap
tiled_map = TiledMap(map_bev, m)

# Setup map
map_bev.load_map(m)
map_bev.build_map(screen, DISC_POS, m)

# CLOCK
clock = pg.time.Clock()

# CoordBox
coordbox = CoordBox(100, (1500, 200), (255,255,255))

# Event
LOCK = Event()
LOCK.set()

# Player
player = Player([DISC_POS[0]+OFFSET_POS[0], DISC_POS[1]+OFFSET_POS[1]], 54, 54, 4)

# Movement Dict
movement = {"up":False, "down":False, "left":False, "right":False, "kup":False, "kdown":False, "kleft":False, "kright":False}

threads.append(Thread(target=game_refresher))
threads.append(Thread(target=char_movement))

for th in threads:
	th.start()

while(not QUIT):
	for ev in pg.event.get():
		if(ev.type in [pg.MOUSEBUTTONDOWN]):#, pg.MOUSEMOTION, pg.MOUSEBUTTONUP]):
			handle_mouse(ev)
		elif(ev.type in [pg.KEYDOWN]):
			handle_keyboard(ev)
		elif(ev.type in [pg.KEYUP]):
			handle_keyups(ev)