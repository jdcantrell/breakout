from math import fabs, sqrt
epsilon = 0.000000000000001
class Vector:
    def __init__(self, point):
        self.x = point[0]
        self.y = point[1]
    
    def __repr__(self):
        return "(%f, %f)" % (self.x, self.y)

    def __getitem__(self, k):
        if k == 0:
            return self.x
        else:
            return self.y

    def __len__(self):
        return 2

    def __sub__(self,vector):
        return Vector((self.x - vector.x, self.y - vector.y))

    def __add__(self, vector):
        return Vector((self.x + vector.x, self.y + vector.y))

    def __mul__(self, scalar):
        return Vector((self.x * scalar, self.y * scalar))

    def __eq__(self,other):
        return fabs(other.x - self.x) <= epsilon and \
                fabs(other.y - self.y) <= epsilon

    def cross(self, v):
        return self.x * v.y - self.y * v.x

    def dot(self, v):
        return self.x * v.x + self.y * v.y

    def reflectNormal(self, nV):
        return  nV * nV.dot(self) * 2 - self

    def magnitudeSquared(self):
        return self.x * self.x  + self.y * self.y

    def unit(self):
        #eventually may need to do some inverse square optimization
        magnitude = sqrt(self.x * self.x + self.y * self.y)
        return self * (1.0 / magnitude)

class Circle:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.rSquared = radius * radius

class Rect:
    def __init__(self, pt1, pt2, pt3, pt4):
        self.vertices = [Vector(pt1), Vector(pt2), Vector(pt3), Vector(pt4)]


class Segment:
    def __init__(self, pt1, pt2):
        self.pt1 = Vector(pt1)
        self.pt2 = Vector(pt2)
        self.vector = self.pt1 - self.pt2
        self.unit = None

    def unitVector(self):
        if self.unit is None:
            self.unit = self.vector.unit()
        return self.unit

    def lengthSquared(self):
        return self.vector.magnitudeSquared()

    
    def get_intersection(self, segment):
        c = self.collide(segment)
        if c:
            return c[0] + c[1] * (c[2]/ (1.0 * c[3]))
        else:
            return None
        
    def collide(self, segment):
        #get segment vectors
        u = self.pt2 - self.pt1
        v = segment.pt2 - segment.pt1
        det = u.cross(v)

        #parallel
        if fabs(det) < epsilon:
            return False
        
        #get vector between the pts
        w = self.pt1 - segment.pt1
        
        #Check if lines intersect but not within our segment
        s = v.cross(w)
        #s = v.x * w.y - v.y * w.x
        if det < 0:
            if s < det or s > 0:
                return False
        elif s < 0 or s > det:
            return False

        #t = u.x * w.y - u.y * w.x
        t = u.cross(w)
        if det < 0:
            if t < det or t > 0:
                return False
        elif t < 0 or t > det:
            return False

        return (self.pt1, u, s, det)
