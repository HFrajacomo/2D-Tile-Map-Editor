from time import sleep
from Lightning import *

class Time:
	def __init__(self, min, sec):
		self.min = min
		self.sec = sec

	def __str__(self):
		if(self.min >=10 and self.sec>=10):
			return f"{self.min}:{self.sec}"
		elif(self.min < 10 and self.sec < 10):
			return f'0{self.min}:0{self.sec}'
		elif(self.min < 10):
			return f'0{self.min}:{self.sec}'
		else:
			return f'{self.min}:0{self.sec}'


	def __repr__(self):
		return str(self)

	def inc(self):
		self.sec += 1
		if(self.sec > 59):
			self.sec = 0
			self.min += 1
			if(self.min > 23):
				self.min = 0

	def inc_hour(self):
		self.min += 1
		if(self.min >23):
			self.min = 0

	def set(self, min, sec):
		self.min = min
		self.sec = sec

	def get_hour(self):
		return self.min

	def get_seconds(self):
		return self.sec

class DaylightConfigurator:
	def __init__(self):
		self.current_level = 0

	# Controls global daylight depending on time of day and map config
	def update_daylight(self, config, tilemap, objmap, shadowmap, clock):
		if(config != "Surface"):
			return

		h = clock.get_hour()
		s = clock.get_seconds()

		# Surface Light Configuration
		if(h == 5 or h == 6):
			self.current_level = -2.125
		elif(h == 18 or h == 19 or (h == 20 and s == 0)):
			self.current_level = 2.125
		else:
			return

		self.__change_daylight(tilemap, objmap, shadowmap)

	def __change_daylight(self, tilemap, objmap, shadowmap):
		for i in range(len(shadowmap)):
			for j in range(len(shadowmap[0])):
				if(shadowmap[i][j].daylight):
					shadowmap[i][j].set_real_light(shadowmap[i][j].natural_light + int(self.current_level))
					Lightning.unpropagate_to_shadow(i,j, Lightning(self.current_level, 5), tilemap, objmap, shadowmap)
