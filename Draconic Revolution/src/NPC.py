import pyglet as pg
from pyglet.gl import *
from pyglet.image.codecs.png import PNGImageDecoder

from Character import *
from AI import *

class NPC(Character, AI):
	def __init__(self, DP, OFFSET, filename):
		self.img = pg.image.load(filename)
		self.img = pg.image.ImageGrid(self.img, 4,3, item_width=64, item_height=64)
		self.img = pg.image.TextureGrid(self.img)
		
		self.animation = [pg.image.Animation.from_image_sequence(self.img[1:3], 0.3, loop=True), 
		pg.image.Animation.from_image_sequence(self.img[3:6], 0.3, loop=True),
		pg.image.Animation.from_image_sequence(self.img[6:9], 0.3, loop=True),
		pg.image.Animation.from_image_sequence(self.img[9:12], 0.3, loop=True)]
		
		self.direction = 1
		self.pos = DP.copy()
		self.offset = OFFSET.copy()
		self.IS_MOVING = False
		self.interrupt = "" # Triggers every odd interaction with the NPC
		self.current_action = "" # Saves last action in case of interruption
		self.speed = 1
		self.position = 0

		self.movingframe = [pg.sprite.Sprite(self.animation[0]), pg.sprite.Sprite(self.animation[3]),
			pg.sprite.Sprite(self.animation[1]), pg.sprite.Sprite(self.animation[2])]
		self.stillframe = [pg.sprite.Sprite(self.img[0]), pg.sprite.Sprite(self.img[9]), 
			pg.sprite.Sprite(self.img[3]), pg.sprite.Sprite(self.img[6])]

		del self.animation
		del self.img	


	def run(self, map, intermap, intermap_obj):
		#self.move_to([60, 60], map, intermap, intermap_obj)
		pass