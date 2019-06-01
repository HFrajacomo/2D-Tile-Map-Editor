from Map import Map

def loadmap(filename):
	map_name = ""
	map_data = []
	obj_data = []
	light_data = []
	count_of_es = 0

	if(filename != None):
		file = open(filename + ".map", "r")
		lines = file.readlines()
		file.close()
		for i in range(len(lines)):
			if(i == 0):
				map_name = lines[i][1:].split("\t")[0]
				map_cord = (int(lines[i][1:].split("\t")[1].split(",")[0].replace("(", "")), int(lines[i][1:].split("\t")[1].split(",")[1].replace(")", "")))
			else:
				if(lines[i] == "&\n"):
					count_of_es += 1
				elif(count_of_es == 0): # Gathering map data
					map_data.append([int(x) for x in lines[i].split(",")])
				elif(count_of_es == 1):
					obj_data.append([int(x) for x in lines[i].split(",")])
				elif(count_of_es == 2):
					light_data.append([int(x) for x in lines[i].split(",")])

		return Map(map_data, obj_data, light_data, mapname=map_name)
	return None, None