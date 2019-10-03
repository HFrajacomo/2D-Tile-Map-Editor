import zmq
from Time import *
from time import sleep
from threading import Thread
from NetMessage import *

def byt(text):
	return bytes(text, "UTF-8")

# Sends a message to all connected
def broadcast(m):
	global s
	global connections

	for conn in connections:
		s.send_multipart([conn, byt(-m)])

# Time processing thread
def timer():
	global global_timer

	while(not QUIT):
		broadcast(NetMessage("TIME", str(global_timer)))
		global_timer.inc()
		sleep(1)

# Global Receive
def receive():
	global s
	global connections

	while(not QUIT):
		try:
			address, data = s.recv_multipart(zmq.NOBLOCK)
		except zmq.Again:
			continue

		data = data.decode()
		m = NetMessage(data)

		if(m.type == "IDENTITY"):
			if(connections == []):
				s.send_multipart([address, byt("0")])
				connections.append(byt("0"))
			else:
				new_ident = byt(str(int(connections[-1])+1))
				s.send_multipart([address, new_ident])
				connections.append(new_ident)
		#else:
		#	n = NetMessage("UKNW", "unidentified type")
		#	s.send_multipart([byt("0001"), byt(-n)])

QUIT = False

context = zmq.Context()
s = context.socket(zmq.ROUTER)
HOST = "127.0.0.1"
PORT = 33000
con_string = "tcp://" + HOST + ":" + str(PORT)
s.bind(con_string)

global_timer = Time(12,0)

connections = []

receive_thread = Thread(target=receive)
time_thread = Thread(target=timer)
time_thread.start()
receive_thread.start()
receive_thread.join()