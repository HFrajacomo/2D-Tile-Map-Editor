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
	def update_daylight(self, config, shadowmap, clock):
		if(config != "Surface"):
			return

		h = clock.get_hour()
		s = clock.get_seconds()

		# Surface Light configuration

		if(h >= 20 or h < 5):
			self.current_level = 255
		elif(h == 5 and s == 0):
			self.current_level = 0
		elif(h == 5):
			self.current_level = -2.372
		elif(h == 6 and s == 0):
			self.current_level = -0.052
		elif(h == 6):
			self.current_level = -1.694
		elif(h == 7 and s == 0):
			self.current_level = -0.054
		elif(h == 18 and s == 0):
			self.current_level = 0	
		elif(h == 18):
			self.current_level = 1.694
		elif(h == 19 and s == 0):
			self.current_level = 0.054
		elif(h == 19):
			self.current_level = 2.372
		elif(h == 20 and s == 0):
			self.current_level = 0.052
		if(h >= 20 or h < 5):
			self.current_level = 0
		if(h >= 7 and h < 18):
			self.current_level = 0		

		if(self.current_level == 0): # If no change, return
			return

		self.__change_daylight(shadowmap)

	def __change_daylight(self, shadowmap):
		for i in range(len(shadowmap)):
			for j in range(len(shadowmap[0])):
				if(shadowmap[i][j].daylight):
					shadowmap[i][j].set_real_light(shadowmap[i][j].natural_light + self.current_level)
