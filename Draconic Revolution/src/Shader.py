import pyglet as pg

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

def color_sub(t, s):
	red = t[0]-s[0]
	green = t[1]-s[1]
	blue = t[2]-s[2]
	alpha = t[3]-s[3]

	if(red > 255):
		red = 255
	if(blue > 255):
		blue = 255
	if(green > 255):
		green = 255
	if(alpha > 255):
		alpha = 255

	if(red < 0):
		red = 0
	if(blue < 0):
		blue = 0
	if(green < 0):
		green = 0
	if(alpha < 0):
		alpha = 0

	return (red, green, blue, alpha)


class Shader:
	def __init__(self):
		self.color = (0,0,0,0)
		self.opacity = 0
		self.texture = pg.image.SolidColorImagePattern((0,0,0,0)).create_image(1344,960).get_texture()
		self.texture = pg.sprite.Sprite(self.texture, x=0, y=120)

	def add_shade(self, color, opacity = 0):
		self.color = color_sum(self.color, color)
		self.opacity += opacity
		self.texture = pg.image.SolidColorImagePattern(self.color).create_image(1344,960).get_texture()
		self.texture = pg.sprite.Sprite(self.texture, x=0, y=120)
		self.texture.opacity = self.opacity

	def sub_shade(self, color, opacity = 0):
		self.color = color_sub(self.color, color)
		self.opacity -= opacity
		self.texture = pg.image.SolidColorImagePattern(self.color).create_image(1344,960).get_texture()
		self.texture = pg.sprite.Sprite(self.texture, x=0, y=120)
		self.texture.opacity = self.opacity

	def draw(self):
		if(self.opacity > 0):
			self.texture.draw()