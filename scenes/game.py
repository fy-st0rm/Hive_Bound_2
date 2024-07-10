from globals import *
from engine import *
from characters import *


class Game(Scene):
	def __init__(self, surface: pygame.Surface, scene_manager: SceneManager):
		self.surface = surface
		self.scene_manager = scene_manager

		self.game_surface = pygame.Surface((266, 200))

		sprite = SpriteSheet("assets/Guard-sheet.png")
		self.guard1 = Guard(sprite, (266 / 3, 50), 5, 45, 300)
		self.guard2 = Guard(sprite, (266 / 3, 100), 3, 45, 300)

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

		self.guard1.update(self.game_surface, dt)
		self.guard2.update(self.game_surface, dt)

		r = pygame.Rect(0, 150, 300, 20)
		r2 = pygame.Rect(0, 100, 50, 10)
		r3 = pygame.Rect(200, 0, 20, 200)
		pygame.draw.rect(self.game_surface, (255, 0, 0), r)
		pygame.draw.rect(self.game_surface, (255, 0, 0), r2)
		pygame.draw.rect(self.game_surface, (255, 0, 0), r3)

		self.player.update(self.game_surface, [r, r2, r3], dt)

		self.surface.blit(
			pygame.transform.scale(
				self.game_surface,
				(self.surface.get_width(), self.surface.get_height())
			),
			(0, 0)
		)

