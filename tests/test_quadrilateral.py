# -*- coding: utf-8 -*-

import unittest
from crossproduct import Point2D, Point3D, Vector2D, Vector3D, \
    Quadrilateral2D, Quadrilateral3D

class Test_Quadrilateral2D(unittest.TestCase):
    """
    P0=Point2D(0,0)
    P1=Point2D(1,0)
    P2=Point2D(1,1)
    P3=Point2D(0,0.5)
    """       
    
    def test___init__(self):
        ""
        q=Quadrilateral2D(P0,P1,P2,P3)
        self.assertIsInstance(q,Quadrilateral2D)
        self.assertEqual(q.P0,P0)
        self.assertEqual(q.P1,P1)
        self.assertEqual(q.P2,P2)
        self.assertEqual(q.P3,P3)
    
        
    def test___repr__(self):
        ""
        q=Quadrilateral2D(P0,P1,P2,P3)
        self.assertEqual(str(q),
                         'Quadrilateral2D(Point2D(0,0), Point2D(1,0), Point2D(1,1), Point2D(0,0.5))')
        
        
    def test_orientation(self):
        ""
        q=Quadrilateral2D(P0,P1,P2,P3) #ccw
        self.assertTrue(q.orientation>0)
    
        q=Quadrilateral2D(P0,P3,P2,P1) #cw
        self.assertTrue(q.orientation<0)
        
        
    def test_points(self):
        ""
        q=Quadrilateral2D(P0,P1,P2,P3)
        self.assertEqual(q.points,
                         (P0,P1,P2,P3))
        
        
    def test_signed_area(self):
        ""
        q=Quadrilateral2D(P0,P1,P2,P3) #ccw
        self.assertEqual(q.signed_area,0.75)
        
        q=Quadrilateral2D(P0,P3,P2,P1) #cw
        self.assertEqual(q.signed_area,-0.75)
    
    
    
class Test_Quadrilateral3D(unittest.TestCase):
    """
    P0=Point2D(0,0,0)
    P1=Point2D(1,0,0)
    P2=Point2D(1,1,0)
    P3=Point2D(0,0.5,0)
    """
    
    def test___init__(self):
        ""
        q=Quadrilateral3D(P0,P1,P2,P3)
        self.assertIsInstance(q,Quadrilateral3D)
        self.assertEqual(q.P0,P0)
        self.assertEqual(q.P1,P1)
        self.assertEqual(q.P2,P2)
        self.assertEqual(q.P3,P3)
        
    
    def test___repr__(self):
        ""
        q=Quadrilateral3D(P0,P1,P2,P3)
        self.assertEqual(str(q),
                         'Quadrilateral3D(Point3D(0,0,0), Point3D(1,0,0), Point3D(1,1,0), Point3D(0,0.5,0))')
        
        
    def test_area(self):
        ""
        q=Quadrilateral3D(P0,P1,P2,P3) #ccw
        self.assertEqual(q.area,0.75)
        
        q=Quadrilateral3D(P0,P1,P2,P3) #cw
        self.assertEqual(q.area,0.75)
        
        
    def test_points(self):
        ""
        q=Quadrilateral3D(P0,P1,P2,P3)
        self.assertEqual(q.points,
                         (P0,P1,P2,P3))
    
    
if __name__=='__main__':
    
    P0=Point2D(0,0)
    P1=Point2D(1,0)
    P2=Point2D(1,1)
    P3=Point2D(0,0.5)
    unittest.main(Test_Quadrilateral2D())
    
    P0=Point3D(0,0,0)
    P1=Point3D(1,0,0)
    P2=Point3D(1,1,0)
    P3=Point3D(0,0.5,0)
    unittest.main(Test_Quadrilateral3D())
    
    