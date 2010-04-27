from math import floor, fabs, ceil
from euclid import Segment

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
        print "Item added to"
        print cell
        self.add(item,cell)
        return cell

    #Return all items that might be close to the x,y
    def getItems(self, x, y):
        cell = (int(floor(x / self.xWidth)), int(floor(y/self.yWidth)))
        if self.cells.has_key(cell):
            return self.cells[cell]
        else:
            return []

    def removeItem(self, item):
        if self.items.has_key(item):
            for cell in self.items[item]:
                self.cells[cell].remove(item)
            del self.items[item]

    #Add a list of points related to the item
    def addPoly(self, item, points):
        previousPoint = None
        for point in points:
            cell = self.addPoint(item,point[0],point[1])
            if previousPoint is not None:
                i = None
                segment = Segment(point,previousPoint)
                print "Segment"
                print point
                print previousPoint
                xDelta = fabs(previousPoint[0] - point[0])
                yDelta = fabs(previousPoint[1] - point[1])
                #Check if segment crosses a grid line
                if xDelta > self.xWidth:
                    #get the start and end point snapping to the nearest grid axis for testing
                    start = ceil(min(previousPoint[0], point[0]) / (self.xWidth * 1.0)) * self.xWidth
                    end = floor(max(previousPoint[0], point[0]) / (self.xWidth * 1.0)) * self.xWidth
                    print "Start %f End %f" % (start, end)
                    while start <= end:
                        print "Testing Segment"
                        print (start,0)
                        print (start,self.height)
                        i = segment.get_intersection(Segment((start,0),(start,self.height)))
                        if i is None:
                            #segment does not intersect and therefore cannot intersect other segments
                            #not sure how this would get called
                            start = end + 1 
                        else:
                            print "Adding"
                            print i
                            self.addPoint(item, i.x - self.halfWidth, i.y)
                            self.addPoint(item, i.x,i.y)
                        start = start + self.xWidth
                elif yDelta > self.yWidth:
                    start = ceil(min(previousPoint[1], point[1]) / (self.yWidth * 1.0)) * self.yWidth
                    end = floor(max(previousPoint[1], point[1]) / (self.yWidth * 1.0)) * self.yWidth
                    while start < end:
                        i = segment.get_intersection(Segment((0, start),(self.width, start)))
                        if i is None:
                            start = end + 1 
                        else:
                            self.addPoint(item, i.x, i.y - self.halfHeight)
                            self.addPoint(item, i.x,i.y)
                        start = start + self.yWidth
            previousPoint = point

if __name__ == "__main__":
#TODO: Make this be a more rigorous test
    c = CollisionGrid(10,10,100,100)
    c.addPoly("a",[(5,5),(20,5)])
    c.addPoly("b",[(5,5),(5,20)])
    c.addPoly("c",[(5,5),(20,20)])
    c.addPoly("d",[(1,5),(15,18)])
    print "Cell 0,0"
    print c.getItems(0,0)
    print "Cell 1,0"
    print c.getItems(10,0)
    print "Cell 1,1"
    print c.getItems(10,10)
    print "Cells"
    print c.cells
    print "Items"
    print c.items

