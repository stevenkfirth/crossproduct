# -*- coding: utf-8 -*-

import unittest
from crossproduct import Point2D, Point3D, \
    Vector2D, Vector3D, Line2D, Polygon2D, Polygon3D, Plane3D, Triangle2D, Triangle3D, \
    Segment2D, Segment3D, Polyhedron3D


    
        
class Test_Polyhedron3D(unittest.TestCase):
    """
    
    """
    
    def test___init__(self):
        ""
        pg=Polygon3D(*points)
        self.assertIsInstance(pg,Polygon3D)
        self.assertEqual(pg.points,points)
        
        
    def test___contains__(self):
        ""
        
        
    def test___eq__(self):
        ""
        
        
        
    def test___repr__(self):
        ""
        
        
    
if __name__=='__main__':
    
        
    unittest.main(Test_Polyhedron3D())
    
    