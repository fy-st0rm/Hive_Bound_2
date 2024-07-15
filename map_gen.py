import cv2
import numpy as np
import os
import pygame
import json
from engine.sprite_sheet import SpriteSheet

pygame.init()


def get_rects(image_data) -> list[list[int]]:
	gray = cv2.cvtColor(image_data, cv2.COLOR_RGB2GRAY)

	# Apply Gaussian blur to reduce noise
	blurred = cv2.GaussianBlur(gray, (5, 5), 0)

	# Perform Canny edge detection
	edges = cv2.Canny(blurred, 50, 150)

	# Find contours
	contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	# Initialize a list to store rectangle approximations
	rectangles = []

	# Iterate through the contours 
	for contour in contours:
		# Approximate the contour to a polygon 
		approx = cv2.approxPolyDP(contour, 0.04 * cv2.arcLength(contour, True), True)
		
		# Check if the polygon has 4 vertices (a rectangle) 
		if len(approx) == 4:
			rectangles.append(approx)

	if not rectangles:
		raise ValueError("No rectangles found in the image.")

	rects = []
	for rect in rectangles:
		x, y, w, h = cv2.boundingRect(rect)
		rects.append([x, y, w, h])

	return rects


def get_guard_pos(surface: pygame.Surface) -> dict[int, dict]:
	pos = {}
	for i, y in enumerate(range(surface.get_height())):
		for x in range(surface.get_width()):
			col = surface.get_at((x, y))
			if col.r == 172 or col.r == 255:
				pos.update({
					i: {
						"pos": [x, y],
						"delay": col.g,
						"f": col.b
					}
				})
	return pos


screen = pygame.display.set_mode((800, 600))
maps = os.listdir("./assets/map_imgs")

for map in maps:
	map_name = map.split(".")[0]
	map_path = f"./assets/map_imgs/{map}"

	sheet = SpriteSheet(map_path)
	rect_image = sheet.image_at(0, 1, 300, 1500)
	rect_image = pygame.transform.flip(rect_image, True, False)
	rect_image = pygame.transform.rotate(rect_image, 90)
	rect_image_data = pygame.surfarray.array3d(rect_image)

	rects = get_rects(rect_image_data)

	guard_image = sheet.image_at(0, 2, 300, 1500)
	guard_pos = get_guard_pos(guard_image)

	map_data = {
		"image": map_path,
		"rects": rects,
		"guard_pos": guard_pos
	}

	with open(f"./assets/map/{map_name}.json", "w") as f:
		json.dump(map_data, f, indent = 2)

