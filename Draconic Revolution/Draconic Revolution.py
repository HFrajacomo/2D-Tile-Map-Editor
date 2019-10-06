# Importing Engine

import pyglet as pg
from pyglet.gl import *
from pyglet.window import key
import sys
from threading import Lock
import zmq
from subprocess import Popen
import colorama
from colorama import Fore

colorama.init(autoreset=True)
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
from Time import *
from Area import *
from Shader import *
from NetMessage import *

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

def global_time_run(Non):
	global GLOBAL_TIME
	global DLconf
	global shadow_map
	global inter_map
	global inter_map_obj
	global shader_layer
	global shader_area_1
	global p

	DLconf.update_daylight("Surface", inter_map, inter_map_obj, shadow_map, GLOBAL_TIME)

	# Area control
	if(p in shader_area_1):
		shader_area_1.enter(p, shader_layer)

	for pl in shader_area_1.entities:
		if(pl not in shader_area_1):
			shader_area_1.exit(pl, shader_layer)


def movement_handler(non):
	global DISC_POS
	global OFFSET
	global LOCK
	global m
	global MOVEMENT_VECTOR
	global p
	global C_LOCK
	global receive_socket

	if(MOVEMENT_VECTOR == []):
		receive_socket.send_string(-NetMessage("POSITION", f"{p.pos[0]},{p.pos[1]};{p.offset[0]},{p.offset[1]};{p.direction};{p.IS_MOVING}"))
		return

	# Admin Movement
	if(MOVEMENT_VECTOR[0] == "KU"):
		LOCK.acquire()
		receive_socket.send_string(-NetMessage("CHANGE_POS", f"{DISC_POS[0]},{DISC_POS[1]}"))
		DISC_POS = list_sum(DISC_POS, [0,-1])
		p.direction = 0
		LOCK.release()
	elif(MOVEMENT_VECTOR[0] == "KD"):
		LOCK.acquire()
		receive_socket.send_string(-NetMessage("CHANGE_POS", f"{DISC_POS[0]},{DISC_POS[1]}"))
		DISC_POS = list_sum(DISC_POS, [0,1])
		p.direction = 1
		LOCK.release()
	elif(MOVEMENT_VECTOR[0] == "KR"):
		LOCK.acquire()
		receive_socket.send_string(-NetMessage("CHANGE_POS", f"{DISC_POS[0]},{DISC_POS[1]}"))
		DISC_POS = list_sum(DISC_POS, [1,0])
		p.direction = 2
		LOCK.release()
	elif(MOVEMENT_VECTOR[0] == "KL"):
		LOCK.acquire()
		receive_socket.send_string(-NetMessage("CHANGE_POS", f"{DISC_POS[0]},{DISC_POS[1]}"))
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
		receive_socket.send_string(-NetMessage("CHANGE_POS", f"{DISC_POS[0]},{DISC_POS[1]}"))
		OFFSET[0] -= 64
		DISC_POS[0] += 1
	elif(OFFSET[0]<-32):
		receive_socket.send_string(-NetMessage("CHANGE_POS", f"{DISC_POS[0]},{DISC_POS[1]}"))
		OFFSET[0] += 64
		DISC_POS[0] -= 1
	if(OFFSET[1]>31):
		receive_socket.send_string(-NetMessage("CHANGE_POS", f"{DISC_POS[0]},{DISC_POS[1]}"))
		OFFSET[1] -= 64
		DISC_POS[1] += 1
	elif(OFFSET[1]<-32):
		receive_socket.send_string(-NetMessage("CHANGE_POS", f"{DISC_POS[0]},{DISC_POS[1]}"))
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

	receive_socket.send_string(-NetMessage("POSITION", f"{DISC_POS[0]},{DISC_POS[1]};{OFFSET[0]},{OFFSET[1]};{p.direction};{p.IS_MOVING}"))

def layer_connection(Non):
	global layer_socket
	global entity_dict

	try:
		message = layer_socket.recv(zmq.NOBLOCK).decode()
		m = NetMessage(message)
	except zmq.Again:
		return

	print(Fore.RED + "ENTITY: " + message)

	# If gets entity layer refreshment
	if(m.type == "ENTITIES"):
		known = list(entity_dict.keys())

		for e in m.data.split(","):
			if(e not in known):
				layer_socket.send_string(-NetMessage("REQ_ENTITY", str(e)))

def timer_connection(Non):
	global timer_socket
	global GLOBAL_TIME
	global LAN_SERVER

	try:
		message = timer_socket.recv(zmq.NOBLOCK).decode()
		m = NetMessage(message)
	except zmq.Again:
		return

	print(Fore.RED + "TIMER: " + message)

	# If receives time data
	if(m.type == "TIME"):
		GLOBAL_TIME.set_string(m.data)

def receive_connection(Non):
	global receive_socket
	global entity_dict
	global p

	try:
		message = receive_socket.recv(zmq.NOBLOCK).decode()
		m = NetMessage(message)
	except zmq.Again:
		return

	print(Fore.RED + "RECEIVE: " + message)

	# If gets your own ID
	if(m.type == "PLAYER_ID"):
		entity_dict[int(m.data)] = p
		p.id = int(m.data)

	# If gets individual entity information
	elif(m.type == "ENTITY_INFO"):
		id, ent_data = m.data.split("#")
		id = int(id)
		ent_data = ent_data.split(";")
		if(id > 0):
			entity_dict[id] = Player([int(x) for x in ent_data[0].split(",")], [int(x) for x in ent_data[1].split(",")], ent_data[2])
		else:
			entity_dict[id] = NPC([int(x) for x in ent_data[0].split(",")], [int(x) for x in ent_data[1].split(",")], ent_data[2])
			entity_dict[id].load()
'''
def NPC_run(Non):
	global NPCS
	global inter_map
	global inter_map_obj

	for npc in NPC.all_npcs:
		if(npc.IS_LOADED):
			NPC.timer.schedule_once(npc.run, Non, inter_map, inter_map_obj)
		else:
			break
'''

def reload_entity_layer(Non):
	global DISC_POS
	global entity_dict

	pop_list = []

	for npc in NPC.all_npcs:
		if(not npc.is_in_entity_layer(DISC_POS)):
			pop_list.append(npc)

	for npc in pop_list:
		NPC.all_npcs.pop(npc)
		entity_dict.pop(npc.id)

@window.event
def on_key_press(symbol, modifiers):
	global PLAYER_DIRECTION
	global inter_map_obj
	global inter_map
	global m
	global MOVEMENT_VECTOR
	global VIEWPORT_UPDATE
	global p
	global GLOBAL_TIME

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
		surroundings = get_submatrix(inter_map_obj, DISC_POS,1,1, non_circular=False)

		for line in surroundings:
			print()
			for element in line:
				print(element, end="\t")

	elif(symbol == key.NUM_9):  
		for npc in NPC.all_npcs:
			npc.add_wander([100,115], 5, 3)

	elif(symbol == key.Z):
		GLOBAL_TIME.inc()
	elif(symbol == key.X):
		GLOBAL_TIME.inc_hour()
	elif(symbol == key.C):
		print(shadow_map[DISC_POS[1]][DISC_POS[0]])


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
	global time_label
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
	time_label = pg.text.Label(str(GLOBAL_TIME), font_name='Arial', font_size=20, x=1450, y=1010)


	# If needs to load new chunks
	if(abs(LAST_RENDER_POS[0] - DISC_POS[0]) + abs(LAST_RENDER_POS[1] - DISC_POS[1]) >= 2 or VIEWPORT_UPDATE):

		matrixes = m.get_region(DISC_POS, 13, 11, non_circular=False)
		interact = get_submatrix(inter_map_obj, DISC_POS, 13, 11, non_circular=False)

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

			k = (DISC_POS[0] - 13) + i  # For shadow optimization
			if(k>=len(inter_map_obj[0])):
				k -= len(inter_map_obj[0])

			for j in range(0,23):

				l = (DISC_POS[1]-11) + j # For shadow optimization
				if(l>=len(inter_map_obj)):
					l -= len(inter_map_obj)

				if(shadow_map[l][k].light != 255): # If it's not completely dark

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
				if(shadow_map[l][k].light != 0):
					batch_shadow.append(pg.sprite.Sprite(img=Lightning.get(shadow_map[l][k].color), x=i*64-OFFSET[0]-128, y=(1272-(j*64))+OFFSET[1], batch=batch_shadow_draw))
					batch_shadow[-1].opacity = shadow_map[l][k].light



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
	global shader_layer

	global side_bev
	global bar_bev
	global player_bev
	global menu_bev
	global label
	global label2
	global fps_clock
	global p
	global NPCS

	LOCK.acquire()
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
	# Shader Layer
	shader_layer.draw()
	# Screen
	side_bev.draw()
	bar_bev.draw()
	menu_bev.draw()
	# Labels
	label.draw()
	label2.draw()
	fps_clock.draw()
	time_label.draw()
	LOCK.release()

@window.event
def on_close():
	global socket
	global LAN_SERVER 

	socket.close()
	LAN_SERVER.kill()
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
DISC_POS = [55,40]
OFFSET = [0,0]
PLAYER_DIRECTION = 0
MOVEMENT_VECTOR = []
LAST_RENDER_POS = [0,0]
LAST_CALL_POS = [DISC_POS[0], DISC_POS[1], OFFSET[0], OFFSET[1]]

# Paralellism
LOCK = Lock()

# Time
FPS = 1/30
GLOBAL_TIME = Time(12,00)

# Animation
animation_handle = 0

# Bevels
side_bev = Bevel([1440, 0], "src\\Resources\\Sidebevel.png")
bar_bev = Bevel([0,0], "src\\Resources\\Barbevel.png")
menu_bev = Bevel([1344,0], "src\\Resources\\Menubevel.png")
label = pg.text.Label(str(DISC_POS), font_name='Arial', font_size=16, x=1800, y=1010)
label2 = pg.text.Label(str(OFFSET), font_name='Arial', font_size=16, x=1800, y=950)
time_label = pg.text.Label(str(GLOBAL_TIME), font_name='Arial', font_size=20, x=1450, y=1010)

# Map
m, inter_map, inter_map_obj, shadow_map = loadmap("map\\draconis")
#m.check_unsigned_data(tile_dictionary, obj_dictionary)

# Lightning
Lightning.propagate_all(inter_map, inter_map_obj, shadow_map)
DLconf = DaylightConfigurator()

# Areas
shader_area_1 = ShaderArea([[30,30], [30,40], [40,30],[40,40]], (0,0,100,255), 50)

# Shader
shader_layer = Shader()

# Start LAN
LAN_SERVER = Popen("python src\\LAN.py")

# Entities
p = Player(DISC_POS, OFFSET, "src\\Char\\Lianna.png")
entity_dict = {}

# Socket Connection
context = zmq.Context()
socket = context.socket(zmq.DEALER)
HOST = "127.0.0.1"
PORT = 33000
receive_string = "tcp://" + HOST + ":" + str(PORT)
timer_string = "tcp://" + HOST + ":" + str(PORT+1)
layer_string = "tcp://" + HOST + ":" + str(PORT+2)
socket.connect(receive_string)
socket.send_string(-NetMessage("IDENTITY", f"{DISC_POS[0]},{DISC_POS[1]};{OFFSET[0]},{OFFSET[1]};{p.filename}"))
ident = socket.recv()
socket.close()

# Actual Sockets
receive_socket = context.socket(zmq.DEALER)
timer_socket = context.socket(zmq.DEALER)
layer_socket = context.socket(zmq.DEALER)
receive_socket.setsockopt(zmq.IDENTITY, ident)
timer_socket.setsockopt(zmq.IDENTITY, ident)
layer_socket.setsockopt(zmq.IDENTITY, ident)
receive_socket.connect(receive_string)
timer_socket.connect(timer_string)
layer_socket.connect(layer_string)


# FPS Clock
fps_clock  = pyglet.window.FPSDisplay(window=window)
fps_clock.label.x = 1800
fps_clock.label.y = 890
fps_clock.label.font_size = 12
fps_clock.label.font_name='Arial'

# Threads
pg.clock.schedule_interval(draw_tiles, FPS)
pg.clock.schedule_interval_soft(movement_handler, FPS)
pg.clock.schedule_interval(animate, 0.3)
#pg.clock.schedule_interval_soft(NPC_run, FPS)
pg.clock.schedule_interval(global_time_run, 1)
pg.clock.schedule_interval(receive_connection, 1/120)
pg.clock.schedule_interval(timer_connection, 1/30)
pg.clock.schedule_interval(layer_connection, 1/60)


while(True):
	window.flip()
	pg.clock.tick()
	NPC.timer.tick()
	window.switch_to()
	window.dispatch_events()
	window.dispatch_event('on_draw') # Goes up to 2100 FPS. Minimize Drawing!