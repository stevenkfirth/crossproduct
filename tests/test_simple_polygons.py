# -*- coding: utf-8 -*-

import unittest
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d

from crossproduct import Point2D, Point3D, Segment2D, Segment3D, Points, Segments, \
    SimplePolyline2D, Triangle2D, Vector2D, Triangles, SimplePolygons, \
    SimpleConvexPolygon2D


plot=True
        
class Test_SimplePolygons(unittest.TestCase):
    """
    
    """
    
    def test___init__(self):
        ""
        sp=SimplePolygons(*simple_polygons)
        self.assertIsInstance(sp,SimplePolygons)
        self.assertEqual(sp.simple_polygons,
                         list(simple_polygons))
        
        
    def test___eq__(self):
        ""
        sp=SimplePolygons(*simple_polygons)
        self.assertTrue(sp==sp)
        
        sp1=SimplePolygons(simple_polygons[0])
        self.assertFalse(sp==sp1)
        
        
    def test___repr__(self):
        ""
        sp=SimplePolygons(*simple_polygons)
        self.assertEqual(str(sp),
                         'SimplePolygons(SimpleConvexPolygon2D(Point2D(0.0,0.0),Point2D(1.0,0.0),Point2D(0.0,1.0)), SimpleConvexPolygon2D(Point2D(1.0,0.0),Point2D(1.0,1.0),Point2D(0.0,1.0)))')
        
    
    def test_segments(self):
        ""
        sp=SimplePolygons(*simple_polygons)
        self.assertEqual(sp.segments,
                         Segments(Segment2D(Point2D(0.0,0.0), Point2D(1.0,0.0)), 
                                  Segment2D(Point2D(1.0,0.0), Point2D(0.0,1.0)), 
                                  Segment2D(Point2D(0.0,1.0), Point2D(0.0,0.0)), 
                                  Segment2D(Point2D(1.0,0.0), Point2D(1.0,1.0)), 
                                  Segment2D(Point2D(1.0,1.0), Point2D(0.0,1.0))))
    
    
    def test_union(self):
        ""
        
    
    
if __name__=='__main__':
    
    simple_polygons=(SimpleConvexPolygon2D(Point2D(0.0,0.0),
                                           Point2D(1.0,0.0),
                                           Point2D(0.0,1.0)), 
                     SimpleConvexPolygon2D(Point2D(1.0,0.0),
                                           Point2D(1.0,1.0),
                                           Point2D(0.0,1.0)))
    unittest.main(Test_SimplePolygons())
    
    