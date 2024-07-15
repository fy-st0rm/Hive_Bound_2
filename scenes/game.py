from globals import *
from engine import *
from characters import *


FREE_CAMERA = False


class Game(Scene):
	def __init__(self, surface: pygame.Surface, scene_manager: SceneManager):
		self.surface = surface
		self.scene_manager = scene_manager

		self.camera = [0, 0]
		self.game_surface = pygame.Surface((SURFACE_WIDTH, SURFACE_HEIGHT))

		self.checkpoint = (0, 100)
		self.player = Player((100, 1500 - 32))
		self.player.checkpoint = self.checkpoint

		self.left = self.right = self.up = self.down = False

		# Loading map
		with open("./assets/map/map.json", "r") as f:
			self.map = json.load(f)
			rects = []
			for r in self.map["rects"]:
				rects.append(pygame.Rect(r[0], r[1], r[2], r[3]))
			self.map["rects"] = rects

		self.map_sprite = SpriteSheet(self.map["image"])
		self.map_img = self.map_sprite.image_at(0, 0, 300, 1500)

		# Loading up guards
		guard_pos = self.map["guard_pos"]
		self.guards = []
		for i in guard_pos:
			pos = guard_pos[i]["pos"]
			delay = guard_pos[i]["delay"]
			f = guard_pos[i]["f"]
			self.guards.append(
				Guard(Sprite.guard_sprite, (pos[0], pos[1] - 32), delay, f, 30, 100)
			)

	def on_entry(self):
		print("Entered game")

	def on_exit(self):
		print("Game exited")

	def on_event(self, event: pygame.event.Event):
		self.player.event(event)
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				self.scene_manager.switch("menu")
			if event.key == pygame.K_w:
				self.up = True
			if event.key == pygame.K_a:
				self.left = True
			if event.key == pygame.K_s:
				self.down = True
			if event.key == pygame.K_d:
				self.right = True

		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_w:
				self.up = False
			if event.key == pygame.K_a:
				self.left = False
			if event.key == pygame.K_s:
				self.down = False
			if event.key == pygame.K_d:
				self.right = False

	def on_update(self, dt: float):
		self.game_surface.fill((0, 0, 0))

		if FREE_CAMERA:
			if self.left:
				self.camera[0] -= 5
			if self.right:
				self.camera[0] += 5
			if self.up:
				self.camera[1] -= 5
			if self.down:
				self.camera[1] += 5
		else:
			self.camera[0] += (self.player.rect.x - self.camera[0] - SURFACE_WIDTH / 2) / 10
			self.camera[1] += (self.player.rect.y - self.camera[1] - SURFACE_HEIGHT / 1.5) / 10

		self.game_surface.blit(
			self.map_img,
			(-self.camera[0], -self.camera[1])
		)

		for guard in self.guards:
			guard.update(self.game_surface, dt, self.camera)

		self.player.update(self.game_surface, self.map["rects"], dt, self.camera)

#		for r in self.map["rects"]:
#			pygame.draw.rect(self.game_surface, (255, 0, 0), [r.x - self.camera[0], r.y - self.camera[1], r.w, r.h])
#
		self.surface.blit(
			pygame.transform.scale(
				self.game_surface,
				(self.surface.get_width(), self.surface.get_height())
			),
			(0, 0),
			special_flags=pygame.BLEND_RGBA_MULT
		)

