class path_data:
	def __init__(self, path, weight):
		self.path = path
		self.weight = weight

	def __repr__(self):
		return self.path

	def get_priority(self):
		return self.weight

	def __hash__(self):
		return hash(self.path)

def neighbors(pos):
	a = []
	x = pos[0]+1
	y = pos[0]-1

	a.append((x, pos[1]))
	a.append((y, pos[1]))

	x = pos[1]+1
	y = pos[1]-1	
	a.append((pos[0], x))
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
			transformed.append("L")
		elif(s == [-1,0]):
			transformed.append("R")
		elif(s == [0,1]):
			transformed.append("U")
		elif(s == [0,-1]):
			transformed.append("D")

		current_pos = t

	return transformed

def a_star_search(m, start, goal):
	frontier = []
	start = tuple(start)
	goal = tuple(goal)
	frontier.append(path_data(start, 0))
	came_from = {}
	cost_so_far = {}
	came_from[start] = None
	cost_so_far[start] = 0
	
	while(frontier):
		current = frontier.pop(0).path

		if(current == goal):
			break
		
		for n in neighbors(current):

			try:
				new_cost = cost_so_far[current] + m.grid[n[0]][n[1]]
			except IndexError:
				continue

			if n not in cost_so_far or new_cost < cost_so_far[n]:
				cost_so_far[n] = new_cost
				priority = new_cost + (heuristic(goal, n)*1.1)
				frontier.append(path_data(n, priority))
				frontier.sort(key=path_data.get_priority)
				came_from[n] = current

	# Gets the path
	way = goal
	pathway = []

	while(way != None):
		pathway.insert(0, way)
		try:
			way = came_from[way]
		except KeyError:
			return start
	
	return path_transform(pathway)