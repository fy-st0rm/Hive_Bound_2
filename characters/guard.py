from engine import *
from globals import *


def collideLineLine(l1_p1, l1_p2, l2_p1, l2_p2):
	# normalized direction of the lines and start of the lines
	P  = pygame.math.Vector2(*l1_p1)
	line1_vec = pygame.math.Vector2(*l1_p2) - P
	R = line1_vec.normalize()
	Q  = pygame.math.Vector2(*l2_p1)
	line2_vec = pygame.math.Vector2(*l2_p2) - Q
	S = line2_vec.normalize()

	# normal vectors to the lines
	RNV = pygame.math.Vector2(R[1], -R[0])
	SNV = pygame.math.Vector2(S[1], -S[0])
	RdotSVN = R.dot(SNV)
	if RdotSVN == 0:
			return False

	# distance to the intersection point
	QP	= Q - P
	t = QP.dot(SNV) / RdotSVN
	u = QP.dot(RNV) / RdotSVN

	return t > 0 and u > 0 and t*t < line1_vec.magnitude_squared() and u*u < line2_vec.magnitude_squared()

def colideRectLine(rect, p1, p2):
	return (collideLineLine(p1, p2, rect.topleft, rect.bottomleft) or
				collideLineLine(p1, p2, rect.bottomleft, rect.bottomright) or
				collideLineLine(p1, p2, rect.bottomright, rect.topright) or
				collideLineLine(p1, p2, rect.topright, rect.topleft))

def collideRectPolygon(rect, polygon):
	for i in range(len(polygon)-1):
		if colideRectLine(rect, polygon[i], polygon[i+1]):
			return True
	return False


class Guard:
	def __init__(self, sprite: SpriteSheet, pos: tuple[int, int], delay: int, walk_factor: int, fov: int, radius: int):
		self.sprite = sprite
		self.delay = delay
		self.fov = fov
		self.walk_factor = 1 / walk_factor
		self.radius = radius
		self.rect = pygame.Rect(pos[0], pos[1], 32, 32)

		# Animations
		self.dir: Dir = Dir.right
		self.state: State = State.walk
		self.animator = Animator()
		self.__init_animation()

		# Guard timings
		self.start = False
		self.start_time = time.time()

		# Cone
		self.head = []
		self.half_ang = 0

	def update(
		self,
		surface: pygame.Surface,
		light_surface: pygame.Surface,
		dt: float,
		camera: tuple[int, int]
	):
		# Calculating fov cone
		if self.dir == Dir.right:
			self.head = [self.rect.x + self.rect.w / 2, self.rect.y]
			self.half_ang = (self.fov / 2) * (math.pi / 180)

		else:
			self.head = [self.rect.x + self.rect.w / 2, self.rect.y]
			self.half_ang = math.pi - ((self.fov / 2) * (math.pi / 180))

		x  = self.head[0] + self.radius * math.cos(self.half_ang)
		y1 = self.head[1] + self.radius * math.sin(self.half_ang)
		y2 = self.head[1] - self.radius * math.sin(self.half_ang)

		pygame.draw.polygon(
			light_surface,
			(255, 255, 255, 20),
			(
				(self.head[0] - camera[0], self.head[1] - camera[1]),
				(x - camera[0], y1 - camera[1]),
				(x - camera[0], y2 - camera[1])
			)
		)

		self.__cal_delay()
		self.__cal_walk()

		self.animator.switch(self.dir, self.state)
		surface.blit(self.animator.get(), (self.rect.x - camera[0], self.rect.y - camera[1]))

	def detect_target(
		self,
		target_rect: pygame.Rect,
		camera
	) -> bool:
		x  = self.head[0] + self.radius * math.cos(self.half_ang)
		y1 = self.head[1] + self.radius * math.sin(self.half_ang)
		y2 = self.head[1] - self.radius * math.sin(self.half_ang)

		polygon = [
			(self.head[0] - camera[0], self.head[1] - camera[1]),
			(x - camera[0], y1 - camera[1]),
			(x - camera[0], y2 - camera[1])
		]
        

		return collideRectPolygon(target_rect, polygon)

		"""
		if self.dir == Dir.right:
			ang = math.atan2(
				target[1] - (self.head[1] - camera[1]),
				target[0] - (self.head[0] - camera[0])
			) * 180 / math.pi
		else:
			ang = math.atan2(
				(self.head[1] - camera[1]) - target[1],
				(self.head[0] - camera[0]) - target[0]
			) * 180 / math.pi

		dist = math.sqrt(math.pow(self.head[1] - target[1], 2) + math.pow(self.head[0] - target[0], 2))
		if (dist <= self.radius and -self.fov <= ang <= self.fov):
			print(dist, ang)
			return True
		return False
	"""

	def __cal_delay(self):
		if not self.start:
			self.start = True
			self.start_time = time.time()

		if time.time() - self.start_time > self.delay:
			if self.dir == Dir.right:
				self.dir = Dir.left
			else:
				self.dir = Dir.right
			self.start_time = time.time()

	def __cal_walk(self):
		if time.time() - self.start_time >= self.delay * self.walk_factor:
			self.state = State.idle
			return

		self.state = State.walk

		if self.dir == Dir.right:
			self.rect.x += 1
		else:
			self.rect.x -= 1

	def __init_animation(self):
		# Walk animation
		self.animator.add(Dir.right, State.walk, self.sprite.load_strip([0, 0, 32, 32], 3), 1)
		self.animator.add(Dir.left, State.walk, [
			pygame.transform.flip(i, True, False) for i in self.sprite.load_strip([0, 0, 32, 32], 3)
		], 1)

		# Idle animation
		self.animator.add(Dir.right, State.idle, self.sprite.load_strip([0, 1, 32, 32], 2), 0.3)
		self.animator.add(Dir.left, State.idle, [
			pygame.transform.flip(i, True, False) for i in self.sprite.load_strip([0, 1, 32, 32], 2)
		], 0.3)


