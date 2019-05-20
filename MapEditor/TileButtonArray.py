import pygame as pg
from TileButton import TileButton
from Obj import Obj

class TileButtonArray:

	def __init__(self, bvl, pos, mode=True, i=0, size=32, spacing=8, v_spac=4, scaling=2):
		self.tilemode = mode
		self.n = 57  # Max amount of tiles on screen each time
		self.bevel = bvl
		self.pos = pos
		self.index = i # Tile page
		self.size = size
		self.h_spacing = spacing
		self.v_spacing = v_spac
		self.scaling = scaling
		self.current_page = 0
		self.buttons = []

		if(not self.tilemode):
			file = open("MapEditor\\Objects\\Obj_ref", "r")
			lines = file.readlines()
			file.close()
		else:
			file = open("MapEditor\\Tiles\\Tile_ref", "r")
			lines = file.readlines()
			file.close()

		self.page_number = int(len(lines)/self.n)

		j = 0
		row = 0
		i = 0
		
		for line in lines:
			h_value = pos[0] + (j)*size*scaling + (j)*self.h_spacing
			if(not h_value <= self.bevel.get_size()[0] + 180):
				row += 1
				j = 0
				h_value = pos[0] + (j)*size*scaling + (j)*self.h_spacing

			if(row >= 4):
				break

			if(self.tilemode):
				self.buttons.append(TileButton((h_value, pos[1] + v_spac + (int(size + v_spac))*row*scaling), size, i, True))
			else:
				self.buttons.append(TileButton((h_value, pos[1] + v_spac + (int(size + v_spac))*row*scaling), size, i, False))

			i += 1
			j += 1


	def __iter__(self):
		return iter(self.buttons)

	def draw_buttons(self, screen, tilemode):
		if(not tilemode):
			self.bevel.draw(screen)
		for b in self.buttons:
			b.draw(screen)

	def change_page(self, screen, tilemode, forward=True):
		self.buttons = []

		if(self.current_page == 0 and not forward):
			return
		elif(self.current_page == self.page_number and forward):
			return
		elif(forward):
			self.current_page += 1
		else:
			self.current_page -= 1

		if(self.tilemode):
			file = open("MapEditor\\Tiles\\Tile_ref", "r")
			lines = file.readlines()
			file.close()
		else:
			file = open("MapEditor\\Objects\\Obj_ref", "r")
			lines = file.readlines()
			file.close()

		j = 0
		row = 0

		for i in range(self.current_page*self.n, (self.current_page+1)*self.n):
			if(i >= len(lines)):
				break

			h_value = self.pos[0] + (j)*self.size*self.scaling + (j)*self.h_spacing
			if(not h_value <= self.bevel.get_size()[0] + 180):
				row += 1
				j = 0
				h_value = self.pos[0] + (j)*self.size*self.scaling + (j)*self.h_spacing

			if(row >= 4):
				break
			self.buttons.append(TileButton((h_value, self.pos[1] + self.v_spacing + (int(self.size + self.v_spacing))*row*self.scaling), self.size, i, tilemode))

			j += 1		

		if(self.current_page == self.page_number):
			self.bevel.draw(screen)
		self.draw_buttons(screen, tilemode)
