from globals import *
from engine import *


class End(Scene):
	def __init__(
		self,
		surface: pygame.Surface,
		scene_manager: SceneManager
	):
		self.surface = surface
		self.scene_manager = scene_manager

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
		self.alpha = 255
		self.bg_h = 0
		self.pl_h = 0
		self.t_h = 0

		self.text = "Game By:\nshri-acha\nFuNk-y0u\nfy-st0rm\n"
		self.text_tex = Font.small.render(self.text, False, (255, 255, 255))

	def on_entry(self):
		global curr_music_index
		curr_music_index = 2
		pygame.mixer.Channel(curr_music_index).play(pygame.mixer.Sound('assets/sounds/end_song.mp3'), loops=-1)

	def on_exit(self):
		pass

	def on_event(self, event: pygame.event.Event):
		pass

	def on_update(self, dt: float):
		self.surface.fill((0, 0, 0))

		if self.alpha:
			pygame.draw.rect(
				self.light_surface,
				[255, 255, 255, self.alpha],
				(0, 0, self.light_surface.get_width(), self.light_surface.get_height())
			)
			self.alpha -= 0.5
			self.bg_h += 0.05
			self.pl_h -= 0.05

		self.game_surface.blit(
			Sprite.end_sprite,
			(
				SURFACE_WIDTH / 2 - Sprite.end_sprite.get_width() / 2,
				SURFACE_HEIGHT / 2 - 100 + self.bg_h
			)
		)

		self.game_surface.blit(
			Sprite.end_pl_sprite,
			(0,100 + self.pl_h)
		)

		self.game_surface.blit(
			self.text_tex,
			(SURFACE_WIDTH / 2 - self.text_tex.get_width() / 2, 100)
		)

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

