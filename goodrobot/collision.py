from math import floor, fabs, ceil
from euclid import Segment, Vector

class CollisionGrid:
    def __init__(self, xWidth, yWidth, height, width):
        self.xWidth = xWidth
        self.yWidth = yWidth
        self.height = height
        self.width = width
        self.halfHeight = yWidth / 2.0
        self.halfWidth = xWidth / 2.0
        self.cells = {}
        self.items = {}

    def add(self,item,cell):
        if not self.cells.has_key(cell):
            self.cells[cell] = []
        if not self.items.has_key(item):
            self.items[item] = []

        try:
            self.items[item].index(cell)
        except ValueError:
            self.cells[cell].append(item)
            self.items[item].append(cell)

    def addPoint(self, item, x, y):
        cell = (int(floor(x / self.xWidth)), int(floor(y/self.yWidth)))
        self.add(item,cell)
        return cell

    #Return all items that might be close to the x,y
    def getItems(self, *remaining):
        list = set()
        checkedCells = {}
        for pt in remaining:
            x = pt[0]
            y = pt[1]
            cell = (int(floor(x / self.xWidth)), int(floor(y/self.yWidth)))
            if not checkedCells.has_key(cell):
                checkedCells[cell] = True
                if self.cells.has_key(cell):
                    list.update(self.cells[cell])
        return list

    def removeItem(self, item):
        if self.items.has_key(item):
            for cell in self.items[item]:
                self.cells[cell].remove(item)
            del self.items[item]

    def addOnGridIntersect(self, item, segment):
        xDelta = fabs(segment.pt1.x - segment.pt2.x)
        yDelta = fabs(segment.pt1.y - segment.pt2.y)
        #Check if segment crosses a grid line
        #get the start and end point snapping to the nearest grid axis for testing
        start = ceil(min(segment.pt1.x, segment.pt2.x) / (self.xWidth * 1.0)) * self.xWidth
        end = floor(max(segment.pt1.x, segment.pt2.x) / (self.xWidth * 1.0)) * self.xWidth
        while start <= end:
            i = segment.get_intersection(Segment((start,0),(start,self.height)))
            if i is None:
                #segment does not intersect and therefore cannot intersect other segments
                #not sure how this would get called
                start = end + 1 
            else:
                self.addPoint(item, i.x - self.halfWidth, i.y)
                self.addPoint(item, i.x,i.y)
            start = start + self.xWidth
        #check in the other direction
        if start > end:
            start = ceil(min(segment.pt1.y, segment.pt2.y) / (self.yWidth * 1.0)) * self.yWidth
            end = floor(max(segment.pt1.y, segment.pt2.y) / (self.yWidth * 1.0)) * self.yWidth
            while start <= end:
                i = segment.get_intersection(Segment((0, start),(self.width, start)))
                if i is None:
                    start = end + 1 
                else:
                    self.addPoint(item, i.x, i.y - self.halfHeight)
                    self.addPoint(item, i.x,i.y)
                start = start + self.yWidth

    #Add a list of points related to the item
    def addPoly(self, item, points):
        previousPoint = None
        for point in points:
            cell = self.addPoint(item,point[0],point[1])
            if previousPoint is not None:
                i = None
                self.addOnGridIntersect(item, Segment(point,previousPoint))
            previousPoint = point
        if len(points) > 2:
            self.addOnGridIntersect(item, Segment(previousPoint, points[0]))

    def search(self, item):
        found = []
        for cell,items in self.cells.iteritems():
            try:
                items.index(item)
                found.append(cell)
            except ValueError:
                pass
        return found

#Collision functions
def collideCircleAABB(c, poly):
    #find AABB
    minV = Vector((poly.vertices[0].x, poly.vertices[0].y))
    maxV = Vector((poly.vertices[0].x, poly.vertices[0].y))
    for vert in poly.vertices:
        minV.x = min(vert.x, minV.x)
        minV.y = min(vert.y, minV.y)
        maxV.x = max(vert.x, maxV.x)
        maxV.y = max(vert.y, maxV.y)

    #get closest point
    cp = Vector((c.x,c.y))
    if c.x < minV.x: cp.x = minV.x
    elif c.x > maxV.x: cp.x = maxV.x

    if c.y < minV.y: cp.y = minV.y
    elif c.y > maxV.y: cp.y = maxV.y

    dirVector = cp - Vector((c.x, c.y)) 
    mag = dirVector.magnitudeSquared()
    if mag < .0001: dirVector = cp
    if mag <= c.rSquared:
        #return normal vector
        if dirVector.y > 0.0001: return Vector((0,-1))
        if dirVector.y < -0.0001: return Vector((0,1))
        if dirVector.x < 0.0001: return Vector((1,0))
        if dirVector.x > -0.0001: return Vector((-1,0))
    #no normal for collision
    return None

def collideCircleSegment(c, segment):
    pass
#rough sketch: 
#calculate c - segment.pt1
#calculate segment.unitVector
#projMag = segment.unitVector.determinant(pt_v)
#if projMag > 0 and projMag < segment.magnitude:
# see if (segment.unitVector * projection - c).magnitudeSquared <= c.radiusSquared
# then collide!

    

