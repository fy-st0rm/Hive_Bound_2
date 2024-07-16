from globals import *
from engine import *


class Story(Scene):
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
			if event.key == pygame.K_SPACE:
				self.scene_manager.switch("menu")

	def on_update(self, dt: float):
		self.surface.fill((0, 0, 0))

		title_tex = Font.small.render('''

In the year 3055, the world has converged into a single, monolithic tower.
The tower stretches endlessly into the sky,
its base teeming with the destitute and desperate,
while the apex is reserved for the opulent and powerful.
No one knows what lies beyond the tower's confines,
for it is a realm shrouded in mystery and fear.

Driven by an insatiable curiosity and a desire for truth, you, a lone wanderer,
embark on a perilous journey to escape this hive of despair.
Ascend through the treacherous heights,
from the grimy depths where the wretched claw for survival,
to the gleaming spires where the elite revel in their decadence.
''', False, (255, 255, 255))
		
		self.surface.blit(
			title_tex,
			(self.surface.get_width() / 2 - title_tex.get_width() / 2, 100)
		)
		self.surface.blit(
			Sprite.title_sprite,
			(WIN_WIDTH / 2 - Sprite.title_sprite.get_width() / 2, 400)
		)
		up_tex = Font.small.render("Start your adventure ", False, (238,162,50))
		self.surface.blit(
			up_tex,
			(545, 335)
		)
		self.surface.blit(
			Sprite.space_key_sprite,
			(730, 330)
		)



