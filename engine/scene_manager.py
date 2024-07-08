from engine import *


class Scene:
	def on_entry(self):
		raise Exception("on_entry hasnt been implemented yet.")

	def on_event(self, event: pygame.event.Event):
		raise Exception("on_event hasnt been implemented yet.")

	def on_update(self, dt: float):
		raise Exception("on_update hasnt been implemented yet.")

	def on_exit(self):
		raise Exception("on_exit hasnt been implemented yet.")


class SceneManager:
	def __init__(self):
		self.curr_scene: Scene = None
		self.scenes: dict[str, Scene] = {}

	def add(self, name: str, scene: Scene):
		self.scenes.update({ name: scene })

	def switch(self, name: str):
		if name not in self.scenes:
			log_error(f"Scene '{name}' doesn't exists.")
			return

		if self.curr_scene:
			self.curr_scene.on_exit()

		self.curr_scene = self.scenes[name]
		self.curr_scene.on_entry()

	def update(self, dt: float):
		if not self.curr_scene:
			log_error("Current scene not set. use switch method to switch to a scene.")
			return

		self.curr_scene.on_update(dt)

	def poll_event(self, event: pygame.event.Event):
		if not self.curr_scene:
			log_error("Current scene not set. use switch method to switch to a scene.")
			return

		self.curr_scene.on_event(event)

	def quit(self):
		if self.curr_scene:
			self.curr_scene.on_exit()

