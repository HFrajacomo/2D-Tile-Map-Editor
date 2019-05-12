from Map import Map
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

	def action(self, map_):
		pass


class SaveButton(Button):
	saveas = True


	# do saveas=False to make a simple save button
	def __init__(self, screen, pos, img_name, saveas=True):
		self.saveas = saveas
		self.pos = pos
		self.image = pg.image.load("Images\\" + img_name)
		self.hitbox = pg.Rect(pos, (self.image.get_width(), self.image.get_height()))

		screen.blit(self.image, self.pos)

	def action(self, map_):
		self.save(map_)

	def save(self, map_):
		# Save as
		if(map_.name == "" or self.saveas):
			name = filesavebox(title="Save Map", default="Maps\\")
			if(name != None):
				file = open(os.path.splitext(name)[0] + ".map", "w")
				file.write(">" + os.path.splitext(os.path.basename(name))[0] + "\n")
				for row in map_.grid:
					file.write(",".join([str(x) for x in row]) + "\n")
		# Save
		else:
			file = open(map_.name + ".map", "w")
			file.write(">" + map_.name + "\n")
			for row in map_.grid:
				file.write(",".join([str(x) for x in row]) + "\n")
			file.close()

class LoadButton(Button):
	def __init__(self, screen, pos, img_name):
		self.pos = pos
		self.image = pg.image.load("Images\\" + img_name)
		self.hitbox = pg.Rect(pos, (self.image.get_width(), self.image.get_height()))

		screen.blit(self.image, self.pos)

	def action(self, map_):
		return self.load()

	def load(self):	
		filename = fileopenbox(title="Load map", filetypes=["*.map"], default="Maps\\")
		map_name = ""
		map_data = []
		if(filename != None):
			file = open(filename, "r")
			lines = file.readlines()
			file.close()
			for i in range(len(lines)):
				if(i == 0):
					map_name = lines[i][1:].replace("\n", "")
				else:
					map_data.append([int(x) for x in lines[i].split(",")])

			return Map(map_data, mapname=map_name)
