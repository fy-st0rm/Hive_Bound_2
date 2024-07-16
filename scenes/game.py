from globals import *
from engine import *
from characters import *


FREE_CAMERA = False


class Game(Scene):
	def __init__(self, surface: pygame.Surface, scene_manager: SceneManager):
		self.surface = surface
		self.scene_manager = scene_manager

		self.camera = [0, 0]

		self.game_surface = pygame.Surface(
			(SURFACE_WIDTH, SURFACE_HEIGHT),
			pygame.SRCALPHA
		)
		self.game_surface.set_alpha(100)

		self.light_surface = pygame.Surface(
			(SURFACE_WIDTH, SURFACE_HEIGHT),
			pygame.SRCALPHA
		)
		self.light_surface.set_colorkey((0,0,0))

		self.checkpoint = (100, 1800 - 64)
		self.player = Player(Sprite.player_sprite, (100, 1800 - 32))
		self.player.checkpoint = self.checkpoint

		self.left = self.right = self.up = self.down = False

		# Loading map
		with open("./assets/map/map.json", "r") as f:
			self.map = json.load(f)
			rects = []
			for r in self.map["rects"]:
				rects.append(pygame.Rect(r[0], r[1], r[2], r[3]))
			self.map["rects"] = rects

		self.map_sprite = SpriteSheet(self.map["image"])
		self.map_img = self.map_sprite.image_at(0, 0, 300, 1800)

		# Loading up guards
		guard_pos = self.map["guard_pos"]
		self.guards = []
		for i in guard_pos:
			pos = guard_pos[i]["pos"]
			delay = guard_pos[i]["delay"]
			f = guard_pos[i]["f"]
			self.guards.append(
				Guard(Sprite.guard_sprite, (pos[0], pos[1] - 32), delay, f, 30, 200)
			)

		self.guard = Guard(
			Sprite.guard_sprite,
			(0, 1500 - 128), 5, 2, 30, 200)

	def on_entry(self):
		pass

	def on_exit(self):
		pass

	def on_event(self, event: pygame.event.Event):
		self.player.event(event)
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				self.scene_manager.switch("menu")
			if event.key == pygame.K_w:
				self.up = True
			if event.key == pygame.K_a:
				self.left = True
			if event.key == pygame.K_s:
				self.down = True
			if event.key == pygame.K_d:
				self.right = True

		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_w:
				self.up = False
			if event.key == pygame.K_a:
				self.left = False
			if event.key == pygame.K_s:
				self.down = False
			if event.key == pygame.K_d:
				self.right = False

	def on_update(self, dt: float):
		self.game_surface.fill((0, 0, 0))
		self.light_surface.fill((0, 0, 0))

		if FREE_CAMERA:
			if self.left:
				self.camera[0] -= 5
			if self.right:
				self.camera[0] += 5
			if self.up:
				self.camera[1] -= 5
			if self.down:
				self.camera[1] += 5
		else:
			self.camera[0] += (self.player.rect.x - self.camera[0] - SURFACE_WIDTH / 2) / 10
			self.camera[1] += (self.player.rect.y - self.camera[1] - SURFACE_HEIGHT / 1.5) / 10

		self.game_surface.blit(
			self.map_img,
			(-self.camera[0], -self.camera[1])
		)

		for guard in self.guards:
			guard.update(self.game_surface, self.light_surface, dt, self.camera)
			if guard.detect_target(
				pygame.Rect(
					self.player.rect.x - self.camera[0],
					self.player.rect.y - self.camera[1],
					self.player.rect.w, self.player.rect.h
				), self.camera
			):
				self.player.jump_to_checkpoint()

		self.player.update(self.game_surface, self.map["rects"], dt, self.camera)

		# Drawing white screen when reached at home
		if self.player.rect.y <= 250:
			pygame.draw.rect(
				self.light_surface,
				[255, 255, 255, 255 - self.player.rect.y],
				(0, 0, self.light_surface.get_width(), self.light_surface.get_height())
			)

		# Ending
		if self.player.rect.y < 50:
			self.scene_manager.switch("end")

		self.surface.blit(
			pygame.transform.scale(
				self.game_surface,
				(self.surface.get_width(), self.surface.get_height())
			),
			(0, 0)
		)
		self.surface.blit(
			pygame.transform.scale(
				self.light_surface,
				(self.surface.get_width(), self.surface.get_height())
			),
			(0, 0)
		)

