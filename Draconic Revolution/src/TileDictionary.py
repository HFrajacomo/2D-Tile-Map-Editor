from Tile import *

tile_dictionary = {-1:NoneTile(),
0:NoneTile(), 
2:CobbleHard(),
3:CobbleLight(),
7:WoodBlock(),
9:StoneBrick(),
10:StoneBrick(),
11:BasaltFloor(),
12:BasaltBrick(),
13:CobbleLight(),
14:CheckerFloor(),
15:CobbleHard(),
16:CobbleStairs(),
17:CobbleStairs(),
18:GrassCliff(),
19:GrassCliff(),
20:Grass(),
21:GrassCliff(),
22:GrassCliff(),
23:GrassCliff(),
24:WoodPlank(),
25:WoodPlank(),
26:WoodPlank(),
27:CobbleHard(),
28:Water(),
29:Sand(),
30:Dirt(),
31:RedCarpet(),
32:RedCarpet(),
33:RedCarpet(),
34:RedCarpet(),
35:RedCarpet(),
36:RedCarpet(),
37:RedCarpet(),
38:RedCarpet(),
39:RedCarpet(),
40:GrassCliff(),
41:GrassCliff(),
42:CobbleHard()
}

def gen_tile(id):
	try:
		aux = tile_dictionary[id]
		return aux
	except:
		return False