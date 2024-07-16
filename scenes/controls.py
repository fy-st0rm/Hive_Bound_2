from globals import *
from engine import *


class Controls(Scene):
	def __init__(
		self,
		surface: pygame.Surface,
		scene_manager: SceneManager
	):
		self.surface = surface
		self.scene_manager = scene_manager

	def on_entry(self):
		pass

	def on_exit(self):
		pass

	def on_event(self, event: pygame.event.Event):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				self.scene_manager.switch("menu")

	def on_update(self, dt: float):
		self.surface.fill((0, 0, 0))

		title_tex = Font.big.render("Controls", False, (255, 255, 255))
		self.surface.blit(
			title_tex,
			(self.surface.get_width() / 2 - title_tex.get_width() / 2, 100)
		)

		# Move left
		left_tex = Font.mid.render("Move left", False, (255, 255, 255))
		self.surface.blit(
			left_tex,
			(self.surface.get_width() / 5, 250)
		)
		self.surface.blit(
			Sprite.a_key_sprite,
			(self.surface.get_width() / 1.5, 250)
		)

		# Move right
		right_tex = Font.mid.render("Move right", False, (255, 255, 255))
		self.surface.blit(
			right_tex,
			(self.surface.get_width() / 5, 310)
		)
		self.surface.blit(
			Sprite.d_key_sprite,
			(self.surface.get_width() / 1.5, 310)
		)

		# Jump
		up_tex = Font.mid.render("Jump", False, (255, 255, 255))
		self.surface.blit(
			up_tex,
			(self.surface.get_width() / 5, 370)
		)
		self.surface.blit(
			Sprite.space_key_sprite,
			(self.surface.get_width() / 1.5, 370)
		)

		# Stick
		stick_tex = Font.mid.render("Stick", False, (255, 255, 255))
		self.surface.blit(
			stick_tex,
			(self.surface.get_width() / 5, 430)
		)
		self.surface.blit(
			Sprite.shift_key_sprite,
			(self.surface.get_width() / 1.5, 430)
		)

		# Back
		back_tex = Font.mid.render("Go Back", False, (255, 255, 255))
		self.surface.blit(
			back_tex,
			(self.surface.get_width() / 5, 480)
		)
		self.surface.blit(
			Sprite.escape_key_sprite,
			(self.surface.get_width() / 1.5, 480)
		)



