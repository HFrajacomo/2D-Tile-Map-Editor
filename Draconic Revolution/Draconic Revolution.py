import pyglet as pg
from pyglet.gl import *
from pyglet.window import key
import sys
from threading import Lock

# Direct OpenGL commands to this window.
#platform = pg.window.get_platform()
display = pg.canvas.get_display()
screen = display.get_default_screen()
template = pyglet.gl.Config(alpha_size=8)
config = screen.get_best_config(template)
window = pg.window.Window(width=1920, height=1080, fullscreen=True, config=config)

sys.path.append('src\\')
from Tile import *
from Map import *
from Obj import *
from TileDictionary import *
from ObjDictionary import *
from Bevel import *
from ServerHolder import *


def list_sum(l1, l2):
	for i in range(len(l1)):
		l1[i] += l2[i]

	return l1

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

	if(MOVEMENT_VECTOR == []):
		return

	# Admin Movement
	if(MOVEMENT_VECTOR[0] == "KU"):
		LOCK.acquire()
		DISC_POS = list_sum(DISC_POS, [0,-1])
		LOCK.release()
	elif(MOVEMENT_VECTOR[0] == "KD"):
		LOCK.acquire()
		DISC_POS = list_sum(DISC_POS, [0,1])
		LOCK.release()
	elif(MOVEMENT_VECTOR[0] == "KR"):
		LOCK.acquire()
		DISC_POS = list_sum(DISC_POS, [1,0])
		LOCK.release()
	elif(MOVEMENT_VECTOR[0] == "KL"):
		LOCK.acquire()
		DISC_POS = list_sum(DISC_POS, [-1,0])
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
	if(DISC_POS[0] < 0):
		DISC_POS[0] = m.get_size()[1]-1
	if(DISC_POS[1] >= m.get_size()[0]):
		DISC_POS[1] = 0
	if(DISC_POS[1] < 0):
		DISC_POS[1] = m.get_size()[0]-1

@window.event
def on_key_press(symbol, modifiers):
	global PLAYER_DIRECTION
	global inter_map_obj
	global m
	global MOVEMENT_VECTOR

	if(symbol == key.Y):
		PLAYER_DIRECTION = 0
		MOVEMENT_VECTOR.insert(0, "U")
	elif(symbol == key.H):
		PLAYER_DIRECTION = 1
		MOVEMENT_VECTOR.insert(0, "D")
	elif(symbol == key.J):
		PLAYER_DIRECTION = 2
		MOVEMENT_VECTOR.insert(0, "R")
	elif(symbol == key.G):
		MOVEMENT_VECTOR.insert(0, "L")
		PLAYER_DIRECTION = 3

	elif(symbol == key.W):
		PLAYER_DIRECTION = 0
		MOVEMENT_VECTOR.insert(0, "KU")
	elif(symbol == key.S):
		PLAYER_DIRECTION = 1
		MOVEMENT_VECTOR.insert(0, "KD")
	elif(symbol == key.D):
		PLAYER_DIRECTION = 2
		MOVEMENT_VECTOR.insert(0, "KR")
	elif(symbol == key.A):
		MOVEMENT_VECTOR.insert(0, "KL")
		PLAYER_DIRECTION = 3

	## Debug Key
	if(symbol == key.Q):
		a = get_submatrix(inter_map_obj, DISC_POS, 1, 1, non_circular=False)
		for element in a:
			print(str(element) + "\n")
	elif(symbol == key.Z):
		if(PLAYER_DIRECTION == 0):
			print(inter_map_obj[DISC_POS[1], DISC_POS[0]-1])
			inter_map_obj[DISC_POS[1], DISC_POS[0]-1].action(0, DISC_POS, m, inter_map_obj)
		elif(PLAYER_DIRECTION == 1):
			print(inter_map_obj[DISC_POS[1], DISC_POS[0]+1])
			inter_map_obj[DISC_POS[1], DISC_POS[0]+1].action(0, DISC_POS, m, inter_map_obj)
		elif(PLAYER_DIRECTION == 2):
			print(inter_map_obj[DISC_POS[1]+1, DISC_POS[0]])
			inter_map_obj[DISC_POS[1]+1, DISC_POS[0]].action(0, DISC_POS, m, inter_map_obj)
		elif(PLAYER_DIRECTION == 3):
			print(inter_map_obj[DISC_POS[1]-1, DISC_POS[0]])
			inter_map_obj[DISC_POS[1]-1, DISC_POS[0]].action(0, DISC_POS, m, inter_map_obj)
		else:
			print(PLAYER_DIRECTION)


@window.event
def on_key_release(symbol, modifiers):
	global PLAYER_DIRECTION
	global MOVEMENT_VECTOR

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
		return
	elif(MOVEMENT_VECTOR[0] == "U" or MOVEMENT_VECTOR == "KU"):
		PLAYER_DIRECTION = 0
	elif(MOVEMENT_VECTOR[0] == "D" or MOVEMENT_VECTOR == "KD"):
		PLAYER_DIRECTION = 1
	elif(MOVEMENT_VECTOR[0] == "R" or MOVEMENT_VECTOR == "KR"):
		PLAYER_DIRECTION = 2
	elif(MOVEMENT_VECTOR[0] == "L" or MOVEMENT_VECTOR == "KL"):
		PLAYER_DIRECTION = 3

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

	global m
	global LOCK
	global label
	global label2
	global label3
	global inter_map_obj
	global MOVEMENT_VECTOR

	matrixes = m.get_region(DISC_POS, 12, 8, non_circular=False)
	interact = get_submatrix(inter_map_obj, DISC_POS, 12, 8, non_circular=False)

	label = pg.text.Label(str(DISC_POS), font_name='Arial', font_size=16, x=1800, y=1010)
	label2 = pg.text.Label(str(OFFSET), font_name='Arial', font_size=16, x=1800, y=950)
	label3 = pg.text.Label(str(MOVEMENT_VECTOR), font_name='Arial', font_size=16, x=1800, y=700)
	
	LOCK.acquire()
	batch_sprites.clear()
	batch_obj.clear()
	batch_anim_tiles.clear()
	batch_anim_obj.clear()
	batch_fg_obj.clear()
	batch_fg_anim_obj.clear()

	for i in range(0,25):
		for j in range(0,17):
			# Tiles and animated tiles
			if(matrixes[0][j][i] in all_tiles_img.keys()):
				batch_sprites.append(pg.sprite.Sprite(img=all_tiles_img[matrixes[0][j][i]], x=i*64-OFFSET[0]-64, y=(1080-(j*64))+OFFSET[1], batch=batch_draw))
			elif(matrixes[0][j][i] in animated_codelist):
				batch_anim_tiles.append(pg.sprite.Sprite(img=animated_dictionary[animation_handle][matrixes[0][j][i]], x=i*64-OFFSET[0]-64, y=(1080-(j*64))+OFFSET[1], batch=batch_anim_tiles_draw))				
			
			# Objects and animated objects
			if(matrixes[1][j][i] > 0): # If found an object in this tile
				# If it has special collision
				if(interact[j][i].special_collision):
					if(matrixes[1][j][i] in all_obj_img.keys()): # if not animated
						batch_fg_obj.append(pg.sprite.Sprite(img=all_obj_img[matrixes[1][j][i]], x=i*64-OFFSET[0]-64, y=(1080-(j*64))+OFFSET[1], batch=batch_fg_obj_draw))
					elif(matrixes[1][j][i] in animated_obj_codelist):
						batch_fg_anim_obj.append(pg.sprite.Sprite(img=animated_obj_dictionary[animation_handle][matrixes[1][j][i]], x=i*64-OFFSET[0]-64, y=(1080-(j*64))+OFFSET[1], batch=batch_fg_anim_obj_draw))
				else: # If normal collision
					if(matrixes[1][j][i] in all_obj_img.keys()):
						batch_obj.append(pg.sprite.Sprite(img=all_obj_img[matrixes[1][j][i]], x=i*64-OFFSET[0]-64, y=(1080-(j*64))+OFFSET[1], batch=batch_obj_draw))
					elif(matrixes[1][j][i] in animated_obj_codelist):
						batch_anim_obj.append(pg.sprite.Sprite(img=animated_obj_dictionary[animation_handle][matrixes[1][j][i]], x=i*64-OFFSET[0]-64, y=(1080-(j*64))+OFFSET[1], batch=batch_anim_obj_draw))				


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

	global side_bev
	global bar_bev
	global player_bev
	global menu_bev
	global label
	global label2
	global label3
	global fps_clock

	LOCK.acquire()
	# Tiles
	batch_draw.draw()
	batch_anim_tiles_draw.draw()
	# Background Objects
	batch_obj_draw.draw()
	batch_anim_obj_draw.draw()
	# Entity
	player_bev.draw()
	# Foreground Objects
	batch_fg_obj_draw.draw()
	batch_fg_anim_obj_draw.draw()
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

# Blitting Queues
batch_draw = pg.graphics.Batch()
batch_obj_draw = pg.graphics.Batch()
batch_anim_tiles_draw = pg.graphics.Batch()
batch_anim_obj_draw = pg.graphics.Batch()
batch_fg_obj_draw = pg.graphics.Batch()
batch_fg_anim_obj_draw = pg.graphics.Batch()

batch_anim_obj = []
batch_anim_tiles = []
batch_sprites = []
batch_obj = []
batch_fg_obj = []
batch_fg_anim_obj = []

# Positioning
DISC_POS = [100,124]
OFFSET = [0,0]
PLAYER_DIRECTION = 4
MOVEMENT_VECTOR = []

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
player_bev = Bevel([704, 568], "src\\Resources\\Player.png")
label = pg.text.Label(str(DISC_POS), font_name='Arial', font_size=16, x=1800, y=1010)
label2 = pg.text.Label(str(OFFSET), font_name='Arial', font_size=16, x=1800, y=950)
label3 = pg.text.Label(str(MOVEMENT_VECTOR), font_name='Arial', font_size=16, x=1800, y=700)

# Map
m, inter_map, inter_map_obj = loadmap("map\\draconis")
m.check_unsigned_data(tile_dictionary, obj_dictionary)

### TEST

# Threads
pg.clock.schedule_interval(draw_tiles, FPS)
pg.clock.schedule_interval(movement_handler, FPS)
pg.clock.schedule_interval(animate, 0.2)

# FPS Clock
fps_clock  = pyglet.window.FPSDisplay(window=window)
fps_clock.label.x = 1800
fps_clock.label.y = 890
fps_clock.label.font_size = 12
fps_clock.label.font_name='Arial'

pg.app.run()
