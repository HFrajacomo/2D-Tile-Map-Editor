from scipy.spatial import ConvexHull

# Does convex hull and
def CH(vertices):
	connections = ConvexHull(vertices).simplices
	found_indexes = []
	border = []

	for element in connections:
		if(element[0] not in found_indexes):
			found_indexes.append(element[0])
		if(element[1] not in found_indexes):
			found_indexes.append(element[1])

	for index in found_indexes:
		if(vertices[index] not in border):
			border.append(vertices[index])

	return border

def get_middle(vertices):
	x = 0
	y = 0

	for e in vertices:
		x += e[0]
		y += e[1]

	return [int(x/len(vertices)), int(y/len(vertices))]


class Area:
	def __init__(self, vertices):
		self.border = CH(vertices)
		self.middle_point = get_middle(self.border)
		self.entities = []

	# "in" operator overload
	def __contains__(self, entity):
		# Tries to find entrants with Convex Hull
		aux = self.border.copy()
		aux.append(entity.pos)
		if(CH(aux) != self.border):
			return False
		else:
			return True

	# Once entity enters area
	def enter(self, entity):
		pass

	# Sets specific configuration of area
	def set_area_config(self, args_dict):
		if("Shader_color" in args_dict.keys()):
			self.shader_color = args_dict["Shader_color"]


class ShaderArea(Area):
	def __init__(self, vertices, shader_color, shade_opacity):
		super().__init__(vertices)
		self.shader_color = shader_color
		self.shader_opacity = shade_opacity

	def enter(self, entity, shader):
		if(entity in self.entities):
			return
		self.entities.append(entity)
		shader.add_shade(self.shader_color, self.shader_opacity)

	def exit(self, entity, shader):
		self.entities.remove(entity)
		shader.sub_shade(self.shader_color, self.shader_opacity)
