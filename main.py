from globals import *
from engine import *
from scenes.game import Game
from scenes.menu import Menu
from scenes.end  import End
from scenes.story  import Story
from scenes.controls import Controls


class Main:
	def __init__(self, width: int, height: int, fps: int):
		self.width  = width
		self.height = height
		self.fps    = fps

		self.screen = pygame.display.set_mode((self.width, self.height), pygame.SRCALPHA)

		self.running = True
		self.clock = pygame.time.Clock()

		self.ui_manager = pygame_gui.UIManager((self.width, self.height))

		self.scene_manager = SceneManager()
		self.scene_manager.add("menu", Menu(self.screen, self.ui_manager, self.scene_manager))
		self.scene_manager.add("controls", Controls(self.screen, self.scene_manager))
		self.scene_manager.add("story", Story(self.screen, self.scene_manager))
		self.scene_manager.add("game", Game(self.screen, self.scene_manager))
		self.scene_manager.add("end", End(self.screen, self.scene_manager))
		self.scene_manager.switch("story")

		self.music_button_rect = pygame.Rect(800-32, 600-32, 32, 32)
		self.music_on_sprite  = pygame.transform.scale(Sprite.music_sprite.image_at(0, 0, 16, 16), (32, 32))
		self.music_off_sprite = pygame.transform.scale(Sprite.music_sprite.image_at(1, 0, 16, 16), (32, 32))
		self.music_tex = self.music_on_sprite
		self.music_on = True

	def run(self):
		last_time = time.time()
		while self.running:

			# Calculating delta time
			dt = time.time() - last_time
			dt *= self.fps
			last_time = time.time()

			self.screen.fill((0, 0, 0))

			self.poll_events()

			t = self.clock.tick(self.fps) / 1000.0

			self.scene_manager.update(t)
			self.ui_manager.update(t)
			self.ui_manager.draw_ui(self.screen)

			self.screen.blit(
				self.music_tex,
				(self.music_button_rect.x, self.music_button_rect.y)
			)

			pygame.display.update()

	def poll_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False

			# Music toggle
			if event.type == pygame.MOUSEBUTTONDOWN:
				mp = pygame.mouse.get_pos()
				if self.music_button_rect.collidepoint(mp) and pygame.mouse.get_pressed()[0]:
					if self.music_on:
						self.music_tex = self.music_off_sprite
						self.music_on = False
						pygame.mixer.Channel(curr_music_index).pause()
					else:
						self.music_tex = self.music_on_sprite
						self.music_on = True
						pygame.mixer.Channel(curr_music_index).unpause()

			self.scene_manager.poll_event(event)
			self.ui_manager.process_events(event)

	def quit(self):
		self.scene_manager.quit()


if __name__ == "__main__":

	pygame.init()
	main = Main(WIN_WIDTH, WIN_HEIGHT, FPS)
	pygame.mixer.music.load(os.path.join(os.getcwd(),'assets/sounds','f_background.mp3'))
	pygame.mixer.music.load(os.path.join(os.getcwd(),'assets/sounds','end_song.mp3'))
	pygame.mixer.Channel(curr_music_index).play(pygame.mixer.Sound('assets/sounds/f_background.mp3'), loops=-1)
	main.run()
	main.quit()

