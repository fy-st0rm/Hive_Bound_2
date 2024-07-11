from globals import *
from engine import *
from characters import *


class Game(Scene):
	def __init__(self, surface: pygame.Surface, scene_manager: SceneManager):
		self.surface = surface
		self.scene_manager = scene_manager

		self.camera = [0, 0]
		self.game_surface = pygame.Surface((SURFACE_WIDTH, SURFACE_HEIGHT))

		self.checkpoint = (0, 100)
		self.player = Player((100, 0))
		self.player.checkpoint = self.checkpoint

		self.guard = Guard(Sprite.guard_sprite, (65, 227 - 32), 3, 30, 100)

		with open("./assets/map/map_1.json", "r") as f:
			self.map = json.load(f)
			rects = []
			for r in self.map["rects"]:
				rects.append(pygame.Rect(r[0], r[1], r[2], r[3]))
			self.map["rects"] = rects
		self.map_sprite = SpriteSheet(self.map["image"])

	def on_entry(self):
		print("Entered game")

	def on_exit(self):
		print("Game exited")

	def on_event(self, event: pygame.event.Event):
		self.player.event(event)
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				self.scene_manager.switch("menu")

	def on_update(self, dt: float):
		self.game_surface.fill((0, 0, 0))

		self.camera[0] += (self.player.rect.x - self.camera[0] - SURFACE_WIDTH / 2) / 10
		self.camera[1] += (self.player.rect.y - self.camera[1] - SURFACE_HEIGHT / 1.5) / 10

		self.game_surface.blit(
			self.map_sprite.image_at(0, 0, 250, 250),
			(-self.camera[0], -self.camera[1])
		)

		# r = pygame.Rect(0, 150, 300, 20)
		# r2 = pygame.Rect(0, 68, 100, 10)
		# r3 = pygame.Rect(200, 0, 20, 200)
		# pygame.draw.rect(self.game_surface, (255, 0, 0), [r.x - self.camera[0], r.y - self.camera[1], r.w, r.h])
		# pygame.draw.rect(self.game_surface, (255, 0, 0), [r2.x - self.camera[0], r2.y - self.camera[1], r2.w, r2.h])
		# pygame.draw.rect(self.game_surface, (255, 0, 0), [r3.x - self.camera[0], r3.y - self.camera[1], r3.w, r3.h])

		# for r in self.map["rects"]:
		# 	pygame.draw.rect(self.game_surface, (255, 0, 0), [r.x - self.camera[0], r.y - self.camera[1], r.w, r.h])

		self.guard.update(self.game_surface, dt, self.camera)
		self.player.update(self.game_surface, self.map["rects"], dt, self.camera)

		self.surface.blit(
			pygame.transform.scale(
				self.game_surface,
				(self.surface.get_width(), self.surface.get_height())
			),
			(0, 0)
		)

