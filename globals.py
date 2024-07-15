from engine.sprite_sheet import SpriteSheet

WIN_WIDTH  = 800
WIN_HEIGHT = 600
SURFACE_WIDTH = 266
SURFACE_HEIGHT = 200
FPS = 60


class State:
	walk = "walk"
	idle = "idle"
	stick = "stick"
	ascent = "ascent"
	descent = "descent"


class Dir:
	left = "left"
	right = "right"
	up = "up"
	down = "down"
	jump = "jump"
	stick = "stick"


class Sprite:
	guard_sprite = SpriteSheet("assets/Guard-sheet.png")
	player_sprite = SpriteSheet("assets/Player-sheet.png")
