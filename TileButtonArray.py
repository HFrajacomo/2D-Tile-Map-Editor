import pygame as pg
from TileButton import TileButton

class TileButtonArray:
	bevel = ""
	buttons = []
	index = 0
	pos = []
	size = 0
	h_spacing = 0
	v_spacing = 0
	scaling = 1


	def __init__(self, bvl, pos, i=0, size=32, spacing=8, v_spac=4, scaling=2):
		self.n = 0 # for Iterator
		self.bevel = bvl
		self.pos = pos
		self.index = i
		self.size = size
		self.h_spacing = spacing
		self.v_spacing = v_spac
		self.scaling = scaling

		j = 0
		row = 0

		file = open("Tiles\\Tile_ref", "r")
		for line in file.readlines():
			h_value = pos[0] + (j)*size*scaling + (j)*self.h_spacing
			if(not h_value <= self.bevel.get_size()[0] + 180):
				row += 1
				j = 0
				h_value = pos[0] + (j)*size*scaling + (j)*self.h_spacing

			if(row >= 4):
				break
			self.buttons.append(TileButton((h_value, pos[1] + v_spac + (int(size + v_spac))*row*scaling), size, int(line.split("\t")[0])))
			j += 1

	def __iter__(self):
		return self.buttons

	def __getitem__(self, i):
		return self.buttons[i]

	def __iter__(self):
		return iter(self.buttons)


	def draw_buttons(self, screen):
		for b in self.buttons:
			b.draw(screen)
