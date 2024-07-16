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

	def on_entry(self):
		pass

	def on_exit(self):
		pass

	def on_event(self, event: pygame.event.Event):
		pass

	def on_update(self, dt: float):
		self.surface.fill((255, 255, 255))

