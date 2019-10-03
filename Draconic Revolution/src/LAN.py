import zmq
from Time import *
from time import sleep
from threading import Thread
from NetMessage import *

def byt(text):
	return bytes(text, "UTF-8")

def receive():
	global s
	global connections

	while(True):
		try:
			address, data = s.recv_multipart(zmq.NOBLOCK)
		except zmq.Again:
			continue

		data = data.decode()
		if(data == "IDENTITY"):
			if(connections == []):
				s.send_multipart([address, byt("0001")])
				connections.append(byt("0"))
			else:
				new_ident = byt(str(int(connections[-1])+1))
				s.send_multipart([address, new_ident])
				connections.append(new_ident)
		else:
			s.send_multipart([byt("0001"), byt("hahah")])

context = zmq.Context()
s = context.socket(zmq.ROUTER)
HOST = "127.0.0.1"
PORT = 33000
con_string = "tcp://" + HOST + ":" + str(PORT)
s.bind(con_string)

connections = []

receive_thread = Thread(target=receive)
receive_thread.start()
receive_thread.join()