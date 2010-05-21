import euclid
import unittest

class euclidTests(unittest.TestCase):
    def testNormalReflect1(self):
        nV = euclid.Vector((0,1))
        vector = euclid.Vector((-1, -1))
        self.assertEqual(vector.reflectNormal(nV), euclid.Vector((1,-1)))

    def testNormalReflect2(self):
        nV = euclid.Vector((1,0))
        vector = euclid.Vector((-1, -1))
        self.assertEqual(vector.reflectNormal(nV), euclid.Vector((-1,1)))

    def testNormalReflect3(self):
        nV = euclid.Vector((-1,0))
        vector = euclid.Vector((1, 1))
        self.assertEqual(vector.reflectNormal(nV), euclid.Vector((1,-1)))

    def testNormalReflectr4(self):
        nV = euclid.Vector((0,-1))
        vector = euclid.Vector((1, 1))
        self.assertEqual(vector.reflectNormal(nV), euclid.Vector((-1,1)))
if __name__ == "__main__":
    unittest.main()
