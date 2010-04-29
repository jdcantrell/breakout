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
                xDelta = fabs(previousPoint[0] - point[0])
                yDelta = fabs(previousPoint[1] - point[1])
                #Check if segment crosses a grid line
                #get the start and end point snapping to the nearest grid axis for testing
                start = ceil(min(previousPoint[0], point[0]) / (self.xWidth * 1.0)) * self.xWidth
                end = floor(max(previousPoint[0], point[0]) / (self.xWidth * 1.0)) * self.xWidth
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
                    start = ceil(min(previousPoint[1], point[1]) / (self.yWidth * 1.0)) * self.yWidth
                    end = floor(max(previousPoint[1], point[1]) / (self.yWidth * 1.0)) * self.yWidth
                    while start <= end:
                        i = segment.get_intersection(Segment((0, start),(self.width, start)))
                        if i is None:
                            start = end + 1 
                        else:
                            self.addPoint(item, i.x, i.y - self.halfHeight)
                            self.addPoint(item, i.x,i.y)
                        start = start + self.yWidth
            previousPoint = point

if __name__ == "__main__":
    def checkGrid(grid,item):
        found = False
        cells = []
        for i in (5,15,25):
            for j in (5,15,25):
                list = grid.getItems(i,j)
                try:
                    list.index(item)
                    #print "%r found in cell at %d, %d" % (item,i/10,j/10)
                    found = True
                    cells.append((i/10,j/10))
                except ValueError:
                    pass
        if found == False:
            #print "(%d, %s) not found in grid" % item
            pass

        return cells

    def checkResults(real,theory):
        if len(theory) != len(real):
            return "Fail - returned %d cells, expected %d" % (len(real), len(theory))

        for i in theory:
            try:
                real.index(i)
            except ValueError:
                return "Fail - segment not in (%d, %d)" % i
        #print "Pass"
        return True


    grid = CollisionGrid(10,10,30,30)
    #create some silly objects to use (useful when debugging)
    a = (1,"Apple")
    b = (2,"Bananna")
    c = (3,"Cookie")
    d = (4,"Dog")
    e = (5,"Elephant")
    f = (6,"Fortune")
    g = (7,"Grapes")
    h = (8,"Hi")
    i = (9,"Inigo")


    #inverse objects
    a1 = (-1,"Apple")
    b1 = (-2,"Bananna")
    c1 = (-3,"Cookie")
    d1 = (-4,"Dog")
    e1 = (-5,"Elephant")
    f1 = (-6,"Fortune")
    g1 = (-7,"Grapes")
    h1 = (-8,"Hi")
    i1 = (-9,"Inigo")
    #test diagonal line that intersects a cell but has no end points inside it
    grid.addPoly(a,[(12,5),(5,12)])
    print "Test 1: %s" % checkResults(checkGrid(grid, a), [(0, 0), (0, 1), (1, 0)])

    grid.addPoly(a1,[(5,12),(12,5)])
    print "Test 2: %s" % checkResults(checkGrid(grid, a1), [(0, 0), (0, 1), (1, 0)])

    #test item removal
    grid.removeItem(a1)
    print "Test 3: %s" % checkResults(checkGrid(grid, a1), [])

    #test diagonal line that intersects a cell but has no end points inside it(reverse direction)
    grid.addPoly(b,[(18,5), (25,12)])
    print "Test 4: %s" % checkResults(checkGrid(grid, b), [(1,0), (2,0), (2,1)])

    #test vertical line
    grid.addPoly(b1,[(25,12), (18,5)])
    print "Test 5: %s" % checkResults(checkGrid(grid, b1), [(1,0), (2,0), (2,1)])

    grid.addPoly(c, [(5,5), (5,25)])
    print "Test 6: %s" % checkResults(checkGrid(grid, c), [(0,0), (0,1), (0,2)])

    grid.addPoly(c1, [(5,25), (5,5)])
    print "Test 7: %s" % checkResults(checkGrid(grid, c1), [(0,0), (0,1), (0,2)])
    #test horizontal line
    grid.addPoly(d, [(5,15), (25,15)])
    print "Test 8: %s" % checkResults(checkGrid(grid, d), [(0,1), (1,1), (2,1)])

    grid.addPoly(d1, [(25,15), (5,15)])
    print "Test 9: %s" % checkResults(checkGrid(grid, d1), [(0,1), (1,1), (2,1)])
    #test diagonally through grid intersections
    grid.addPoly(e, [(5,5), (25,25)])
    print "Test 10: %s" % checkResults(checkGrid(grid, e), [(0,0),(0,1),(1,0),(1,1),(1,2), (2,1),(2,2)])

    grid.addPoly(e1, [(25,25), (5,5)])
    print "Test 11: %s" % checkResults(checkGrid(grid, e1), [(0,0),(0,1),(1,0),(1,1),(1,2), (2,1),(2,2)])

    #Same as the above test, only going diagonally the other direction
    #Causes the grid to only put the item in the upper half (may need to think about if this an actual fail)
    grid.addPoly(f, [(25,5), (5,25)])
    print "Test 12: %s" % checkResults(checkGrid(grid, f), [(0, 2), (1, 1), (2, 0), (0, 1), (2, 1), (1, 0), (2, 1)])

    grid.addPoly(f1, [(5,25), (25,5)])
    print "Test 13: %s" % checkResults(checkGrid(grid, f1), [(0, 2), (1, 1), (2, 0), (0, 1), (2, 1), (1, 0), (2, 1)])

    grid.addPoly(g, [(1,1), (9,9)])
    print "Test 14: %s" % checkResults(checkGrid(grid, g), [(0, 0)])

    grid.addPoly(g1, [(9,9), (1,1)])
    print "Test 15: %s" % checkResults(checkGrid(grid, g1), [(0, 0)])

    #check horizontal and vertical grid lines and lines that end on intersections
    grid.addPoly(h, [(10,10), (20,10)])
    print "Test 16: %s" % checkResults(checkGrid(grid, h), [(0,1),(1, 1),(2,1)])

    grid.addPoly(i, [(10,10), (10,20)])
    print "Test 17: %s" % checkResults(checkGrid(grid, i), [(1, 1),(1,0),(1,2)])
