from globals import *
from engine import *

class Player:
	def __init__(self, sprite: SpriteSheet, pos: tuple[int, int]):
		self.sprite = sprite
		self.rect = pygame.Rect(pos[0], pos[1], 18, 25)

		self.speed = 3
		self.vert_movement = 0
		self.airtime = 0
		self.movement = {
			Dir.left: False,
			Dir.right: False,
			Dir.jump: False,
			Dir.stick: False
		}
		self.coll_dir = {
			Dir.left: False,
			Dir.right: False,
			Dir.up: False,
			Dir.down: False
		}

		self.checkpoint: tuple[int, int] = None

		# Animation
		self.state: State = State.idle
		self.dir: Dir = Dir.right
		self.animator = Animator()

		self.__init_animation()

	def event(self, event: pygame.event.Event):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_a:
				self.movement[Dir.left] = True
			elif event.key == pygame.K_d:
				self.movement[Dir.right] = True
			elif event.key == pygame.K_SPACE:
				self.movement[Dir.jump] = True
				if self.airtime < 3:
					self.vert_movement = -5
					pygame.mixer.Channel(0).play(pygame.mixer.Sound("assets/sounds/f_jump.wav"),maxtime=600)
			elif event.key == pygame.K_LSHIFT:
				self.movement[Dir.stick] = True

		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_a:
				self.movement[Dir.left] = False
			elif event.key == pygame.K_d:
				self.movement[Dir.right] = False
			elif event.key == pygame.K_SPACE:
				self.movement[Dir.jump] = False
			elif event.key == pygame.K_LSHIFT:
				self.movement[Dir.stick] = False

		elif event.type == pygame.MOUSEBUTTONDOWN:
			if pygame.mouse.get_pressed()[0]:
				self.movement[Dir.stick] = True

		elif event.type == pygame.MOUSEBUTTONUP:
			if not pygame.mouse.get_pressed()[0]:
				self.movement[Dir.stick] = False

	def update(
		self,
		surface: pygame.Surface,
		rects: list[pygame.Rect],
		dt: float,
		camera: list[int, int]
	):
		delta_pos = [0, 0]

		if delta_pos[0] == 0:
			self.state = State.idle;

		if self.vert_movement < 0:
			self.state = State.ascent

		# Updating the delta position if the player is not stuck to wall
		if not (
			self.movement[Dir.stick] and (
				self.coll_dir[Dir.left] or self.coll_dir[Dir.right]
			)
		):
			if self.movement[Dir.left]:
				delta_pos[0] -= self.speed
				self.dir = Dir.left
				self.state = State.walk
			if self.movement[Dir.right]:
				delta_pos[0] += self.speed
				self.dir = Dir.right
				self.state = State.walk

			delta_pos[1] += self.vert_movement
		else:
			# Reset the airtime when stuck to wall
			self.airtime = 0
			self.state = State.stick

		# Decreasing vertical movement
		self.vert_movement += 0.3
		if self.vert_movement > 3:
			self.vert_movement = 3

		self.__check_collision(rects, delta_pos, dt)

		# Decrease air time if player is in air
		if self.coll_dir[Dir.down]:
			self.airtime = 0
		else:
			self.airtime += 1

		self.animator.switch(self.dir, self.state)
		surface.blit(
			self.animator.get(),
			(self.rect.x - camera[0], self.rect.y - camera[1])
		)

	def jump_to_checkpoint(self) -> bool:

		pygame.mixer.Channel(2).play(pygame.mixer.Sound("assets/sounds/f_teleport.wav"),maxtime=600)
		if not self.checkpoint:
			print("No checkpoint")
			return False

		self.rect.x = self.checkpoint[0]
		self.rect.y = self.checkpoint[1]
		return True

	def __check_for_hit(self, rects: list[pygame.Rect]) -> list[pygame.Rect]:
		hits = []

		for i in rects:
			if self.rect.colliderect(i):
				hits.append(i)
		return hits

	def __check_collision(
			self,
			rects: list[pygame.Rect],
			delta_pos: tuple[int, int],
			dt: float
		):

		if not self.movement[Dir.stick]:
			self.coll_dir[Dir.left] = False
			self.coll_dir[Dir.right] = False

		self.coll_dir[Dir.up] = False
		self.coll_dir[Dir.down] = False

		self.rect.x += delta_pos[0]
		hits = self.__check_for_hit(rects)
		for hit in hits:
			if delta_pos[0] > 0:
				self.rect.right = hit.left
				self.coll_dir[Dir.right] = True
			if delta_pos[0] < 0:
				self.rect.left = hit.right
				self.coll_dir[Dir.left] = True

		self.rect.y += delta_pos[1]
		hits = self.__check_for_hit(rects)
		for hit in hits:
			if delta_pos[1] > 0:
				self.rect.bottom = hit.top
				self.coll_dir[Dir.down] = True
			if delta_pos[1] < 0:
				self.rect.top = hit.bottom
				self.coll_dir[Dir.up] = True

	def __init_animation(self):
		# Idle animation
		self.animator.add(Dir.right, State.idle, self.sprite.load_strip([0, 0, 18, 25], 1), 1)
		self.animator.add(Dir.left, State.idle, [
			pygame.transform.flip(i, True, False) for i in self.sprite.load_strip([0, 0, 18, 25], 1)
		], 1)

		# Walk animation
		self.animator.add(Dir.right, State.walk, self.sprite.load_strip([2, 0, 18, 25], 2), 1)
		self.animator.add(Dir.left, State.walk, [
			pygame.transform.flip(i, True, False) for i in self.sprite.load_strip([2, 0, 18, 25], 2)
		], 1)

		# Jump ascent animation
		self.animator.add(Dir.right, State.ascent, self.sprite.load_strip([1, 0, 18, 25], 1), 1)
		self.animator.add(Dir.left, State.ascent, [
			pygame.transform.flip(i, True, False) for i in self.sprite.load_strip([1, 0, 18, 25], 1)
		], 1)

		# Stick animation
		self.animator.add(Dir.right, State.stick, self.sprite.load_strip([4, 0, 18, 25], 1), 1)
		self.animator.add(Dir.left, State.stick, [
			pygame.transform.flip(i, True, False) for i in self.sprite.load_strip([4, 0, 18, 25], 1)
		], 1)


