from engine.sprite_sheet import SpriteSheet
import pygame
import os

pygame.init()
pygame.font.init()


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
	a_key_sprite = pygame.image.load("assets/keys/A-Key.png")
	d_key_sprite = pygame.image.load("assets/keys/D-Key.png")
	space_key_sprite = pygame.image.load("assets/keys/Space-Key.png")
	shift_key_sprite = pygame.image.load("assets/keys/Shift-Key.png")
	escape_key_sprite = pygame.image.load("assets/keys/Esc-Key.png")
	title_sprite = pygame.transform.scale(
		pygame.image.load("assets/title.png"),
		(90 * 5, 35 * 5)
	)
	music_sprite = SpriteSheet("assets/music.png")

class Font:
	big = pygame.font.Font("assets/font.ttf", 50)
	mid = pygame.font.Font("assets/font.ttf", 35)
	small = pygame.font.Font("assets/font.ttf", 16)

pygame.mixer.init();
pygame.mixer.Channel(0).set_volume(1)
pygame.mixer.Channel(1).set_volume(.3)

