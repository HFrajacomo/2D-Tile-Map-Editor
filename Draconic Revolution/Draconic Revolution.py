# Importing Engine

import pyglet as pg
from pyglet.gl import *
from pyglet.window import key
import sys
from threading import Lock
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

# Direct OpenGL commands to this window.
#platform = pg.window.get_platform()
display = pg.canvas.get_display()
screen = display.get_default_screen()
template = pyglet.gl.Config(alpha_size=8)
config = screen.get_best_config(template)
window = pg.window.Window(width=1920, height=1080, fullscreen=True, vsync=False, config=config)
window.set_exclusive_keyboard(exclusive=False)

# Importing Game Structure
sys.path.append('src\\')
from Tile import *
from Map import *
from Obj import *
from TileDictionary import *
from ObjDictionary import *
from Bevel import *
from ServerHolder import *
from NPC import *
from Player import *
from Lightning import *

# Game Events
dispatcher = NPC_Dispatcher()

def list_sum(l1, l2):
	l = l1.copy()
	for i in range(len(l)):
		l[i] += l2[i]

	return l

# Moves animation handle every second
def animate(Non):
	global animation_handle

	if(animation_handle >= 2):
		animation_handle = 0
	else:
		animation_handle += 1

def collision_check(DISC_POS, OFFSET, MOVEMENT_VECTOR):
	global inter_map
	global inter_map_obj
	global PLAYER_DIRECTION

	# Collision to Tiles
	surroundings = get_submatrix(inter_map, DISC_POS, 1,1, non_circular=False)

	if(OFFSET[0]<=0 and MOVEMENT_VECTOR[0] == "L"):
		if(surroundings[1][0].solid):
			return True
	elif(OFFSET[0]>=0 and MOVEMENT_VECTOR[0] == "R"):
		if(surroundings[1][2].solid):
			return True
	elif(OFFSET[1]<=0 and MOVEMENT_VECTOR[0] == "U"):
		if(surroundings[0][1].solid):
			return True	
	elif(OFFSET[1]>=0 and MOVEMENT_VECTOR[0] == "D"):
		if(surroundings[2][1].solid):
			return True

	# Diagonal Correction for Tiles
	if(OFFSET[0]>0 and surroundings[2][2].solid and PLAYER_DIRECTION == 2 and OFFSET[1]>0):
		OFFSET[1] = 0
	elif(OFFSET[0]>0 and surroundings[0][2].solid and PLAYER_DIRECTION == 2 and OFFSET[1]<0):
		OFFSET[1] = 0
	elif(OFFSET[0]<0 and surroundings[2][0].solid and PLAYER_DIRECTION == 3 and OFFSET[1]>0):
		OFFSET[1] = 0
	elif(OFFSET[0]<0 and surroundings[0][0].solid and PLAYER_DIRECTION == 3 and OFFSET[1]<0):
		OFFSET[1] = 0
	
	elif(OFFSET[0]<0 and surroundings[0][0].solid and PLAYER_DIRECTION == 0 and OFFSET[1]<0):
		OFFSET[0] = 0
	elif(OFFSET[0]>0 and surroundings[0][2].solid and PLAYER_DIRECTION == 0 and OFFSET[1]<0):
		OFFSET[0] = 0
	elif(OFFSET[0]<0 and surroundings[2][0].solid and PLAYER_DIRECTION == 1 and OFFSET[1]>0):
		OFFSET[0] = 0
	elif(OFFSET[0]>0 and surroundings[2][2].solid and PLAYER_DIRECTION == 1 and OFFSET[1]>0):
		OFFSET[0] = 0

	del surroundings

	# Collision to Objects
	surroundings = get_submatrix(inter_map_obj, DISC_POS, 1,1, non_circular=False)

	if(OFFSET[0]<=0 and MOVEMENT_VECTOR[0] == "L"):
		if(surroundings[1][0].solid):
			return True
	elif(OFFSET[0]>=0 and MOVEMENT_VECTOR[0] == "R"):
		if(surroundings[1][2].solid):
			return True
	elif(OFFSET[1]<=0 and MOVEMENT_VECTOR[0] == "U"):
		if(surroundings[0][1].solid):
			return True	
	elif(OFFSET[1]>=0 and MOVEMENT_VECTOR[0] == "D"):
		if(surroundings[2][1].solid):
			return True	


	# Diagonal Correction for Objects
	if(OFFSET[0]>0 and surroundings[2][2].solid and PLAYER_DIRECTION == 2 and OFFSET[1]>0):
		OFFSET[1] = 0
	elif(OFFSET[0]>0 and surroundings[0][2].solid and PLAYER_DIRECTION == 2 and OFFSET[1]<0):
		OFFSET[1] = 0
	elif(OFFSET[0]<0 and surroundings[2][0].solid and PLAYER_DIRECTION == 3 and OFFSET[1]>0):
		OFFSET[1] = 0
	elif(OFFSET[0]<0 and surroundings[0][0].solid and PLAYER_DIRECTION == 3 and OFFSET[1]<0):
		OFFSET[1] = 0
	
	elif(OFFSET[0]<0 and surroundings[0][0].solid and PLAYER_DIRECTION == 0 and OFFSET[1]<0):
		OFFSET[0] = 0
	elif(OFFSET[0]>0 and surroundings[0][2].solid and PLAYER_DIRECTION == 0 and OFFSET[1]<0):
		OFFSET[0] = 0
	elif(OFFSET[0]<0 and surroundings[2][0].solid and PLAYER_DIRECTION == 1 and OFFSET[1]>0):
		OFFSET[0] = 0
	elif(OFFSET[0]>0 and surroundings[2][2].solid and PLAYER_DIRECTION == 1 and OFFSET[1]>0):
		OFFSET[0] = 0

	return False

def movement_handler(non):
	global DISC_POS
	global OFFSET
	global LOCK
	global m
	global MOVEMENT_VECTOR
	global p
	global C_LOCK

	if(MOVEMENT_VECTOR == []):
		return

	# Admin Movement
	if(MOVEMENT_VECTOR[0] == "KU"):
		LOCK.acquire()
		DISC_POS = list_sum(DISC_POS, [0,-1])
		p.direction = 0
		LOCK.release()
	elif(MOVEMENT_VECTOR[0] == "KD"):
		LOCK.acquire()
		DISC_POS = list_sum(DISC_POS, [0,1])
		p.direction = 1
		LOCK.release()
	elif(MOVEMENT_VECTOR[0] == "KR"):
		LOCK.acquire()
		DISC_POS = list_sum(DISC_POS, [1,0])
		p.direction = 2
		LOCK.release()
	elif(MOVEMENT_VECTOR[0] == "KL"):
		LOCK.acquire()
		DISC_POS = list_sum(DISC_POS, [-1,0])
		p.direction = 3
		LOCK.release()

	# Collision Check
	if(not collision_check(DISC_POS, OFFSET, MOVEMENT_VECTOR)):
		# Normal Movement
		if(MOVEMENT_VECTOR[0] == "U"):
			LOCK.acquire()
			OFFSET = list_sum(OFFSET, [0,-8])
			LOCK.release()
		elif(MOVEMENT_VECTOR[0] == "D"):
			LOCK.acquire()
			OFFSET = list_sum(OFFSET, [0,8])
			LOCK.release()
		elif(MOVEMENT_VECTOR[0] == "R"):
			LOCK.acquire()
			OFFSET = list_sum(OFFSET, [8,0])
			LOCK.release()
		elif(MOVEMENT_VECTOR[0] == "L"):
			LOCK.acquire()
			OFFSET = list_sum(OFFSET, [-8,0])
			LOCK.release()

	# Tile Change
	if(OFFSET[0]>31):
		OFFSET[0] -= 64
		DISC_POS[0] += 1
	elif(OFFSET[0]<-32):
		OFFSET[0] += 64
		DISC_POS[0] -= 1
	if(OFFSET[1]>31):
		OFFSET[1] -= 64
		DISC_POS[1] += 1
	elif(OFFSET[1]<-32):
		OFFSET[1] += 64
		DISC_POS[1] -= 1

	# Map Wrapping
	if(DISC_POS[0] >= m.get_size()[1]):
		DISC_POS[0] = 0
		p.pos[0] = 0
	if(DISC_POS[0] < 0):
		DISC_POS[0] = m.get_size()[1]-1
		p.pos[0] = 0
	if(DISC_POS[1] >= m.get_size()[0]):
		DISC_POS[1] = 0
		p.pos[0] = 0
	if(DISC_POS[1] < 0):
		DISC_POS[1] = m.get_size()[0]-1
		p.pos[0] = 0


def NPC_run(Non):
	global NPCS
	global inter_map
	global inter_map_obj

	for npc in NPC.all_npcs:
		if(npc.IS_LOADED):
			NPC.timer.schedule_once(npc.run, Non, inter_map, inter_map_obj)
		else:
			break

def reload_entity_layer(Non):
	global DISC_POS

	for npc in NPC.all_npcs:
		if(npc.is_in_entity_layer(DISC_POS)):
			npc.load()
		else:
			npc.unload()
	NPC.all_npcs[0].sort_npc_list()

@window.event
def on_key_press(symbol, modifiers):
	global PLAYER_DIRECTION
	global inter_map_obj
	global inter_map
	global m
	global MOVEMENT_VECTOR
	global VIEWPORT_UPDATE
	global p
	global NPCS


	if(symbol == key.Y):
		PLAYER_DIRECTION = 0
		p.direction = 0
		p.IS_MOVING = True
		MOVEMENT_VECTOR.insert(0, "U")
	elif(symbol == key.H):
		PLAYER_DIRECTION = 1
		p.direction = 1
		p.IS_MOVING = True
		MOVEMENT_VECTOR.insert(0, "D")
	elif(symbol == key.J):
		PLAYER_DIRECTION = 2
		p.direction = 2
		p.IS_MOVING = True
		MOVEMENT_VECTOR.insert(0, "R")
	elif(symbol == key.G):
		MOVEMENT_VECTOR.insert(0, "L")
		PLAYER_DIRECTION = 3
		p.IS_MOVING = True
		p.direction = 3

	elif(symbol == key.W):
		PLAYER_DIRECTION = 0
		p.direction = 0
		p.IS_MOVING = True
		MOVEMENT_VECTOR.insert(0, "KU")
	elif(symbol == key.S):
		PLAYER_DIRECTION = 1
		p.direction = 1
		p.IS_MOVING = True
		MOVEMENT_VECTOR.insert(0, "KD")
	elif(symbol == key.D):
		PLAYER_DIRECTION = 2
		p.direction = 2
		p.IS_MOVING = True
		MOVEMENT_VECTOR.insert(0, "KR")
	elif(symbol == key.A):
		MOVEMENT_VECTOR.insert(0, "KL")
		PLAYER_DIRECTION = 3
		p.IS_MOVING = True
		p.direction = 3

	## Debug Key
	if(symbol == key.Q):
		a = get_submatrix(inter_map_obj, DISC_POS, 1, 1, non_circular=False)
		for element in a:
			print(str(element) + "\n")

	elif(symbol == key.NUM_9):  
		for npc in NPC.all_npcs:
			npc.add_wander([100,115], 5, 3)

@window.event
def on_key_release(symbol, modifiers):
	global PLAYER_DIRECTION
	global MOVEMENT_VECTOR
	global p

	if(symbol == key.Y):
		MOVEMENT_VECTOR.remove("U")
	elif(symbol == key.H):
		MOVEMENT_VECTOR.remove("D")
	elif(symbol == key.J):
		MOVEMENT_VECTOR.remove("R")
	elif(symbol == key.G):
		MOVEMENT_VECTOR.remove("L")
	elif(symbol == key.W):
		MOVEMENT_VECTOR.remove("KU")
	elif(symbol == key.S):
		MOVEMENT_VECTOR.remove("KD")
	elif(symbol == key.D):
		MOVEMENT_VECTOR.remove("KR")
	elif(symbol == key.A):
		MOVEMENT_VECTOR.remove("KL")

	# Adjust player direction
	if(MOVEMENT_VECTOR == []):
		p.IS_MOVING = False
		return
	elif(MOVEMENT_VECTOR[0] == "U" or MOVEMENT_VECTOR == "KU"):
		PLAYER_DIRECTION = 0
		p.direction = 0
	elif(MOVEMENT_VECTOR[0] == "D" or MOVEMENT_VECTOR == "KD"):
		PLAYER_DIRECTION = 1
		p.direction = 1
	elif(MOVEMENT_VECTOR[0] == "R" or MOVEMENT_VECTOR == "KR"):
		PLAYER_DIRECTION = 2
		p.direction = 2
	elif(MOVEMENT_VECTOR[0] == "L" or MOVEMENT_VECTOR == "KL"):
		PLAYER_DIRECTION = 3
		p.direction = 3

# Rebuilds viewport
def draw_tiles(Non):

	global batch_sprites
	global batch_obj
	global batch_draw
	global batch_obj_draw
	global batch_anim_tiles
	global batch_anim_tiles_draw
	global batch_anim_obj
	global batch_anim_obj_draw
	global batch_fg_obj
	global batch_fg_obj_draw
	global batch_fg_anim_obj
	global batch_fg_anim_obj_draw
	global batch_shadow
	global batch_shadow_draw

	global m
	global LOCK
	global label
	global label2
	global label3
	global inter_map_obj
	global shadow_map
	global MOVEMENT_VECTOR
	global LAST_RENDER_POS
	global DISC_POS
	global OFFSET
	global LAST_CALL_POS
	global VIEWPORT_UPDATE

	global p

	label = pg.text.Label(str(DISC_POS), font_name='Arial', font_size=16, x=1800, y=1010)
	label2 = pg.text.Label(str(OFFSET), font_name='Arial', font_size=16, x=1800, y=950)
	label3 = pg.text.Label(str([NPC.all_npcs[0].IS_LOADED, NPC.all_npcs[1].IS_LOADED, NPC.all_npcs[2].IS_LOADED]), font_name='Arial', font_size=16, x=1800, y=850)

	# If needs to load new chunks
	if(abs(LAST_RENDER_POS[0] - DISC_POS[0]) + abs(LAST_RENDER_POS[1] - DISC_POS[1]) >= 2 or VIEWPORT_UPDATE):

		matrixes = m.get_region(DISC_POS, 13, 11, non_circular=False)
		interact = get_submatrix(inter_map_obj, DISC_POS, 13, 11, non_circular=False)
		shadows = get_submatrix(shadow_map, DISC_POS, 13,11, non_circular=False)

		VIEWPORT_UPDATE = False

		p.pos = DISC_POS.copy()
		p.offset = OFFSET.copy()

		LOCK.acquire()
		batch_sprites.clear()
		batch_obj.clear()
		batch_anim_tiles.clear()
		batch_anim_obj.clear()
		batch_fg_obj.clear()
		batch_fg_anim_obj.clear()
		batch_shadow.clear()

		LAST_CALL_POS = [DISC_POS[0], DISC_POS[1], OFFSET[0], OFFSET[1]]

		for i in range(0,27):
			for j in range(0,23):
				# Tiles and animated tiles
				if(matrixes[0][j][i] in all_tiles_img.keys()):
					batch_sprites.append(pg.sprite.Sprite(img=all_tiles_img[matrixes[0][j][i]], x=i*64-OFFSET[0]-128, y=(1272-(j*64))+OFFSET[1], batch=batch_draw))
				elif(matrixes[0][j][i] in animated_codelist):
					batch_anim_tiles.append([pg.sprite.Sprite(img=animated_dictionary[animation_handle][matrixes[0][j][i]], x=i*64-OFFSET[0]-128, y=(1272-(j*64))+OFFSET[1], batch=batch_anim_tiles_draw), matrixes[0][j][i]])				
				
				# Objects and animated objects
				if(matrixes[1][j][i] > 0): # If found an object in this tile
					# If it has special collision
					if(interact[j][i].special_collision):
						if(matrixes[1][j][i] in all_obj_img.keys()): # if not animated
							batch_fg_obj.append(pg.sprite.Sprite(img=all_obj_img[matrixes[1][j][i]], x=i*64-OFFSET[0]-128, y=(1272-(j*64))+OFFSET[1], batch=batch_fg_obj_draw))
						elif(matrixes[1][j][i] in animated_obj_codelist):
							batch_fg_anim_obj.append([pg.sprite.Sprite(img=animated_obj_dictionary[animation_handle][matrixes[1][j][i]], x=i*64-OFFSET[0]-128, y=(1272-(j*64))+OFFSET[1], batch=batch_fg_anim_obj_draw), matrixes[1][j][i]])
					else: # If normal collision
						if(matrixes[1][j][i] in all_obj_img.keys()):
							batch_obj.append(pg.sprite.Sprite(img=all_obj_img[matrixes[1][j][i]], x=i*64-OFFSET[0]-128, y=(1272-(j*64))+OFFSET[1], batch=batch_obj_draw))
						elif(matrixes[1][j][i] in animated_obj_codelist):
							batch_anim_obj.append([pg.sprite.Sprite(img=animated_obj_dictionary[animation_handle][matrixes[1][j][i]], x=i*64-OFFSET[0]-128, y=(1272-(j*64))+OFFSET[1], batch=batch_anim_obj_draw), matrixes[1][j][i]])				

				# Shadow handling
				batch_shadow.append(pg.sprite.Sprite(img=Lightning.get(shadows[j][i].color), x=i*64-OFFSET[0]-128, y=(1272-(j*64))+OFFSET[1], batch=batch_shadow_draw))
				batch_shadow[-1].opacity = shadows[j][i].current_light

		LAST_RENDER_POS = DISC_POS.copy()
		p.pos = DISC_POS.copy()
		p.offset = OFFSET.copy()
		LOCK.release()

	else:
		diff_x = (DISC_POS[0] - LAST_CALL_POS[0])*64 + (OFFSET[0] - LAST_CALL_POS[2])
		diff_y = (DISC_POS[1] - LAST_CALL_POS[1])*64 + (OFFSET[1] - LAST_CALL_POS[3])

		LOCK.acquire()

		# For animated objs
		if(diff_x == 0 and diff_y == 0):
			for i in range(len(batch_anim_tiles)):
				batch_anim_tiles[i][0].image = animated_dictionary[animation_handle][batch_anim_tiles[i][1]]
			for i in range(len(batch_anim_obj)):
				batch_anim_obj[i][0].image = animated_obj_dictionary[animation_handle][batch_anim_obj[i][1]]
			for i in range(len(batch_fg_anim_obj)):
				batch_fg_anim_obj[i][0].image = animated_obj_dictionary[animation_handle][batch_fg_anim_obj[i][1]]
			LOCK.release()
			return
		
		# Change position
		for i in range(len(batch_sprites)):
			batch_sprites[i].x -= diff_x
			batch_sprites[i].y += diff_y
		for i in range(len(batch_obj)):
			batch_obj[i].x -= diff_x
			batch_obj[i].y += diff_y
		for i in range(len(batch_anim_tiles)):
			batch_anim_tiles[i][0].x -= diff_x
			batch_anim_tiles[i][0].y += diff_y
			batch_anim_tiles[i][0].image = animated_dictionary[animation_handle][batch_anim_tiles[i][1]]
		for i in range(len(batch_anim_obj)):
			batch_anim_obj[i][0].x -= diff_x
			batch_anim_obj[i][0].y += diff_y
			batch_anim_obj[i][0].image = animated_obj_dictionary[animation_handle][batch_anim_obj[i][1]]
		for i in range(len(batch_fg_obj)):
			batch_fg_obj[i].x -= diff_x
			batch_fg_obj[i].y += diff_y
		for i in range(len(batch_fg_anim_obj)):
			batch_fg_anim_obj[i][0].x -= diff_x
			batch_fg_anim_obj[i][0].y += diff_y		
			batch_fg_anim_obj[i][0].image = animated_obj_dictionary[animation_handle][batch_fg_anim_obj[i][1]]
		for i in range(len(batch_shadow)):
			batch_shadow[i].x -= diff_x
			batch_shadow[i].y += diff_y

		LAST_CALL_POS = [DISC_POS[0], DISC_POS[1], OFFSET[0], OFFSET[1]]
		p.pos = DISC_POS.copy()
		p.offset = OFFSET.copy()
		LOCK.release()

# Game refresh function
@window.event
def on_draw():
	global LOCK
	global batch_sprites
	global batch_obj
	global batch_draw
	global batch_obj_draw
	global batch_anim_tiles
	global batch_anim_tiles_draw
	global batch_anim_obj
	global batch_anim_obj_draw
	global batch_fg_obj_draw
	global batch_fg_anim_obj
	global batch_fg_anim_obj_draw
	global batch_shadow
	global batch_shadow_draw

	global side_bev
	global bar_bev
	global player_bev
	global menu_bev
	global label
	global label2
	global label3
	global fps_clock
	global p
	global NPCS

	LOCK.acquire()
	window.flip()
	# Tiles
	batch_draw.draw()
	batch_anim_tiles_draw.draw()
	# Background Objects
	batch_obj_draw.draw()
	batch_anim_obj_draw.draw()
	# Entity
	for npc in NPC.all_npcs:
		if(npc.IS_LOADED):
			npc.draw(DISC_POS, OFFSET)
		else:
			break

	p.draw(DISC_POS, OFFSET)
	# Foreground Objects
	batch_fg_obj_draw.draw()
	batch_fg_anim_obj_draw.draw()
	# Light Layer
	batch_shadow_draw.draw()
	# Screen
	side_bev.draw()
	bar_bev.draw()
	menu_bev.draw()
	# Labels
	label.draw()
	label2.draw()
	label3.draw()
	fps_clock.draw()
	LOCK.release()

@window.event
def on_close():
	exit()

# Blitting Queues
batch_draw = pg.graphics.Batch()
batch_obj_draw = pg.graphics.Batch()
batch_anim_tiles_draw = pg.graphics.Batch()
batch_anim_obj_draw = pg.graphics.Batch()
batch_fg_obj_draw = pg.graphics.Batch()
batch_fg_anim_obj_draw = pg.graphics.Batch()
batch_shadow_draw = pg.graphics.Batch()

batch_anim_obj = []
batch_anim_tiles = []
batch_sprites = []
batch_obj = []
batch_fg_obj = []
batch_fg_anim_obj = []
batch_shadow = []

VIEWPORT_UPDATE = True

# Positioning
DISC_POS = [43,22]
OFFSET = [0,0]
PLAYER_DIRECTION = 0
MOVEMENT_VECTOR = []
LAST_RENDER_POS = [0,0]
LAST_CALL_POS = [DISC_POS[0], DISC_POS[1], OFFSET[0], OFFSET[1]]

# Paralellism
LOCK = Lock()

# Time
FPS = 1/60

# Animation
animation_handle = 0

# Bevels
side_bev = Bevel([1440, 0], "src\\Resources\\Sidebevel.png")
bar_bev = Bevel([0,0], "src\\Resources\\Barbevel.png")
menu_bev = Bevel([1344,0], "src\\Resources\\Menubevel.png")
#player_bev = Bevel([704, 568], "src\\Resources\\Player.png")
label = pg.text.Label(str(DISC_POS), font_name='Arial', font_size=16, x=1800, y=1010)
label2 = pg.text.Label(str(OFFSET), font_name='Arial', font_size=16, x=1800, y=950)
# Map
m, inter_map, inter_map_obj, shadow_map = loadmap("map\\draconis")
#m.check_unsigned_data(tile_dictionary, obj_dictionary)

# FPS Clock
fps_clock  = pyglet.window.FPSDisplay(window=window)
fps_clock.label.x = 1800
fps_clock.label.y = 890
fps_clock.label.font_size = 12
fps_clock.label.font_name='Arial'

# Entities
p = Player(DISC_POS, OFFSET, "src\\Char\\Lianna.png")
NPC([100, 115], [0,0], "src\\Char\\Lianna.png")
NPC([103, 116], [0,0], "src\\Char\\Lianna.png")
NPC([96, 111], [0,0], "src\\Char\\Lianna.png")
label3 = pg.text.Label(str([NPC.all_npcs[0].IS_LOADED, NPC.all_npcs[1].IS_LOADED, NPC.all_npcs[2].IS_LOADED]), font_name='Arial', font_size=16, x=1800, y=900)

# Threads
pg.clock.schedule_interval(draw_tiles, FPS)
pg.clock.schedule_interval(movement_handler, FPS)
pg.clock.schedule_interval(animate, 0.3)
pg.clock.schedule_interval(NPC_run, 1/60)
pg.clock.schedule_interval(reload_entity_layer, 1)


while(True):
	pg.clock.tick()
	NPC.timer.tick()
	window.switch_to()
	window.dispatch_events()
	window.dispatch_event('on_draw')