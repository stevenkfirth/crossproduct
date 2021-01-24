# -*- coding: utf-8 -*-

import unittest
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d
import cProfile
from pprint import pprint

from crossproduct import Point, Vector, Line, Halfline, Segment, Polyline, Plane, 
from crossproduct import Polygon, Polygons


plot=False # Set to true to see the test plots



class Test_Polygon(unittest.TestCase):
    """
    points2d=(Point(0,0),Point(1,0),Point(1,1),Point(0,1))
    points3d=(Point(0,0,0),Point(1,0,0),Point(1,1,0),Point(0,1,0))
    
    """

    def test___init__(self):
        ""
        pg=Polygon(*points2d)
        self.assertIsInstance(pg,Polygon)
        self.assertEqual(pg.points,Points(*points))


class Test_Polygon_old(unittest.TestCase):
    """
    points2d=(Point2D(0,0),Point2D(1,0),Point2D(1,1),Point2D(0,1))
    """

    def test___init__(self):
        ""
        pg=Polygon2D(*points2d)
        self.assertIsInstance(pg,Polygon2D)
        self.assertEqual(pg.points,Points(*points2d))
        
        
    def test___add__(self):
        ""
        pg=Polygon2D(*points2d)
        
        # # no intersection
        # pg1=Polygon2D(Point2D(-2,0),
        #               Point2D(-1,0),
        #               Point2D(-1,1),
        #               Point2D(-2,1))
        # self.assertEqual(pg+pg1,
        #                  None)
        
        # # point intersection
        # pg1=Polygon2D(Point2D(-1,-1),
        #               Point2D(0,-1),
        #               Point2D(0,0),
        #               Point2D(-1,0))
        # self.assertEqual(pg+pg1,
        #                  None)
        
        # edge intersection
        pg1=Polygon2D(Point2D(-1,0),
                      Point2D(0,0),
                      Point2D(0,1),
                      Point2D(-1,1))
        self.assertEqual(pg+pg1,
                         Polygon2D(Point2D(-1,0),
                                   Point2D(1,0),
                                   Point2D(1,1),
                                   Point2D(-1,1)))
                        
        # parial edge intersection
        pg1=Polygon2D(Point2D(1,0.5),
                      Point2D(2,0.5),
                      Point2D(2,1.5),
                      Point2D(1,1.5))
        self.assertEqual(pg+pg1,
                         Polygon2D(Point2D(1,1),
                                   Point2D(0,1),
                                   Point2D(0,0),
                                   Point2D(1,0),
                                   Point2D(1.0,0.5),
                                   Point2D(2,0.5),
                                   Point2D(2,1.5),
                                   Point2D(1,1.5)))
    
        # rounding example
        pg1=Polygon2D(Point2D(1.0,0.0),
                      Point2D(2.0,0.0),
                      Point2D(2.0,1.0),
                      Point2D(1.7142857142857144,0.8571428571428572),
                      Point2D(1.6666666666666667,1.0),
                      Point2D(1.0,1.0))
        pg2=Polygon2D(Point2D(1.6666666666666665,1.0),
                      Point2D(1.7142857142857144,0.8571428571428572),
                      Point2D(2.0,1.0))
    
        self.assertEqual(pg1+pg2,
                         Polygon2D(Point2D(1.0,1.0),
                                   Point2D(1.0,0.0),
                                   Point2D(2.0,0.0),
                                   Point2D(2.0,1.0)))
    
    def test___eq__(self):
        ""
        pg=Polygon2D(*points2d)
        self.assertTrue(pg==pg)
        
        pg2=Polygon2D(Point2D(0,0),Point2D(1,0),Point2D(0,1))
        self.assertFalse(pg==pg2)
        
        
    def test_add_segments(self):
        ""
        pg=Polygon2D(Point2D(0,0),
                     Point2D(0.5,0),
                     Point2D(1,0),
                     Point2D(1,1),
                     Point2D(0,1))
        self.assertEqual(pg.add_segments,
                         Polygon2D(Point2D(0,0),
                                   Point2D(1,0),
                                   Point2D(1,1),
                                   Point2D(0,1)))
        
        pg=Polygon2D(Point2D(0.5,0),
                     Point2D(1,0),
                     Point2D(1,1),
                     Point2D(0,1),
                     Point2D(0,0))
        self.assertEqual(pg.add_segments,
                         Polygon2D(Point2D(0,0),
                                   Point2D(1,0),
                                   Point2D(1,1),
                                   Point2D(0,1)))


    def test_known_convex(self):
        ""
        pg=Polygon2D(*points2d)
        self.assertFalse(pg.known_convex)
        
        
    def test_known_simple(self):
        ""
        pg=Polygon2D(*points2d)
        self.assertTrue(pg.known_simple)
        
        
    def test_intersect_polyline(self):
        ""
        
        # 2D SIMPLE CONVEX POLYGON
        
        pg=Polygon2D(*points2d, known_convex=True)
        
        # segment is a polygon edge
        self.assertEqual(pg.intersect_polyline(Polyline2D(Point2D(0,0),
                                                          Point2D(1,1))),
                        (Points(), 
                         Polylines(Polyline2D(Point2D(0.0,0.0), 
                                              Point2D(1.0,1.0)))))    
        
        # as above, with 2 segments
        self.assertEqual(pg.intersect_polyline(Polyline2D(Point2D(-0.5,-0.5),
                                                          Point2D(0.5,0.5),
                                                          Point2D(1.5,1.5))),
                        (Points(), 
                         Polylines(Polyline2D(Point2D(0.0,0.0), 
                                              Point2D(1.0,1.0)))))
        
        
        # example
        pg=Polygon3D(Point3D(0,0,3),Point3D(10,0,3),Point3D(10,10,3),Point3D(0,10,3)) 
        pl=Polyline3D(Point3D(0,0,0),Point3D(10,0,0),Point3D(10,10,0),Point3D(0,10,0))
        #print(pg.intersect_polyline(pl))
        #print(pl1.intersect_polyline(pl))
        
        # example
        pg=Polygon3D(Point3D(0,0,0),Point3D(10,0,0),Point3D(10,0,3),Point3D(0,0,3)) 
        pg1=Polygon3D(Point3D(0,0,0),Point3D(10,0,0),Point3D(10,10,0),Point3D(0,10,0))
        #print(pg.intersect_polyline(pg1.polyline))
        
        
        # 3D SIMPLE CONVEX POLYGON
        
        pg=Polygon3D(*points3d, known_convex=True)
        
        # polyline is skew and intersects at two points
        self.assertEqual(pg.intersect_polyline(Polyline3D(Point3D(0,0,1),
                                                          Point3D(0,0,-1),
                                                          Point3D(0.5,0.5,-1),
                                                          Point3D(0.5,0.5,1))),
                         (Points(Point3D(0.0,0.0,0.0), 
                                 Point3D(0.5,0.5,0.0)), 
                          Polylines()))
        
        
    def test__intersect_polygon_simple_convex_and_simple_convex(self):
        ""
        
        # TWO SIMPLE CONVEX POLYGONS
        
        # full overlap intersection
        pg1=Polygon2D(Point2D(0,0),Point2D(1,0),Point2D(1,1),Point2D(0,1),
                      known_convex=True)
        self.assertEqual(pg1._intersect_polygon_simple_convex_and_simple_convex(pg1),
                          (Points(),Polylines(),Polygons(pg1)))
        
        # half overlap
        pg2=Polygon2D(Point2D(0.5,0),Point2D(1.5,0),Point2D(1.5,1),Point2D(0.5,1),
                      known_convex=True)
        self.assertEqual(pg1._intersect_polygon_simple_convex_and_simple_convex(pg2),
                          (Points(), 
                           Polylines(), 
                           Polygons(Polygon2D(Point2D(1.0,1.0),
                                              Point2D(0.5,1),
                                              Point2D(0.5,0.0),
                                              Point2D(1.0,0.0)))))
        
        # corner overlap
        pg2=Polygon2D(Point2D(0.5,-0.5),Point2D(1.5,-0.5),Point2D(1.5,0.5),Point2D(0.5,0.5),
                      known_convex=True)
        self.assertEqual(pg1._intersect_polygon_simple_convex_and_simple_convex(pg2),
                          (Points(), 
                           Polylines(), 
                           Polygons(Polygon2D(Point2D(1.0,0.5),
                                              Point2D(0.5,0.5),
                                              Point2D(0.5,0.0),
                                              Point2D(1.0,0.0)))))
        
        # no intersection
        pg2=Polygon2D(Point2D(2,0),Point2D(3,0),Point2D(3,1),Point2D(2,1),
                      known_convex=True)
        self.assertEqual(pg1._intersect_polygon_simple_convex_and_simple_convex(pg2),
                          (Points(), 
                           Polylines(), 
                           Polygons()))
        
        # point intersection
        pg2=Polygon2D(Point2D(1,1),Point2D(2,1),Point2D(2,2),Point2D(1,2),
                      known_convex=True)
        self.assertEqual(pg1._intersect_polygon_simple_convex_and_simple_convex(pg2),
                          (Points(Point2D(1,1)), 
                           Polylines(), 
                           Polygons()))
        
        # segment intersection
        pg2=Polygon2D(Point2D(1,0.5),Point2D(2,0.5),Point2D(2,1.5),Point2D(1,1.5),
                      known_convex=True)
        self.assertEqual(pg1._intersect_polygon_simple_convex_and_simple_convex(pg2),
                          (Points(), 
                           Polylines(Polyline2D(Point2D(1,0.5),Point2D(1,1))), 
                           Polygons()))
        
        
        # example
        pg=Polygon3D(Point3D(0,0,3),Point3D(10,0,3),Point3D(10,10,3),Point3D(0,10,3),known_convex=True) 
        pg1=Polygon3D(Point3D(0,0,0),Point3D(10,0,0),Point3D(10,10,0),Point3D(0,10,0),known_convex=True)
        #print(pg._intersect_polygon_simple_convex_and_simple_convex(pg1))
        
        # example
        pg=Polygon3D(Point3D(0,0,0),Point3D(10,0,0),Point3D(10,0,3),Point3D(0,0,3)) 
        pg1=Polygon3D(Point3D(0,0,0),Point3D(10,0,0),Point3D(10,10,0),Point3D(0,10,0))
        #print(pg._intersect_polygon_simple_convex_and_simple_convex(pg1))
        
        
    def test__intersect_polygon_simple_and_simple_convex(self):
        ""
        
        # full overlap intersection
        pg=Polygon2D(Point2D(0,0),Point2D(1,0),Point2D(1,1),Point2D(0,1))
        pg1=Polygon2D(Point2D(0,0),Point2D(1,0),Point2D(1,1),Point2D(0,1),
                      known_convex=True)
        
        self.assertEqual(pg._intersect_polygon_simple_and_simple_convex(pg1),
                         (Points(), 
                          Polylines(),
                          Polygons(pg)))
        
        # half overlap
        pg1=Polygon2D(Point2D(0.5,0),Point2D(1.5,0),Point2D(1.5,1),Point2D(0.5,1),
                      known_convex=True)
        self.assertEqual(pg._intersect_polygon_simple_and_simple_convex(pg1),
                          (Points(), 
                           Polylines(), 
                           Polygons(Polygon2D(Point2D(1.0,1.0),
                                              Point2D(0.5,1),
                                              Point2D(0.5,0.0),
                                              Point2D(1.0,0.0)))))
        
        # corner overlap
        pg1=Polygon2D(Point2D(0.5,-0.5),Point2D(1.5,-0.5),Point2D(1.5,0.5),Point2D(0.5,0.5),
                      known_convex=True)
        self.assertEqual(pg._intersect_polygon_simple_convex_and_simple_convex(pg1),
                          (Points(), 
                           Polylines(), 
                           Polygons(Polygon2D(Point2D(1.0,0.5),
                                              Point2D(0.5,0.5),
                                              Point2D(0.5,0.0),
                                              Point2D(1.0,0.0)))))
        
        # no intersection
        pg1=Polygon2D(Point2D(2,0),Point2D(3,0),Point2D(3,1),Point2D(2,1),
                      known_convex=True)
        self.assertEqual(pg._intersect_polygon_simple_and_simple_convex(pg1),
                          (Points(), 
                           Polylines(), 
                           Polygons()))
        
        # point intersection
        pg1=Polygon2D(Point2D(1,1),Point2D(2,1),Point2D(2,2),Point2D(1,2),
                      known_convex=True)
        self.assertEqual(pg._intersect_polygon_simple_and_simple_convex(pg1),
                          (Points(Point2D(1,1)), 
                           Polylines(), 
                           Polygons()))
        
        # segment intersection
        pg1=Polygon2D(Point2D(1,0.5),Point2D(2,0.5),Point2D(2,1.5),Point2D(1,1.5),
                      known_convex=True)
        self.assertEqual(pg._intersect_polygon_simple_and_simple_convex(pg1),
                          (Points(), 
                           Polylines(Polyline2D(Point2D(1,0.5),Point2D(1,1))), 
                           Polygons()))
        
        # C-SHAPE
        pg1=Polygon2D(Point2D(0,0),
                      Point2D(2,0),
                      Point2D(2,1),
                      Point2D(1,1),
                      Point2D(1,2),
                      Point2D(2,2),
                      Point2D(2,3),
                      Point2D(0,3))
        pg2=Polygon2D(Point2D(1,0),
                      Point2D(2,0),
                      Point2D(2,3),
                      Point2D(1,3),
                      known_convex=True)
        #print('test')
        #print(pg1.intersect_polygon(pg2))
        #return
        self.assertEqual(pg1._intersect_polygon_simple_and_simple_convex(pg2),
                          (Points(), 
                           Polylines(Polyline2D(Point2D(1.0,2.0), 
                                                Point2D(1.0,1.0))), 
                           Polygons(Polygon2D(Point2D(1.0,0.0),
                                              Point2D(2.0,0.0),
                                              Point2D(2.0,1.0),
                                              Point2D(1.0,1.0)), 
                                    Polygon2D(Point2D(1.0,2.0),
                                              Point2D(2.0,2.0),
                                              Point2D(2.0,3.0),
                                              Point2D(1,3)))))
        
        
    def test__intersect_polygon_simple_and_simple(self):
        ""
        
        pg=Polygon2D(Point2D(0,0),Point2D(1,0),Point2D(1,1),Point2D(0,1))
        
        # full overlap intersection
        self.assertEqual(pg._intersect_polygon_simple_and_simple(pg),
                         (Points(), 
                          Polylines(),
                          Polygons(pg)))
        
        
        # half overlap
        pg1=Polygon2D(Point2D(0.5,0),Point2D(1.5,0),Point2D(1.5,1),Point2D(0.5,1))
        self.assertEqual(pg._intersect_polygon_simple_and_simple(pg1),
                          (Points(), 
                           Polylines(), 
                           Polygons(Polygon2D(Point2D(1.0,1.0),
                                              Point2D(0.5,1),
                                              Point2D(0.5,0.0),
                                              Point2D(1.0,0.0)))))
        
        
         # corner overlap
        pg1=Polygon2D(Point2D(0.5,-0.5),Point2D(1.5,-0.5),Point2D(1.5,0.5),Point2D(0.5,0.5))
        self.assertEqual(pg._intersect_polygon_simple_and_simple(pg1),
                          (Points(), 
                           Polylines(), 
                           Polygons(Polygon2D(Point2D(1.0,0.5),
                                              Point2D(0.5,0.5),
                                              Point2D(0.5,0.0),
                                              Point2D(1.0,0.0)))))
        
        # no intersection
        pg1=Polygon2D(Point2D(2,0),Point2D(3,0),Point2D(3,1),Point2D(2,1))
        self.assertEqual(pg._intersect_polygon_simple_and_simple(pg1),
                          (Points(), 
                           Polylines(), 
                           Polygons()))
        
        # point intersection
        pg1=Polygon2D(Point2D(1,1),Point2D(2,1),Point2D(2,2),Point2D(1,2))
        self.assertEqual(pg._intersect_polygon_simple_and_simple(pg1),
                          (Points(Point2D(1,1)), 
                           Polylines(), 
                           Polygons()))
        
        # segment intersection
        pg1=Polygon2D(Point2D(1,0.5),Point2D(2,0.5),Point2D(2,1.5),Point2D(1,1.5))
        self.assertEqual(pg._intersect_polygon_simple_and_simple(pg1),
                          (Points(), 
                           Polylines(Polyline2D(Point2D(1,0.5),Point2D(1,1))), 
                           Polygons()))
        
        
        # C-SHAPE
        pg1=Polygon2D(Point2D(0,0),
                      Point2D(2,0),
                      Point2D(2,1),
                      Point2D(1,1),
                      Point2D(1,2),
                      Point2D(2,2),
                      Point2D(2,3),
                      Point2D(0,3))
        pg2=Polygon2D(Point2D(1,0),
                      Point2D(2,0),
                      Point2D(2,3),
                      Point2D(1,3))
        self.assertEqual(pg1._intersect_polygon_simple_and_simple(pg2),
                          (Points(), 
                           Polylines(Polyline2D(Point2D(1.0,2.0), 
                                                Point2D(1.0,1.0))), 
                           Polygons(Polygon2D(Point2D(1.0,0.0),
                                              Point2D(2.0,0.0),
                                              Point2D(2.0,1.0),
                                              Point2D(1.0,1.0)), 
                                    Polygon2D(Point2D(1.0,2.0),
                                              Point2D(2.0,2.0),
                                              Point2D(2.0,3.0),
                                              Point2D(1,3)))))
        
        # example
        pg=Polygon3D(Point3D(0,0,0),Point3D(10,0,0),Point3D(10,0,3),Point3D(0,0,3)) 
        pg1=Polygon3D(Point3D(0,0,0),Point3D(10,0,0),Point3D(10,10,0),Point3D(0,10,0))
        #print(pg._intersect_polygon_simple_and_simple(pg1))
        
    def test_intersect_polygon(self):
        ""
        
        # 2D TWO SIMPLE CONVEX POLYGONS
        # full overlap intersection
        pg=Polygon2D(Point2D(0,0),Point2D(1,0),Point2D(1,1),Point2D(0,1),
                     known_convex=True)
        self.assertEqual(pg.intersect_polygon(pg),
                         (Points(),
                          Polylines(),
                          Polygons(pg)))
        
        # 2D SIMPLE AND SIMPLE CONVEX POLYGONS
        # full overlap intersection
        pg=Polygon2D(Point2D(0,0),Point2D(1,0),Point2D(1,1),Point2D(0,1),
                     known_convex=True)
        pg1=Polygon2D(Point2D(0,0),Point2D(1,0),Point2D(1,1),Point2D(0,1))
        self.assertEqual(pg.intersect_polygon(pg1),
                         (Points(),
                          Polylines(),
                          Polygons(pg)))
        self.assertEqual(pg1.intersect_polygon(pg),
                         (Points(),
                          Polylines(),
                          Polygons(pg)))
        
        # 2D SIMPLE AND SIMPLE POLYGONS
        # full overlap intersection
        pg=Polygon2D(Point2D(0,0),Point2D(1,0),Point2D(1,1),Point2D(0,1))
        pg1=Polygon2D(Point2D(0,0),Point2D(1,0),Point2D(1,1),Point2D(0,1))
        self.assertEqual(pg.intersect_polygon(pg1),
                         (Points(),
                          Polylines(),
                          Polygons(pg)))
        self.assertEqual(pg1.intersect_polygon(pg),
                         (Points(),
                          Polylines(),
                          Polygons(pg)))        
        
        # 3D TWO SIMPLE CONVEX POLYGONS
        # full overlap intersection
        pg=Polygon3D(Point3D(0,0,0),Point3D(1,0,0),Point3D(1,1,0),Point3D(0,1,0),
                     known_convex=True)
        self.assertEqual(pg.intersect_polygon(pg),
                         (Points(),
                          Polylines(),
                          Polygons(pg)))
        
        # 3D SIMPLE AND SIMPLE CONVEX POLYGONS
        # full overlap intersection
        pg=Polygon3D(Point3D(0,0,0),Point3D(1,0,0),Point3D(1,1,0),Point3D(0,1,0),
                     known_convex=True)
        pg1=Polygon3D(Point3D(0,0,0),Point3D(1,0,0),Point3D(1,1,0),Point3D(0,1,0))
        self.assertEqual(pg.intersect_polygon(pg1),
                         (Points(),
                          Polylines(),
                          Polygons(pg)))
        self.assertEqual(pg1.intersect_polygon(pg),
                         (Points(),
                          Polylines(),
                          Polygons(pg)))
    
        # 3D SIMPLE AND SIMPLE POLYGONS
        # full overlap intersection
        pg=Polygon3D(Point3D(0,0,0),Point3D(1,0,0),Point3D(1,1,0),Point3D(0,1,0))
        pg1=Polygon3D(Point3D(0,0,0),Point3D(1,0,0),Point3D(1,1,0),Point3D(0,1,0))
        self.assertEqual(pg.intersect_polygon(pg1),
                         (Points(),
                          Polylines(),
                          Polygons(pg)))
        self.assertEqual(pg1.intersect_polygon(pg),
                         (Points(),
                          Polylines(),
                          Polygons(pg)))   
    
        # half overlap
        pg1=Polygon3D(Point3D(0.5,0,0),Point3D(1.5,0,0),Point3D(1.5,1,0),Point3D(0.5,1,0))
        self.assertEqual(pg._intersect_polygon_simple_and_simple(pg1),
                          (Points(), 
                           Polylines(), 
                           Polygons(Polygon3D(Point3D(1.0,1.0,0),
                                              Point3D(0.5,1,0),
                                              Point3D(0.5,0.0,0),
                                              Point3D(1.0,0.0,0)))))
    
    
        # example
        #print('test')
        pg=Polygon3D(Point3D(5,0,0),Point3D(15,0,0),Point3D(15,0,3),Point3D(5,0,3))
        pg1=Polygon3D(Point3D(0,0,0),Point3D(10,0,0),Point3D(10,0,3),Point3D(0,0,3))
        #print(pg1.intersect_polygon(pg))
        
        
        # example
        pg=Polygon3D(Point3D(0,0,3),Point3D(10,0,3),Point3D(10,10,3),Point3D(0,10,3)) 
        pg1=Polygon3D(Point3D(0,0,0),Point3D(10,0,0),Point3D(10,10,0),Point3D(0,10,0))
        #print(pg.intersect_polygon(pg1))
        
        # example
        pg=Polygon3D(Point3D(0,0,0),Point3D(10,0,0),Point3D(10,0,3),Point3D(0,0,3)) 
        pg1=Polygon3D(Point3D(0,0,0),Point3D(10,0,0),Point3D(10,10,0),Point3D(0,10,0))
        #print('test')
        #print(pg.intersect_polygon(pg1))
        
        # example
        pg=Polygon3D(Point3D(-0.0,5.63,2.5),
                     Point3D(-0.0,1.2,2.5),
                     Point3D(2.06,1.2,2.5),
                     Point3D(2.06,4.43,2.5),
                     Point3D(2.93,4.43,2.5),
                     Point3D(2.93,5.63,2.5))
        pg1=Polygon3D(Point3D(-0.0,3.57,2.5),
                      Point3D(1.0,3.57,2.5),
                      Point3D(1.0,4.43,2.5),
                      Point3D(2.93,4.43,2.5),
                      Point3D(2.93,1.2,2.5),
                      Point3D(-0.0,1.2,2.5))
        #print(pg.intersect_polygon(pg1))
        
        ax=pg.plot()
        pg1.plot(ax)
        pg.intersect_polygon(pg1)[2][0].plot(ax)
        
        # example
        pg=Polygon3D(Point3D(-8.881784197001252e-16,5.63,2.5),
                     Point3D(-8.881784197001252e-16,1.2000000000000002,2.5),
                     Point3D(2.059999999999999,1.2000000000000002,2.5),
                     Point3D(2.0599999999999996,4.43,2.5),
                     Point3D(2.9299999999999993,4.43,2.5),
                     Point3D(2.9299999999999993,5.63,2.5))
        pg1=Polygon3D(Point3D(-8.881784197001252e-16,3.57,2.5),
                      Point3D(0.9999999999999991,3.57,2.5),
                      Point3D(0.9999999999999991,4.43,2.5),
                      Point3D(2.9299999999999993,4.43,2.5),
                      Point3D(2.9299999999999993,1.1999999999999997,2.5),
                      Point3D(-8.881784197001252e-16,1.1999999999999997,2.5))
        
        #print(pg.intersect_polygon(pg1))
        
        ax=pg.plot()
        pg1.plot(ax)
        pg.intersect_polygon(pg1)[2][0].plot(ax)
        
        
        
        
        
    def test__intersect_line_t_values_simple_convex(self):
        ""
        
        # 2D
        pg=Polygon2D(*points2d)
        
        # edge
        l=Line2D(Point2D(0,0),Vector2D(1,0))
        self.assertEqual(pg._intersect_line_t_values_simple_convex(l),
                        (0,1))  
        
        # vertex
        l=Line2D(Point2D(0,0),Vector2D(-1,1))
        self.assertEqual(pg._intersect_line_t_values_simple_convex(l),
                        (0,0))  
        
        # diagonal
        l=Line2D(Point2D(0,0),Vector2D(1,1))
        self.assertEqual(pg._intersect_line_t_values_simple_convex(l),
                        (0,1))  
        
        # no intersection
        l=Line2D(Point2D(-1,0),Vector2D(-1,1))
        self.assertEqual(pg._intersect_line_t_values_simple_convex(l),
                         None)  
        
        
        # 3D
        pg=Polygon3D(*points3d)
        
        # line in polygon plane
        # edge
        l=Line3D(Point3D(0,0,0),Vector3D(1,0,0))
        self.assertEqual(pg._intersect_line_t_values_simple_convex(l),
                         (0,1))  
        # vertex
        l=Line3D(Point3D(0,0,0),Vector3D(-1,1,0))
        self.assertEqual(pg._intersect_line_t_values_simple_convex(l),
                        (0,0))  
        
        # diagonal
        l=Line3D(Point3D(0,0,0),Vector3D(1,1,0))
        self.assertEqual(pg._intersect_line_t_values_simple_convex(l),
                        (0,1))  
        
        # no intersection
        l=Line3D(Point3D(-1,0,0),Vector3D(-1,1,0))
        self.assertEqual(pg._intersect_line_t_values_simple_convex(l),
                         None)  
        
        # skew line
        # point on edge
        l=Line3D(Point3D(0,0,0),Vector3D(1,0,1))
        self.assertEqual(pg._intersect_line_t_values_simple_convex(l),
                         (0,0))  
        
        # point in polygon
        l=Line3D(Point3D(0.5,0.5,0),Vector3D(1,0,1))
        self.assertEqual(pg._intersect_line_t_values_simple_convex(l),
                         (0,0))  
        
        # no intersection
        # point in polygon
        l=Line3D(Point3D(-1,-1,0),Vector3D(1,0,1))
        self.assertEqual(pg._intersect_line_t_values_simple_convex(l),
                         None)  
        
        # perpendicular line
        l=Line3D(Point3D(0,0,0),Vector3D(0,0,1))
        self.assertEqual(pg._intersect_line_t_values_simple_convex(l),
                         (0,0))  
        
        # parallel line
        l=Line3D(Point3D(0,0,1),Vector3D(1,0,0))
        self.assertEqual(pg._intersect_line_t_values_simple_convex(l),
                         None)  
        
        
        pg=Polygon3D(Point3D(0,0,0),
                     Point3D(1,0,1),
                     Point3D(1,1,1),
                     Point3D(0,1,0))
        l=Line3D(Point3D(0,0,0),Vector3D(1,1,1))
        self.assertEqual(pg._intersect_line_t_values_simple_convex(l),
                         (0,1))  
        
        
        
        
    def test__intersect_segment_simple_convex(self):
        ""
        pg=Polygon2D(*points2d)
        
        # segment is a polygon edge
        s=Segment2D(Point2D(0,0),Point2D(1,1))
        self.assertEqual(pg._intersect_segment_simple_convex(s),
                         s)
        
        # segment starts on a polygon edge
        s=Segment2D(Point2D(0,0),Point2D(1,-1))
        self.assertEqual(pg._intersect_segment_simple_convex(s),
                         Point2D(0,0))    
        
        # segment is a partial polygon edge
        s=Segment2D(Point2D(0.5,0.5),Point2D(1,1))
        self.assertEqual(pg._intersect_segment_simple_convex(s),
                         s)    
        
        # segment is wholly inside the polygon
        s=Segment2D(Point2D(0.25,0.25),Point2D(0.75,0.75))
        self.assertEqual(pg._intersect_segment_simple_convex(s),
                         s)   
        
        # segment starts inside the polygon and ends outside it
        s=Segment2D(Point2D(0.5,0.5),Point2D(1.5,0.5))
        self.assertEqual(pg._intersect_segment_simple_convex(s),
                         Segment2D(Point2D(0.5,0.5),Point2D(1.0,0.5)))  
        
        
    def test__intersect_segment_simple(self):
        ""
        
        # simple concave polygon
        pg=Polygon2D(Point2D(0,0),
                    Point2D(2,0),
                    Point2D(1,1),
                    Point2D(2,2),
                    Point2D(0,2))
        
        self.assertEqual(pg._intersect_segment_simple(Segment2D(Point2D(1.5,0),
                                                                Point2D(1.5,10))),
                        (Points(),
                         Segments(Segment2D(Point2D(1.5,0), 
                                            Point2D(1.5,0.5)),
                                  Segment2D(Point2D(1.5,1.5), 
                                            Point2D(1.5,2)))))
        
        self.assertEqual(pg._intersect_segment_simple(Segment2D(Point2D(2,0),
                                                                Point2D(2,10))),
                        (Points(Point2D(2,0),
                                Point2D(2,2)), 
                         Segments()))  
    
        self.assertEqual(pg._intersect_segment_simple(Segment2D(Point2D(1,0),
                                                                Point2D(1,10))),
                         (Points(), 
                          Segments(Segment2D(Point2D(1,0), 
                                             Point2D(1,2)))))  
    
        self.assertEqual(pg._intersect_segment_simple(Segment2D(Point2D(0,0),
                                                                Point2D(0,10))),
                        (Points(), 
                         Segments(Segment2D(Point2D(0,0), 
                                            Point2D(0,2)))))  
    
        self.assertEqual(pg._intersect_segment_simple(Segment2D(Point2D(0,0.5),
                                                                Point2D(10,0.5))),
                        (Points(), 
                         Segments(Segment2D(Point2D(0,0.5), 
                                            Point2D(1.5,0.5))))) 
    
    
    def test_intersect_segment(self):
        ""
        
        # 2D SIMPLE CONVEX POLYGON
        
        pg=Polygon2D(*points2d, known_convex=True)
        
        # segment is a polygon edge
        self.assertEqual(pg.intersect_segment(Segment2D(Point2D(0,0),
                                                        Point2D(1,0))),
                        (Points(), 
                         Segments(Segment2D(Point2D(0.0,0.0), 
                                            Point2D(1.0,0.0)))))        
        
        # segment starts on a polygon edge
        self.assertEqual(pg.intersect_segment(Segment2D(Point2D(0,0),
                                                        Point2D(1,-1))),
                        (Points(Point2D(0,0)),
                         Segments()))
    
        # segment is a partial polygon edge
        self.assertEqual(pg.intersect_segment(Segment2D(Point2D(0.5,0.5),
                                                        Point2D(1,1))),
                        (Points(), 
                         Segments(Segment2D(Point2D(0.5,0.5), 
                                            Point2D(1.0,1.0)))))    
            
        
        # 2D SIMPLE POLYGON (concave)
        
        pg=Polygon2D(Point2D(0,0),
                    Point2D(2,0),
                    Point2D(1,1),
                    Point2D(2,2),
                    Point2D(0,2))
        
        self.assertEqual(pg.intersect_segment(Segment2D(Point2D(1.5,0),
                                                        Point2D(1.5,10))),
                        (Points(),
                         Segments(Segment2D(Point2D(1.5,0), 
                                            Point2D(1.5,0.5)),
                                  Segment2D(Point2D(1.5,1.5), 
                                            Point2D(1.5,2)))))
        
        self.assertEqual(pg.intersect_segment(Segment2D(Point2D(2,0),
                                                        Point2D(2,10))),
                        (Points(Point2D(2,0),
                                Point2D(2,2)), 
                         Segments()))  
    
        self.assertEqual(pg.intersect_segment(Segment2D(Point2D(1,0),
                                                        Point2D(1,10))),
                         (Points(), 
                          Segments(Segment2D(Point2D(1,0), 
                                             Point2D(1,2)))))  
    
        self.assertEqual(pg.intersect_segment(Segment2D(Point2D(0,0),
                                                        Point2D(0,10))),
                        (Points(), 
                         Segments(Segment2D(Point2D(0,0), 
                                            Point2D(0,2)))))  
    
        self.assertEqual(pg.intersect_segment(Segment2D(Point2D(0,0.5),
                                                        Point2D(10,0.5))),
                        (Points(), 
                         Segments(Segment2D(Point2D(0,0.5), 
                                            Point2D(1.5,0.5))))) 
        
        # 3D SIMPLE CONVEX POLYGON
        
        pg=Polygon3D(*points3d, known_convex=True)
        
        # segment is a polygon edge
        self.assertEqual(pg.intersect_segment(Segment3D(Point3D(0,0,0),
                                                        Point3D(1,0,0))),
                        (Points(), 
                         Segments(Segment3D(Point3D(0.0,0.0,0), 
                                            Point3D(1.0,0.0,0)))))  
        
        # segment is skew and intersects polygon
        self.assertEqual(pg.intersect_segment(Segment3D(Point3D(0.5,0.5,-1),
                                                        Point3D(0.5,0.5,1))),
                        (Points(Point3D(0.5,0.5,0)), 
                         Segments()))  
        
        
        # 3D SIMPLE POLYGON (concave)
        
        pg=Polygon3D(Point3D(0,0,0),
                     Point3D(2,0,0),
                     Point3D(1,1,0),
                     Point3D(2,2,0),
                     Point3D(0,2,0))
        
        self.assertEqual(pg.intersect_segment(Segment3D(Point3D(1.5,0,0),
                                                        Point3D(1.5,10,0))),
                        (Points(),
                         Segments(Segment3D(Point3D(1.5,0,0), 
                                            Point3D(1.5,0.5,0)),
                                  Segment3D(Point3D(1.5,1.5,0), 
                                            Point3D(1.5,2,0)))))
                
        # example
        
        pg=Polygon3D(Point3D(5,0,0),
                     Point3D(15,0,0),
                     Point3D(15,0,3),
                     Point3D(5,0,3))
        #print('test99')
        #print(pg.intersect_segment(Segment3D(Point3D(5,0,0),Point3D(15,0,0))))
        
        pg=Polygon3D(Point3D(0,0,3),Point3D(10,0,3),Point3D(10,10,3),Point3D(0,10,3)) 
        s=Segment3D(Point3D(0,0,0),Point3D(10,0,0))
        #print(pg.intersect_segment(s))
        #print(pg._intersect_segment_simple_convex(s))
        
        
    def test_intersect_segments(self):
        ""
        
        # SIMPLE CONVEX POLYGON
        
        pg=Polygon2D(*points2d, known_convex=True)
        
        # segment is a polygon edge
        self.assertEqual(pg.intersect_segments(Segments(Segment2D(Point2D(0,0),
                                                                  Point2D(1,1)))),
                        (Points(), 
                         Segments(Segment2D(Point2D(0.0,0.0), 
                                            Point2D(1.0,1.0)))))    
        
        # as above, with 2 segments
        self.assertEqual(pg.intersect_segments(Segments(Segment2D(Point2D(-0.5,-0.5),
                                                                  Point2D(0.5,0.5)),
                                                        Segment2D(Point2D(0.5,0.5),
                                                                  Point2D(1.5,1.5)))),
                        (Points(), 
                         Segments(Segment2D(Point2D(0.0,0.0), 
                                            Point2D(1.0,1.0)))))   
        
        
        # example
        pg=Polygon3D(Point3D(0,0,3),Point3D(10,0,3),Point3D(10,10,3),Point3D(0,10,3)) 
        sgmts=Segments(Segment3D(Point3D(0,0,0),Point3D(10,0,0)))
        #print(pg.intersect_segments(sgmts))
        #print(pl1.intersect_polyline(pl))
        
    
        
    def test_next_index(self):
        ""
        pg=Polygon2D(*points2d)
        self.assertEqual(pg.next_index(0),
                         1)
        self.assertEqual(pg.next_index(3),
                         0)
        
    def test_plot(self):
        ""
        if plot:
            
            pg=Polygon2D(*points2d)
            fig, ax = plt.subplots()
            pg.plot(ax)
            
            # concave polygon
            pg=Polygon2D(Point2D(0,0),
                         Point2D(2,0),
                         Point2D(1,1),
                         Point2D(2,2),
                         Point2D(0,2))
            fig, ax = plt.subplots()
            pg.plot(ax)
            
    
    def test_prevous_index(self):
        ""
        pg=Polygon2D(*points2d)
        self.assertEqual(pg.previous_index(0),
                         3)
        self.assertEqual(pg.previous_index(3),
                         2)
        
        
    def test_reorder(self):
        ""
        pg=Polygon2D(*points2d)
        self.assertEqual(pg.reorder(1),
                         Polygon2D(Point2D(1,0),
                                   Point2D(1,1),
                                   Point2D(0,1),
                                   Point2D(0,0)))
        
        
    def test_reverse(self):
        ""
        pg=Polygon2D(*points2d)
        self.assertEqual(pg.reverse,
                         Polygon2D(Point2D(0,1),
                                   Point2D(1,1),
                                   Point2D(1,0),
                                   Point2D(0,0)))
        

    def test__triangulate(self):
        ""
        # convex polygon
        pg=Polygon2D(*points2d)
        self.assertEqual(pg._triangulate,
                         Polygons(Polygon2D(Point2D(0,0),
                                            Point2D(1,0),
                                            Point2D(1,1)), 
                                  Polygon2D(Point2D(0,0),
                                            Point2D(1,1),
                                            Point2D(0,1))))
        
        
        # concave polygon
        pg=Polygon2D(Point2D(0,0),
                      Point2D(2,0),
                      Point2D(1,1),
                      Point2D(2,2),
                      Point2D(0,2))
        self.assertEqual(pg._triangulate,
                         Polygons(Polygon2D(Point2D(0,0),
                                            Point2D(2,0),
                                            Point2D(1,1)), 
                                  Polygon2D(Point2D(0.0,0.0),
                                            Point2D(2,2),
                                            Point2D(0,2))))
    
    
    def test_triangles(self):
        ""
    


class Test_Polygon2D(unittest.TestCase):
    """
    points2d=(Point2D(0,0),Point2D(1,0),Point2D(1,1),Point2D(0,1))
    """
    
    
        
    def test___contains__(self):
        ""
        
        pg=Polygon2D(*points2d)
        
        # Point
        self.assertTrue(pg.points[0] in pg)
        self.assertTrue(pg.points[1] in pg)
        self.assertTrue(pg.points[2] in pg)
        self.assertTrue(pg.points[3] in pg)        
        self.assertTrue(Point2D(0.5,0.5) in pg)
        
        
    
        
    def test___repr__(self):
        ""
        pg=Polygon2D(*points2d)
        self.assertEqual(str(pg),
                         'Polygon2D(Point2D(0,0),Point2D(1,0),Point2D(1,1),Point2D(0,1))')
        
        
    def test_area(self):
        ""
        pg=Polygon2D(*points2d)
        self.assertEqual(pg.area, # ccw
                         1)
        self.assertEqual(pg.reverse.area, # cw
                         1)
        
        
    def test_ccw(self):
        ""
        
        
    def test_centroid(self):
        ""
        pg=Polygon2D(*points2d)
        self.assertEqual(pg.centroid, 
                         Point2D(0.5,0.5))
        
        
    def test__crossing_number(self):
        ""
        pg=Polygon2D(*points2d)
        self.assertEqual(pg._crossing_number(pg.points[0]),
                         1)
        self.assertEqual(pg._crossing_number(pg.points[1]),
                         0)
        self.assertEqual(pg._crossing_number(pg.points[2]),
                         0)
        self.assertEqual(pg._crossing_number(pg.points[3]),
                         0) 
        self.assertEqual(pg._crossing_number(Point2D(-0.5,0.5)),
                         2)
        self.assertEqual(pg._crossing_number(Point2D(0.5,0.5)),
                         1)
        
        
    def test_is_counterclockwise(self):
        ""
        pg=Polygon2D(*points2d)
        self.assertTrue(pg.is_counterclockwise)
        self.assertFalse(pg.reverse.is_counterclockwise)
        
        
    def test_rightmost_lowest_vertex(self):
        ""
        pg=Polygon2D(*points2d)
        self.assertEqual(pg.rightmost_lowest_vertex, 
                         1)
        
        
    def test_signed_area(self):
        ""
        pg=Polygon2D(*points2d)
        self.assertEqual(pg.signed_area, # ccw
                         1)
        self.assertEqual(pg.reverse.signed_area, # cw
                         -1)
        
        
    def test__winding_number(self):
        ""
        
        pg=Polygon2D(*points2d)
        self.assertEqual(pg._winding_number(pg.points[0]),
                         1)
        self.assertEqual(pg._winding_number(pg.points[1]),
                         0)
        self.assertEqual(pg._winding_number(pg.points[2]),
                         0)
        self.assertEqual(pg._winding_number(pg.points[3]),
                         0) 
        self.assertEqual(pg._winding_number(Point2D(-0.5,0.5)),
                         0)
        self.assertEqual(pg._winding_number(Point2D(0.5,0.5)),
                         1)
        
        
        
    
    
    
        
class Test_Polygon3D(unittest.TestCase):
    """
    points3d=(Point3D(0,0,0),Point3D(1,0,0),Point3D(1,1,0),Point3D(0,1,0))
    """
    
    def test___init__(self):
        ""
        pg=Polygon3D(*points3d)
        self.assertIsInstance(pg,Polygon3D)
        self.assertEqual(pg.points,Points(*points3d))
        
        
    def test___contains__(self):
        ""
        pg=Polygon3D(*points3d)
        
        
    def test___repr__(self):
        ""
        pg=Polygon3D(*points3d)
        self.assertEqual(str(pg),
                          'Polygon3D(Point3D(0,0,0),Point3D(1,0,0),Point3D(1,1,0),Point3D(0,1,0))')
        
        
    def test_area(self):
        ""
        pg=Polygon3D(*points3d)
        self.assertEqual(pg.area, # ccw
                          1)
        self.assertEqual(pg.reverse.area, # cw
                          1)
        
        
    def test_centroid(self):
        ""
        pg=Polygon3D(*points3d)
        self.assertEqual(pg.centroid, 
                          Point3D(0.5,0.5,0))
        
        
    def test__intersect_plane_volume_simple_convex(self):
        ""
        pg=Polygon3D(*points3d,known_convex=True)
        
        # no intersection
        pv=PlaneVolume3D(Point3D(-1,0,0),
                         Vector3D(1,0,0))
        self.assertEqual(pg._intersect_plane_volume_simple_convex(pv),
                         None)
        
        # point intersection
        pv=PlaneVolume3D(Point3D(0,0,0),
                         Vector3D(1,1,0))
        self.assertEqual(pg._intersect_plane_volume_simple_convex(pv),
                         Point3D(0.0,0.0,0.0))
        
        # segment intersection
        pv=PlaneVolume3D(Point3D(0,0,0),
                         Vector3D(1,0,0))
        self.assertEqual(pg._intersect_plane_volume_simple_convex(pv),
                         Segment3D(Point3D(0,1,0), 
                                   Point3D(0,0,0)))
        
        # partial polygon intersection
        pv=PlaneVolume3D(Point3D(0.5,0,0),
                         Vector3D(1,0,0))
        self.assertEqual(pg._intersect_plane_volume_simple_convex(pv),
                         Polygon3D(Point3D(0.5,1.0,0.0),
                                   Point3D(0,1,0),
                                   Point3D(0,0,0),
                                   Point3D(0.5,0.0,0.0)))
        
        # full polygon intersection
        pv=PlaneVolume3D(Point3D(0,0,0),
                         Vector3D(-1,0,0))
        self.assertEqual(pg._intersect_plane_volume_simple_convex(pv),
                         pg)
        
        
    def test__intersect_plane_volume_simple(self):
        ""
        pg=Polygon3D(*points3d)
        
        # no intersection
        pv=PlaneVolume3D(Point3D(-1,0,0),
                         Vector3D(1,0,0))
        self.assertEqual(pg._intersect_plane_volume_simple(pv),
                         (Points(),
                          Segments(),
                          Polygons()))
        
       # point intersection
        pv=PlaneVolume3D(Point3D(0,0,0),
                         Vector3D(1,1,0))
        self.assertEqual(pg._intersect_plane_volume_simple(pv),
                         (Points(Point3D(0.0,0.0,0.0)),
                          Segments(),
                          Polygons()))
                         
        # segment intersection
        pv=PlaneVolume3D(Point3D(0,0,0),
                         Vector3D(1,0,0))
        self.assertEqual(pg._intersect_plane_volume_simple(pv),
                         (Points(),
                          Segments(Segment3D(Point3D(0,1,0), 
                                             Point3D(0,0,0))),
                          Polygons()))
                         
        # partial polygon intersection
        pv=PlaneVolume3D(Point3D(0.5,0,0),
                         Vector3D(1,0,0))
        self.assertEqual(pg._intersect_plane_volume_simple(pv),
                         (Points(),
                          Segments(),
                          Polygons(Polygon3D(Point3D(0.5,1.0,0.0),
                                   Point3D(0,1,0),
                                   Point3D(0,0,0),
                                   Point3D(0.5,0.0,0.0)))))
                         
        # full polygon intersection
        pv=PlaneVolume3D(Point3D(0,0,0),
                         Vector3D(-1,0,0))
        self.assertEqual(pg._intersect_plane_volume_simple(pv),
                         (Points(),
                          Segments(),
                          Polygons(pg)))
                        
        
    def test_intersect_plane_volume(self):
        ""
        pg=Polygon3D(*points3d,known_convex=True)
        
        # no intersection
        pv=PlaneVolume3D(Point3D(-1,0,0),
                         Vector3D(1,0,0))
        self.assertEqual(pg.intersect_plane_volume(pv),
                         (Points(),
                          Segments(),
                          Polygons()))
        
       # point intersection
        pv=PlaneVolume3D(Point3D(0,0,0),
                         Vector3D(1,1,0))
        self.assertEqual(pg.intersect_plane_volume(pv),
                         (Points(Point3D(0.0,0.0,0.0)),
                          Segments(),
                          Polygons()))
                         
        # segment intersection
        pv=PlaneVolume3D(Point3D(0,0,0),
                         Vector3D(1,0,0))
        self.assertEqual(pg.intersect_plane_volume(pv),
                         (Points(),
                          Segments(Segment3D(Point3D(0,1,0), 
                                             Point3D(0,0,0))),
                          Polygons()))
                         
        # partial polygon intersection
        pv=PlaneVolume3D(Point3D(0.5,0,0),
                         Vector3D(1,0,0))
        self.assertEqual(pg.intersect_plane_volume(pv),
                         (Points(),
                          Segments(),
                          Polygons(Polygon3D(Point3D(0.5,1.0,0.0),
                                   Point3D(0,1,0),
                                   Point3D(0,0,0),
                                   Point3D(0.5,0.0,0.0)))))
                         
        # full polygon intersection
        pv=PlaneVolume3D(Point3D(0,0,0),
                         Vector3D(-1,0,0))
        self.assertEqual(pg.intersect_plane_volume(pv),
                         (Points(),
                          Segments(),
                          Polygons(pg)))
        
        
    def test__intersect_plane_simple_convex_skew(self):
        ""
        pg=Polygon3D(*points3d,known_convex=True)
        
        
        # no intersection - skew plane
        self.assertEqual(pg._intersect_plane_simple_convex_skew(Plane3D(Point3D(-1,0,0),
                                                                        Vector3D(1,0,0))),
                         None)
        
        # intersection - point
        self.assertEqual(pg._intersect_plane_simple_convex_skew(Plane3D(Point3D(0,0,0),
                                                                        Vector3D(1,1,0))),
                         Point3D(0.0,0.0,0.0))
        
        # intersection - edge segment
        self.assertEqual(pg._intersect_plane_simple_convex_skew(Plane3D(Point3D(0,0,0),
                                                                        Vector3D(1,0,0))),
                         Segment3D(Point3D(0.0,0.0,0.0), 
                                   Point3D(0.0,1.0,0.0)))
        
        # intersection - internal segment
        self.assertEqual(pg._intersect_plane_simple_convex_skew(Plane3D(Point3D(0,0,0),
                                                                        Vector3D(1,-1,0))),
                         Segment3D(Point3D(0.0,0.0,0.0), 
                                   Point3D(1.0,1.0,0.0)))
        
    
    def test__intersect_plane_simple_skew(self):
        ""
        pg=Polygon3D(*points3d)
        
        
        # no intersection - skew plane
        self.assertEqual(pg._intersect_plane_simple_skew(Plane3D(Point3D(-1,0,0),
                                                                 Vector3D(1,0,0))),
                         (Points(),
                          Segments()))
        
        # intersection - point
        self.assertEqual(pg._intersect_plane_simple_skew(Plane3D(Point3D(0,0,0),
                                                                 Vector3D(1,1,0))),
                         (Points(Point3D(0.0,0.0,0.0)),
                          Segments()))
        
        # intersection - edge segment
        self.assertEqual(pg._intersect_plane_simple_skew(Plane3D(Point3D(0,0,0),
                                                                 Vector3D(1,0,0))),
                         (Points(),
                          Segments(Segment3D(Point3D(0.0,0.0,0.0), 
                                             Point3D(0.0,1.0,0.0)))))
        
        # intersection - internal segment
        self.assertEqual(pg._intersect_plane_simple_skew(Plane3D(Point3D(0,0,0),
                                                                 Vector3D(1,-1,0))),
                         (Points(),
                          Segments(Segment3D(Point3D(0.0,0.0,0.0), 
                                             Point3D(1.0,1.0,0.0)))))
        
        
    def test_intersect_plane(self):
        ""
        
        pg=Polygon3D(*points3d)
        
        # polygon in plane
        self.assertEqual(pg.intersect_plane(Plane3D(Point3D(0,0,0),
                                                    Vector3D(0,0,1))),
                         (Points(),
                          Segments(),
                          Polygons(pg)))
        
        # polygon parallel to plane
        self.assertEqual(pg.intersect_plane(Plane3D(Point3D(0,0,1),
                                                    Vector3D(0,0,1))),
                         (Points(),
                          Segments(),
                          Polygons()))
 
        # SIMPLE CONVEX POLYGON
        pg=Polygon3D(*points3d, known_convex=True)
        
        # no intersection - skew plane
        self.assertEqual(pg.intersect_plane(Plane3D(Point3D(-1,0,0),
                                                    Vector3D(1,0,0))),
                         (Points(),
                          Segments(),
                          Polygons()))
        
        # intersection - point
        self.assertEqual(pg.intersect_plane(Plane3D(Point3D(0,0,0),
                                                    Vector3D(1,1,0))),
                         (Points(Point3D(0.0,0.0,0.0)),
                          Segments(),
                          Polygons()))
        
        # intersection - edge segment
        self.assertEqual(pg.intersect_plane(Plane3D(Point3D(0,0,0),
                                                    Vector3D(1,0,0))),
                         (Points(),
                          Segments(Segment3D(Point3D(0.0,0.0,0.0), 
                                             Point3D(0.0,1.0,0.0))),
                          Polygons()))
        
        # intersection - internal segment
        self.assertEqual(pg.intersect_plane(Plane3D(Point3D(0,0,0),
                                                    Vector3D(1,-1,0))),
                         (Points(),
                          Segments(Segment3D(Point3D(0.0,0.0,0.0), 
                                             Point3D(1.0,1.0,0.0))),
                          Polygons()))
        
        # SIMPLE POLYGON
        pg=Polygon3D(*points3d)
        
        # no intersection - skew plane
        self.assertEqual(pg.intersect_plane(Plane3D(Point3D(-1,0,0),
                                                    Vector3D(1,0,0))),
                         (Points(),
                          Segments(),
                          Polygons()))
        
        # intersection - point
        self.assertEqual(pg.intersect_plane(Plane3D(Point3D(0,0,0),
                                                    Vector3D(1,1,0))),
                         (Points(Point3D(0.0,0.0,0.0)),
                          Segments(),
                          Polygons()))
        
        # intersection - edge segment
        self.assertEqual(pg.intersect_plane(Plane3D(Point3D(0,0,0),
                                                    Vector3D(1,0,0))),
                         (Points(),
                          Segments(Segment3D(Point3D(0.0,0.0,0.0), 
                                             Point3D(0.0,1.0,0.0))),
                          Polygons()))
        
        # intersection - internal segment
        self.assertEqual(pg.intersect_plane(Plane3D(Point3D(0,0,0),
                                                    Vector3D(1,-1,0))),
                         (Points(),
                          Segments(Segment3D(Point3D(0.0,0.0,0.0), 
                                             Point3D(1.0,1.0,0.0))),
                          Polygons()))
    
    
    def test_plane(self):
        ""
        pg=Polygon3D(*points3d)
        self.assertEqual(pg.plane,
                         Plane3D(Point3D(0,0,0),Vector3D(0,0,1)))
        
        
    def test_polyline(self):
        ""
        pg=Polygon3D(*points3d)
        self.assertEqual(pg.polyline,
                         Polyline3D(Point3D(0,0,0),
                                    Point3D(1,0,0),
                                    Point3D(1,1,0),
                                    Point3D(0,1,0),
                                    Point3D(0,0,0)))
        
        
    def test_project_2D(self):
        ""
        pg=Polygon3D(*points3d)
        self.assertEqual(pg.project_2D,
                          (2,Polygon2D(Point2D(0,0),Point2D(1,0),Point2D(1,1),Point2D(0,1))))
        
        
#     def test_plot(self):
#         ""
        
#         if plot:
        
#             pg=Polygon3D(*points)
#             fig = plt.figure()
#             ax = fig.add_subplot(111, projection='3d')
#             pg.plot(ax)
            
#             fig = plt.figure()
#             ax = fig.add_subplot(111, projection='3d')
#             pg.plot(ax,normal=True)
            
        
        
class Test_Example(unittest.TestCase):
        
    def test1(self):
        ""
        pg=Polygon3D(Point3D(-8.881784197001252e-16,5.63,2.5),
                     Point3D(-8.881784197001252e-16,1.2000000000000002,2.5),
                     Point3D(2.059999999999999,1.2000000000000002,2.5),
                     Point3D(2.0599999999999996,4.43,2.5),
                     Point3D(2.9299999999999993,4.43,2.5),
                     Point3D(2.9299999999999993,5.63,2.5))
        pg1=Polygon3D(Point3D(-8.881784197001252e-16,3.57,2.5),
                      Point3D(0.9999999999999991,3.57,2.5),
                      Point3D(0.9999999999999991,4.43,2.5),
                      Point3D(2.9299999999999993,4.43,2.5),
                      Point3D(2.9299999999999993,1.1999999999999997,2.5),
                      Point3D(-8.881784197001252e-16,1.1999999999999997,2.5))
        
        result=pg.intersect_polygon(pg1,debug=True)
        
        #ax=pg.plot()
        #pg1.plot(ax)
        #pg.intersect_polygon(pg1)[2][0].plot(ax)
        
        
class Test_Example1(unittest.TestCase):
        
    # def test1(self):
    #     ""
    #     pg1=Polygon3D(Point3D(-0.0,5.63,2.5),
    #                   Point3D(-0.0,1.2,2.5),
    #                   Point3D(2.06,1.2,2.5)) 
    #     pg2=Polygon3D(Point3D(-0.0,1.2,2.5),
    #                   Point3D(2.93,1.2,2.5),
    #                   Point3D(2.93,4.43,2.5))

    #     print(pg1.intersect_polygon(pg2))
        
        
    def test2(self):
        ""
        pg1=Polygon3D(Point3D(-8.881784197001252e-16,5.63,2.5),
                      Point3D(-8.881784197001252e-16,1.2000000000000002,2.5),
                      Point3D(2.059999999999999,1.2000000000000002,2.5),
                      known_convex=True) 
        pg2=Polygon3D(Point3D(-8.881784197001252e-16,1.1999999999999997,2.5),
                      Point3D(2.9299999999999993,1.1999999999999997,2.5),
                      Point3D(2.9299999999999993,4.43,2.5),
                      known_convex=True)
        
        result=pg1.intersect_polygon(pg2, debug=True)
        
        print(result)
    
    
    
if __name__=='__main__':
    
    points2d=(Point(0,0),Point(1,0),Point(1,1),Point(0,1))
    points3d=(Point(0,0,0),Point(1,0,0),Point(1,1,0),Point(0,1,0))
    
    #cProfile.run('unittest.main(Test_Polygon())')
    
    unittest.main(Test_Polygon())
    
    #unittest.main(Test_Polygon2D())
    
    #unittest.main(Test_Polygon3D())
    
    #unittest.main(Test_Example())
    
    #unittest.main(Test_Example1())
    
    # points=(Point3D(0,0,0),Point3D(1,0,0),Point3D(1,1,0),Point3D(0,1,0))
    # 
    
    