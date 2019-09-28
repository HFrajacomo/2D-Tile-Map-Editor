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

	def __init__(self, light, radius, color=(0,0,0,255)):
		self.natural_light = light  # Natural light level for saving and loading maps
		self.light = light
		self.color = color
		self.radius = radius

		if(light == 0):
			self.daylight = True
		else:
			self.daylight = False

	def __add__(self, Light):
		new = Lightning(self.light - Light.light, 5, color = (self.color[0]+Light.color[0], self.color[1]+Light.color[1], self.color[2]+Light.color[2], 255))
		if(self.daylight or Light.daylight):
			new.daylight = True
		else:
			new.daylight = False

		return new 

	def __sub__(self, Light):
		new = Lightning(self.light + Light.light, 5, color = (self.color[0]-Light.color[0], self.color[1]-Light.color[1], self.color[2]-Light.color[2], 255))
		if(self.daylight or Light.daylight):
			new.daylight = True
		else:
			new.daylight = False

		return new 

	def set_real_light(self, n):
		self.natural_light = n
		self.set_light(n)

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
	def propagate_light(x, y, tilemap, objmap, shadow_map, bypass_wall=False):
		level = shadow_map[y][x].natural_light
		color = shadow_map[y][x].color
		radius = shadow_map[y][x].radius

		decay = int((255 - level)/(radius+1))
		decayment = (255-level) - decay
		color_decay = (int(color[0]/(radius+1)), int(color[1]/(radius+1)), int(color[2]/(radius+1)), 255)
		
		if(bypass_wall):
			transparency = True
		else:
			transparency = check_transparency(x,y, tilemap, objmap)

		visited = []
		available = [[y,x]]
		data = [[color_decay, decayment, transparency]]

		while(available != []):
			x,y = available.pop(0)
			cd, dc, trans = data.pop(0)
			visited.append([x,y])

			if([x+1,y] not in visited and [x+1,y] not in available and trans):
				Lightning.propagate(x+1, y, cd, dc, shadow_map)
				if([x+1,y] not in available and dc>decay):
					available.append([x+1,y])
					data.append([cd+color_decay, dc-decay, check_transparency(x+1,y,tilemap, objmap)])
			
			if([x-1,y] not in visited and [x-1,y] not in available and trans):
				Lightning.propagate(x-1, y, cd, dc, shadow_map)
				if([x-1,y] not in available and dc>decay):
					available.append([x-1,y])
					data.append([cd+color_decay, dc-decay, check_transparency(x-1,y,tilemap, objmap)])
			
			if([x,y+1] not in visited and [x,y+1] not in available and trans):
				Lightning.propagate(x, y+1, cd, dc, shadow_map)
				if([x,y+1] not in available and dc>decay):
					available.append([x,y+1])
					data.append([cd+color_decay, dc-decay, check_transparency(x,y+1,tilemap, objmap)])

			if([x,y-1] not in visited and [x,y-1] not in available and trans):
				Lightning.propagate(x, y-1, cd, dc, shadow_map)
				if([x,y-1] not in available and dc>decay):
					available.append([x,y-1])
					data.append([cd+color_decay, dc-decay, check_transparency(x,y-1,tilemap, objmap)])
			

	@staticmethod
	def propagate(x, y, color_decay, decay, shadow_map):
		shadow_map[x][y].set_real_light(shadow_map[x][y].natural_light - decay)
		shadow_map[x][y].color = (shadow_map[x][y].color[0]+color_decay[0], shadow_map[x][y].color[1]+color_decay[1],
				shadow_map[x][y].color[2]+color_decay[2], 255)


	# Removes light from light emiting objects or tiles
	@staticmethod
	def unpropagate_light(x, y, Light, tilemap, objmap, shadow_map, bypass_wall=False):
		level = Light.natural_light
		color = Light.color
		radius = Light.radius

		decay = int((255 - level)/(radius+1))
		decayment = (255-level) - decay
		color_decay = (int(color[0]/(radius+1)), int(color[1]/(radius+1)), int(color[2]/(radius+1)), 255)
		
		if(bypass_wall):
			transparency = True
		else:
			transparency = check_transparency(x,y, tilemap, objmap)

		visited = []
		available = [[y,x]]
		data = [[color_decay, decayment, transparency]]

		while(available != []):
			x,y = available.pop(0)
			cd, dc, trans = data.pop(0)
			visited.append([x,y])

			if([x+1,y] not in visited and [x+1,y] not in available and trans):
				Lightning.unpropagate(x+1, y, cd, dc, shadow_map)
				if([x+1,y] not in available and dc>decay):
					available.append([x+1,y])
					data.append([cd+color_decay, dc-decay, check_transparency(x+1,y,tilemap, objmap)])
			
			if([x-1,y] not in visited and [x-1,y] not in available and trans):
				Lightning.unpropagate(x-1, y, cd, dc, shadow_map)
				if([x-1,y] not in available and dc>decay):
					available.append([x-1,y])
					data.append([cd+color_decay, dc-decay, check_transparency(x-1,y,tilemap, objmap)])
			
			if([x,y+1] not in visited and [x,y+1] not in available and trans):
				Lightning.unpropagate(x, y+1, cd, dc, shadow_map)
				if([x,y+1] not in available and dc>decay):
					available.append([x,y+1])
					data.append([cd+color_decay, dc-decay, check_transparency(x,y+1,tilemap, objmap)])

			if([x,y-1] not in visited and [x,y-1] not in available and trans):
				Lightning.unpropagate(x, y-1, cd, dc, shadow_map)
				if([x,y-1] not in available and dc>decay):
					available.append([x,y-1])
					data.append([cd+color_decay, dc-decay, check_transparency(x,y-1,tilemap, objmap)])

	@staticmethod
	def unpropagate(x, y, color_decay, decay, shadow_map):
		shadow_map[x][y].set_real_light(shadow_map[x][y].natural_light + decay)
		shadow_map[x][y].color = (shadow_map[x][y].color[0]-color_decay[0], shadow_map[x][y].color[1]-color_decay[1],
				shadow_map[x][y].color[2]-color_decay[2], 255)
	'''
	@staticmethod
	def propagate_all(tilemap, objmap, shadowmap):
		# Natural light propagation
		for i in range(len(shadowmap)):
			for j in range(len(shadowmap[0])):
				if(shadowmap[j][i].daylight):
					Lightning.propagate_light(i,j, 5, tilemap, objmap, shadowmap)
	'''

