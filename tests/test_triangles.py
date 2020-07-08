# -*- coding: utf-8 -*-

import unittest
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d
from pprint import pprint

from crossproduct import Point2D, Point3D, Segment2D, Segment3D, Points, Segments, \
    SimplePolyline2D, Triangle2D, Vector2D, Triangles, SimplePolygons, \
    SimpleConvexPolygon2D


plot=True
        
class Test_Triangles(unittest.TestCase):
    """
    
    """
    
    def test___init__(self):
        ""
        t=Triangles(*triangles)
        self.assertIsInstance(t,Triangles)
        self.assertEqual(t.triangles,
                         list(triangles))
        
        
        
        
    def test___eq__(self):
        ""
        t=Triangles(*triangles)
        self.assertTrue(t==t)
        
        t1=Triangles(triangles[0])
        self.assertFalse(t==t1)
        
        
    def test___repr__(self):
        ""
        t=Triangles(*triangles)
        self.assertEqual(str(t),
                         'Triangles(Triangle2D(Point2D(0,0), Vector2D(1,0), Vector2D(0,1)), Triangle2D(Point2D(1,1), Vector2D(-1,0), Vector2D(0,-1)))')
        
        
    def test_intersect_simple_convex_polygon(self):
        ""
        t=Triangles(Triangle2D(Point2D(2,0), Vector2D(0,1), Vector2D(-2,0)), 
                    Triangle2D(Point2D(2,1), Vector2D(-1,0), Vector2D(-2,-1)), 
                    Triangle2D(Point2D(0,0), Vector2D(1,1), Vector2D(0,3)), 
                    Triangle2D(Point2D(1,1), Vector2D(0,1), Vector2D(-1,2)), 
                    Triangle2D(Point2D(1,2), Vector2D(1,0), Vector2D(-1,1)), 
                    Triangle2D(Point2D(2,2), Vector2D(0,1), Vector2D(-2,1)))
        fig, ax = plt.subplots()
        t.plot(ax)
        scp=SimpleConvexPolygon2D(Point2D(1,0),Point2D(2,0),Point2D(2,3),Point2D(1,3))
        scp.plot(ax)
        
        self.assertEqual(t.intersect_simple_convex_polygon(scp),
                         (Points(Point2D(1.0,1.0)),
                          Segments(Segment2D(Point2D(1.0,2.0), 
                                             Point2D(1.0,1.0))),
                          SimplePolygons(SimpleConvexPolygon2D(Point2D(1.0,0.5),
                                                               Point2D(1.0,0.0),
                                                               Point2D(2.0,0.0),
                                                               Point2D(2.0,1.0)), 
                                         SimpleConvexPolygon2D(Point2D(2.0,1.0),
                                                               Point2D(1.0,1.0),
                                                               Point2D(1.0,0.5)), 
                                         SimpleConvexPolygon2D(Point2D(1.0,2.5),
                                                               Point2D(1.0,2.0),
                                                               Point2D(2.0,2.0)), 
                                         SimpleConvexPolygon2D(Point2D(2.0,2.0),
                                                               Point2D(2.0,3.0),
                                                               Point2D(1,3),
                                                               Point2D(1.0,2.5)))))
        
        
        
    def test_intersect_triangle(self):
        ""
        t=Triangles(*triangles)
        
        # self intersection with first triangle
        self.assertEqual(t.intersect_triangle(triangles[0]),
                         (Points(), 
                          Segments(), 
                          SimplePolygons(SimpleConvexPolygon2D(Point2D(0.0,0.0),
                                                               Point2D(1.0,0.0),
                                                               Point2D(0.0,1.0)))))
        
        # self intersection with second triangle
        self.assertEqual(t.intersect_triangle(triangles[1]),
                         (Points(), 
                          Segments(), 
                          SimplePolygons(SimpleConvexPolygon2D(Point2D(1.0,1.0),
                                                               Point2D(0.0,1.0),
                                                               Point2D(1.0,0.0)))))
    
        # intersection across the two triangles
        tr1=Triangle2D(Point2D(0,0),
                       Vector2D(1,0),
                       Vector2D(1,1))
        self.assertEqual(t.intersect_triangle(tr1),
                         (Points(), 
                          Segments(), 
                          SimplePolygons(SimpleConvexPolygon2D(Point2D(0.5,0.5),
                                                               Point2D(0.0,0.0),
                                                               Point2D(1.0,0.0)), 
                                         SimpleConvexPolygon2D(Point2D(1.0,0.0),
                                                               Point2D(1.0,1.0),
                                                               Point2D(0.5,0.5)))))
    
    def test_intersect_triangles(self):
        ""
        t=Triangles(*triangles)
        
        # self intersection
        self.assertEqual(t.intersect_triangles(t),
                         (Points(), 
                          Segments(), 
                          SimplePolygons(SimpleConvexPolygon2D(Point2D(0.0,0.0),
                                                               Point2D(1.0,0.0),
                                                               Point2D(0.0,1.0)), 
                                         SimpleConvexPolygon2D(Point2D(1.0,1.0),
                                                               Point2D(0.0,1.0),
                                                               Point2D(1.0,0.0)))))
        
        # intersection
        triangles1=(Triangle2D(Point2D(1,0),Vector2D(-1,0),Vector2D(0,1)),
                    Triangle2D(Point2D(0,1),Vector2D(1,0),Vector2D(0,-1)))
        t1=Triangles(*triangles1)
        self.assertEqual(t.intersect_triangles(t1),
                         (Points(), 
                          Segments(), 
                          SimplePolygons(SimpleConvexPolygon2D(Point2D(0.5,0.5),
                                                               Point2D(0.0,0.0),
                                                               Point2D(1.0,0.0)), 
                                         SimpleConvexPolygon2D(Point2D(1.0,0.0),
                                                               Point2D(1.0,1.0),
                                                               Point2D(0.5,0.5)), 
                                         SimpleConvexPolygon2D(Point2D(0.0,1.0),
                                                               Point2D(0.0,0.0),
                                                               Point2D(0.5,0.5)), 
                                         SimpleConvexPolygon2D(Point2D(0.5,0.5),
                                                               Point2D(1.0,1.0),
                                                               Point2D(0.0,1.0)))))
            
    
if __name__=='__main__':
    
    triangles=(Triangle2D(Point2D(0,0),Vector2D(1,0),Vector2D(0,1)),
               Triangle2D(Point2D(1,1),Vector2D(-1,0),Vector2D(0,-1)))
    unittest.main(Test_Triangles())
    
    