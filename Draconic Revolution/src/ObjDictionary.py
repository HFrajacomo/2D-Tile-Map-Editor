from Obj import *

def gen_obj(id):
	return obj_dictionary[id]

# Adds callables (classes) to key ident in obj_dictionary
def add(ident, callable):
	global obj_dictionary

	if(type(ident) == int):
		obj_dictionary[ident] = callable(ident)
	elif(type(ident) == list):
		for el in ident:
			obj_dictionary[el] = callable(el)
	elif(type(ident) == range):
		ident = list(ident)
		for el in ident:
			obj_dictionary[el] = callable(el)

obj_dictionary = {}

# Fill obj_dict
add([-1,0], NoneObj)
add(range(1,7), VegetableStand)
add([7,8,53], Logs)
add(range(14,28), Fountain)
add([28,29,541,542,543,544], Statue)
add(range(30,35), GraveStone)
add([39,175], WoodenBarrel)
add([40,41], Bucket)
add([43,196,199], Bush)
add([46,48,50,163,164,165,166,167,183,184,185,442,334,351,368], ItemCrate)
add(47, Crate)
add([49,63], EmptyCrate)
add([52,54,55,56,57,402,403,436,437,455], Flower)
add(range(152,159), FoodBasket)
add([421,422,440,441], FoodBasket)
add(range(227,237), Blackboard)
add([512,565,566,567,245,246,247,
	259,260,261,262,263,264,265,266,511,306,314,315,459,460,477,478,496], Chair)
add([514,515,527,529,532,533,572, 256,257,258,248,428,328,463,475,480,508,498], Table)
add([510,525,526,509,288,289,439,450,490,491], Bed)
add([539,540,187,188,190,191,192,193], Piles)
add(range(545,554), Hangings)
add([559,560,561,159,160,161,162,180,181,182,186,189,194,405,438,399,400,
	401,316,317,332,352,369], Hangings)
add(range(554,560), Altar)
add([562,563,564,565,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,
	132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,151,
	225,226], Fence)
add([568,98], Window)
add([67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,86,569,575], Sign)
add([570,571], Pillar)
add([64,65], Stone)
add([66,365,44,45,46,195,197,198,42], TallGrass)
add(range(576,580), Bookshelf)
add(range(237,245), Bookshelf)
add([594,595], SilverwoodTree)
add([82,83,84,85,101,102,103,104], Stairs)
add(range(597,600), LightPole)
add(range(600,603), Torch)
add([105,106], Counter)
add([107,108,109,111,112,113], Door)
add([110,114,115,116,603,604], OpenDoor)
add(range(168,174), Sack)
add(174, Anvil)
add(range(176,180), Forge)
add(range(201,207), OakTree)
add(range(219,225), PineTree)
add([389,408,427,432,433,445,319,448,321,449,323,451,336,338,341,357,586,587], Cupboard)
add(range(270,282), Bottle)
add(range(249,256), Slider)
add([365,366,384,382], FlowerPot)
add([580,581,582,583,584,585,588,589,590,591,592,593], Throne)