import pygame
import os

class InfiniteBackground:
    def __init__(self, screen, image_paths, scroll_speed=10):
        self.screen = screen
        self.scroll_speed = scroll_speed
        self.images = [pygame.transform.scale(pygame.image.load(path), screen.get_size()) for path in image_paths]
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

        if y_offset > 0:
            next_tile_index = num_tiles % len(self.images)
            self.screen.blit(self.images[next_tile_index], (0, self.map_height - y_offset))

import pygame

# Define screen size
WIDTH = 800
HEIGHT = 1200

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("meow meow")
clock = pygame.time.Clock()

# Paths to background images (replace these with your actual image paths)
image_paths = [
    "map_tile1.png",
]

# Initialize Infinite Background
background = InfiniteBackground(screen, image_paths)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get user input for background scroll
    keys = pygame.key.get_pressed()
    direction = None
    if keys[pygame.K_DOWN]:
        direction = 'down'
    if keys[pygame.K_UP]:
        direction = 'up'

    # Update background scroll
    background.update(direction)

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the infinite background
    background.draw()

    # Update the display
    pygame.display.flip()

    # Set FPS
    clock.tick(60)

pygame.quit()
