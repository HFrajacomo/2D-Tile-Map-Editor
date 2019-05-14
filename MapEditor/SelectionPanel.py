from Tile import Tile
import pygame as pg
from time import sleep

class SelectionPanel:
	bevel = None
	selections = [1,0,0,0,0,0,0,0,0]
	selected = 0
	pos = ""
	button_pos = []
	hitboxes = []
	panelsize = 0
	scaling = 2

	def __init__(self, bevel, pos, panelsize=32, scaling=2):
		self.pos = pos
		self.panelsize = panelsize
		self.bevel = bevel
		self.scaling = scaling

		for i in range(0,3):
			for j in range(0,3):
				self.hitboxes.append(pg.Rect((pos[0]+panelsize*scaling*j + j*15, pos[1]+i*panelsize*scaling+ (i+1)*6), (panelsize*scaling,panelsize*scaling)))
				self.button_pos.append((pos[0]+panelsize*scaling*j + j*15, pos[1]+i*panelsize*scaling+ (i+1)*6))

	def __iter__(self):
		return iter(self.hitboxes)

	def get(self):
		return self.selections[self.selected]
	
	def click(self, screen, pos):
		for i in range(len(self.hitboxes)):
			if(self.hitboxes[i].collidepoint(pos)):
				self.selected = i
				return True
		return False

	def select(self, i):
		if(i>8 or i<0):
			return False
		self.selected = i
		return True

	def draw_tiles(self, screen):
		for i in range(len(self.button_pos)):
			screen.blit(Tile(self.selections[i], scaling=self.scaling).image, self.button_pos[i])

	# Actual draw function for selection panel
	def draw_selected(self, screen):
		rectangle = pg.Rect((self.button_pos[self.selected][0]-2, self.button_pos[self.selected][1]-2), (self.scaling*self.panelsize+3, self.scaling*self.panelsize+3))
		self.bevel.draw(screen)
		self.draw_tiles(screen)
		pg.draw.rect(screen, pg.Color(255,0,0,255), rectangle, 2)

	# Insert new tile into selection
	def update_selected(self, id_):
		self.selections[self.selected] = id_
