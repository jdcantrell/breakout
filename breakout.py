import sys
import pygame
from pygame.locals import *
from pygame.color import *
from goodrobot.collision import CollisionGrid, collideCircleAABB
from goodrobot.euclid import *


class Brick(Rect):
    def __init__(self, x, y, hp):
        self.coords = [(x, y), (x + 40, y), (x + 40, y + 10), (x, y + 10)]
        self.hp = hp
        self.dying = False
        self.dead = False
        self.dyingTick = False

    def draw(self, screen, tick):
        alpha = 255
        if self.dying:
            if self.dyingTick is False:
                self.dyingTick = tick
            else:
                secs = tick - self.dyingTick
                if secs > .5:
                    self.dead = True
                    alpha = 0
                else:
                    alpha = 510 * (.5 - secs)
        pygame.draw.rect(screen, (255,0,0,alpha), self.coords)

    def decreaseHP(self):
        self.hp -= 1
        if self.hp == 0:
            self.dying = True
        return self.hp

class Ball(Circle):
    def __init__(self, x, y, directionVector,velocity):
        self.position = Vector(x,y)
        self.radius = 10
        self.dV = directionVector.unit()
        self.velocty = velocity

    def update(step):
        self.position = self.dV * self.velocty * step + self.position

    def draw(self, screen):
        pygame.draw.circle(screen, (0,255,255), self.position, self.radius)




class BreakoutState:
    def __init__(self):
        self.grid = CollisionGrid(20, 20, 600, 600)
        self.bricks = [
            Brick(20,20,1),
            Brick(70,20,1),
            Brick(120,20,1),
            Brick(170,20,1),
            Brick(220,20,1),
            Brick(270,20,1),
            Brick(320,20,1),
            Brick(370,20,1),
        ]
        self.edges = [
            Rect((10, 10), (590, 10), (590, 20), (10, 20)),
            Rect((10, 580), (590, 580), (590, 590), (10, 590)),
            Rect((10, 22), (20, 22), (20, 579), (10, 579)),
            Rect((580, 22), (590, 22), (590, 579), (580, 579))
        ]
        for i in self.bricks: self.grid.addPoly(i.coords)
        for i in self.edges: self.grid.addPoly(i.vertices)
        self.ball = Ball(300,300, Vector(1,1), 1)

    def updatePhyics(self, time, step):
        items = self.grid.getItems(self.ball.position,(circle.x + circle.radius * xDir, circle.y + circle.radius * yDir))
        for i in items:
            normal =  collideCircleAABB(circle, i)
            if normal is not None:
                i.decreaseHP()
                self.ball.direction = self.ball.direction.reflectNormal(normal)
                if i.dying:
                    self.grid.removeItem(i)

    def updateScreen(self, time, step, intLatency):
        #draw stuff
        pass


        



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
