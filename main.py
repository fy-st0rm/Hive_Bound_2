import pygame
import time
from const import *
def main():
	pygame.init()
	
	surface = pygame.display.set_mode((800,600))
	
	running = True

	# Player Position
	PX = 60
	PY = 60

	# Action Flags
	up = False
	left = False
	right = False

	# Player Velocity
	PVELY = 0
	PVELX = 0

	# Ground Pos
	GY = 500

	# Ground Height
	GH = 20

	clock = pygame.time.Clock()


	while running:
		t = clock.tick(60)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					left = True
				
				if event.key == pygame.K_RIGHT:
					right = True
			
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_SPACE:
					up = True

				if event.key == pygame.K_LEFT:
					left = False
				
				if event.key == pygame.K_RIGHT:
					right = False

		surface.fill((0,0,0))

		# Drawing player and ground
		pygame.draw.rect(surface, (255,0,0), pygame.Rect(PX,PY,30,30))
		pygame.draw.rect(surface, (255,255,255), pygame.Rect(0,GY,800,GH))

		# Kinematics Calc
		PVELY = PVELY + g * t

		# DIY Collision
		if PY >= (GY - GH):
			PVELY = 0
			PY = GY - GH
		
		if (PY >= (GY - GH)) and up == True:
			PVELY -= 40

		# Movement 
		if left:
			PX -= HORIZONTAL_SPEED
		
		if right:
			PX += HORIZONTAL_SPEED

		PY += PVELY

		# Needed
		up = False
		
		pygame.display.update()


if __name__ == "__main__":
	main()
