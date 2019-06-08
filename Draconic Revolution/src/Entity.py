import pygame as pg

collision_mapping = {}

def get_surroundings(inter_map, disc_pos):
	surroundings = []

	for i in range(disc_pos[1]-1,disc_pos[1]+2):
		surroundings.append([])
		for j in range(disc_pos[0], disc_pos[0]+3):
			surroundings[-1].append(inter_map[i][j].solid)

	return surroundings

class Entity():
	def __init__(self):
		self.pos = None
		self.hitbox = None

	def collision(self, entity):
		if(self.hitbox.colliderect(entity.hitbox)):
			return True
		else:
			return False

	def collide_action(self, entity):
		pass

class Player(Entity):
	def __init__(self, position, hb_width, hb_height, speed):
		self.pos = position
		self.hitbox = pg.Rect((position[0]-hb_width/2, position[1]-hb_height/2), (hb_width, hb_height))
		self.speed = speed
		self.image = pg.Surface((64,64))
		self.image.fill((180,0,40))

	def draw(self, screen):
		screen.blit(self.image, (704, 448))
