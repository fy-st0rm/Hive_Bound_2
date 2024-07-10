from globals import *
from engine import *
from characters import *


class Game(Scene):
	def __init__(self, surface: pygame.Surface, scene_manager: SceneManager):
		self.surface = surface
		self.scene_manager = scene_manager

		self.camera = [0, 0]
		self.game_surface = pygame.Surface((SURFACE_WIDTH, SURFACE_HEIGHT))

		self.player = Player((100, 0))

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
		self.game_surface.fill((165, 165, 165))

		self.camera[0] += (self.player.rect.x - self.camera[0] - SURFACE_WIDTH / 2) / 10
		self.camera[1] += (self.player.rect.y - self.camera[1] - SURFACE_HEIGHT / 2) / 10

		r = pygame.Rect(0, 150, 300, 20)
		r2 = pygame.Rect(0, 100, 50, 10)
		r3 = pygame.Rect(200, 0, 20, 200)
		pygame.draw.rect(self.game_surface, (255, 0, 0), [r.x - self.camera[0], r.y - self.camera[1], r.w, r.h])
		pygame.draw.rect(self.game_surface, (255, 0, 0), [r2.x - self.camera[0], r2.y - self.camera[1], r2.w, r2.h])
		pygame.draw.rect(self.game_surface, (255, 0, 0), [r3.x - self.camera[0], r3.y - self.camera[1], r3.w, r3.h])

		self.player.update(self.game_surface, [r, r2, r3], dt, self.camera)

		self.surface.blit(
			pygame.transform.scale(
				self.game_surface,
				(self.surface.get_width(), self.surface.get_height())
			),
			(0, 0)
		)

