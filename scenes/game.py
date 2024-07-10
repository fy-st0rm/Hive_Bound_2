from globals import *
from engine import *

class State:
	walk = "walk"
	idle = "idle"

class Dir:
	left = "left"
	right = "right"


class Guard:
	def __init__(self, sprite: SpriteSheet, pos: tuple[int, int], delay: int, fov: int, radius: int):
		self.sprite = sprite
		self.delay = delay
		self.fov = fov
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

	def update(self, surface: pygame.Surface, dt: float):
		self.__cal_delay()
		self.__cal_walk()

		self.animator.switch(self.dir, self.state)
		surface.blit(self.animator.get(), (self.rect.x, self.rect.y))

	def detect_target(self, target: tuple[int, int]) -> bool:
		if self.dir == Dir.right:
			head = [self.rect.x + self.rect.w / 2, self.rect.y]
			half_ang = (self.fov / 2) * (math.pi / 180)
			ang = math.atan2(target[1] - head[1], target[0] - head[0]) * 180 / math.pi
		else:
			head = [self.rect.x + self.rect.w / 2, self.rect.y]
			half_ang = math.pi - ((self.fov / 2) * (math.pi / 180))
			ang = math.atan2(head[1] - target[1], head[0] - target[0]) * 180 / math.pi

		x  = head[0] + self.radius * math.cos(half_ang)
		y1 = head[1] + self.radius * math.sin(half_ang)
		y2 = head[1] - self.radius * math.sin(half_ang)

		dist = math.sqrt(math.pow(head[1] - target[1], 2) + math.pow(head[0] - target[0], 2))
		return (dist <= self.radius and -45 <= ang <= 45)

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
		if time.time() - self.start_time >= self.delay / 3:
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


class Game(Scene):
	def __init__(self, surface: pygame.Surface, scene_manager: SceneManager):
		self.surface = surface
		self.scene_manager = scene_manager

		self.game_surface = pygame.Surface((266, 200))

		sprite = SpriteSheet("assets/Guard-sheet.png")
		self.guard1 = Guard(sprite, (266 / 3, 50), 5, 45, 300)
		self.guard2 = Guard(sprite, (266 / 3, 100), 3, 45, 300)

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
		self.guard2.update(self.game_surface, dt)

		self.surface.blit(
			pygame.transform.scale(
				self.game_surface,
				(self.surface.get_width(), self.surface.get_height())
			),
			(0, 0)
		)

