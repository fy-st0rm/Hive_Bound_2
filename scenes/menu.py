from globals import *
from engine import *

class InfiniteBackground:
	def __init__(self, screen, scroll_speed=5):
		self.screen = screen
		self.scroll_speed = scroll_speed
		self.bg_image = SpriteSheet("./assets/map_imgs/map.png")
		self.images = [
			pygame.transform.scale(i, screen.get_size())
			for i in self.bg_image.load_strip_y([0, 0, 300, 300], 6)
		]
		self.map_height = screen.get_height()
		self.scroll = 0

	def update(self, direction):
		if direction == 'down':
			self.scroll += self.scroll_speed
		elif direction == 'up':
			self.scroll -= self.scroll_speed

	def draw(self):
		num_tiles = (self.scroll // self.map_height) + 1
		y_offset = self.scroll % self.map_height

		tile_index = (num_tiles - 1) % len(self.images)
		self.screen.blit(self.images[tile_index], (0, -y_offset))

		if y_offset>0:
			next_tile_index = num_tiles % len(self.images)
			self.screen.blit(self.images[next_tile_index], (0, self.map_height - y_offset))


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

		self.bg = InfiniteBackground(self.surface)

		self.start_button = pygame_gui.elements.UIButton(
			relative_rect = pygame.Rect(WIN_WIDTH / 2 - 200 / 2, 275, 200, 50),
			text = "Start",
			manager = self.ui_manager
		)

		self.controls_button = pygame_gui.elements.UIButton(
			relative_rect = pygame.Rect(WIN_WIDTH / 2 - 200 / 2, 375, 200, 50),
			text = "Controls",
			manager = self.ui_manager
		)

		self.quit_button = pygame_gui.elements.UIButton(
			relative_rect = pygame.Rect(WIN_WIDTH / 2 - 200 / 2, 475, 200, 50),
			text = "Quit",
			manager = self.ui_manager
		)

		self.start_button.hide()
		self.controls_button.hide()
		self.quit_button.hide()

	def on_entry(self):
		global curr_music_index
		curr_music_index = 1
		self.start_button.show()
		self.controls_button.show()
		self.quit_button.show()

	def on_exit(self):
		self.start_button.hide()
		self.controls_button.hide()
		self.quit_button.hide()

	def on_event(self, event: pygame.event.Event):
		if event.type == pygame_gui.UI_BUTTON_PRESSED:
			if event.ui_element == self.start_button:
				self.scene_manager.switch("game")
			elif event.ui_element == self.controls_button:
				self.scene_manager.switch("controls")
			elif event.ui_element == self.quit_button:
				pygame.event.post(pygame.event.Event(pygame.QUIT))

	def on_update(self, dt: float):
		self.surface.fill((0, 0, 0))
		self.bg.update("down")
		self.bg.draw()

		self.surface.blit(
			Sprite.title_sprite,
			(WIN_WIDTH / 2 - Sprite.title_sprite.get_width() / 2, 100)
		)

