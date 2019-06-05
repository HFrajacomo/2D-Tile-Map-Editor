from bresenham import *
import pygame as pg

def remove_duplicates(l):
	aux = []
	for element in l:
		if(element not in aux):
			aux.append(element)
	return aux

def get_region(m, player_pos):
	x_start = player_pos[1]-7
	y_start = player_pos[0]-10
	matrix = []
	breaker = False
	breaker_index = 0

	for i in range(x_start, x_start+16):
		matrix.append([])
		for j in range(y_start, y_start+22):
			try:
				matrix[-1].append(m[i][j])
			except IndexError:
				breaker = True
				breaker_index = i
				break
		if(breaker):
			break

	if(breaker):
		for i in range(0, x_start+16-breaker_index-1):
			matrix.append([])
			for j in range(y_start, y_start+22):
				matrix[-1].append(m[i][j])

	return matrix


def line_of_sight(pos, m):
	darkness = []
	protected = []
	dark = False

	m = get_region(m, pos)


	for i in range(0,16):
		for j in range(0,23):
			for element in bresenham(7,11,i,j):
				try:
					if(dark):
						darkness.append(element)
					elif(m[element[0]][element[1]].transparency == False):
						protected.append(element)
						dark = True
				except:
					pass
			dark = False

	protected = remove_duplicates(protected)
	darkness = remove_duplicates(darkness)
	for element in protected:
		if(element in darkness):
			darkness.remove(element)
	return darkness