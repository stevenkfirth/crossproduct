# -*- coding: utf-8 -*-

import unittest
from crossproduct import Point2D, Point3D,Vector2D, Vector3D, \
    HalfLine2D, HalfLine3D, Line2D, Line3D, Segment2D, Segment3D, \
    Polyline2D, Polyline3D



class Test_Polyline2D(unittest.TestCase):
    """
    points(Point2D(0,0),
            Point2D(0,1),
            Point2D(1,1))
    """

    def test___init__(self):
        ""
        pl=Polyline2D(*points)
        self.assertIsInstance(pl,Polyline2D)
        self.assertEqual(pl.points,points)
        
        
    def test___eq__(self):
        ""
        pl=Polyline2D(*points)
        
        self.assertTrue(pl==pl)
        self.assertTrue(pl==Polyline2D(Point2D(1,1),
                                       Point2D(0,1),
                                       Point2D(0,0)))
        
          
    def test___repr__(self):
        ""
        pl=Polyline2D(*points)
        self.assertEqual(str(pl),'Polyline2D(Point2D(0,0),Point2D(0,1),Point2D(1,1))')
    

    def test_reverse(self):
        ""
        pl=Polyline2D(*points)
        
        self.assertEqual(pl.reverse,
                         Polyline2D(Point2D(1,1),
                                    Point2D(0,1),
                                    Point2D(0,0)))
    
    
    def test_segments(self):
        ""
        pl=Polyline2D(*points)
        self.assertEqual(pl.segments,
                         (Segment2D(Point2D(0,0),
                                    Point2D(0,1)),
                          Segment2D(Point2D(0,1),
                                    Point2D(1,1))))
    
    
    
        
class Test_Polyline3D(unittest.TestCase):
    """
    points=(Point2D(0,0,0),
            Point2D(0,1,0),
            Point2D(1,1,0))
    """

    def test___init__(self):
        ""
        pl=Polyline3D(*points)
        self.assertIsInstance(pl,Polyline3D)
        self.assertEqual(pl.points,points)
    
    
    def test___eq__(self):
        ""
        pl=Polyline3D(*points)
        
        self.assertTrue(pl==pl)
        self.assertTrue(pl==Polyline3D(Point3D(1,1,0),
                                       Point3D(0,1,0),
                                       Point3D(0,0,0)))
    
        
    def test___repr__(self):
        ""
        pl=Polyline3D(*points)
        self.assertEqual(str(pl),'Polyline3D(Point3D(0,0,0),Point3D(0,1,0),Point3D(1,1,0))')
        
        
    def test_reverse(self):
        ""
        pl=Polyline3D(*points)
        
        self.assertEqual(pl.reverse,
                         Polyline3D(Point3D(1,1,0),
                                    Point3D(0,1,0),
                                    Point3D(0,0,0)))
        
        
    def test_segments(self):
        ""
        pl=Polyline3D(*points)
        self.assertEqual(pl.segments,
                         (Segment3D(Point3D(0,0,0),
                                    Point3D(0,1,0)),
                          Segment3D(Point3D(0,1,0),
                                    Point3D(1,1,0))))
        
        
    
if __name__=='__main__':
    
    points=(Point2D(0,0),
            Point2D(0,1),
            Point2D(1,1))
    unittest.main(Test_Polyline2D())
    
    points=(Point3D(0,0,0),
            Point3D(0,1,0),
            Point3D(1,1,0))
    unittest.main(Test_Polyline3D())