# -*- coding: utf-8 -*-

import unittest
from crossproduct import Point2D, Point3D, Halfline2D, Halfline3D, \
    Vector2D, Vector3D, Line2D, Line3D, SimpleConvexPolygon2D, SimpleConvexPolygon3D, Plane3D, Segment2D, Segment3D, \
    SimplePolyline2D, SimplePolyline3D, Points, Segments, Polylines, SimplePolygons
    

class Test_SimpleConvexPolygon2D(unittest.TestCase):
    """
    points=(Point2D(0,0),Point2D(1,0),Point2D(1,1),Point2D(0,1))
    """
    
    def test___init__(self):
        ""
        pg=SimpleConvexPolygon2D(*points)
        self.assertIsInstance(pg,SimpleConvexPolygon2D)
        self.assertEqual(pg.points,points)
        
        
    def test_intersect_halfline(self):
        ""
        pg=SimpleConvexPolygon2D(*points)
        
        self.assertEqual(pg.intersect_halfline(Halfline2D(Point2D(0,0),
                                                          Vector2D(1,0))),
                         (Points(),
                          Segments(Segment2D(Point2D(0,0),
                                             Point2D(1,0)))))
        self.assertEqual(pg.intersect_halfline(Halfline2D(Point2D(-1,0.5),
                                                          Vector2D(1,0))),
                         (Points(),
                          Segments(Segment2D(Point2D(0,0.5),
                                              Point2D(1,0.5)))))
        self.assertEqual(pg.intersect_halfline(Halfline2D(Point2D(0,-0.5),
                                                          Vector2D(1,0))),
                         (Points(),
                          Segments()))
        self.assertEqual(pg.intersect_halfline(Halfline2D(Point2D(0,0),
                                                          Vector2D(-1,1))),
                         (Points(Point2D(0,0)),
                          Segments()))
        self.assertEqual(pg.intersect_halfline(Halfline2D(Point2D(2,0),
                                                          Vector2D(1,0))),
                         (Points(),
                          Segments()))
        self.assertEqual(pg.intersect_halfline(Halfline2D(Point2D(0.5,0.5),
                                                          Vector2D(1,0))),
                         (Points(),
                          Segments(Segment2D(Point2D(0.5,0.5),
                                             Point2D(1,0.5)))))
        self.assertEqual(pg.intersect_halfline(Halfline2D(Point2D(-1,1),
                                                          Vector2D(-1,1))),
                         (Points(),
                          Segments()))
    
        
    def test_intersect_line(self):
        ""
        pg=SimpleConvexPolygon2D(*points)
        
        self.assertEqual(pg.intersect_line(Line2D(Point2D(0,0),
                                                  Vector2D(1,0))),
                         (Points(),
                          Segments(Segment2D(Point2D(0,0),
                                             Point2D(1,0)))))
        self.assertEqual(pg.intersect_line(Line2D(Point2D(-1,0.5),
                                                  Vector2D(1,0))),
                         (Points(),
                          Segments(Segment2D(Point2D(0,0.5),
                                             Point2D(1,0.5)))))
        self.assertEqual(pg.intersect_line(Line2D(Point2D(0,-0.5),
                                                  Vector2D(1,0))),
                         (Points(),
                          Segments()))
        self.assertEqual(pg.intersect_line(Line2D(Point2D(0,0),
                                                  Vector2D(-1,1))),
                         (Points(Point2D(0,0)),
                          Segments()))
        
        
    def test_intersect_line_t_values(self):
        ""
        pg=SimpleConvexPolygon2D(*points)
        
        self.assertEqual(pg.intersect_line_t_values(Line2D(Point2D(0,0),
                                                           Vector2D(1,0))),
                         [0,1])
        self.assertEqual(pg.intersect_line_t_values(Line2D(Point2D(-1,0.5),
                                                           Vector2D(1,0))),
                         [1,2])
        self.assertEqual(pg.intersect_line_t_values(Line2D(Point2D(0,-0.5),
                                                           Vector2D(1,0))),
                         [])
        self.assertEqual(pg.intersect_line_t_values(Line2D(Point2D(0,0),
                                                           Vector2D(-1,1))),
                         [0])    
        
    
    def test_intersect_segment(self):
        ""
        pg=SimpleConvexPolygon2D(*points)
        
        self.assertEqual(pg.intersect_segment(Segment2D(Point2D(0,0),
                                                        Point2D(1,0))),
                         (Points(),
                          Segments(Segment2D(Point2D(0,0),
                                            Point2D(1,0)))))
        self.assertEqual(pg.intersect_segment(Segment2D(Point2D(-1,0.5),
                                                        Point2D(2,0.5))),
                         (Points(),
                          Segments(Segment2D(Point2D(0,0.5),
                                             Point2D(1,0.5)))))
        self.assertEqual(pg.intersect_segment(Segment2D(Point2D(0,-0.5),
                                                        Point2D(1,-0.5))),
                         (Points(),
                          Segments()))
        self.assertEqual(pg.intersect_segment(Segment2D(Point2D(0,0),
                                                        Point2D(-1,1))),
                         (Points(Point2D(0,0)),
                          Segments()))
        self.assertEqual(pg.intersect_segment(Segment2D(Point2D(1,0),
                                                        Point2D(2,0))),
                         (Points(Point2D(1,0)),
                          Segments()))
        self.assertEqual(pg.intersect_segment(Segment2D(Point2D(0.5,0.5),
                                                        Point2D(1.5,0.5))),
                         (Points(),
                          Segments(Segment2D(Point2D(0.5,0.5),
                                             Point2D(1,0.5)))))
        self.assertEqual(pg.intersect_segment(Segment2D(Point2D(-0.5,0.5),
                                                        Point2D(0.5,0.5))),
                         (Points(),
                          Segments(Segment2D(Point2D(0,0.5),
                                             Point2D(0.5,0.5)))))
        self.assertEqual(pg.intersect_segment(Segment2D(Point2D(0,0.25),
                                                        Point2D(0,0.75))),
                         (Points(),
                          Segments(Segment2D(Point2D(0,0.25),
                                             Point2D(0,0.75)))))
    
    
    def test_intersect_simple_convex_polygon(self):
        ""
        pg=SimpleConvexPolygon2D(*points)
        
        # no intersection
        pg1=SimpleConvexPolygon2D(Point2D(-2,0),
                                  Point2D(-1,0),
                                  Point2D(-1,1),
                                  Point2D(-2,1))
        
        self.assertEqual(pg.intersect_simple_convex_polygon(pg1),
                         (Points(),
                          Segments()))
        
        # point intersection
        pg1=SimpleConvexPolygon2D(Point2D(-1,-1),
                                  Point2D(0,-1),
                                  Point2D(0,0),
                                  Point2D(-1,0))
        
        self.assertEqual(pg.intersect_simple_convex_polygon(pg1),
                         (Points(Point2D(0,0)),
                          Segments()))
    
        # edge intersection
        pg1=SimpleConvexPolygon2D(Point2D(-1,0),
                                  Point2D(0,0),
                                  Point2D(0,1),
                                  Point2D(-1,1))
        
        self.assertEqual(pg.intersect_simple_convex_polygon(pg1),
                         (Points(),
                          Segments(Segment2D(Point2D(0,0),
                                             Point2D(0,1)))))
        
        # overlap intersection - same polygon
        self.assertEqual(pg.intersect_simple_convex_polygon(pg),
                         (Points(),
                          pg.polyline.segments))
    
        
        # overlap intersection
        pg1=SimpleConvexPolygon2D(Point2D(-0.5,-0.5),
                                  Point2D(0.5,-0.5),
                                  Point2D(0.5,0.5),
                                  Point2D(-0.5,0.5))
        
        self.assertEqual(pg.intersect_simple_convex_polygon(pg1),
                         (Points(),
                          Segments(Segment2D(Point2D(0.5,0),
                                             Point2D(0.5,0.5)),
                                   Segment2D(Point2D(0.5,0.5),
                                             Point2D(0,0.5)))))
        
        self.assertEqual(pg1.intersect_simple_convex_polygon(pg),
                         (Points(), 
                          Segments(Segment2D(Point2D(0,0), 
                                             Point2D(0.5,0.0)), 
                                   Segment2D(Point2D(0.0,0.5), 
                                             Point2D(0,0)))))
        
        
    def test_union_simple_convex_polygon(self):
        ""
        pg=SimpleConvexPolygon2D(*points)
        
        # no intersection
        pg1=SimpleConvexPolygon2D(Point2D(-2,0),
                                  Point2D(-1,0),
                                  Point2D(-1,1),
                                  Point2D(-2,1))
        self.assertEqual(pg.union_simple_convex_polygon(pg1),
                         (Points(), 
                          Polylines(), 
                          SimplePolygons()))

        # point intersection
        pg1=SimpleConvexPolygon2D(Point2D(-1,-1),
                                  Point2D(0,-1),
                                  Point2D(0,0),
                                  Point2D(-1,0))
        self.assertEqual(pg.union_simple_convex_polygon(pg1),
                         (Points(Point2D(0,0)), 
                          Polylines(), 
                          SimplePolygons()))
                         
                         
        # edge intersection
        pg1=SimpleConvexPolygon2D(Point2D(-1,0),
                            Point2D(0,0),
                            Point2D(0,1),
                            Point2D(-1,1))
        self.assertEqual(pg.union_simple_convex_polygon(pg1),
                         (Points(), 
                          Polylines(SimplePolyline2D(Point2D(0,0),
                                                     Point2D(0,1))), 
                          SimplePolygons()))
                         
                         
        
        # overlap intersection - same polygon
        self.assertEqual(pg.union_simple_convex_polygon(pg),
                         (Points(),
                          Polylines(),
                          SimplePolygons(pg)))

        # overlap intersection
        pg1=SimpleConvexPolygon2D(Point2D(-0.5,-0.5),
                            Point2D(0.5,-0.5),
                            Point2D(0.5,0.5),
                            Point2D(-0.5,0.5))
        self.assertEqual(pg.union_simple_convex_polygon(pg1),
                         (Points(),
                          Polylines(),
                          SimplePolygons(SimpleConvexPolygon2D(Point2D(0.5,0.0),
                                                               Point2D(0.5,0.5),
                                                               Point2D(0.0,0.5),
                                                               Point2D(0,0)))))
        
        
        
class Test_SimpleConvexPolygon3D(unittest.TestCase):
    """
    points=(Point3D(0,0,0),
            Point3D(1,0,0),
            Point3D(1,1,0),
            Point3D(0,1,0))
    """
    
    def test___init__(self):
        ""
        pg=SimpleConvexPolygon3D(*points)
        self.assertIsInstance(pg,SimpleConvexPolygon3D)
        self.assertEqual(pg.points,points)
        
        
    def test_intersect_halfline(self):
        ""
        pg=SimpleConvexPolygon3D(*points)
        
        self.assertEqual(pg.intersect_halfline(Halfline3D(Point3D(0,0,0),
                                                          Vector3D(1,0,0))),
                         (Points(),
                          Segments(Segment3D(Point3D(0,0,0),
                                             Point3D(1,0,0)))))
        self.assertEqual(pg.intersect_halfline(Halfline3D(Point3D(-1,0.5,0),
                                                          Vector3D(1,0,0))),
                         (Points(),
                          Segments(Segment3D(Point3D(0,0.5,0),
                                              Point3D(1,0.5,0)))))
        self.assertEqual(pg.intersect_halfline(Halfline3D(Point3D(0,-0.5,0),
                                                          Vector3D(1,0,0))),
                         (Points(),
                          Segments()))
        self.assertEqual(pg.intersect_halfline(Halfline3D(Point3D(0,0,0),
                                                          Vector3D(-1,1,0))),
                         (Points(Point3D(0,0,0)),
                          Segments()))
        self.assertEqual(pg.intersect_halfline(Halfline3D(Point3D(2,0,0),
                                                          Vector3D(1,0,0))),
                         (Points(),
                          Segments()))
        self.assertEqual(pg.intersect_halfline(Halfline3D(Point3D(0.5,0.5,0),
                                                          Vector3D(1,0,0))),
                         (Points(),
                          Segments(Segment3D(Point3D(0.5,0.5,0),
                                             Point3D(1,0.5,0)))))
        self.assertEqual(pg.intersect_halfline(Halfline3D(Point3D(-1,1,0),
                                                          Vector3D(-1,1,0))),
                         (Points(),
                          Segments()))
        
        
    def test_intersect_line(self):
        ""
        
        pg=SimpleConvexPolygon3D(*points)
        
        # no intersection -> parallel, non-coplanar
        self.assertEqual(pg.intersect_line(Line3D(Point3D(0,0,1),
                                                  Vector3D(1,0,0))),
                         (Points(),
                          Segments()))
        
        # no intersection -> skew, non-intersecting
        self.assertEqual(pg.intersect_line(Line3D(Point3D(-1,0,0),
                                                  Vector3D(0,0,1))),
                         (Points(),
                          Segments()))
    
        # segment intersection -> coplanar, intersects at 2 points
        self.assertEqual(pg.intersect_line(Line3D(Point3D(0,0,0),
                                                  Vector3D(1,1,0))),
                         (Points(),
                          Segments(Segment3D(Point3D(0,0,0),
                                             Point3D(1,1,0)))))
            
        # point intersection -> skew plane and line
        self.assertEqual(pg.intersect_line(Line3D(Point3D(0.5,0.5,0),
                                                  Vector3D(0,0,1))),
                         (Points(Point3D(0.5,0.5,0)),
                          Segments()))
            
        # -- note that this 'point intersection' returns None, as the 
        #   point is not considered inside the polygon if it's on the top or
        #   righthand edge
        self.assertEqual(pg.intersect_line(Line3D(Point3D(1,1,0),
                                                  Vector3D(0,0,1))),
                         (Points(),
                          Segments()))
            
            
        # point intersection -> coplanar, intersects at 1 point
        self.assertEqual(pg.intersect_line(Line3D(Point3D(1,1,0),
                                                  Vector3D(-1,1,0))),
                         (Points(Point3D(1,1,0)),
                          Segments()))
    
        
    def test_intersect_segment(self):
        ""
        pg=SimpleConvexPolygon3D(*points)
        
        self.assertEqual(pg.intersect_segment(Segment3D(Point3D(0,0,0),
                                                        Point3D(1,0,0))),
                         (Points(),
                          Segments(Segment3D(Point3D(0,0,0),
                                            Point3D(1,0,0)))))
        self.assertEqual(pg.intersect_segment(Segment3D(Point3D(-1,0.5,0),
                                                        Point3D(2,0.5,0))),
                         (Points(),
                          Segments(Segment3D(Point3D(0,0.5,0),
                                             Point3D(1,0.5,0)))))
        self.assertEqual(pg.intersect_segment(Segment3D(Point3D(0,-0.5,0),
                                                        Point3D(1,-0.5,0))),
                         (Points(),
                          Segments()))
        self.assertEqual(pg.intersect_segment(Segment3D(Point3D(0,0,0),
                                                        Point3D(-1,1,0))),
                         (Points(Point3D(0,0,0)),
                          Segments()))
        self.assertEqual(pg.intersect_segment(Segment3D(Point3D(1,0,0),
                                                        Point3D(2,0,0))),
                         (Points(Point3D(1,0,0)),
                          Segments()))
        self.assertEqual(pg.intersect_segment(Segment3D(Point3D(0.5,0.5,0),
                                                        Point3D(1.5,0.5,0))),
                         (Points(),
                          Segments(Segment3D(Point3D(0.5,0.5,0),
                                             Point3D(1,0.5,0)))))
        self.assertEqual(pg.intersect_segment(Segment3D(Point3D(-0.5,0.5,0),
                                                        Point3D(0.5,0.5,0))),
                         (Points(),
                          Segments(Segment3D(Point3D(0,0.5,0),
                                             Point3D(0.5,0.5,0)))))
        self.assertEqual(pg.intersect_segment(Segment3D(Point3D(0,0.25,0),
                                                        Point3D(0,0.75,0))),
                         (Points(),
                          Segments(Segment3D(Point3D(0,0.25,0),
                                             Point3D(0,0.75,0)))))
        
    
    def test_intersect_simple_convex_polygon(self):
        ""
        pg=SimpleConvexPolygon3D(*points)
        
        # no intersection - parallel but not coplanar
        pg1=SimpleConvexPolygon3D(Point3D(0,0,1),
                                  Point3D(1,0,1),
                                  Point3D(1,1,1),
                                  Point3D(0,1,1))
        self.assertEqual(pg.intersect_simple_convex_polygon(pg1),
                         (Points(), 
                          Segments()))
        
        # no intersection - coplanar
        pg1=SimpleConvexPolygon3D(Point3D(-2,0,0),
                                  Point3D(-1,0,0),
                                  Point3D(-1,1,0),
                                  Point3D(-2,1,0))
        self.assertEqual(pg.intersect_simple_convex_polygon(pg1),
                         (Points(), 
                          Segments()))
        
        # no intersection - skew
        pg1=SimpleConvexPolygon3D(Point3D(-1,0,0),
                                  Point3D(-1,1,0),
                                  Point3D(-1,1,1),
                                  Point3D(-1,0,1))
        self.assertEqual(pg.intersect_simple_convex_polygon(pg1),
                         (Points(), 
                          Segments()))
        
#        # point intersection - coplanar
        pg1=SimpleConvexPolygon3D(Point3D(-1,-1,0),
                                  Point3D(0,-1,0),
                                  Point3D(0,0,0),
                                  Point3D(-1,0,0))
        self.assertEqual(pg.intersect_simple_convex_polygon(pg1),
                         (Points(Point3D(0,0,0)), 
                          Segments()))
        
        # point intersection - skew
        pg1=SimpleConvexPolygon3D(Point3D(0,0,0),
                            Point3D(0,-1,0),
                            Point3D(0,-1,-1),
                            Point3D(0,0,-1))
        self.assertEqual(pg.intersect_simple_convex_polygon(pg1),
                         (Points(Point3D(0,0,0)), 
                          Segments()))
    
        # edge intersection - coplanar
        pg1=SimpleConvexPolygon3D(Point3D(-1,0,0),
                                  Point3D(0,0,0),
                                  Point3D(0,1,0),
                                  Point3D(-1,1,0))
        self.assertEqual(pg.intersect_simple_convex_polygon(pg1),
                         (Points(), 
                          Segments(Segment3D(Point3D(0,0,0),
                                             Point3D(0,1,0)))))
        
        # edge intersection - skew
        pg1=SimpleConvexPolygon3D(Point3D(0,0,0),
                                  Point3D(0,1,0),
                                  Point3D(0,1,1),
                                  Point3D(0,0,1))
        self.assertEqual(pg.intersect_simple_convex_polygon(pg1),
                         (Points(), 
                          Segments(Segment3D(Point3D(0,0,0),
                                             Point3D(0,1,0)))))
        
        # overlap intersection - same polygon
        self.assertEqual(pg.intersect_simple_convex_polygon(pg),
                         (Points(), 
                          pg.polyline.segments))
    
        
        # overlap intersection - coplanar
        pg1=SimpleConvexPolygon3D(Point3D(-0.5,-0.5,0),
                                  Point3D(0.5,-0.5,0),
                                  Point3D(0.5,0.5,0),
                                  Point3D(-0.5,0.5,0))
        self.assertEqual(pg.intersect_simple_convex_polygon(pg1),
                         (Points(), 
                          Segments(Segment3D(Point3D(0.5,0,0),
                                             Point3D(0.5,0.5,0)),
                                   Segment3D(Point3D(0.5,0.5,0),
                                             Point3D(0,0.5,0)))))
        
        self.assertEqual(pg1.intersect_simple_convex_polygon(pg),
                         (Points(), Segments(Segment3D(Point3D(0.0,0.0,0.0), 
                                                       Point3D(0.5,0.0,0.0)), 
                                             Segment3D(Point3D(0.0,0.5,0.0), 
                                                       Point3D(0.0,0.0,0.0)))))
                         

        # overlap intersection - skew - segment
        pg1=SimpleConvexPolygon3D(Point3D(0.5,0,-1),
                                  Point3D(0.5,0,1),
                                  Point3D(0.5,0.5,1),
                                  Point3D(0.5,0.5,-1))
        self.assertEqual(pg.intersect_simple_convex_polygon(pg1),
                         (Points(), 
                          Segments(Segment3D(Point3D(0.5,0,0),
                                             Point3D(0.5,0.5,0)))))
    
        #print(pg1.intersect_simple_convex_polygon(pg))
        #assert False
    
    
        # overlap intersection - skew - point
        pg1=SimpleConvexPolygon3D(Point3D(0.5,-0.5,-1),
                            Point3D(0.5,-0.5,1),
                            Point3D(0.5,0.5,1),
                            Point3D(0.5,0.5,-1))
        self.assertEqual(pg.intersect_simple_convex_polygon(pg1),
                         (Points(Point3D(0.5,0.5,0)),
                          Segments()))
    
    
    def test_union_simple_convex_polygon(self):
        ""
        pg=SimpleConvexPolygon3D(*points)
        
        # no union - parallel but not coplanar
        pg1=SimpleConvexPolygon3D(Point3D(0,0,1),
                                  Point3D(1,0,1),
                                  Point3D(1,1,1),
                                  Point3D(0,1,1))
        self.assertEqual(pg.union_simple_convex_polygon(pg1),
                         (Points(),
                          Polylines(),
                          SimplePolygons()))
        
        # no union - coplanar
        pg1=SimpleConvexPolygon3D(Point3D(-2,0,0),
                                  Point3D(-1,0,0),
                                  Point3D(-1,1,0),
                                  Point3D(-2,1,0))
        self.assertEqual(pg.union_simple_convex_polygon(pg1),
                         (Points(),
                          Polylines(),
                          SimplePolygons()))
        
        # no union - skew
        pg1=SimpleConvexPolygon3D(Point3D(-1,0,0),
                                  Point3D(-1,1,0),
                                  Point3D(-1,1,1),
                                  Point3D(-1,0,1))
        self.assertEqual(pg.union_simple_convex_polygon(pg1),
                         (Points(),
                          Polylines(),
                          SimplePolygons()))
        
        # point union - coplanar
        pg1=SimpleConvexPolygon3D(Point3D(-1,-1,0),
                                  Point3D(0,-1,0),
                                  Point3D(0,0,0),
                                  Point3D(-1,0,0))
        self.assertEqual(pg.union_simple_convex_polygon(pg1),
                         (Points(Point3D(0,0,0)),
                          Polylines(),
                          SimplePolygons()))
        
        # point union - skew
        pg1=SimpleConvexPolygon3D(Point3D(0,0,0),
                                  Point3D(0,-1,0),
                                  Point3D(0,-1,-1),
                                  Point3D(0,0,-1))
        self.assertEqual(pg.union_simple_convex_polygon(pg1),
                         (Points(Point3D(0,0,0)),
                          Polylines(),
                          SimplePolygons()))
    
        # edge union - coplanar
        pg1=SimpleConvexPolygon3D(Point3D(-1,0,0),
                                  Point3D(0,0,0),
                                  Point3D(0,1,0),
                                  Point3D(-1,1,0))
        self.assertEqual(pg.union_simple_convex_polygon(pg1),
                         (Points(),
                          Polylines(SimplePolyline3D(Point3D(0,0,0),
                                                     Point3D(0,1,0))),
                          SimplePolygons()))
        
        
        # edge union - skew
        pg1=SimpleConvexPolygon3D(Point3D(0,0,0),
                                  Point3D(0,1,0),
                                  Point3D(0,1,1),
                                  Point3D(0,0,1))
        self.assertEqual(pg.union_simple_convex_polygon(pg1),
                         (Points(),
                          Polylines(SimplePolyline3D(Point3D(0,0,0),
                                                     Point3D(0,1,0))),
                          SimplePolygons()))
        
        # overlap union - same polygon
        self.assertEqual(pg.union_simple_convex_polygon(pg),
                         (Points(),
                          Polylines(),
                          SimplePolygons(pg)))
        
        # overlap union - coplanar
        pg1=SimpleConvexPolygon3D(Point3D(-0.5,-0.5,0),
                                  Point3D(0.5,-0.5,0),
                                  Point3D(0.5,0.5,0),
                                  Point3D(-0.5,0.5,0))
        self.assertEqual(pg.union_simple_convex_polygon(pg1),
                         (Points(),
                          Polylines(),
                          SimplePolygons(SimpleConvexPolygon3D(Point3D(0.5,0,0),
                                                               Point3D(0.5,0.5,0),
                                                               Point3D(0,0.5,0),
                                                               Point3D(0,0,0)))))
                         
        
        self.assertEqual(pg1.union_simple_convex_polygon(pg),
                         (Points(),
                          Polylines(),
                          SimplePolygons(SimpleConvexPolygon3D(Point3D(0.5,0,0),
                                                               Point3D(0.5,0.5,0),
                                                               Point3D(0,0.5,0),
                                                               Point3D(0,0,0)))))
    
        # overlap union - skew - segment
        pg1=SimpleConvexPolygon3D(Point3D(0.5,0,-1),
                                  Point3D(0.5,0,1),
                                  Point3D(0.5,0.5,1),
                                  Point3D(0.5,0.5,-1))
        
        self.assertEqual(pg.union_simple_convex_polygon(pg1),
                         (Points(),
                          Polylines(SimplePolyline3D(Point3D(0.5,0,0),
                                                     Point3D(0.5,0.5,0))),
                          SimplePolygons()))
        
        # overlap union - skew - point
        pg1=SimpleConvexPolygon3D(Point3D(0.5,-0.5,-1),
                            Point3D(0.5,-0.5,1),
                            Point3D(0.5,0.5,1),
                            Point3D(0.5,0.5,-1))
        self.assertEqual(pg.union_simple_convex_polygon(pg1),
                         (Points(),
                          Polylines(SimplePolyline3D(Point3D(0.5,0,0),
                                                     Point3D(0.5,0.5,0))),
                          SimplePolygons()))
    
    
if __name__=='__main__':
    
    points=(Point2D(0,0),Point2D(1,0),Point2D(1,1),Point2D(0,1))
    unittest.main(Test_SimpleConvexPolygon2D())
    
    points=(Point3D(0,0,0),Point3D(1,0,0),Point3D(1,1,0),Point3D(0,1,0))
    unittest.main(Test_SimpleConvexPolygon3D())
    
    