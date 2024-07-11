import cv2
import numpy as np
import pygame

# Read the image 
image = cv2.imread('./test.png')

# Convert the image to grayscale 
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Canny edge detection 
edges = cv2.Canny(gray, 50, 150)

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
        # Draw the rectangle on the original image 
        cv2.drawContours(image, [approx], 0, (0, 255, 0), 2)

# Display the result 
cv2.imshow('Rectangles', image)
cv2.waitKey(0)
cv2.destroyAllWindows()

if not rectangles:
    raise ValueError("No rectangles found in the image.")

WIDTH = 1024
HEIGHT = 1024

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game View")
clock = pygame.time.Clock()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    # Draw all the rectangles
    for rect in rectangles:
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(
            rect[0][0][0], rect[0][0][1],
            rect[2][0][0] - rect[0][0][0],
            rect[2][0][1] - rect[0][0][1]
        ))

    # Update the display
    pygame.display.flip()

    # Set FPS
    clock.tick(60)

pygame.quit()
