import pygame as pg


class Tile:
	image = []
	passable = True

	def __init__(self, id, passable=True):
		self.image = pg.image.load(get_tile_index(id))
		self.passable = passable

def get_tile_index(id):
	if(id <= 0):
		return "none.png"

	ref = open("Tile_ref", "r")
	data = ref.read()
	return data.split("\n")[id].split("\t")[1]