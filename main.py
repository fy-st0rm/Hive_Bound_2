import pygame
import os
import pygame

class InfiniteBackground:
    def __init__(self, screen, image_paths, scroll_speed=5):
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

        if y_offset>0:
            next_tile_index = num_tiles % len(self.images)
            self.screen.blit(self.images[next_tile_index], (0, self.map_height - y_offset))

class Player:
    def __init__(self,posX,posY,spritePath=""):
        self.posX = posX
        self.posY = posY
        self.spritePath=spritePath

    def update(self,direction):
        if direction =='left' and self.posX > 0:
            self.posX -= 10;
        elif direction =='right' and self.posX < 1024-50:
            self.posX += 10;
        
    def draw(self,surf):
        pygame.draw.rect(surf,(255,0,0),pygame.Rect(self.posX,self.posY,50,50))

# Define screen size
WIDTH = 1024
HEIGHT = 1024

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game View")
clock = pygame.time.Clock()

# Paths to background images (replace these with your actual image paths)
image_paths = {

    "./Ultra-Rich.png":3,
        "./Medium-Modern.png":3,
    "./Low-Rags.png":3
}


# Initialize Infinite Background
background = InfiniteBackground(screen, image_paths)
player = Player(512,512)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get user input for background scroll
    keys = pygame.key.get_pressed()
    Pdirection = None
    direction = None
    if keys[pygame.K_DOWN]:
        direction = 'down'
    if keys[pygame.K_UP]:
        direction = 'up'
    if keys[pygame.K_LEFT]:
        Pdirection = 'left'
    if keys[pygame.K_RIGHT]:
        Pdirection = 'right'

    # Update background scroll
    background.update(direction)
    player.update(Pdirection)
    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the infinite background
    background.draw()
    player.draw(screen)

    # Update the display
    pygame.display.flip()

    # Set FPS
    clock.tick(60)

pygame.quit()
