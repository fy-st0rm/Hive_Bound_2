from globals import *
from engine import *


class Player:
	def __init__(self, pos: tuple[int, int]):
		self.rect = pygame.Rect(pos[0], pos[1], 32, 32)

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
				self.coll_dir = {
					Dir.left: False,
					Dir.right: False,
					Dir.up: False,
					Dir.down: False
				}

	def update(
		self,
		surface: pygame.Surface,
		rects: list[pygame.Rect],
		dt: float,
		camera: list[int, int]
	):
		delta_pos = [0, 0]
		# Updating the delta position if the player is not stuck to wall
		if not (
			self.movement[Dir.stick] and (
				self.coll_dir[Dir.left] or self.coll_dir[Dir.right]
			)
		):
			if self.movement[Dir.left]:
				delta_pos[0] -= self.speed * dt
			if self.movement[Dir.right]:
				delta_pos[0] += self.speed * dt

			delta_pos[1] += self.vert_movement
		else:
			# Reset the airtime when stuck to wall
			self.airtime = 0

		# Decreasing vertical movement
		self.vert_movement += 0.3
		if self.vert_movement > 3:
			self.vert_movement = 3

		self.__check_collision(rects, delta_pos)

		# Decrease air time if player is in air
		if self.coll_dir[Dir.down]:
			self.airtime = 0
		else:
			self.airtime += 1

		pygame.draw.rect(
			surface,
			[255, 255, 0],
			[
				self.rect.x - camera[0],
				self.rect.y - camera[1],
				self.rect.w,
				self.rect.h
			]
		)

	def jump_to_checkpoint(self) -> bool:
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
			delta_pos: tuple[int, int]
		):
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

