import pyglet as pg

def check_transparency(x,y,tilemap,objmap):
	if(not tilemap[x][y].transparency):
		return False
	elif(not objmap[x][y].transparency):
		return False
	else:
		return True

class Lightning:
	dictionary = {}

	def __init__(self, light, color=(0,0,0,255)):
		self.light = light
		self.color = color

	def set_light(self, n):
		if(n>255):
			self.light = 255
		elif(n<=0):
			self.light = 0
		else:
			self.light = n

	def change_light(self, n):
		new_val = self.light + n
		self.set_light(n)

	@staticmethod
	def get(color):
		if(Lightning.dictionary.get(color, False) == False):
			Lightning.dictionary[color] = pg.image.SolidColorImagePattern(color).create_image(64,64).get_texture()
		return Lightning.dictionary[color]

	# Propagates light from a Light tile
	# If limit == None, that it's propagating daylight. Else for object light
	@staticmethod
	def propagate_light(x, y, radius, tilemap, objmap, shadow_map, bypass_wall=False):
		level = shadow_map[y][x].light
		color = shadow_map[y][x].color

		decay = int((255 - level)/(radius+1))
		color_decay = (int(color[0]/(radius+1)), int(color[1]/(radius+1)), int(color[2]/(radius+1)), 255)
		
		if(bypass_wall):
			transparency = True
		else:
			transparency = check_transparency(x,y, tilemap, objmap)

		visited = []
		available = [[y,x]]
		data = [[color_decay, decay, transparency]]

		while(available != []):
			x,y = available.pop(0)
			cd, dc, trans = data.pop(0)
			visited.append([x,y])

			if([x+1,y] not in visited and shadow_map[x+1][y].light>level+dc):
				Lightning.propagate(x+1, y, level, cd, dc, shadow_map)
				if([x+1,y] not in available and level+dc<254 and trans):
					available.append([x+1,y])
					data.append([cd+color_decay, dc+decay, check_transparency(x+1,y,tilemap, objmap)])

			if([x-1,y] not in visited and shadow_map[x-1][y].light>level+dc):
				Lightning.propagate(x-1, y, level, cd, dc, shadow_map)
				if([x-1,y] not in available and level+dc<254 and trans):
					available.append([x-1,y])
					data.append([cd+color_decay, dc+decay, check_transparency(x-1,y,tilemap, objmap)])	

			if([x,y+1] not in visited and shadow_map[x][y+1].light>level+dc):
				Lightning.propagate(x, y+1, level, cd, dc, shadow_map)
				if([x,y+1] not in available and level+dc<254 and trans):
					available.append([x,y+1])
					data.append([cd+color_decay, dc+decay, check_transparency(x,y+1,tilemap, objmap)])	

			if([x,y-1] not in visited and shadow_map[x][y-1].light>level+dc):
				Lightning.propagate(x, y-1, level, cd, dc, shadow_map)
				if([x,y-1] not in available and level+dc<254 and trans):
					available.append([x,y-1])
					data.append([cd+color_decay, dc+decay, check_transparency(x,y-1,tilemap, objmap)])

	@staticmethod
	def propagate(x, y, level, color_decay, decay, shadow_map):
		shadow_map[x][y].set_light(level + decay)
		shadow_map[x][y].color = (shadow_map[x][y].color[0]+color_decay[0], shadow_map[x][y].color[1]+color_decay[1],
				shadow_map[x][y].color[2]+color_decay[2], 255)

