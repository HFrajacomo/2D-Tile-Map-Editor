from easygui import *
import pygame as pg
import os

class Button:
	pos = None
	hitbox = None
	image = None

	def click(self, pos):
		if(not self.hitbox.collidepoint(pos)):
			return False
		return True

	def action(self, screen, tup):
		pass


class SaveButton(Button):

	# do saveas=False to make a simple save button
	def __init__(self, screen, pos, img_name):
		self.pos = pos
		self.image = pg.image.load("ModelEditor\\Images\\" + img_name)
		self.hitbox = pg.Rect(pos, (self.image.get_width(), self.image.get_height()))

		screen.blit(self.image, self.pos)

	def action(self, screen, tup, surface):
		return self.save(screen, tup), None

	def save(self, screen, tup):
		name = filesavebox(title="Save Model", default="ModelEditor\\Models\\")
		if(name != None):
			surface = screen.subsurface(pg.Rect((tup[0]/2-64, tup[1]/2-64), (128,128)))
			pg.image.save(surface, name + ".png")


class LoadButton(Button):
	code = False  # False = Tile, True = Model

	def __init__(self, screen, pos, img_name, code):
		self.pos = pos
		self.image = pg.image.load("ModelEditor\\Images\\" + img_name)
		self.hitbox = pg.Rect(pos, (self.image.get_width(), self.image.get_height()))
		self.code = code

		screen.blit(self.image, self.pos)

	def action(self, screen, tup, surface):
		return self.load()

	def load(self):	
		filename = fileopenbox(title="Load Model", filetypes=["*.png"], default="MapEditor\\Tiles\\")
		if(filename == None):
			return None, None

		image = pg.transform.scale(pg.image.load(filename), (128,128))
		image = image.convert_alpha()


		return image, self.code

class NewButton(Button):
	code = False

	def __init__(self, screen, pos, img_name):
		self.pos = pos
		self.image = pg.image.load("ModelEditor\\Images\\" + img_name)
		self.hitbox = pg.Rect(pos, (self.image.get_width(), self.image.get_height()))

		screen.blit(self.image, self.pos)

	def action(self, screen, tup, surface):
		return self.new(surface), None

	def new(self, surface):
		surface.fill((0,0,0))
		surface.convert_alpha()
