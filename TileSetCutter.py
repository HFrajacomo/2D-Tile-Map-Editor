import pygame as pg
import sys


def strcode(num):
	dikt = {0:"a", 1:"b", 2:"c", 3:"d", 4:"e", 5:"f", 6:"g", 7:"h", 8:"i", 9:"j", 10:"k", 11:"l", 12:"m", 13:"n", 14:"o", 15:"p", 16:"q", 17:"r", 18:"s", 19:"t", 20:"u", 21:"v", 22:"x", 23:"z", 24:"w"}
	acc = ""
	while(num > 24):
		acc += "z"
		num -= 24
	acc += dikt[num]

	return acc

def codetonum(code):
	dikt = {"a":0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7, "i":8, "j":9, "k":10, "l":11, "m":12, "n":13, "o":14, "p":15, "q":16, "r":17, "s":18, "t":19, "u":20, "v":21, "x":22, "z":23, "w":24}
	num = 0
	for element in code:
		if(element == "z"):
			num += 24
		else:
			return num + dikt[element]

'''
argv[1] = filename
argv[2] = tile size
'''

filename = sys.argv[1]
size = int(sys.argv[2])
surf_array = []
file = open("Tiles\\Tile_ref", "r")
count = int(file.readlines()[-1].split("\t")[0]) + 1
file.close()

tileset = pg.image.load(filename)
for i in range(0, tileset.get_height(), size):
	for j in range(0, tileset.get_width(), size):
		surf_array.append(tileset.subsurface(pg.Rect((i,j), (size,size))))


file = open("Tiles\\Tile_ref", "a")

for element in surf_array:
	pg.image.save(element, "Tiles\\" + strcode(count) + ".png")
	file.write("\n" + str(count) + "\t" + strcode(count) + ".png")
	count += 1
