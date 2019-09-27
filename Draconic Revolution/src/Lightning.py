import pyglet as pg

class Lightning:
	dictionary = {}

	def __init__(self, light, color=(0,0,0,255)):
		self.max_light = light
		self.current_light = light
		self.color = color

	@staticmethod
	def get(color):
		if(Lightning.dictionary.get(color, False) == False):
			Lightning.dictionary[color] = pg.image.SolidColorImagePattern(color).create_image(64,64).get_texture()
		return Lightning.dictionary[color]