from engine import *


class SpriteSheet:
	def __init__(self, filename):
		self.transColor = (255, 255, 255, 0)
		try:
			self.sheet = pygame.image.load(filename)
		except pygame.error:
			print('Unable to load spritesheet image:', filename)
			raise SystemExit

	def image_at(self, x, y, w, h, colorkey=None):
		xp = x * w
		yp = y * h

		rect = pygame.Rect(xp, yp, w, h)
		image = pygame.Surface(rect.size).convert_alpha()
		image.fill(self.transColor)
		image.blit(self.sheet, (0, 0), rect)

		if colorkey is not None:
			if colorkey == -1:
				colorkey = image.get_at((0, 0))
			image.set_colorkey(colorkey, pygame.RLEACCEL)

		return image

	# Load a whole bunch of images and return them as a list
	def images_at(self, rects, colorkey=None):
		"Loads multiple images, supply a list of coordinates"
		return [self.image_at(rect, colorkey) for rect in rects]

	def load_strip(self, rect: pygame.Rect, image_count: int) -> list[pygame.Surface]:
		images = []
		for i in range(image_count):
			images.append(self.image_at(rect[0], rect[1], rect[2], rect[3]))
			rect[0] += 1
		return images

"""
	# Load a specific image from a specific rectangle
	def image_at(self, rectangle, colorkey=None):
		"Loads image from x,y,x+offset,y+offset"
		rect = pygame.Rect(rectangle)
		image = pygame.Surface(rect.size).convert_alpha()
		image.fill(self.transColor)
		image.blit(self.sheet, (0, 0), rect)
		if colorkey is not None:
			if colorkey == -1:
				colorkey = image.get_at((0, 0))
			image.set_colorkey(colorkey, pygame.RLEACCEL)
		return image
"""


"""
	# Load a whole strip of images
	def load_strip(self, rect, image_count, colorkey=None):
		"Loads a strip of images and returns them as a list"
		tups = [(rect[0] + rect[2] * x, rect[1], rect[2], rect[3])
		        for x in range(image_count)]
		return self.images_at(tups, colorkey)
	"""
