# -*- coding: utf-8 -*-

import unittest
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d
import cProfile

from crossproduct import Point2D, Point3D, \
    Vector2D, Vector3D, Line2D, Polygon2D, Polygon3D, Plane3D, \
    Segment2D, Segment3D, Halfline2D, Points, Segments, Polygons, Polygon2D, \
    Polyline2D, Polylines, Line3D


plot=False # Set to true to see the test plots


class Test_Polygon(unittest.TestCase):
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
        
        # SIMPLE CONVEX POLYGON
        
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
        
        
    def test__intersect_line_t_values_simple_convex(self):
        ""
        
        # 2D
        pg=Polygon2D(*points2d)
        
        l=Line2D(Point2D(0,0),Vector2D(1,0))
        self.assertEqual(pg._intersect_line_t_values_simple_convex(l),
                        (0,1))  
        
        
        # 3D
        pg=Polygon3D(*points3d)
        l=Line3D(Point3D(0,0,0),Vector3D(1,0,0))
        self.assertEqual(pg._intersect_line_t_values_simple_convex(l),
                         (0,1))  
        
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
                                            Point2D(0,1)), 
                                  Polygon2D(Point2D(1,0),
                                            Point2D(1,1),
                                            Point2D(0,1))))
        
        
        # concave polygon
        pg=Polygon2D(Point2D(0,0),
                      Point2D(2,0),
                      Point2D(1,1),
                      Point2D(2,2),
                      Point2D(0,2))
        self.assertEqual(pg._triangulate,
                         Polygons(Polygon2D(Point2D(2,0),
                                            Point2D(1,1),
                                            Point2D(0,0)), 
                                  Polygon2D(Point2D(0,0),
                                            Point2D(1,1),
                                            Point2D(0,2)), 
                                  Polygon2D(Point2D(1,1),
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
        
        
        
    # def test_difference_simple_polygon_interior(self):
    #     ""
    #     pg=Polygon2D(Point2D(0,0),
    #                        Point2D(2,0),
    #                        Point2D(2,1),
    #                        Point2D(0,1))
    #     #pg.plot()
        
    #     # self intersection
    #     self.assertEqual(pg.difference_simple_polygon_interior(pg),
    #                      None)
        
    #     # half intersection
    #     pg1=Polygon2D(Point2D(1,0),
    #                         Point2D(2,0),
    #                         Point2D(2,1),
    #                         Point2D(1,1))
    #     self.assertEqual(pg.difference_simple_polygon_interior(pg1),
    #                      Polygons(Polygon2D(Point2D(1,1),
    #                                                     Point2D(0,1),
    #                                                     Point2D(0,0),
    #                                                     Point2D(1,0))))
        
    #     # corner intersection
    #     pg1=Polygon2D(Point2D(1,0),
    #                         Point2D(2,0),
    #                         Point2D(2,0.5),
    #                         Point2D(1,0.5))
    #     self.assertEqual(pg.difference_simple_polygon_interior(pg1),
    #                      Polygons(Polygon2D(Point2D(2.0,0.5),
    #                                                     Point2D(2,1),
    #                                                     Point2D(0,1),
    #                                                     Point2D(0,0),
    #                                                     Point2D(1.0,0.0),
    #                                                     Point2D(1,0.5))))
        
    #     # mid intersection
    #     pg1=Polygon2D(Point2D(0.5,0),
    #                         Point2D(1.5,0),
    #                         Point2D(1.5,1),
    #                         Point2D(0.5,1))
    #     self.assertEqual(pg.difference_simple_polygon_interior(pg1),
    #                      Polygons(Polygon2D(Point2D(0.5,1.0),
    #                                                     Point2D(0,1),
    #                                                     Point2D(0,0),
    #                                                     Point2D(0.5,0.0)), 
    #                                     Polygon2D(Point2D(1.5,0.0),
    #                                                     Point2D(2,0),
    #                                                     Point2D(2,1),
    #                                                     Point2D(1.5,1.0))))
        
    #     # interior intersection
    #     pg1=Polygon2D(Point2D(0.25,0.25),
    #                         Point2D(1.75,0.25),
    #                         Point2D(1.75,0.75),
    #                         Point2D(0.25,0.75))
    #     # NOT IMPLEMENTED AT PRESENT AS THIS CREATES A POLYGON WITH A HOLE
    #     #print(pg.difference_simple_polygon_interior(pg1))
          
        
        
    # def test_is_adjacent(self):
    #     ""
    #     pr=Parallelogram2D(Point2D(0,0),Vector2D(1,0),Vector2D(0,1))
        
    #     # no intersection
    #     pr1=Parallelogram2D(Point2D(0,10), Vector2D(1,0), Vector2D(0,1))
    #     self.assertFalse(pr.is_adjacent(pr1))
        
    #     # point intersection
    #     pr1=Parallelogram2D(Point2D(1,1), Vector2D(1,0), Vector2D(0,1))
    #     self.assertFalse(pr.is_adjacent(pr1))
        
    #     # segment intersection
    #     pr1=Parallelogram2D(Point2D(0,1), Vector2D(1,0), Vector2D(0,1))
    #     self.assertTrue(pr.is_adjacent(pr1))
                
        
    # def test_intersect_simple_convex_polygon(self):
    #     ""
    #     # SQUARE
    #     sp=Polygon2D(Point2D(0,0),Point2D(1,0),Point2D(1,1),Point2D(0,1))
        
    #     # no intersection
    #     scp=SimpleConvexPolygon2D(Point2D(2,0),Point2D(3,0),Point2D(3,1),Point2D(2,1))
    #     self.assertEqual(sp.intersect_simple_convex_polygon(scp),
    #                      (Points(), 
    #                       Segments(), 
    #                       Polygons()))
        
    #     # point intersection
    #     scp=SimpleConvexPolygon2D(Point2D(1,1),Point2D(2,1),Point2D(2,2),Point2D(1,2))
    #     self.assertEqual(sp.intersect_simple_convex_polygon(scp),
    #                      (Points(Point2D(1,1)), 
    #                       Segments(), 
    #                       Polygons()))
        
    #     # edge intersection
    #     scp=SimpleConvexPolygon2D(Point2D(1,0),Point2D(2,0),Point2D(2,1),Point2D(1,1))
    #     self.assertEqual(sp.intersect_simple_convex_polygon(scp),
    #                      (Points(), 
    #                       Segments(Segment2D(Point2D(1.0,1.0), 
    #                                          Point2D(1.0,0.0))), 
    #                       Polygons()))
                     
    #     # self intersection
    #     scp=SimpleConvexPolygon2D(Point2D(0,0),Point2D(1,0),Point2D(1,1),Point2D(0,1))
    #     self.assertEqual(sp.intersect_simple_convex_polygon(scp),
    #                      (Points(), 
    #                       Segments(), 
    #                       Polygons(sp)))
        
    #     # mid intersection
    #     scp=SimpleConvexPolygon2D(Point2D(0.5,0),Point2D(1,0),Point2D(1,1),Point2D(0.5,1))
    #     self.assertEqual(sp.intersect_simple_convex_polygon(scp),
    #                      (Points(), 
    #                       Segments(), 
    #                       Polygons(Polygon2D(Point2D(0.5,0.0),
    #                                                      Point2D(1.0,0.0),
    #                                                      Point2D(1.0,1.0),
    #                                                      Point2D(0.5,1)))))
        
    #     # C-SHAPE
    #     sp=Polygon2D(Point2D(0,0),
    #                        Point2D(2,0),
    #                        Point2D(2,1),
    #                        Point2D(1,1),
    #                        Point2D(1,2),
    #                        Point2D(2,2),
    #                        Point2D(2,3),
    #                        Point2D(0,3))
        
    #     # two polygon intersection
    #     scp=SimpleConvexPolygon2D(Point2D(1,0),
    #                               Point2D(2,0),
    #                               Point2D(2,3),
    #                               Point2D(1,3))
    #     self.assertEqual(sp.intersect_simple_convex_polygon(scp),
    #                      (Points(), 
    #                       Segments(Segment2D(Point2D(1.0,2.0), 
    #                                          Point2D(1.0,1.0))), 
    #                       Polygons(Polygon2D(Point2D(1.0,0.0),
    #                                                      Point2D(2.0,0.0),
    #                                                      Point2D(2.0,1.0),
    #                                                      Point2D(1.0,1.0)), 
    #                                      Polygon2D(Point2D(1.0,2.0),
    #                                                      Point2D(2.0,2.0),
    #                                                      Point2D(2.0,3.0),
    #                                                      Point2D(1,3)))))
        

    # def test_intersect_simple_polygon(self):
    #     ""
    #     # SQUARE
    #     sp=Polygon2D(Point2D(0,0),Point2D(1,0),Point2D(1,1),Point2D(0,1))
        
    #     # no intersection
    #     sp1=Polygon2D(Point2D(2,0),Point2D(3,0),Point2D(3,1),Point2D(2,1))
    #     self.assertEqual(sp.intersect_simple_polygon(sp1),
    #                      (Points(), 
    #                       Segments(), 
    #                       Polygons()))
        
    #     # point intersection
    #     sp1=Polygon2D(Point2D(1,1),Point2D(2,1),Point2D(2,2),Point2D(1,2))
    #     self.assertEqual(sp.intersect_simple_polygon(sp1),
    #                      (Points(Point2D(1,1)), 
    #                       Segments(), 
    #                       Polygons()))
        
    #     # edge intersection
    #     sp1=Polygon2D(Point2D(1,0),Point2D(2,0),Point2D(2,1),Point2D(1,1))
    #     self.assertEqual(sp.intersect_simple_polygon(sp1),
    #                      (Points(), 
    #                       Segments(Segment2D(Point2D(1.0,1.0), 
    #                                          Point2D(1.0,0.0))), 
    #                       Polygons()))
                     
    #     # self intersection
    #     sp1=Polygon2D(Point2D(0,0),Point2D(1,0),Point2D(1,1),Point2D(0,1))
    #     self.assertEqual(sp.intersect_simple_polygon(sp1),
    #                      (Points(), 
    #                       Segments(), 
    #                       Polygons(sp)))
        
    #     # mid intersection
    #     sp1=Polygon2D(Point2D(0.5,0),Point2D(1,0),Point2D(1,1),Point2D(0.5,1))
    #     self.assertEqual(sp.intersect_simple_polygon(sp1),
    #                      (Points(Point2D(1.0,0.0)), 
    #                       Segments(), 
    #                       Polygons(Polygon2D(Point2D(0.5,0.0),
    #                                                      Point2D(1.0,0.0),
    #                                                      Point2D(1.0,1.0),
    #                                                      Point2D(0.5,1)))))
        
    #     # C-SHAPE
    #     sp=Polygon2D(Point2D(0,0),
    #                        Point2D(2,0),
    #                        Point2D(2,1),
    #                        Point2D(1,1),
    #                        Point2D(1,2),
    #                        Point2D(2,2),
    #                        Point2D(2,3),
    #                        Point2D(0,3))
        
    #     # two polygon intersection
    #     sp1=Polygon2D(Point2D(1,0),
    #                         Point2D(2,0),
    #                         Point2D(2,3),
    #                         Point2D(1,3))
    #     self.assertEqual(sp.intersect_simple_polygon(sp1),
    #                      (Points(), 
    #                       Segments(Segment2D(Point2D(1.0,2.0), 
    #                                          Point2D(1.0,1.0))), 
    #                       Polygons(Polygon2D(Point2D(1.0,0.0),
    #                                                      Point2D(2.0,0.0),
    #                                                      Point2D(2.0,1.0),
    #                                                      Point2D(1.0,1.0)), 
    #                                      Polygon2D(Point2D(1.0,2.0),
    #                                                      Point2D(2.0,2.0),
    #                                                      Point2D(2.0,3.0),
    #                                                      Point2D(1,3)))))
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
        
    def test_union_adjacent_simple_polygon(self):
        ""
        
        
        
#    def test_intersect_simple_polygon__triangle(self):
#        ""
#        tr=Triangle2D(Point2D(0,0),Vector2D(1,0),Vector2D(0.5,1))
#        
#        # no intersection
#        tr1=Triangle2D(Point2D(0,10), Vector2D(1,10), Vector2D(0.5,10))
#        self.assertEqual(tr.intersect_simple_polygon(tr1),
#                         (Points(), 
#                          Segments(), 
#                          Polygons()))
#        
#        # point intersection
#        tr1=Triangle2D(Point2D(1,0), Vector2D(2,0), Vector2D(1.5,1))
#        self.assertEqual(tr.intersect_simple_polygon(tr1),
#                         (Points(Point2D(1,0)), 
#                          Segments(), 
#                          Polygons()))
#                
#        # segment intersection
#        tr1=Triangle2D(Point2D(0,0), Vector2D(1,0), Vector2D(0.5,-1))
#        self.assertEqual(tr.intersect_simple_polygon(tr1),
#                         (Points(), 
#                          Segments(Segment2D(Point2D(0,0),
#                                             Point2D(1,0))), 
#                          Polygons()))
#        
#        # polygon intersetion - self
#        self.assertEqual(tr.intersect_simple_polygon(tr),
#                         (Points(), 
#                          Segments(), 
#                          Polygons(tr)))
#        
#        # polygon intersetion - overlap - result is a triangle
#        tr1=Triangle2D(Point2D(0.5,0), Vector2D(1,0), Vector2D(0.5,1))
#        self.assertEqual(tr.intersect_simple_polygon(tr1),
#                         (Points(), 
#                          Segments(), 
#                          Polygons(SimpleConvexPolygon2D(Point2D(0.75,0.5),
#                                                               Point2D(0.5,0.0),
#                                                               Point2D(1.0,0.0)))))
#        
#        # polygon intersetion - overlap - result is a parallelogram
#        tr1=Triangle2D(Point2D(0,1), Vector2D(1,0), Vector2D(0.5,-1))
#        self.assertEqual(tr.intersect_simple_polygon(tr1),
#                         (Points(), 
#                          Segments(), 
#                          Polygons(SimpleConvexPolygon2D(Point2D(0.25,0.5),
#                                               Point2D(0.5,0.0),
#                                               Point2D(0.75,0.5),
#                                               Point2D(0.5,1.0)))))
#        
#    def test_intersect_simple_polygon__parallelogram(self):
#        ""
#        pr=Parallelogram2D(Point2D(0,0),Vector2D(1,0),Vector2D(0,1))
#        
#        # no intersection
#        pr1=Parallelogram2D(Point2D(0,10), Vector2D(1,0), Vector2D(0,1))
#        self.assertEqual(pr.intersect_simple_polygon(pr1),
#                         (Points(), 
#                          Segments(), 
#                          Polygons()))
#        
#        # point intersection
#        pr1=Parallelogram2D(Point2D(1,1), Vector2D(1,0), Vector2D(0,1))
#        self.assertEqual(pr.intersect_simple_polygon(pr1),
#                         (Points(Point2D(1,1)), 
#                          Segments(), 
#                          Polygons()))
#        
#        # segment intersection
#        pr1=Parallelogram2D(Point2D(0,1), Vector2D(1,0), Vector2D(0,1))
#        self.assertEqual(pr.intersect_simple_polygon(pr1),
#                         (Points(), 
#                          Segments(Segment2D(Point2D(0,1),
#                                             Point2D(1,1))), 
#                          Polygons()))
#        
#        # polygon intersection - self
#        #print(pr.intersect_simple_polygon(pr))
#        return
#        self.assertEqual(pr.intersect_simple_polygon(pr),
#                         (Points(), 
#                          Segments(), 
#                          Polygons(pr)))
#        
        
#    def test_intersect_halfline(self):
#        ""
#        pg=Polygon2D(*points)
#        
#        # convex polygon
#        
#        print(pg.intersect_halfline(Halfline2D(Point2D(0,0),
#                                                          Vector2D(1,1))))
#        
#        return
#        
#        self.assertEqual(pg.intersect_halfline(Halfline2D(Point2D(0,0),
#                                                          Vector2D(1,1))),
#                         ([], 
#                          [Segment2D(Point2D(0.0,0.0), 
#                                     Point2D(1.0,1.0))]))        
#        
#        self.assertEqual(pg.intersect_halfline(Halfline2D(Point2D(0,0),
#                                                          Vector2D(1,-1))),
#                         ([Point2D(0,0)], 
#                          []))     
#    
#        self.assertEqual(pg.intersect_halfline(Halfline2D(Point2D(0.5,0.5),
#                                                          Vector2D(1,1))),
#                         ([], 
#                          [Segment2D(Point2D(0.5,0.5), 
#                                     Point2D(1.0,1.0))]))    
#            
#        # concave polygon
#        pg=Polygon2D(Point2D(0,0),
#                     Point2D(2,0),
#                     Point2D(1,1),
#                     Point2D(2,2),
#                     Point2D(0,2))
#        
#        self.assertEqual(pg.intersect_halfline(Halfline2D(Point2D(1.5,0),
#                                                          Vector2D(0,1))),
#                         ([], 
#                          [Segment2D(Point2D(1.5,0), 
#                                     Point2D(1.5,0.5)),
#                           Segment2D(Point2D(1.5,1.5), 
#                                     Point2D(1.5,2))]))  
#    
#        self.assertEqual(pg.intersect_halfline(Halfline2D(Point2D(2,0),
#                                                          Vector2D(0,1))),
#                         ([Point2D(2,0),
#                           Point2D(2,2)], 
#                          []))  
#    
#        self.assertEqual(pg.intersect_halfline(Halfline2D(Point2D(1,0),
#                                                          Vector2D(0,1))),
#                         ([], 
#                          [Segment2D(Point2D(1,0), 
#                                     Point2D(1,2))]))  
#    
#        self.assertEqual(pg.intersect_halfline(Halfline2D(Point2D(0,0),
#                                                          Vector2D(0,1))),
#                         ([], 
#                          [Segment2D(Point2D(0,0), 
#                                     Point2D(0,2))]))  
#    
#        self.assertEqual(pg.intersect_halfline(Halfline2D(Point2D(0,0.5),
#                                                          Vector2D(1,0))),
#                         ([], 
#                          [Segment2D(Point2D(0,0.5), 
#                                     Point2D(1.5,0.5))]))  
#        
#        
#    def test_intersect_line(self):
#        ""
#        pg=Polygon2D(*points)
#        
#        # convex polygon
#        self.assertEqual(pg.intersect_line(Line2D(Point2D(0,0),
#                                                  Vector2D(1,1))),
#                         ([], 
#                          [Segment2D(Point2D(0.0,0.0), 
#                                     Point2D(1.0,1.0))]))        
#        
#        self.assertEqual(pg.intersect_line(Line2D(Point2D(0,0),
#                                                  Vector2D(1,-1))),
#                         ([Point2D(0,0)], 
#                          []))     
#        
#            
#        # concave polygon
#        pg=Polygon2D(Point2D(0,0),
#                     Point2D(2,0),
#                     Point2D(1,1),
#                     Point2D(2,2),
#                     Point2D(0,2))
#        
#        self.assertEqual(pg.intersect_line(Line2D(Point2D(1.5,0),
#                                                  Vector2D(0,1))),
#                         ([], 
#                          [Segment2D(Point2D(1.5,0), 
#                                     Point2D(1.5,0.5)),
#                           Segment2D(Point2D(1.5,1.5), 
#                                     Point2D(1.5,2))]))  
#    
#        self.assertEqual(pg.intersect_line(Line2D(Point2D(2,0),
#                                                  Vector2D(0,1))),
#                         ([Point2D(2,0),
#                           Point2D(2,2)], 
#                          []))  
#    
#        self.assertEqual(pg.intersect_line(Line2D(Point2D(1,0),
#                                                  Vector2D(0,1))),
#                         ([], 
#                          [Segment2D(Point2D(1,0), 
#                                     Point2D(1,2))]))  
#    
#        self.assertEqual(pg.intersect_line(Line2D(Point2D(0,0),
#                                                  Vector2D(0,1))),
#                         ([], 
#                          [Segment2D(Point2D(0,0), 
#                                     Point2D(0,2))]))  
#    
#        self.assertEqual(pg.intersect_line(Line2D(Point2D(0,0.5),
#                                                  Vector2D(1,0))),
#                         ([], 
#                          [Segment2D(Point2D(0,0.5), 
#                                     Point2D(1.5,0.5))]))  
#    
#    

#    def test_intersect_polygon(self):
#        ""
#        pg=Polygon2D(*points)
#        
#        # no intersection
#        pg1=Polygon2D(Point2D(-2,0),
#                       Point2D(-1,0),
#                       Point2D(-1,1),
#                       Point2D(-2,1))
#        self.assertEqual(pg.intersect_polygon(pg1),
#                         ([],
#                          []))
#        
#        # point intersection
#        pg1=Polygon2D(Point2D(-1,-1),
#                      Point2D(0,-1),
#                      Point2D(0,0),
#                      Point2D(-1,0))
#        self.assertEqual(pg.intersect_polygon(pg1),
#                         ([Point2D(0,0)],
#                         []))
#    
#        # edge intersection
#        pg1=Polygon2D(Point2D(-1,0),
#                      Point2D(0,0),
#                      Point2D(0,1),
#                      Point2D(-1,1))
#        self.assertEqual(pg.intersect_polygon(pg1),
#                         ([],
#                         [Segment2D(Point2D(0,0),Point2D(0,1))]))
#        
#        # overlap intersection - same polygon
#        self.assertEqual(pg.intersect_polygon(pg),
#                         ([], 
#                          [Segment2D(Point2D(0.0,0.0), Point2D(0.0,1.0)), 
#                           Segment2D(Point2D(0.0,0.0), Point2D(1.0,0.0)), 
#                           Segment2D(Point2D(0.0,1.0), Point2D(1.0,1.0)), 
#                           Segment2D(Point2D(1.0,0.0), Point2D(1.0,1.0))]))  
#        
#        # overlap intersection
#        pg1=Polygon2D(Point2D(-0.5,-0.5),
#                      Point2D(0.5,-0.5),
#                      Point2D(0.5,0.5),
#                      Point2D(-0.5,0.5))
#        self.assertEqual(pg.intersect_polygon(pg1),
#                         ([],
#                          [Segment2D(Point2D(0,0.5), Point2D(0.5,0.5)), 
#                           Segment2D(Point2D(0.5,0), Point2D(0.5,0.5))]))  
#        self.assertEqual(pg1.intersect_polygon(pg),
#                         ([],
#                          [Segment2D(Point2D(0,0), Point2D(0,0.5)), 
#                           Segment2D(Point2D(0,0), Point2D(0.5,0))]))  
#    
#    

        
    
        
    
    
        
# class Test_Polygon3D(unittest.TestCase):
#     """
#     points=(Point3D(0,0,0),Point3D(1,0,0),Point3D(1,1,0),Point3D(0,1,0))
#     """
    
#     def test___init__(self):
#         ""
#         pg=Polygon3D(*points)
#         self.assertIsInstance(pg,Polygon3D)
#         self.assertEqual(pg.points,points)
        
        
#     def test___contains__(self):
#         ""
#         pg=Polygon3D(*points)
        
#         # Point
        
#         # --> TO DO
        
#         # Segment
        
#         # Polygon
        
        
#     def test___eq__(self):
#         ""
#         pg=Polygon3D(*points)
#         self.assertTrue(pg==pg)
        
#         pg2=Polygon3D(Point3D(0,0,0),Point3D(1,0,0),Point3D(0,1,0))
#         self.assertFalse(pg==pg2)
        
        
#     def test___repr__(self):
#         ""
#         pg=Polygon3D(*points)
#         self.assertEqual(str(pg),
#                          'Polygon3D(Point3D(0,0,0),Point3D(1,0,0),Point3D(1,1,0),Point3D(0,1,0))')
        
#     def test_area(self):
#         ""
#         pg=Polygon3D(*points)
#         self.assertEqual(pg.area, # ccw
#                          1)
#         self.assertEqual(pg.reverse.area, # cw
#                          1)
        
        
#     def test_centroid(self):
#         ""
#         pg=Polygon3D(*points)
#         self.assertEqual(pg.centroid, 
#                          Point3D(0.5,0.5,0))
        
        
#     def test_next_index(self):
#         ""
#         pg=Polygon3D(*points)
#         self.assertEqual(pg.next_index(0),
#                          1)
#         self.assertEqual(pg.next_index(3),
#                          0)
        
    
#     def test_plane(self):
#         ""
#         pg=Polygon3D(*points)
#         self.assertEqual(pg.plane,
#                          Plane3D(Point3D(0,0,0),Vector3D(0,0,1)))
        
        
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
            
        
        
#     def test_prevous_index(self):
#         ""
#         pg=Polygon3D(*points)
#         self.assertEqual(pg.previous_index(0),
#                          3)
#         self.assertEqual(pg.previous_index(3),
#                          2)
        
        
#     def test_project_2D(self):
#         ""
#         pg=Polygon3D(*points)
#         self.assertEqual(pg.project_2D,
#                          (2,Polygon2D(Point2D(0,0),Point2D(1,0),Point2D(1,1),Point2D(0,1))))
        
        
#     def test_reorder(self):
#         ""
#         pg=Polygon3D(*points)
#         self.assertEqual(pg.reorder(1),
#                          Polygon3D(Point3D(1,0,0),
#                                    Point3D(1,1,0),
#                                    Point3D(0,1,0),
#                                    Point3D(0,0,0)))
        
        
#     def test_reverse(self):
#         ""
#         pg=Polygon3D(*points)
#         self.assertEqual(pg.reverse,
#                          Polygon3D(Point3D(0,1,0),
#                                    Point3D(1,1,0),
#                                    Point3D(1,0,0),
#                                    Point3D(0,0,0)))
        
        
#     def test_triangulate(self):
#         ""
#         # convex polygon
#         pg=Polygon3D(*points)
#         self.assertEqual(pg.triangulate,
#                          Triangles(*[Triangle3D(Point3D(0,0,0), Vector3D(1,0,0), Vector3D(0,1,0)), 
#                                      Triangle3D(Point3D(1,0,0), Vector3D(0,1,0), Vector3D(-1,1,0))]))
        
#         # concave polygon
#         pg=Polygon3D(Point3D(0,0,2),
#                      Point3D(2,0,2),
#                      Point3D(1,1,2),
#                      Point3D(2,2,2),
#                      Point3D(0,2,2))
#         self.assertEqual(pg.triangulate,
#                          Triangles(*[Triangle3D(Point3D(2,0,2), Vector3D(-1,1,0), Vector3D(-2,0,0)), 
#                                      Triangle3D(Point3D(0,0,2), Vector3D(1,1,0), Vector3D(0,2,0)), 
#                                      Triangle3D(Point3D(1,1,2), Vector3D(1,1,0), Vector3D(-1,1,0))]))
        
        
    
if __name__=='__main__':
    
    points2d=(Point2D(0,0),Point2D(1,0),Point2D(1,1),Point2D(0,1))
    points3d=(Point3D(0,0,0),Point3D(1,0,0),Point3D(1,1,0),Point3D(0,1,0))
    
    #cProfile.run('unittest.main(Test_Polygon())')
    
    unittest.main(Test_Polygon())
    
    unittest.main(Test_Polygon2D())
    
    # points=(Point3D(0,0,0),Point3D(1,0,0),Point3D(1,1,0),Point3D(0,1,0))
    # unittest.main(Test_Polygon3D())
    
    