import pygame as pg
import sys
import os


'''
argv[1] = "tile" or "object"
'''

assign_dir = None
already_assigned = []
assign_type = sys.argv[1]

if(assign_type == "tile"):
	assign_dir = "Tile_ref"
elif(assign_type == "object"):
	assign_dir = "Obj_ref"
else:
	print("Only 'tile' and 'object' values are supported for argument")
	exit()

ref_file = open("ChoppedTiles\\" + assign_dir, "r")
count = int(ref_file.readlines()[-1].split("\t")[0]) + 1
ref_file.seek(0)

for line in ref_file.readlines():
	already_assigned.append(line.split("\t")[1].replace("\n", ""))
ref_file.close()

ref_file = open("ChoppedTiles\\" + assign_dir, "a")

for r,d,f in os.walk("ChoppedTiles\\"):
	for file in f:
		if(file == "Tile_ref" or file == "Obj_ref" or file in already_assigned):
			continue

		ref_file.write("\n" + file.split(".")[0])
		count += 1
ref_file.close()

