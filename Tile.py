import pygame as pg


class Tile:
	image = []

	def __init__(self, id):
		self.image = pg.image.load(get_tile_index(id))

def get_tile_index(id):
	if(id <= 0):
		return "Tiles\\none.png"

	ref = open("Tiles\\Tile_ref", "r")
	data = ref.read()
	return "Tiles\\" + data.split("\n")[id].split("\t")[1]