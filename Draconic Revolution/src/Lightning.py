import pyglet as pg

def check_transparency(x,y,tilemap,objmap):
	try:
		if(not tilemap[x][y].transparency):
			return False
		elif(not objmap[x][y].transparency):
			return False
		else:
			return True
	except:
		return False


def color_sum(t,s):
	red = t[0]+s[0]
	green = t[1]+s[1]
	blue = t[2]+s[2]

	if(red > 255):
		red = 255
	if(blue > 255):
		blue = 255
	if(green > 255):
		green = 255

	if(red < 0):
		red = 0
	if(blue < 0):
		blue = 0
	if(green < 0):
		green = 0

	return (red, green, blue, 255)

class Lightning:
	dictionary = {}

	def __init__(self, light, radius, color=(0,0,0,255), bypass=False):
		self.darkness_compensation = 0
		self.natural_light = light  # Natural light level for saving and loading maps
		self.light = light
		self.color = color
		self.radius = radius
		self.bypass = bypass

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

	def __repr__(self):
		return "Daylight: " + str(self.daylight) + "\nLight: " + str(self.natural_light) + "\nColor: " + str(self.color) + "\nDarkness Compensation: " + str(self.darkness_compensation)

	def set_real_light(self, n):
		if(n >255):
			self.darkness_compensation = 255 - n
			n = 255

		self.natural_light = n
		self.set_light(int(n))

	def add_real_light(self, n):
		if(self.darkness_compensation > 0):
			if(self.darkness_compensation + n < 0):
				self.set_real_light(self.natural_light + (self.darkness_compensation + n))
				self.darkness_compensation = 0
				return
			elif(self.darkness_compensation >= n):
				self.darkness_compensation += n
				return

		self.set_real_light(self.natural_light + n)

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
	def propagate_light(x, y, Light, tilemap, objmap, shadow_map):
		level = Light.light
		color = Light.color
		radius = Light.radius

		decay = int((255 - level)/(radius+1))
		decayment = (255-level) - decay
		color_decay = (-int(color[0]/(radius+1)), -int(color[1]/(radius+1)), -int(color[2]/(radius+1)), 255)
		new_color = color_sum(color, color_decay)

		if(Light.bypass):
			transparency = True
		else:
			transparency = check_transparency(x,y, tilemap, objmap)

		visited = []
		available = [[x,y]]
		data = [[new_color, decayment, transparency]]
		flip = None

		while(available != []):
			x,y = available.pop(0)
			cd, dc, trans = data.pop(0)
			visited.append([x,y])

			if([x+1,y] not in visited and [x+1,y] not in available and trans):
				flip = Lightning.propagate(x+1, y, cd, dc, shadow_map)
				if([x+1,y] not in available and dc>decay and flip):
					available.append([x+1,y])
					data.append([color_sum(cd,color_decay), dc-decay, check_transparency(x+1,y,tilemap, objmap)])
			
			if([x-1,y] not in visited and [x-1,y] not in available and trans):
				flip = Lightning.propagate(x-1, y, cd, dc, shadow_map)
				if([x-1,y] not in available and dc>decay and flip):
					available.append([x-1,y])
					data.append([color_sum(cd,color_decay), dc-decay, check_transparency(x-1,y,tilemap, objmap)])
			
			if([x,y+1] not in visited and [x,y+1] not in available and trans):
				flip = Lightning.propagate(x, y+1, cd, dc, shadow_map)
				if([x,y+1] not in available and dc>decay and flip):
					available.append([x,y+1])
					data.append([color_sum(cd,color_decay), dc-decay, check_transparency(x,y+1,tilemap, objmap)])

			if([x,y-1] not in visited and [x,y-1] not in available and trans):
				flip = Lightning.propagate(x, y-1, cd, dc, shadow_map)
				if([x,y-1] not in available and dc>decay and flip):
					available.append([x,y-1])
					data.append([color_sum(cd,color_decay), dc-decay, check_transparency(x,y-1,tilemap, objmap)])
			

	@staticmethod
	def propagate(x, y, color_decay, decay, shadow_map):
		try:
			shadow_map[x][y].set_real_light(shadow_map[x][y].natural_light - decay)
			shadow_map[x][y].color = color_sum(shadow_map[x][y].color, color_decay)
			return True
		except IndexError:
			return False

	# Removes light from light emiting objects or tiles
	@staticmethod
	def unpropagate_light(x, y, Light, tilemap, objmap, shadow_map, bypass_wall=False):
		level = Light.light
		color = Light.color
		radius = Light.radius

		decay = int((255 - level)/(radius+1))
		decayment = (255-level) - decay
		color_decay = (-int(color[0]/(radius+1)), -int(color[1]/(radius+1)), -int(color[2]/(radius+1)), 255)
		new_color = color_sum(color, color_decay)

		if(Light.bypass):
			transparency = True
		else:
			transparency = check_transparency(x,y, tilemap, objmap)

		visited = []
		available = [[x,y]]
		data = [[new_color, decayment, transparency]]
		flip = None

		while(available != []):
			x,y = available.pop(0)
			cd, dc, trans = data.pop(0)
			visited.append([x,y])

			if([x+1,y] not in visited and [x+1,y] not in available and trans):
				flip = Lightning.unpropagate(x+1, y, cd, dc, shadow_map)
				if([x+1,y] not in available and dc>decay and flip):
					available.append([x+1,y])
					data.append([color_sum(cd,color_decay), dc-decay, check_transparency(x+1,y,tilemap, objmap)])
			
			if([x-1,y] not in visited and [x-1,y] not in available and trans):
				flip = Lightning.unpropagate(x-1, y, cd, dc, shadow_map)
				if([x-1,y] not in available and dc>decay and flip):
					available.append([x-1,y])
					data.append([color_sum(cd,color_decay), dc-decay, check_transparency(x-1,y,tilemap, objmap)])
			
			if([x,y+1] not in visited and [x,y+1] not in available and trans):
				flip = Lightning.unpropagate(x, y+1, cd, dc, shadow_map)
				if([x,y+1] not in available and dc>decay and flip):
					available.append([x,y+1])
					data.append([color_sum(cd,color_decay), dc-decay, check_transparency(x,y+1,tilemap, objmap)])

			if([x,y-1] not in visited and [x,y-1] not in available and trans):
				flip = Lightning.unpropagate(x, y-1, cd, dc, shadow_map)
				if([x,y-1] not in available and dc>decay and flip):
					available.append([x,y-1])
					data.append([color_sum(cd,color_decay), dc-decay, check_transparency(x,y-1,tilemap, objmap)])
	
	@staticmethod
	def unpropagate(x, y, color_decay, decay, shadow_map):
		try:
			shadow_map[x][y].set_real_light(shadow_map[x][y].natural_light + decay)
			shadow_map[x][y].color = color_sum(shadow_map[x][y].color, (-color_decay[0], -color_decay[1], -color_decay[2], 255))
			return True
		except:
			return False

	############## Propagate all functions

	# Propagates daylight to shadows (used in propagate all)
	@staticmethod
	def propagate_to_shadow(x, y, tilemap, objmap, shadow_map, bypass_wall=False):
		try:
			if(shadow_map[x+1][y].daylight and shadow_map[x-1][y].daylight and shadow_map[x][y+1].daylight and shadow_map[x][y-1].daylight):
				return
		except IndexError:
			return

		level = shadow_map[x][y].natural_light
		color = shadow_map[x][y].color
		radius = shadow_map[x][y].radius

		decay = int((255 - level)/(radius+1))
		decayment = (255-level) - decay
		color_decay = (-int(color[0]/(radius+1)), -int(color[1]/(radius+1)), -int(color[2]/(radius+1)), 255)
		new_color = color_sum(color, color_decay)

		if(bypass_wall):
			transparency = True
		else:
			transparency = check_transparency(x,y, tilemap, objmap)

		visited = []
		available = [[x,y]]
		data = [[new_color, decayment, transparency]]

		while(available != []):
			x,y = available.pop(0)
			cd, dc, trans = data.pop(0)
			visited.append([x,y])


			if([x+1,y] not in visited and [x+1,y] not in available and trans and not shadow_map[x+1][y].daylight):
				Lightning.propagate(x+1, y, cd, dc, shadow_map)
				if([x+1,y] not in available and dc>decay):
					available.append([x+1,y])
					data.append([color_sum(cd,color_decay), dc-decay, check_transparency(x+1,y,tilemap, objmap)])
			
			if([x-1,y] not in visited and [x-1,y] not in available and trans and not shadow_map[x-1][y].daylight):
				Lightning.propagate(x-1, y, cd, dc, shadow_map)
				if([x-1,y] not in available and dc>decay):
					available.append([x-1,y])
					data.append([color_sum(cd,color_decay), dc-decay, check_transparency(x-1,y,tilemap, objmap)])
			
			if([x,y+1] not in visited and [x,y+1] not in available and trans and not shadow_map[x][y+1].daylight):
				Lightning.propagate(x, y+1, cd, dc, shadow_map)
				if([x,y+1] not in available and dc>decay):
					available.append([x,y+1])
					data.append([color_sum(cd,color_decay), dc-decay, check_transparency(x,y+1,tilemap, objmap)])

			if([x,y-1] not in visited and [x,y-1] not in available and trans and not shadow_map[x][y-1].daylight):
				Lightning.propagate(x, y-1, cd, dc, shadow_map)
				if([x,y-1] not in available and dc>decay):
					available.append([x,y-1])
					data.append([color_sum(cd,color_decay), dc-decay, check_transparency(x,y-1,tilemap, objmap)])
			

	# Darkens sunset propagated daylight
	@staticmethod
	def unpropagate_to_shadow(x, y, Light, tilemap, objmap, shadow_map, bypass_wall=False):
		try:
			if(shadow_map[x+1][y].daylight and shadow_map[x-1][y].daylight and shadow_map[x][y+1].daylight and shadow_map[x][y-1].daylight):
				return
		except IndexError:
			return

		level = Light.light
		radius = Light.radius

		decayment = level

		if(Light.bypass):
			transparency = True
		else:
			transparency = check_transparency(x,y, tilemap, objmap)

		# 1.775
		if(level < 0):
			decay = 0.35
		else:
			decay = -0.35

		visited = []
		available = [[x,y]]
		data = [[decayment+decay, transparency, radius]]
		flip = None

		while(available != []):
			x,y = available.pop(0)
			dc, trans, rd = data.pop(0)
			visited.append([x,y])

			if([x+1,y] not in visited and [x+1,y] not in available and trans and not shadow_map[x+1][y].daylight):
				flip = Lightning.unpropagate_shadow(x+1, y, dc, shadow_map)
				if([x+1,y] not in available and flip and rd != 0):
					available.append([x+1,y])
					data.append([dc+decay, check_transparency(x+1,y,tilemap, objmap), rd-1])
			
			if([x-1,y] not in visited and [x-1,y] not in available and trans and not shadow_map[x-1][y].daylight):
				flip = Lightning.unpropagate_shadow(x-1, y, dc, shadow_map)
				if([x-1,y] not in available and flip and rd != 0):
					available.append([x-1,y])
					data.append([dc+decay, check_transparency(x-1,y,tilemap, objmap), rd-1])
			
			if([x,y+1] not in visited and [x,y+1] not in available and trans and not shadow_map[x][y+1].daylight):
				flip = Lightning.unpropagate_shadow(x, y+1, dc, shadow_map)
				if([x,y+1] not in available and flip and rd != 0):
					available.append([x,y+1])
					data.append([dc+decay, check_transparency(x,y+1,tilemap, objmap), rd-1])

			if([x,y-1] not in visited and [x,y-1] not in available and trans and not shadow_map[x][y-1].daylight):
				flip = Lightning.unpropagate_shadow(x, y-1, dc, shadow_map)
				if([x,y-1] not in available and flip and rd != 0):
					available.append([x,y-1])
					data.append([dc+decay, check_transparency(x,y-1,tilemap, objmap), rd-1])
	
	@staticmethod
	def unpropagate_shadow(x, y, decay, shadow_map):
		try:
			if(shadow_map[x][y].natural_light + decay > 255):
				shadow_map[x][y].darkness_compensation += shadow_map[x][y].natural_light + decay - 255
				shadow_map[x][y].set_real_light(255)
			else:
				shadow_map[x][y].add_real_light(decay)
			return True
		except:
			return False

	# Natural light propagation
	@staticmethod
	def propagate_daylight(tilemap, objmap, shadowmap):
		for i in range(len(shadowmap)):
			for j in range(len(shadowmap[0])):
				if(shadowmap[i][j].daylight):
					Lightning.propagate_to_shadow(i,j, tilemap, objmap, shadowmap)		

	# Object light propagation
	@staticmethod
	def propagate_element_light(tilemap, objmap, shadowmap):
		for i in range(len(tilemap)):
			for j in range(len(tilemap[0])):
				if(tilemap[i][j].luminosity != None):
					shadowmap[i][j].set_real_light(shadowmap[i][j].natural_light - (255 - tilemap[i][j].luminosity.light))
					#shadowmap[i][j].color = color_sum(shadowmap[i][j].color, tilemap[i][j].luminosity.color)
					Lightning.propagate_light(i,j,tilemap[i][j].luminosity,tilemap,objmap,shadowmap)

		for i in range(0,len(objmap)):
			for j in range(0,len(objmap[0])):
				if(objmap[i][j].luminosity != None):
					shadowmap[i][j].set_real_light(shadowmap[i][j].natural_light - (255 - objmap[i][j].luminosity.light))
					#shadowmap[i][j].color = color_sum(shadowmap[i][j].color, objmap[i][j].luminosity.color)
					Lightning.propagate_light(i,j,objmap[i][j].luminosity,tilemap,objmap,shadowmap)

	@staticmethod
	def propagate_all(tilemap, objmap, shadowmap):
		Lightning.propagate_daylight(tilemap,objmap,shadowmap)
		Lightning.propagate_element_light(tilemap,objmap,shadowmap)
		