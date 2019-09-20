from Tile import *

animated_dictionary = [{28:AnimatedTile(28,1)}]
animated_dictionary_interactive = {28:Water()}

def gen_atile_inter(id):
		return animated_dictionary_interactive[id]

def gen_atile(id):
	try:
		aux = animated_dictionary[id]
		return aux
	except:
		return False