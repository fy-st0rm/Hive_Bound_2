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
 
# Iterate through the contours 
for contour in contours: 
    # Approximate the contour to a polygon 
    approx = cv2.approxPolyDP(contour, 0.04 * cv2.arcLength(contour, True), True) 
     
    # Check if the polygon has 4 vertices (a rectangle) 
    if len(approx) == 4: 
        # Draw the rectangle on the original image 
        cv2.drawContours(image, [approx], 0, (0, 255, 0), 2) 
        
# Display the result 
cv2.imshow('Rectangles', image) 
cv2.waitKey(0) 
cv2.destroyAllWindows() 


print(approx)
WIDTH = 1024
HEIGHT = 1024

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game View")
clock = pygame.time.Clock()

# Paths to background images (replace these with your actual image paths)
image_paths = {

    "./assets/Ultra-Rich.png":3,
        "./assets/Medium-Modern.png":3,
    "./assets/Low-Rags.png":3
}



# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    pygame.draw.rect(screen,(255,0,0),pygame.Rect(approx[0][0][0],approx[0][0][0],50,50))
    print(f"Width : {approx[6][0][0] - approx[0][0][0]}")
    # Draw the infinite background
    # Update the display
    pygame.display.flip()

    # Set FPS
    clock.tick(60)

pygame.quit()
