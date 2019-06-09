from bresenham import *
import pygame as pg
from threading import Thread, Event

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
	global threaded_result

	m = get_region(m, pos)
	threads = []
	density = 2

	threads.append(Thread(target=threaded_sight, args=([14,22], m, [0,16,0,22])))
	threads.append(Thread(target=threaded_sight, args=([14,23], m, [0,16,22,44])))
	threads.append(Thread(target=threaded_sight, args=([15,22], m, [16,32,0,22])))
	threads.append(Thread(target=threaded_sight, args=([15,23], m, [16,32,22,44])))

	for th in threads:
		th.start()
	output = set()
	for th in threads:
		th.join()

	for element in threaded_result:
		output = output | element

	threaded_result = []

	return output

	'''
	for i in range(0,32):
		for j in range(0,44):
			for element in bresenham(14,22,i,j):
				try:
					if(dark == 2):
						darkness.add(element)
					elif(m[int(element[0]/2)][int(element[1]/2)].transparency == False):
						protected.add(element)
						dark += 1
				except:
					pass
			dark = 0

	darkness = darkness - protected
	return darkness
	'''

def threaded_sight(pos, m, rang):
	global threaded_result

	darkness = set()
	protected = set()
	dark = 0

	for i in range(rang[0],rang[1]):
		for j in range(rang[2],rang[3]):
			for element in bresenham(pos[0],pos[1],i,j):
				try:
					if(dark == 2):
						darkness.add(element)
					elif(m[int(element[0]/2)][int(element[1]/2)].transparency == False):
						protected.add(element)
						dark += 1
				except:
					pass
			dark = 0

	darkness = darkness - protected
	threaded_result.append(darkness)

threaded_result = []
ev = Event()
ev.set()