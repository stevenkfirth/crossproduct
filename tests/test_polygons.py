# -*- coding: utf-8 -*-

import unittest
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d

from crossproduct import Point2D, Point3D, Segment2D, Segment3D, Points, Segments, \
    SimplePolyline2D, Triangle2D, Vector2D, Triangles, Polygons, \
    SimpleConvexPolygon2D, Polygon2D


plot=True
        
class Test_Polygons(unittest.TestCase):
    """
    
    """
    
    def test___init__(self):
        ""
        sp=Polygons(*simple_polygons)
        self.assertIsInstance(sp,Polygons)
        self.assertEqual(sp.simple_polygons,
                         list(simple_polygons))
        
        
    def test___eq__(self):
        ""
        sp=Polygons(*simple_polygons)
        self.assertTrue(sp==sp)
        
        sp1=Polygons(simple_polygons[0])
        self.assertFalse(sp==sp1)
        
        
    def test___repr__(self):
        ""
        sp=Polygons(*simple_polygons)
        self.assertEqual(str(sp),
                         'Polygons(SimpleConvexPolygon2D(Point2D(0.0,0.0),Point2D(1.0,0.0),Point2D(0.0,1.0)), SimpleConvexPolygon2D(Point2D(1.0,0.0),Point2D(1.0,1.0),Point2D(0.0,1.0)))')
        
    
    def test_segments(self):
        ""
        sp=Polygons(*simple_polygons)
        self.assertEqual(sp.segments,
                         Segments(Segment2D(Point2D(0.0,0.0), Point2D(1.0,0.0)), 
                                  Segment2D(Point2D(1.0,0.0), Point2D(0.0,1.0)), 
                                  Segment2D(Point2D(0.0,1.0), Point2D(0.0,0.0)), 
                                  Segment2D(Point2D(1.0,0.0), Point2D(1.0,1.0)), 
                                  Segment2D(Point2D(1.0,1.0), Point2D(0.0,1.0))))
    
    
    def test_union_adjacent(self):
        ""
        sp=Polygons(*simple_polygons)
        self.assertEqual(sp.union_adjacent,
                         Polygons(Polygon2D(Point2D(0.0,1.0),
                                                        Point2D(0.0,0.0),
                                                        Point2D(1.0,0.0),
                                                        Point2D(1.0,1.0))))
    
        sp=Polygons(SimpleConvexPolygon2D(Point2D(1.0,0.5),Point2D(1.0,0.0),Point2D(2.0,0.0),Point2D(2.0,1.0)), 
                          SimpleConvexPolygon2D(Point2D(2.0,1.0),Point2D(1.0,1.0),Point2D(1.0,0.5)), 
                          SimpleConvexPolygon2D(Point2D(1.0,2.5),Point2D(1.0,2.0),Point2D(2.0,2.0)), 
                          SimpleConvexPolygon2D(Point2D(2.0,2.0),Point2D(2.0,3.0),Point2D(1,3),Point2D(1.0,2.5)))
        
        self.assertEqual(sp.union_adjacent,
                         Polygons(Polygon2D(Point2D(1.0,0.0),
                                                        Point2D(2.0,0.0),
                                                        Point2D(2.0,1.0),
                                                        Point2D(1.0,1.0)), 
                                        Polygon2D(Point2D(1.0,2.0),
                                                        Point2D(2.0,2.0),
                                                        Point2D(2.0,3.0),
                                                        Point2D(1,3))))
        #sp.plot()
        #sp.union_adjacent.plot()
    
    
if __name__=='__main__':
    
    simple_polygons=(SimpleConvexPolygon2D(Point2D(0.0,0.0),
                                           Point2D(1.0,0.0),
                                           Point2D(0.0,1.0)), 
                     SimpleConvexPolygon2D(Point2D(1.0,0.0),
                                           Point2D(1.0,1.0),
                                           Point2D(0.0,1.0)))
    unittest.main(Test_Polygons())
    
    