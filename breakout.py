import sys
import pygame
from pygame.locals import *
from pygame.color import *
from goodrobot.collision import CollisionGrid, collideCircleAABB
from goodrobot.euclid import *
from goodrobot.util import heartBeat

class Brick(Rect):
    def __init__(self, x, y, hp):
        self.vertices = [Vector((x, y)), Vector((x + 40, y)), Vector((x + 40, y + 10)), Vector((x, y + 10))]
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
                self.dyingTick += tick
                secs = self.dyingTick
                if secs > .5:
                    self.dead = True
                    alpha = 0
                else:
                    alpha = 510 * (.5 - secs)
                    print "Alpha: %f" % alpha
        pygame.draw.rect(screen, (0,255,0,alpha), (self.vertices[0][0], self.vertices[0][1], 40,10))

    def decreaseHP(self):
        self.hp -= 1
        if self.hp == 0:
            print "Dying!"
            self.dying = True
        return self.hp

class Ball(Circle):
    def __init__(self, x, y, directionVector,velocity):
        self.position = Vector((x,y))
        self.radius = 10
        self.rSquared = 100
        self.dV = directionVector.unit()
        self.velocty = velocity

    def update(self,step):
        self.position = self.dV * self.velocty * step + self.position
        self.x = self.position[0]
        self.y = self.position[1]

    def draw(self, screen):
        pygame.draw.circle(screen, (0,255,255), self.position, self.radius)

class BreakoutState:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((600, 600))
        pygame.display.set_caption('Breakout')
        self.clock = pygame.time.Clock()
        self.running = True
        self.prevIgnore = []
        self.ignore = []

        self.grid = CollisionGrid(20, 20, 600, 600)
        self.bricks = [
            Brick(30,50,1),
            Brick(80,50,1),
            Brick(130,50,1),
            Brick(180,50,1),
            Brick(230,50,1),
            Brick(280,50,1),
            Brick(330,50,1),
            Brick(380,50,1),
        ]
        self.edges = [
            Rect((10, 10), (590, 10), (590, 20), (10, 20)),
            Rect((10, 580), (590, 580), (590, 590), (10, 590)),
            Rect((10, 22), (20, 22), (20, 579), (10, 579)),
            Rect((580, 22), (590, 22), (590, 579), (580, 579))
        ]
        for i in self.bricks: self.grid.addPoly(i, i.vertices)
        for i in self.edges: self.grid.addPoly(i, i.vertices)
        self.ball = Ball(300,300, Vector((-1,-1)), 200)

        heartBeat(self.updateScreen, self.updatePhysics, .01)


    def updatePhysics(self, time, step):
        self.ball.update(step)
        items = self.grid.getItems(self.ball.position)
        self.prevIgnore = self.ignore
        self.ignore = []
        for i in items:
            normal =  collideCircleAABB(self.ball, i)
            if normal is not None:
                if i not in self.prevIgnore:
                    self.ball.dV = self.ball.dV.reflectNormal(normal)
                    if isinstance(i, Brick): 
                        i.decreaseHP()
                        if i.dying:
                            self.grid.removeItem(i)
                self.ignore.append(i)

    def updateScreen(self, time, step, intLatency):
        #draw stuff
        self.screen.fill(THECOLORS["black"])
        for edge in self.edges:
            pygame.draw.rect(self.screen, (255,0,0), (edge.vertices[0][0],edge.vertices[0][1], edge.vertices[1][0] - edge.vertices[0][0], edge.vertices[2][1] - edge.vertices[0][1]))

        for brick in self.bricks:
            brick.draw(self.screen, step)
        
        self.ball.draw(self.screen)
        pygame.display.flip()
        return False
        #self.clock.tick(60)

def main():
    b = BreakoutState()
        



if __name__ == '__main__':
    sys.exit(main())
