class path_data:
	def __init__(self, path, weight):
		self.path = path
		self.weight = weight

	def __repr__(self):
		return str(self.path) + " => " + str(self.weight) + "\n"

	def get_priority(self):
		return self.weight

	def __hash__(self):
		return hash(self.path)

	def __eq__(self, other):
		return self.path == other

def neighbors(pos, m, m_obj):
	a = []

	x = pos[0]+1
	y = pos[0]-1

	if(x >= len(m[0])-1 or y < 0):
		return []

	if(not (m[x][pos[1]].solid or m_obj[x][pos[1]].solid)):	
		a.append((x, pos[1]))

	if(not (m[y][pos[1]].solid or m_obj[y][pos[1]].solid)):	
		a.append((y, pos[1]))

	x = pos[1]+1
	y = pos[1]-1	

	if(x >= len(m)-1 or y < 0):
		return []	

	if(not (m[pos[0]][x].solid or m_obj[pos[0]][x].solid)):	
		a.append((pos[0], x))
	if(not (m[pos[0]][y].solid or m_obj[pos[0]][y].solid)):	
		a.append((pos[0], y))	

	return a

def get_weight(element):
	return element[1]

def heuristic(a, b):
	return abs(a[0] - b[0]) + abs(a[1] - b[1])

def easy_sub(list1, list2):
	return [list1[0]-list2[0], list1[1] - list2[1]]

def path_transform(list_pos):
	transformed = ["C"]
	current_pos = list_pos.pop(0)


	for t in list_pos:
		s = easy_sub(current_pos, t)

		if(s == [1,0]):
			transformed.append("U")
		elif(s == [-1,0]):
			transformed.append("D")
		elif(s == [0,1]):
			transformed.append("L")
		elif(s == [0,-1]):
			transformed.append("R")

		current_pos = t

	return transformed

def AStarSearch(inter, inter_obj, start, end):
 
	start = tuple([start[1], start[0]])
	end = tuple([end[1], end[0]])

	G = {} #Actual movement cost to each position from the start position
	F = {} #Estimated movement cost of start to end going via this position
 
	#Initialize starting values
	G[start] = 0 
	F[start] = heuristic(start, end)
 
	closedVertices = set()
	openVertices = set([start])
	cameFrom = {}
 
	while len(openVertices) > 0:
		#Get the vertex in the open list with the lowest F score
		current = None
		currentFscore = None
		for pos in openVertices:
			if current is None or F[pos] < currentFscore:
				currentFscore = F[pos]
				current = pos
 
		#Check if we have reached the goal
		if current == end:
			#Retrace our route backward
			path = [current]
			while current in cameFrom:
				current = cameFrom[current]
				path.append(current)
			path.reverse()
			return path_transform(path) #Done!
 
		#Mark the current vertex as closed
		openVertices.remove(current)
		closedVertices.add(current)
 
		#Update scores for vertices near the current position
		for neighbour in neighbors((current[0], current[1]), inter, inter_obj):
			if neighbour in closedVertices: 
				continue #We have already processed this node exhaustively
			candidateG = G[current] + inter[current[0]][current[1]].work
 
			if neighbour not in openVertices:
				openVertices.add(neighbour) #Discovered a new vertex
			elif candidateG >= G[neighbour]:
				continue #This G score is worse than previously found
 
			#Adopt this G score
			cameFrom[neighbour] = current
			G[neighbour] = candidateG
			H = heuristic(neighbour, end)
			F[neighbour] = G[neighbour] + H
 
	return path_transform(start)

