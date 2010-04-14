import sys
import pygame
from pygame.color import *

def main():
	pygame.init()
	screen = pygame.display.set_mode((600, 600))
	pygame.display.set_caption('Breakout')
	clock = pygame.time.Clock()
	running = True

	while running:
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False
		screen.fill(THECOLORS["black"])

		pygame.display.flip()
		clock.tick(60)

if __name__ == '__main__':
	sys.exit(main())
