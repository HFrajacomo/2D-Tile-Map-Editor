class NetMessage:
	def __init__(self, type, data):
		self.type = type
		self.data = data

	def __init__(self, serialized):
		self.type, self.data = serialized.split("@")

	def __str__(self):
		return self.type + "@" + self.data

	def __repr__(self):
		return "Type: " + self.type + "\n" + "Data: " + self.data + "\n"

	def __neg__(self):
		return str(self)