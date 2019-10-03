class NetMessage:
	def __init__(self, type, data=None):
		# If serialized
		if(data == None):
			self.type, self.data = type.split("@")	
		# If constructed	
		else:	
			self.type = type
			self.data = data


	def __str__(self):
		return self.type + "@" + self.data

	def __repr__(self):
		return "Type: " + self.type + "\n" + "Data: " + self.data + "\n"

	def __neg__(self):
		return str(self)