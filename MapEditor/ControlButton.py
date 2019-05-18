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
		self.image = pg.image.load("MapEditor\\Images\\" + img_name)
		self.hitbox = pg.Rect(pos, (self.image.get_width(), self.image.get_height()))

		screen.blit(self.image, self.pos)

	def action(self, tiledmap):
		return self.save(tiledmap), None

	def save(self, tiledmap):
		# Save as
		if(tiledmap.map_.name == "" or self.saveas):
			name = filesavebox(title="Save Map", default="MapEditor\\Maps\\")
			if(name != None):
				file = open(os.path.splitext(name)[0] + ".map", "w")
				file.write(">" + os.path.splitext(os.path.basename(name))[0] + "\t" + str(tiledmap.win_cord) + "\n")
				for row in tiledmap.map_.grid:
					file.write(",".join([str(x) for x in row]) + "\n")
				file.write("&\n")
				for row in tiledmap.map_.obj_grid:
					file.write(",".join([str(x) for x in row]) + "\n")
				file.write("&\n")
				for row in tiledmap.map_.light_grid:
					file.write(",".join([str(x) for x in row]) + "\n")
				file.close()
				
		# Save
		else:
			file = open("MapEditor\\Maps\\" + tiledmap.map_.name + ".map", "w")
			file.write(">" + tiledmap.map_.name + "\t" + str(tiledmap.win_cord) + "\n")
			for row in tiledmap.map_.grid:
				file.write(",".join([str(x) for x in row]) + "\n")
			file.write("&\n")
			for row in tiledmap.map_.obj_grid:
				file.write(",".join([str(x) for x in row]) + "\n")	
			file.write("&\n")
			for row in tiledmap.map_.light_grid:
				file.write(",".join([str(x) for x in row]) + "\n")
			file.close()

class LoadButton(Button):
	def __init__(self, screen, pos, img_name):
		self.pos = pos
		self.image = pg.image.load("MapEditor\\Images\\" + img_name)
		self.hitbox = pg.Rect(pos, (self.image.get_width(), self.image.get_height()))

		screen.blit(self.image, self.pos)

	def action(self, tiledmap):
		return self.load()

	def load(self):	
		filename = fileopenbox(title="Load map", filetypes=["*.map"], default="MapEditor\\Maps\\")
		map_name = ""
		map_data = []
		obj_data = []
		light_data = []
		count_of_es = 0

		if(filename != None):
			file = open(filename, "r")
			lines = file.readlines()
			file.close()
			for i in range(len(lines)):
				if(i == 0):
					map_name = lines[i][1:].split("\t")[0]
					map_cord = (int(lines[i][1:].split("\t")[1].split(",")[0].replace("(", "")), int(lines[i][1:].split("\t")[1].split(",")[1].replace(")", "")))
				else:
					if(lines[i] == "&\n"):
						count_of_es += 1
					elif(count_of_es == 0): # Gathering map data
						map_data.append([int(x) for x in lines[i].split(",")])
					elif(count_of_es == 1):
						obj_data.append([int(x) for x in lines[i].split(",")])
					elif(count_of_es == 2):
						light_data.append([int(x) for x in lines[i].split(",")])

			return Map(map_data, obj_data, light_data, mapname=map_name), map_cord
		return None, None

class NewButton(Button):

	def __init__(self, screen, pos, img_name):
		self.pos = pos
		self.image = pg.image.load("MapEditor\\Images\\" + img_name)
		self.hitbox = pg.Rect(pos, (self.image.get_width(), self.image.get_height()))

		screen.blit(self.image, self.pos)

	def action(self, tiledmap):
		return self.new(tiledmap), None

	def new(self, tiledmap):
		tiledmap.win_cord = (0,0)
		tiledmap.load_map(Map([[0]], [[0]], mapname=""))
