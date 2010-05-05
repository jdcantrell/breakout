import sys
import pygame
from pygame.locals import *
from pygame.color import *
from goodrobot.collision import CollisionGrid, collideCircleAABB
from goodrobot.euclid import *

def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption('Breakout')
    clock = pygame.time.Clock()
    running = True

    grid = CollisionGrid(20, 20, 600, 600)
    poly1= (10,10,580,10)
    poly2= (10,580,580,10)
    poly3= (10,22,10,557)
    poly4= (580,22,10,557)

    top = Rect((10, 10), (590, 10), (590, 20), (10, 20))
    bottom = Rect((10, 580), (590, 580), (590, 590), (10, 590))
    left = Rect((10, 22), (20, 22), (20, 579), (10, 579))
    right = Rect((580, 22), (590, 22), (590, 579), (580, 579))

    grid.addPoly(top, [(10, 10), (590, 10), (590, 20), (10, 20)])
    grid.addPoly(bottom, [(10, 580), (590, 580), (590, 590), (10, 590)])
    grid.addPoly(left, [(10, 22), (20, 22), (20, 579), (10, 579)])
    grid.addPoly(right, [(580, 22), (590, 22), (590, 579), (580, 579)])

    circle = Circle(300,300,10)
    xDir = -1
    yDir = 1

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False
        screen.fill(THECOLORS["black"])
        

        #update position
        circle.x = circle.x + xDir
        circle.y = circle.y + yDir

        items = grid.getItems((circle.x, circle.y),(circle.x + circle.radius * xDir, circle.y + circle.radius * yDir))
        for i in items:
            if collideCircleAABB(circle, i):
                if i is top:
                    print "Top Collide!"
                    yDir = yDir * -1
                elif i is bottom:
                    print "Bottom Collide!"
                    yDir = yDir * -1
                elif i is right:
                    print "Right Collide!"
                    xDir = xDir * -1
                elif i is left:
                    print "Left Collide!"
                    xDir = xDir * -1

        #draw rects
        pygame.draw.rect(screen, (255,0,0), poly1)
        pygame.draw.rect(screen, (0,0,255), poly2)
        pygame.draw.rect(screen, (0,255,0), poly3)
        pygame.draw.rect(screen, (255,255,0), poly4)
        pygame.draw.circle(screen, (0,255,255), (circle.x, circle.y), circle.radius)

        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    sys.exit(main())
