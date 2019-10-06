import zmq
from Time import *
from time import sleep
from threading import Thread, Lock
from NetMessage import *
from ServerHolder import *
from NPC import *
from Player import *
from Map import *
from datetime import datetime
import colorama
from colorama import Fore

colorama.init(autoreset=True)

def list_remove(lista, e):
	aux = []
	for elem in lista:
		aux.append(elem)
	aux.remove(e)
	return aux

def generate_entity_layer(m):
	entity_layer = []

	for i in range(len(m.grid)):
		entity_layer.append([])
		for j in range(len(m.grid[0])):
			entity_layer[-1].append([])

	return entity_layer

# Adds player to entity layer
def add_player(p):
	global players_dict
	global connected_player_ids

	i = 1
	while(i in connected_player_ids):
		i += 1

	connected_player_ids.append(i)
	players_dict[i] = p	

	return i

# Adds entity to entity layer
def add_entity(e):
	global entities_dict
	global connected_entity_ids
	global entity_layer

	i = -1
	while(i in connected_entity_ids):
		i -= 1

	connected_entity_ids.append(i)
	entities_dict[i] = e	
	entity_layer[e.pos[0]][e.pos[1]].append(i)
	entities_dict[i].id = i

# Converts string to byte string
def byt(text):
	return text.encode("UTF-8")

# Sends a message to all connected
def broadcast(sock, m):
	global connections

	for conn in connections:
		sock.send_multipart([conn, byt(-m)])

# Sends entities position to players
def npc_info():
	global npc_socket
	global connections
	global player_known_ids
	global players_dict
	global entities_dict
	global loaded_npcs

	while(not QUIT):
		currently_loaded = set()
		t = datetime.now()
		for conn in connections:
			try:
				for id in player_known_ids[connection_to_id[conn]]:
					currently_loaded.add(id)
					if(id == connection_to_id[conn]):
						continue
					if(id > 0):
						entity = players_dict[id]
					else:
						entity = entities_dict[id]

					data = str(id) + ";" + str(entity.pos)[1:-1] + ";" + str(entity.offset)[1:-1] + ";" + str(entity.direction) + ";" + str(entity.IS_MOVING)
					npc_socket.send_multipart([conn, byt(-NetMessage("NPC_INFO", data))])
			except KeyError:
				continue

		loaded_npcs = currently_loaded


		# FPS calibrator
		dt = (t - datetime.now()).total_seconds()
		if(dt > 1/60):
			print("Npc information is overloaded!")
		else:
			sleep(1/60 - dt)	

# Sends layer information to connected users Thread
def layer_refreshment():
	global entity_layer
	global layer_socket
	global connections
	global player_known_ids
	global LOCK

	while(not QUIT):
		t = datetime.now()
		
		for conn in connections:
			found_ids = []
			id = connection_to_id[conn]
			pos = players_dict[id].pos

			for i in range(pos[0] - 24, pos[0] + 25): # 24 25
				for j in range(pos[1] - 24, pos[1] + 25):
					if(i>=len(entity_layer) and j>=len(entity_layer[0])):
						i -= len(entity_layer)
						j -= len(entity_layer[0])
					elif(i>=len(entity_layer)):
						i -= len(entity_layer)
						if(entity_layer[i][j] != []):
							for entity in entity_layer[i][j]:
								found_ids.append(entity)
					elif(j>=len(entity_layer[0])):
						j -= len(entity_layer[0])
						if(entity_layer[i][j] != []):
							for entity in entity_layer[i][j]:
								found_ids.append(entity)
					else:
						if(entity_layer[i][j] != []):
							for entity in entity_layer[i][j]:
								found_ids.append(entity)

			player_known_ids[id] = found_ids
			found_ids = list(set(found_ids))
			n = NetMessage("ENTITIES", str(found_ids)[1:-1])
			layer_socket.send_multipart([conn, byt(-n)])

		# FPS calibrator
		dt = (t - datetime.now()).total_seconds()
		if(dt > 1):
			print("Refresher is overloaded!")
		else:
			sleep(1 - dt)	

# Time processing thread
def timer():
	global global_timer
	global LOCK
	global timer_socket

	while(not QUIT):
		t = datetime.now()
		broadcast(timer_socket, NetMessage("TIME", str(global_timer)))
		
		global_timer.inc()
		print("TIMER: " + str(global_timer))

		# FPS calibrator
		dt = (t - datetime.now()).total_seconds()
		if(dt > 1):
			print("Timer is overloaded!")
		else:
			sleep(1 - dt)		

# Global Receive
def receive():
	global receive_socket
	global connections
	global players_dict
	global connection_to_id
	global entity_layer

	while(not QUIT):
		try:
			address, data = receive_socket.recv_multipart(zmq.NOBLOCK)
		except zmq.Again:
			continue

		data = data.decode()
		m = NetMessage(data)
		print("RECEIVE: " + data)

		# Assigning ID and connection to entrant users
		if(m.type == "IDENTITY"):
			if(connections == []):
				new_ident = byt("0")
				receive_socket.send_multipart([address, new_ident])
				connections.append(new_ident)
			else:
				new_ident = byt(str(int(connections[-1])+1))
				receive_socket.send_multipart([address, new_ident])
				connections.append(new_ident)

			disc_pos, offset, filename = m.data.split(";")
			disc_pos = [int(x) for x in disc_pos.split(",")]
			offset = [int(x) for x in offset.split(",")]
			id = add_player(Player(disc_pos, offset, filename, server=True))
			receive_socket.send_multipart([new_ident, byt(-NetMessage("PLAYER_ID", str(id)))])
			connection_to_id[new_ident] = id
			entity_layer[disc_pos[0]][disc_pos[1]].append(id)

		# Update users position data (Every step)
		elif(m.type == "POSITION"):
			players_dict[connection_to_id[address]].pos = [int(x) for x in m.data.split(";")[0].split(",")]
			players_dict[connection_to_id[address]].offset = [int(x) for x in m.data.split(";")[1].split(",")]
			players_dict[connection_to_id[address]].direction = int(m.data.split(";")[2])
			if(m.data.split(";")[3] == "True"):
				players_dict[connection_to_id[address]].IS_MOVING = True
			else:
				players_dict[connection_to_id[address]].IS_MOVING = False

			disc_pos = players_dict[connection_to_id[address]].pos
			id = int(connection_to_id[address])
			if(id not in entity_layer[disc_pos[0]][disc_pos[1]]):
				entity_layer[disc_pos[0]][disc_pos[1]].append(id)

		# Change users position in entity layer (Every block change)
		elif(m.type == "CHANGE_POS"):
			id = int(connection_to_id[address])
			disc_pos = [int(x) for x in m.data.split(",")]
			
			if(id in entity_layer[disc_pos[0]][disc_pos[1]]):
				entity_layer[disc_pos[0]][disc_pos[1]] = list_remove(entity_layer[disc_pos[0]][disc_pos[1]], id)

		# Sends requested id information
		elif(m.type == "REQ_ENTITY"):
			id = int(m.data)
			if(id == connection_to_id[address]):
				continue
			elif(id > 0):
				receive_socket.send_multipart([address, byt(-NetMessage("ENTITY_INFO", str(id) + "#" + str(players_dict[id])))])
			else:
				receive_socket.send_multipart([address, byt(-NetMessage("ENTITY_INFO", str(id) + "#" + str(entities_dict[id])))])

# NPC activities thread
def NPC_run(FPS):
	global NPCS
	global inter_map
	global inter_map_obj
	global s
	global entity_layer
	global QUIT
	global LOCK

	while(not QUIT):
		t = datetime.now()
		for npc in NPC.all_npcs:
			if(npc.id in loaded_npcs):
				npc.run(FPS, inter_map, inter_map_obj, entity_layer)

		# FPS calibrator
		dt = (t - datetime.now()).total_seconds()
		if(dt > 1/60):
			print("NPCs are overloaded!")
		else:
			sleep(FPS - dt)


m, inter_map, inter_map_obj, shadow_map = loadmap("map\\draconis")
entity_layer = generate_entity_layer(m)

QUIT = False

context = zmq.Context()
receive_socket = context.socket(zmq.ROUTER)
timer_socket = context.socket(zmq.ROUTER)
layer_socket = context.socket(zmq.ROUTER)
npc_socket = context.socket(zmq.ROUTER)
HOST = "127.0.0.1"
PORT = 33000
receive_string = "tcp://" + HOST + ":" + str(PORT)
timer_string = "tcp://" + HOST + ":" + str(PORT+1)
layer_string = "tcp://" + HOST + ":" + str(PORT+2)
npc_string = "tcp://" + HOST + ":" + str(PORT+3)
receive_socket.bind(receive_string)
timer_socket.bind(timer_string)
layer_socket.bind(layer_string)
npc_socket.bind(npc_string)

global_timer = Time(12,0)

connections = []

# Entities tracking
players_dict = {}
entities_dict = {}
connected_player_ids = []
connected_entity_ids = []
connection_to_id = {}
player_known_ids = {}
loaded_npcs = {}

add_entity(NPC([101, 115], [0,0], "src\\Char\\Lianna.png"))
add_entity(NPC([102, 115], [0,0], "src\\Char\\Lianna.png"))
add_entity(NPC([103, 115], [0,0], "src\\Char\\Lianna.png"))
NPC.all_npcs[0].add_wander([103, 115], 8, 0)

# Threads
receive_thread = Thread(target=receive)
time_thread = Thread(target=timer)
layer_refreshment_thread = Thread(target=layer_refreshment)
npc_info_thread = Thread(target=npc_info)
npc_run_thread = Thread(target=NPC_run, args=(1/60,))
receive_thread.start()
time_thread.start()
layer_refreshment_thread.start()
npc_info_thread.start()
npc_run_thread.start()
receive_thread.join()