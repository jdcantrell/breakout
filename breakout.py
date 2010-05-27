import sys
import pygame
from OpenGL.GL import *
from pygame.locals import *
from pygame.color import *
from goodrobot.collision import CollisionGrid, collideCircleAABB
from goodrobot.euclid import *
from goodrobot.util import heartBeat

from time import clock,time

class Brick(Rect):
    def __init__(self, x, y, hp):
        self.vertices = [Vector((x, y)), Vector((x + 40, y)), Vector((x + 40, y + 10)), Vector((x, y + 10))]
        self.hp = hp
        self.dying = False
        self.dead = False
        self.dyingTick = False

    def draw(self, tick):
        alpha = 1.0
        if self.dying:
            if self.dyingTick is False:
                self.dyingTick = tick
            else:
                self.dyingTick += tick
                secs = self.dyingTick
                if secs > 0.5:
                    self.dead = True
                    alpha = 0
                else:
                    alpha =  2.0 * (.5 - secs)
        glColor4f(0, 1, 0, alpha)
        glRectf(self.vertices[0][0],self.vertices[0][1], self.vertices[1][0], self.vertices[2][1])

    def decreaseHP(self):
        self.hp -= 1
        if self.hp == 0:
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

    def draw(self):
        glColor4f(0,0,1,1)
        glBegin(GL_POINTS)
        glVertex2f(self.position.x, self.position.y)
        glEnd()

class BreakoutState:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((600, 600), OPENGL | DOUBLEBUF)

        glMatrixMode(GL_PROJECTION) 
        glLoadIdentity()
        glOrtho (0,600,0,600,-1,1)
        glMatrixMode(GL_MODELVIEW);
        glEnable(GL_BLEND);
        glClearColor(0.0,0.0,0.0,0.0)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE);
        glPointSize(10)

        pygame.display.set_caption('Breakout')
        self.clock = pygame.time.Clock()
        self.running = True
        self.prevIgnore = []
        self.ignore = []

        self.grid = CollisionGrid(20, 20, 600, 600)
        self.bricks = []
        for x in range(0, 11):
            for y in range(0, 24):
                self.bricks.append(Brick(x*50 + 30, y *20 + 50,1))
        self.edges = [
            Rect((10, 10), (590, 10), (590, 20), (10, 20),"top"),
            Rect((10, 580), (590, 580), (590, 590), (10, 590),"bottom"),
            Rect((10, 22), (20, 22), (20, 579), (10, 579),"left"),
            Rect((580, 22), (590, 22), (590, 579), (580, 579),"right")
        ]
        for i in self.bricks: self.grid.addPoly(i, i.vertices)
        for i in self.edges: self.grid.addPoly(i, i.vertices)
        self.ball = Ball(100,550, Vector((2,9)), 400)

        self.frames = 1
        self.pFrames = 1
        self.pTime = 0.0
        self.frameTime = 0
        self.fTime = 0.0

        heartBeat(self.updateScreen, self.updatePhysics, .01)


    def updatePhysics(self, t, step):
        #start = time()
        self.ball.update(step)
        items = self.grid.getItems(self.ball.position + (self.ball.dV * 10) )
        self.prevIgnore = self.ignore
        self.ignore = []
        #self.pFrames += 1
        for i in items:
            normal =  collideCircleAABB(self.ball, i)
            if normal is not None:
                if i not in self.prevIgnore:
                    self.ball.dV = self.ball.dV.reflectNormal(normal)
                    if isinstance(i, Brick): 
                        if i.decreaseHP() <= 0:
                            self.grid.removeItem(i)
                self.ignore.append(i)
        #self.pTime += time() - start

    def updateScreen(self, t, step, intLatency):
        start = time()
        #draw stuff
        glClear(GL_COLOR_BUFFER_BIT)

        glColor4f(255, 0, 0, 1);
        for edge in self.edges:
            glRectf(edge.vertices[0][0],edge.vertices[0][1], edge.vertices[1][0], edge.vertices[2][1])

        for brick in self.bricks:
            if brick.dead:
                self.bricks.remove(brick)
            else:
                brick.draw(step)
        self.ball.draw()
        glFlush()
        pygame.display.flip()

        self.fTime += time() - start
        self.frames += 1
        if (t - self.frameTime) > 1:
            #print "pFrames: %d(%f)" % (self.pFrames, self.pTime / self.pFrames) 
            print "Frames: %d(%f), time: %f" % (self.frames, self.fTime/self.frames, t - self.frameTime)
            self.frames = 0
            #self.pFrames = 0
            #self.pTime = 0.0
            self.fTime = 0.0
            self.frameTime = t
        return False

def main():
    b = BreakoutState()
        
if __name__ == '__main__':
    sys.exit(main())
