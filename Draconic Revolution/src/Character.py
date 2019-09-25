import pyglet as pg
from pyglet.gl import *
from pyglet.image.codecs.png import PNGImageDecoder

class Character:

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


		self.movingframe = [pg.sprite.Sprite(self.animation[0]), pg.sprite.Sprite(self.animation[3]),
			pg.sprite.Sprite(self.animation[1]), pg.sprite.Sprite(self.animation[2])]
		self.stillframe = [pg.sprite.Sprite(self.img[0]), pg.sprite.Sprite(self.img[9]), 
			pg.sprite.Sprite(self.img[3]), pg.sprite.Sprite(self.img[6])]

		del self.animation
		del self.img

	def get_total_x(self):
		return self.pos[0]*64 + self.offset[0]

	def get_total_y(self):
		return self.pos[1]*64 + self.offset[1]

	def draw(self, DISC_POS, OFFSET):
		total_x = DISC_POS[0]*64 + OFFSET[0] - 704#704
		total_y = DISC_POS[1]*64 + OFFSET[1] + 568#568

		draw_pos = [self.get_total_x() - total_x, total_y - self.get_total_y()]

		# If is not moving
		
		if(not self.IS_MOVING):
			if(self.direction == 0):
				self.stillframe[0].x = draw_pos[0]
				self.stillframe[0].y = draw_pos[1]
				self.stillframe[0].draw()
			elif(self.direction == 1):
				self.stillframe[1].x = draw_pos[0]
				self.stillframe[1].y = draw_pos[1]
				self.stillframe[1].draw()
			elif(self.direction == 2):
				self.stillframe[2].x = draw_pos[0]
				self.stillframe[2].y = draw_pos[1]
				self.stillframe[2].draw()
			elif(self.direction == 3):
				self.stillframe[3].x = draw_pos[0]
				self.stillframe[3].y = draw_pos[1]
				self.stillframe[3].draw()

		# If is moving
		else:
			if(self.direction == 0):
				self.movingframe[0].x = draw_pos[0]
				self.movingframe[0].y = draw_pos[1]
				self.movingframe[0].draw()
			elif(self.direction == 1):
				self.movingframe[1].x = draw_pos[0]
				self.movingframe[1].y = draw_pos[1]
				self.movingframe[1].draw()
			elif(self.direction == 2):
				self.movingframe[2].x = draw_pos[0]
				self.movingframe[2].y = draw_pos[1]
				self.movingframe[2].draw()
			elif(self.direction == 3):
				self.movingframe[3].x = draw_pos[0]
				self.movingframe[3].y = draw_pos[1]
				self.movingframe[3].draw()		

		
