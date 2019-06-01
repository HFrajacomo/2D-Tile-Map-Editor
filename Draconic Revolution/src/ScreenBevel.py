import pygame as pg

class ScreenBevel:
	def __init__(self, width, height, rgb, pos):
		self.fullscreen = pg.Surface(((25*64), (25*64)))
		self.surf = pg.Surface((width, height))
		self.bg_color = rgb
		self.surf.fill(rgb)
		self.pos = pos
		self.rect = pg.Rect(pos, (width, height))

	def draw(self, screen):
		screen.blit(self.surf, self.pos)
		pg.display.update(self.rect)

	def update(self, screen):
		pg.display.update(pg.Rect(self.pos, self.surf.get_size()))

	def get_size(self):
		return self.surf.get_size()

	def scroll(self, screen, dx, dy):
		self.fullscreen.scroll(dx=dx, dy=dy)
		screen.blit(self.fullscreen, (0,0))
		self.update(screen)
