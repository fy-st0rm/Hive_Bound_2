import pygame

def main():
	pygame.init()
	
	surface = pygame.display.set_mode((800,600))
	
	running = True

	g = 9.8

	playerx = 30
	playery = 30

	groundy = 500

	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					g = 9.8
			
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_UP:
					g = -14
		
		surface.fill((0,0,0))
		pygame.draw.rect(surface, (255,0,0), pygame.Rect(playerx,playery,60,60))
		pygame.draw.rect(surface, (255,0,0), pygame.Rect(0,groundy,800,60))

		playery = playery + g * 0.02
		
		if playery >= (groundy-60):
			playery = groundy-60

		pygame.display.update()


if __name__ == "__main__":
	main()
