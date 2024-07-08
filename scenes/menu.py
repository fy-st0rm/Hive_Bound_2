from globals import *
from engine import *


class Menu(Scene):
	def __init__(
		self,
		surface: pygame.Surface,
		ui_manager: pygame_gui.UIManager,
		scene_manager: SceneManager
	):
		self.surface = surface
		self.ui_manager = ui_manager
		self.scene_manager = scene_manager

		self.title = pygame_gui.elements.UILabel(
			relative_rect = pygame.Rect(WIN_WIDTH / 2 - 200 / 2, 100, 200, 100),
			text = "Game Jam",
			manager = self.ui_manager
		)

		self.start_button = pygame_gui.elements.UIButton(
			relative_rect = pygame.Rect(WIN_WIDTH / 2 - 200 / 2, 275, 200, 50),
			text = "Start",
			manager = self.ui_manager
		)

		self.quit_button = pygame_gui.elements.UIButton(
			relative_rect = pygame.Rect(WIN_WIDTH / 2 - 200 / 2, 375, 200, 50),
			text = "Quit",
			manager = self.ui_manager
		)

		self.title.hide()
		self.start_button.hide()
		self.quit_button.hide()

	def on_entry(self):
		self.title.show()
		self.start_button.show()
		self.quit_button.show()

	def on_exit(self):
		self.title.hide()
		self.start_button.hide()
		self.quit_button.hide()

	def on_event(self, event: pygame.event.Event):
		if event.type == pygame_gui.UI_BUTTON_PRESSED:
			if event.ui_element == self.start_button:
				self.scene_manager.switch("game")
			elif event.ui_element == self.quit_button:
				pygame.event.post(pygame.event.Event(pygame.QUIT))

	def on_update(self, dt: float):
		self.surface.fill((0, 0, 0))

