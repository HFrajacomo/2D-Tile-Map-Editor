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
	print(connected_entity_ids)

	i = -1
	while(i in connected_entity_ids):
		i -= 1

	connected_entity_ids.append(i)
	entities_dict[i] = e	
	entity_layer[e.pos[0]][e.pos[1]].append(i)
	entities_dict[i].id = i

# Converts string to byte string
def byt(text):
	return bytes(text, "UTF-8")

# Sends a message to all connected
def broadcast(m):
	global s
	global connections

	for conn in connections:
		s.send_multipart([conn, byt(-m)])

# Sends layer information to connected users Thread
def layer_refreshment():
	global entity_layer
	global s
	global connections
	global player_known_ids
	global LOCK

	while(not QUIT):
		t = datetime.now()
		
		for conn in connections:
			found_ids = []
			id = connection_player_dict[conn]
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
			print(found_ids)
			n = NetMessage("ENTITIES", str(found_ids)[1:-1])
			s.send_multipart([conn, byt(-n)])

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

	while(not QUIT):
		t = datetime.now()
		broadcast(NetMessage("TIME", str(global_timer)))
		
		global_timer.inc()

		# FPS calibrator
		dt = (t - datetime.now()).total_seconds()
		if(dt > 1):
			print("Timer is overloaded!")
		else:
			sleep(1 - dt)		

# Global Receive
def receive():
	global s
	global connections
	global players_dict
	global connection_player_dict
	global entity_layer

	while(not QUIT):
		try:
			address, data = s.recv_multipart(zmq.NOBLOCK)
		except zmq.Again:
			continue

		print("Recebi mensagem: " + data.decode())

		data = data.decode()
		m = NetMessage(data)

		# Assigning ID and connection to entrant users
		if(m.type == "IDENTITY"):
			if(connections == []):
				new_ident = byt("0")
				s.send_multipart([address, new_ident])
				connections.append(new_ident)
			else:
				new_ident = byt(str(int(connections[-1])+1))
				s.send_multipart([address, new_ident])
				connections.append(new_ident)

			disc_pos, offset, filename = m.data.split(";")
			disc_pos = [int(x) for x in disc_pos.split(",")]
			offset = [int(x) for x in offset.split(",")]
			id = add_player(Player(disc_pos, offset, filename, server=True))
			s.send_multipart([new_ident, byt(-NetMessage("PLAYER_ID", str(id)))])
			connection_player_dict[new_ident] = id
			entity_layer[disc_pos[0]][disc_pos[1]].append(id)

		# Update users position data (Every step)
		elif(m.type == "POSITION"):
			players_dict[connection_player_dict[address]].pos = [int(x) for x in m.data.split(";")[0].split(",")]
			players_dict[connection_player_dict[address]].offset = [int(x) for x in m.data.split(";")[1].split(",")]
			players_dict[connection_player_dict[address]].direction = int(m.data.split(";")[2])
			if(m.data.split(";")[3] == "True"):
				players_dict[connection_player_dict[address]].IS_MOVING = True
			else:
				players_dict[connection_player_dict[address]].IS_MOVING = False

			disc_pos = players_dict[connection_player_dict[address]].pos
			id = int(connection_player_dict[address])
			if(id not in entity_layer[disc_pos[0]][disc_pos[1]]):
				entity_layer[disc_pos[0]][disc_pos[1]].append(id)

		# Change users position in entity layer (Every block change)
		elif(m.type == "CHANGE_POS"):
			id = int(connection_player_dict[address])
			disc_pos = [int(x) for x in m.data.split(",")]
			
			if(id in entity_layer[disc_pos[0]][disc_pos[1]]):
				entity_layer[disc_pos[0]][disc_pos[1]] = list_remove(entity_layer[disc_pos[0]][disc_pos[1]], id)

		# Sends requested id information
		elif(m.type == "REQ_ENTITY"):
			id = int(m.data)
			if(id > 0):
				s.send_multipart([address, byt(-NetMessage("ENTITY_INFO", str(id) + "#" + str(players_dict[id])))])
			else:
				s.send_multipart([address, byt(-NetMessage("ENTITY_INFO", str(id) + "#" + str(entities_dict[id])))])

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
			if(npc.IS_LOADED):
				npc.run(FPS, inter_map, inter_map_obj, s, entity_layer)
			else:
				break

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
s = context.socket(zmq.ROUTER)
HOST = "127.0.0.1"
PORT = 33000
con_string = "tcp://" + HOST + ":" + str(PORT)
s.bind(con_string)

global_timer = Time(12,0)

connections = []

# Entities tracking
players_dict = {}
entities_dict = {}
connected_player_ids = []
connected_entity_ids = []
connection_player_dict = {}
player_known_ids = {}

add_entity(NPC([101, 115], [0,0], "src\\Char\\Lianna.png"))
add_entity(NPC([102, 115], [0,0], "src\\Char\\Lianna.png"))
add_entity(NPC([103, 115], [0,0], "src\\Char\\Lianna.png"))

receive_thread = Thread(target=receive)
time_thread = Thread(target=timer)
layer_refreshment_thread = Thread(target=layer_refreshment)
time_thread.start()
receive_thread.start()
layer_refreshment_thread.start()
receive_thread.join()