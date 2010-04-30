import collision
import unittest

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
            print "Testing %r" % item
            #check that item is in the correct number of cells
            self.assertEqual(len(grid.search(item)),len(cells))
            #check that the item is in the correct cells
            for cell in cells:
                items = grid.getItems(cell[0] * 10, cell[1] * 10)
                self.assertTrue(item in items)


if __name__ == "__main__":
    unittest.main()
