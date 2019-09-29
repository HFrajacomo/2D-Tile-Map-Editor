from time import sleep

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