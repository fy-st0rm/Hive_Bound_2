from globals import *
from engine import *


class Guard:
	def __init__(self, img: pygame.Surface, pos: tuple[int, int], delay: int, fov: int, radius: int):
		self.img = img
		self.delay = delay
		self.fov = fov
		self.radius = radius

		self.dir = "right"
		self.rect = pygame.Rect(pos[0], pos[1], img.get_width(), img.get_height())
		self.start = False
		self.start_time = time.time()
		self.color = [255, 255, 0]

	def update(self, surface: pygame.Surface, dt: float):
		self.__cal_delay()
		self.__cal_walk()

		surface.blit(self.img, (self.rect.x, self.rect.y))

		mp = list(pygame.mouse.get_pos())
		mp[0] = mp[0] / WIN_WIDTH * 266
		mp[1] = mp[1] / WIN_HEIGHT * 200

		if self.dir == "right":
			head = [self.rect.x + self.rect.w / 2, self.rect.y]
			half_ang = (self.fov / 2) * (math.pi / 180)
			ang = math.atan2(mp[1] - head[1], mp[0] - head[0]) * 180 / math.pi
		else:
			head = [self.rect.x + self.rect.w / 2, self.rect.y]
			half_ang = math.pi - ((self.fov / 2) * (math.pi / 180))
			ang = math.atan2(head[1] - mp[1], head[0] - mp[0]) * 180 / math.pi

		x  = head[0] + self.radius * math.cos(half_ang)
		y1 = head[1] + self.radius * math.sin(half_ang)
		y2 = head[1] - self.radius * math.sin(half_ang)

		pygame.draw.line(surface, self.color, [head[0], head[1]], [x, y1])
		pygame.draw.line(surface, self.color, [head[0], head[1]], [x, y2])

		dist = math.sqrt(math.pow(head[1] - mp[1], 2) + math.pow(head[0] - mp[0], 2))
		if dist <= self.radius and -45 <= ang <= 45:
			self.color = [255, 0, 0]
		else:
			self.color = [255, 255, 0]

	def __cal_delay(self):
		if not self.start:
			self.start = True
			self.start_time = time.time()

		if time.time() - self.start_time > self.delay:
			if self.dir == "right":
				self.dir = "left"
				self.img = pygame.transform.flip(self.img, True, False)
			else:
				self.dir = "right"
				self.img = pygame.transform.flip(self.img, True, False)
			self.start_time = time.time()

	def __cal_walk(self):
		if time.time() - self.start_time >= self.delay / 3:
			return

		if self.dir == "right":
			self.rect.x += 1
		else:
			self.rect.x -= 1


class Game(Scene):
	def __init__(self, surface: pygame.Surface, scene_manager: SceneManager):
		self.surface = surface
		self.scene_manager = scene_manager

		self.game_surface = pygame.Surface((266, 200))

		guard_img = pygame.image.load("assets/Guard.png")
		self.guard1 = Guard(guard_img, (266 / 2, 200 / 2), 5, 90, 300)

	def on_entry(self):
		print("Entered game")

	def on_exit(self):
		print("Game exited")

	def on_event(self, event: pygame.event.Event):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				self.scene_manager.switch("menu")

	def on_update(self, dt: float):
		self.game_surface.fill((165, 165, 165))
		self.guard1.update(self.game_surface, dt)

		self.surface.blit(
			pygame.transform.scale(
				self.game_surface,
				(self.surface.get_width(), self.surface.get_height())
			),
			(0, 0)
		)

