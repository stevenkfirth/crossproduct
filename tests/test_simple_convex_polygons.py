# -*- coding: utf-8 -*-

import unittest
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d

from crossproduct import Point2D, Point3D, Segment2D, Segment3D, Points, Segments, \
    SimplePolyline2D, Triangle2D, Vector2D, Triangles, SimpleConvexPolygons, \
    SimpleConvexPolygon2D


plot=True
        
class Test_SimpleConvexPolygons(unittest.TestCase):
    """
    
    """
    
    def test___init__(self):
        ""
        sp=SimpleConvexPolygons(*simple_convex_polygons)
        self.assertIsInstance(sp,SimpleConvexPolygons)
        self.assertEqual(sp.simple_convex_polygons,
                         list(simple_convex_polygons))
        
        
    def test___eq__(self):
        ""
        sp=SimpleConvexPolygons(*simple_convex_polygons)
        self.assertTrue(sp==sp)
        
        sp1=SimpleConvexPolygons(simple_convex_polygons[0])
        self.assertFalse(sp==sp1)
        
        
    def test___repr__(self):
        ""
        sp=SimpleConvexPolygons(*simple_convex_polygons)
        self.assertEqual(str(sp),
                         'SimpleConvexPolygons(SimpleConvexPolygon2D(Point2D(0.0,0.0),Point2D(1.0,0.0),Point2D(0.0,1.0)), SimpleConvexPolygon2D(Point2D(1.0,0.0),Point2D(1.0,1.0),Point2D(0.0,1.0)))')
        
    
    
    
    
if __name__=='__main__':
    
    simple_convex_polygons=(SimpleConvexPolygon2D(Point2D(0.0,0.0),
                                           Point2D(1.0,0.0),
                                           Point2D(0.0,1.0)), 
                     SimpleConvexPolygon2D(Point2D(1.0,0.0),
                                           Point2D(1.0,1.0),
                                           Point2D(0.0,1.0)))
    unittest.main(Test_SimpleConvexPolygons())
    
    