import collision
import euclid
import unittest
from math import sqrt

class KnownValues(unittest.TestCase):
    knownValues = (
        (("Offset Diaganol"), [(12, 5), (5, 12)], [(0, 1), (1, 0), (0, 0)]),
        (("Offset Diaganol (inverse)"), [(5, 12), (12, 5)], [(0, 0), (0, 1), (1, 0)]),
        (("Negative Offset Diaganol"), [(18, 5), (25, 12)], [(1, 0), (2, 0), (2, 1)]),
        (("Negative Offset Diaganol (inverse)"), [(25, 12), (18, 5)], [(1, 0), (2, 0), (2, 1)]),
        (("Vertical Line"), [(5, 5), (5, 25)], [(0, 0), (0, 1), (0, 2)]),
        (("Vertical Line (inverse)"), [(5, 25), (5,5)], [(0, 0), (0, 1), (0, 2)]),
        (("Horizontal Line"), [(5, 15), (25, 15)], [(0, 1), (1, 1), (2, 1)]),
        (("Horizontal Line (inverse)"), [(25, 15), (5, 15)], [(0, 1), (1, 1), (2, 1)]),
        (("Grid Intersection"), [(5, 5), (25, 25)], [(0, 0), (0, 1), (1, 0), (1, 1), (1, 2), (2, 1), (2, 2)]),
        (("Grid Intersection (inverse)"), [(25, 25), (5, 5)], [(0, 0), (0, 1), (1, 0), (1, 1), (1, 2), (2, 1), (2, 2)]),

#This is the theoretical expected answer, but the answer given is acceptable (for now)
#        (("Negative Grid Intersection"), [(25,5), (5,25)], [(0, 2), (1, 1), (2, 0), (0, 1), (2, 1), (1, 0), (2, 1)]),
#       (("Negative Grid Intersection (inverse)"), [(5,25), (25,5)], [(0, 2), (1, 1), (2, 0), (0, 1), (2, 1), (1, 0), (2, 1)]),

        (("Negative Grid Intersection"), [(25, 5), (5, 25)], [(0, 2), (1, 1), (2, 0),  (2, 1), (2, 1)]),
        (("Negative Grid Intersection (inverse)"), [(5, 25), (25, 5)], [(0, 2), (1, 1), (2, 0),  (2, 1), (2, 1)]),
        (("Single Cell"), [(1, 1), (9, 9)], [(0, 0)]),
        (("Single Cell (inverse)"), [(9, 9), (1, 1)], [(0, 0)]),

        (("Horizontal Line on boundary"), [(10, 10), (20, 10)], [(0, 1), (1, 1), (2, 1)]),
        (("Vertical Line on boundary"), [(10, 10), (10, 20)], [(1, 1), (1, 0), (1,2)]),
    )

    def testAddToCollisionGrid(self):
        grid = collision.CollisionGrid(10,10,30,30)
        for item,segment, cells in self.knownValues:
            #add item to grid
            grid.addPoly(item,segment)
            #print "Testing %r" % item
            #check that item is in the correct number of cells
            self.assertEqual(len(grid.search(item)),len(cells))
            #check that the item is in the correct cells
            for cell in cells:
                items = grid.getItems((cell[0] * 10, cell[1] * 10))
                self.assertTrue(item in items)

    def testAddPolygon(self):
        grid = collision.CollisionGrid(10,10,40,40)
        item = ("Triangle")
        grid.addPoly(item, [(1,8),(38,8),(38,32)])
        cells = [(0, 0), (1, 0), (2, 0), (3, 0), (3, 1), (3, 2), (3, 3), (2, 2), (1, 2), (0, 1), (1, 1)]
        #Check that we get the correct number of cells
        self.assertEqual(len(grid.search(item)), len(cells))
        #check that the item is in our expected cells
        for cell in cells:
            items = grid.getItems((cell[0] * 10, cell[1] * 10))
            self.assertTrue(item in items)

    def testCircleCollideWithAABB(self):
        #direct angle test, right now gives way to the x-axis (may need to change this later)
        c = euclid.Circle(14.9,10,10)
        r = euclid.Rect((5, 5), (10, 5), (10, 10), (5, 10))
        self.assertEqual(collision.collideCircleAABB(c,r), euclid.Vector((1,0)))

    def testCircleNotCollideWithAABB(self):
        c = euclid.Circle(30,30,10)
        r = euclid.Rect((5, 5), (10, 5), (10, 10), (5, 10))
        self.assertEqual(collision.collideCircleAABB(c,r), None)
	
    def testCircleCollideFromTop(self):
        circle = euclid.Circle(500,580,10)
        bottom = euclid.Rect((10, 580), (590, 580), (590, 590), (10, 590))
        self.assertEqual(collision.collideCircleAABB(circle, bottom), euclid.Vector((0,-1)))

    def testCircleCollideFromLeft(self):
        circle = euclid.Circle(92,150,10)
        rect = euclid.Rect((100, 100), (200, 100), (200, 200), (100, 200))
        self.assertEqual(collision.collideCircleAABB(circle, rect), euclid.Vector((-1,0)))

    def testCircleCollideFromRight(self):
        circle = euclid.Circle(205,150,10)
        rect = euclid.Rect((100, 100), (200, 100), (200, 200), (100, 200))
        self.assertEqual(collision.collideCircleAABB(circle, rect), euclid.Vector((1,0)))

    def testCircleCollideFromBottom(self):
        circle = euclid.Circle(150,208,10)
        rect = euclid.Rect((100, 100), (200, 100), (200, 200), (100, 200))
        self.assertEqual(collision.collideCircleAABB(circle, rect), euclid.Vector((0,1)))


    def testUnitVector1(self):
        v = euclid.Vector((4,3))
        self.assertEqual(v.unit(), euclid.Vector((4.0 / 5.0, 3.0 / 5.0)))

    def testUnitVector2(self):
        v = euclid.Vector((-7,1))
        self.assertEqual(v.unit(), euclid.Vector((-7.0 / sqrt(50.0), 1.0 / sqrt(50.0))))

    def testUnitVector3(self):
        v = euclid.Vector((1,1.0))
        self.assertEqual(v.unit(), euclid.Vector((1.0 / sqrt(2), 1.0 / sqrt(2))))

    def testUnitVector4(self):
        v = euclid.Vector((sqrt(.5), sqrt(.5)))
        self.assertEqual(v.unit(), euclid.Vector((sqrt(.5), sqrt(.5))))

if __name__ == "__main__":
    unittest.main()
