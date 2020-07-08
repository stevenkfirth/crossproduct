# -*- coding: utf-8 -*-

import unittest
from crossproduct import Point2D, Point3D, Halfline2D, Halfline3D, \
    Vector2D, Vector3D, Line2D, Line3D, SimpleConvexPolygon2D, SimpleConvexPolygon3D, Plane3D, Segment2D, Segment3D, \
    SimplePolyline2D, SimplePolyline3D, Points, Segments, Polylines, SimplePolygons, SimplePolygon2D
    

class Test_SimpleConvexPolygon2D(unittest.TestCase):
    """
    points=(Point2D(0,0),Point2D(1,0),Point2D(1,1),Point2D(0,1))
    """
    
    def test___init__(self):
        ""
        pg=SimpleConvexPolygon2D(*points)
        self.assertIsInstance(pg,SimpleConvexPolygon2D)
        self.assertEqual(pg.points,points)
        
        # test to show merging of adjacent collinear segments
        pg1=SimpleConvexPolygon2D(*(Point2D(0,0),
                                    Point2D(0.5,0),
                                    Point2D(1,0),
                                    Point2D(1,1),
                                    Point2D(0,1)))
        
        self.assertEqual(pg1,pg)
        
        
    def test_difference_simple_convex_polygon(self):
        ""
        pg=SimpleConvexPolygon2D(*points)
        
        # self intersection - no difference
        self.assertEqual(pg.difference_simple_convex_polygon(pg),
                         None)
        
        # point intersection - difference is the polygon pg
        pg1=SimpleConvexPolygon2D(Point2D(1,1),
                                  Point2D(2,1),
                                  Point2D(2,2),
                                  Point2D(1,2))
        self.assertEqual(pg.difference_simple_convex_polygon(pg1),
                         pg)
        
        # edge intersection - difference is the polygon pg
        pg1=SimpleConvexPolygon2D(Point2D(1,0),
                                  Point2D(2,0),
                                  Point2D(2,1),
                                  Point2D(1,1))
        self.assertEqual(pg.difference_simple_convex_polygon(pg1),
                         pg)
                         
        
        # overlap intersection - difference is the remaining segments
        pg1=SimpleConvexPolygon2D(Point2D(0.5,0),
                                  Point2D(1.5,0),
                                  Point2D(1.5,1),
                                  Point2D(0.5,1))
        self.assertEqual(pg.difference_simple_convex_polygon(pg1),
                         SimpleConvexPolygon2D(Point2D(0,0),
                                               Point2D(0.5,0),
                                               Point2D(0.5,1),
                                               Point2D(0,1)))
        
        
    def test_intersect_halfline(self):
        ""
        pg=SimpleConvexPolygon2D(*points)
        
        self.assertEqual(pg.intersect_halfline(Halfline2D(Point2D(0,0),
                                                          Vector2D(1,0))),
                         Segment2D(Point2D(0,0),
                                   Point2D(1,0)))
        self.assertEqual(pg.intersect_halfline(Halfline2D(Point2D(-1,0.5),
                                                          Vector2D(1,0))),
                         Segment2D(Point2D(0,0.5),
                                   Point2D(1,0.5)))
        self.assertEqual(pg.intersect_halfline(Halfline2D(Point2D(0,-0.5),
                                                          Vector2D(1,0))),
                         None)
        self.assertEqual(pg.intersect_halfline(Halfline2D(Point2D(0,0),
                                                          Vector2D(-1,1))),
                         Point2D(0,0))
        self.assertEqual(pg.intersect_halfline(Halfline2D(Point2D(2,0),
                                                          Vector2D(1,0))),
                         None)
        self.assertEqual(pg.intersect_halfline(Halfline2D(Point2D(0.5,0.5),
                                                          Vector2D(1,0))),
                         Segment2D(Point2D(0.5,0.5),
                                   Point2D(1,0.5)))
        self.assertEqual(pg.intersect_halfline(Halfline2D(Point2D(-1,1),
                                                          Vector2D(-1,1))),
                         None)
    
        
    def test_intersect_line(self):
        ""
        pg=SimpleConvexPolygon2D(*points)
        
        self.assertEqual(pg.intersect_line(Line2D(Point2D(0,0),
                                                  Vector2D(1,0))),
                         Segment2D(Point2D(0,0),
                                    Point2D(1,0)))
        self.assertEqual(pg.intersect_line(Line2D(Point2D(-1,0.5),
                                                  Vector2D(1,0))),
                         Segment2D(Point2D(0,0.5),
                                   Point2D(1,0.5)))
        self.assertEqual(pg.intersect_line(Line2D(Point2D(0,-0.5),
                                                  Vector2D(1,0))),
                         None)
        self.assertEqual(pg.intersect_line(Line2D(Point2D(0,0),
                                                  Vector2D(-1,1))),
                         Point2D(0,0))
        
        
    def test_intersect_line_t_values(self):
        ""
        pg=SimpleConvexPolygon2D(*points)
        
        self.assertEqual(pg.intersect_line_t_values(Line2D(Point2D(0,0),
                                                           Vector2D(1,0))),
                         (0,1))
        self.assertEqual(pg.intersect_line_t_values(Line2D(Point2D(-1,0.5),
                                                           Vector2D(1,0))),
                         (1,2))
        self.assertEqual(pg.intersect_line_t_values(Line2D(Point2D(0,-0.5),
                                                           Vector2D(1,0))),
                         None)
        self.assertEqual(pg.intersect_line_t_values(Line2D(Point2D(0,0),
                                                           Vector2D(-1,1))),
                         (0,0))    
        
    
    def test_intersect_segment(self):
        ""
        pg=SimpleConvexPolygon2D(*points)
        
        # no intersection
        self.assertEqual(pg.intersect_segment(Segment2D(Point2D(0,-0.5),
                                                        Point2D(1,-0.5))),
                         None)
        
        # point intersection - bottom left
        self.assertEqual(pg.intersect_segment(Segment2D(Point2D(0,0),
                                                        Point2D(-1,1))),
                         Point2D(0,0))
            
        # point intersection - bottom right
        self.assertEqual(pg.intersect_segment(Segment2D(Point2D(1,0),
                                                        Point2D(2,0))),
                         Point2D(1,0))
        
        # segment edge intersection - bottom edge exact
        self.assertEqual(pg.intersect_segment(Segment2D(Point2D(0,0),
                                                        Point2D(1,0))),
                         Segment2D(Point2D(0,0),
                                   Point2D(1,0)))

        # segment interior intersection - horizontal from outside to outside
        self.assertEqual(pg.intersect_segment(Segment2D(Point2D(-1,0.5),
                                                        Point2D(2,0.5))),
                         Segment2D(Point2D(0,0.5),
                                   Point2D(1,0.5)))
        
        # segment interior intersection - horizontal from inside to outside
        self.assertEqual(pg.intersect_segment(Segment2D(Point2D(0.5,0.5),
                                                        Point2D(1.5,0.5))),
                         Segment2D(Point2D(0.5,0.5),
                                   Point2D(1,0.5)))         
        
        # segment interior intersection - vertical from outside to inside
        self.assertEqual(pg.intersect_segment(Segment2D(Point2D(-0.5,0.5),
                                                        Point2D(0.5,0.5))),
                         Segment2D(Point2D(0,0.5),
                                   Point2D(0.5,0.5)))
            
        # segment interior intersection - vertical from inside to inside
        self.assertEqual(pg.intersect_segment(Segment2D(Point2D(0,0.25),
                                                        Point2D(0,0.75))),
                         Segment2D(Point2D(0,0.25),
                                   Point2D(0,0.75)))
    
    
    def test_intersect_simple_convex_polygon(self):
        ""
        pg=SimpleConvexPolygon2D(*points)
        
        # no intersection
        pg1=SimpleConvexPolygon2D(Point2D(-2,0),
                                  Point2D(-1,0),
                                  Point2D(-1,1),
                                  Point2D(-2,1))
        self.assertEqual(pg.intersect_simple_convex_polygon(pg1),
                         None)
        
        # point intersection
        pg1=SimpleConvexPolygon2D(Point2D(-1,-1),
                                  Point2D(0,-1),
                                  Point2D(0,0),
                                  Point2D(-1,0))
        self.assertEqual(pg.intersect_simple_convex_polygon(pg1),
                         Point2D(0,0))
    
        # edge intersection
        pg1=SimpleConvexPolygon2D(Point2D(-1,0),
                                  Point2D(0,0),
                                  Point2D(0,1),
                                  Point2D(-1,1))
        self.assertEqual(pg.intersect_simple_convex_polygon(pg1),
                         Segment2D(Point2D(0,0),
                                   Point2D(0,1)))
        
        # overlap intersection - same polygon
        self.assertEqual(pg.intersect_simple_convex_polygon(pg),
                         pg)
    
        
        # overlap intersection
        pg1=SimpleConvexPolygon2D(Point2D(-0.5,-0.5),
                                  Point2D(0.5,-0.5),
                                  Point2D(0.5,0.5),
                                  Point2D(-0.5,0.5))
        
        self.assertEqual(pg.intersect_simple_convex_polygon(pg1),
                         SimpleConvexPolygon2D(Point2D(0.5,0),
                                               Point2D(0.5,0.5),
                                               Point2D(0,0.5),
                                               Point2D(0,0)))
        
        # overlap intersection - polygons reversed from above       
        self.assertEqual(pg1.intersect_simple_convex_polygon(pg),
                         SimpleConvexPolygon2D(Point2D(0.5,0),
                                               Point2D(0.5,0.5),
                                               Point2D(0,0.5),
                                               Point2D(0,0)))
        
        # another overlap intersection
        pg1=SimpleConvexPolygon2D(Point2D(0.5,0),
                                  Point2D(2,0),
                                  Point2D(2,1),
                                  Point2D(0.5,1))
        self.assertEqual(pg.intersect_simple_convex_polygon(pg1),
                         SimpleConvexPolygon2D(Point2D(1.0,1.0),
                                               Point2D(0.5,1),
                                               Point2D(0.5,0.0),
                                               Point2D(1.0,0.0)))
        
        
    def test_union_simple_convex_polygon(self):
        ""
        pg=SimpleConvexPolygon2D(*points)
        
        # no intersection
        pg1=SimpleConvexPolygon2D(Point2D(-2,0),
                                  Point2D(-1,0),
                                  Point2D(-1,1),
                                  Point2D(-2,1))
        self.assertEqual(pg.union_simple_convex_polygon(pg1),
                         None)
        
        # point unionion
        pg1=SimpleConvexPolygon2D(Point2D(-1,-1),
                                  Point2D(0,-1),
                                  Point2D(0,0),
                                  Point2D(-1,0))
        self.assertEqual(pg.union_simple_convex_polygon(pg1),
                         None)
        
        # edge unionion
        pg1=SimpleConvexPolygon2D(Point2D(-1,0),
                                  Point2D(0,0),
                                  Point2D(0,1),
                                  Point2D(-1,1))
        self.assertEqual(pg.union_simple_convex_polygon(pg1),
                         SimplePolygon2D(Point2D(1,0),
                                         Point2D(1,1),
                                         Point2D(-1,1),
                                         Point2D(-1,0)))
        
        # overlap union - same polygon
        self.assertEqual(pg.union_simple_convex_polygon(pg),
                         pg)
    
        
        # overlap union
        pg1=SimpleConvexPolygon2D(Point2D(0.5,0),
                                  Point2D(2,0),
                                  Point2D(2,1),
                                  Point2D(0.5,1))
        self.assertEqual(pg.union_simple_convex_polygon(pg1),
                         SimplePolygon2D(Point2D(0,1),
                                         Point2D(0,0),
                                         Point2D(2,0),
                                         Point2D(2,1)))
        
        # above, reversed
        self.assertEqual(pg1.union_simple_convex_polygon(pg),
                         SimplePolygon2D(Point2D(0,1),
                                         Point2D(0,0),
                                         Point2D(2,0),
                                         Point2D(2,1)))
        
        # overlap union
        pg1=SimpleConvexPolygon2D(Point2D(-0.5,-0.5),
                                  Point2D(0.5,-0.5),
                                  Point2D(0.5,0.5),
                                  Point2D(-0.5,0.5))
        self.assertEqual(pg.union_simple_convex_polygon(pg1),
                         SimplePolygon2D(Point2D(0.5,0.0),
                                         Point2D(1,0),
                                         Point2D(1,1),
                                         Point2D(0,1),
                                         Point2D(0.0,0.5),
                                         Point2D(-0.5,0.5),
                                         Point2D(-0.5,-0.5),
                                         Point2D(0.5,-0.5)))
        
        # overlap union - polygons reversed from above       
        self.assertEqual(pg1.union_simple_convex_polygon(pg),
                         SimplePolygon2D(Point2D(0.5,0.0),
                                         Point2D(1,0),
                                         Point2D(1,1),
                                         Point2D(0,1),
                                         Point2D(0.0,0.5),
                                         Point2D(-0.5,0.5),
                                         Point2D(-0.5,-0.5),
                                         Point2D(0.5,-0.5)))
        
        
        
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
        
        
#    def test_intersect_halfline(self):
#        ""
#        pg=SimpleConvexPolygon3D(*points)
#        
#        self.assertEqual(pg.intersect_halfline(Halfline3D(Point3D(0,0,0),
#                                                          Vector3D(1,0,0))),
#                         (Points(),
#                          Segments(Segment3D(Point3D(0,0,0),
#                                             Point3D(1,0,0)))))
#        self.assertEqual(pg.intersect_halfline(Halfline3D(Point3D(-1,0.5,0),
#                                                          Vector3D(1,0,0))),
#                         (Points(),
#                          Segments(Segment3D(Point3D(0,0.5,0),
#                                              Point3D(1,0.5,0)))))
#        self.assertEqual(pg.intersect_halfline(Halfline3D(Point3D(0,-0.5,0),
#                                                          Vector3D(1,0,0))),
#                         (Points(),
#                          Segments()))
#        self.assertEqual(pg.intersect_halfline(Halfline3D(Point3D(0,0,0),
#                                                          Vector3D(-1,1,0))),
#                         (Points(Point3D(0,0,0)),
#                          Segments()))
#        self.assertEqual(pg.intersect_halfline(Halfline3D(Point3D(2,0,0),
#                                                          Vector3D(1,0,0))),
#                         (Points(),
#                          Segments()))
#        self.assertEqual(pg.intersect_halfline(Halfline3D(Point3D(0.5,0.5,0),
#                                                          Vector3D(1,0,0))),
#                         (Points(),
#                          Segments(Segment3D(Point3D(0.5,0.5,0),
#                                             Point3D(1,0.5,0)))))
#        self.assertEqual(pg.intersect_halfline(Halfline3D(Point3D(-1,1,0),
#                                                          Vector3D(-1,1,0))),
#                         (Points(),
#                          Segments()))
#        
#        
#    def test_intersect_line(self):
#        ""
#        
#        pg=SimpleConvexPolygon3D(*points)
#        
#        # no intersection -> parallel, non-coplanar
#        self.assertEqual(pg.intersect_line(Line3D(Point3D(0,0,1),
#                                                  Vector3D(1,0,0))),
#                         (Points(),
#                          Segments()))
#        
#        # no intersection -> skew, non-intersecting
#        self.assertEqual(pg.intersect_line(Line3D(Point3D(-1,0,0),
#                                                  Vector3D(0,0,1))),
#                         (Points(),
#                          Segments()))
#    
#        # segment intersection -> coplanar, intersects at 2 points
#        self.assertEqual(pg.intersect_line(Line3D(Point3D(0,0,0),
#                                                  Vector3D(1,1,0))),
#                         (Points(),
#                          Segments(Segment3D(Point3D(0,0,0),
#                                             Point3D(1,1,0)))))
#            
#        # point intersection -> skew plane and line
#        self.assertEqual(pg.intersect_line(Line3D(Point3D(0.5,0.5,0),
#                                                  Vector3D(0,0,1))),
#                         (Points(Point3D(0.5,0.5,0)),
#                          Segments()))
#            
#        # -- note that this 'point intersection' returns None, as the 
#        #   point is not considered inside the polygon if it's on the top or
#        #   righthand edge
#        self.assertEqual(pg.intersect_line(Line3D(Point3D(1,1,0),
#                                                  Vector3D(0,0,1))),
#                         (Points(),
#                          Segments()))
#            
#            
#        # point intersection -> coplanar, intersects at 1 point
#        self.assertEqual(pg.intersect_line(Line3D(Point3D(1,1,0),
#                                                  Vector3D(-1,1,0))),
#                         (Points(Point3D(1,1,0)),
#                          Segments()))
#    
#        
#    def test_intersect_segment(self):
#        ""
#        pg=SimpleConvexPolygon3D(*points)
#        
#        self.assertEqual(pg.intersect_segment(Segment3D(Point3D(0,0,0),
#                                                        Point3D(1,0,0))),
#                         (Points(),
#                          Segments(Segment3D(Point3D(0,0,0),
#                                            Point3D(1,0,0)))))
#        self.assertEqual(pg.intersect_segment(Segment3D(Point3D(-1,0.5,0),
#                                                        Point3D(2,0.5,0))),
#                         (Points(),
#                          Segments(Segment3D(Point3D(0,0.5,0),
#                                             Point3D(1,0.5,0)))))
#        self.assertEqual(pg.intersect_segment(Segment3D(Point3D(0,-0.5,0),
#                                                        Point3D(1,-0.5,0))),
#                         (Points(),
#                          Segments()))
#        self.assertEqual(pg.intersect_segment(Segment3D(Point3D(0,0,0),
#                                                        Point3D(-1,1,0))),
#                         (Points(Point3D(0,0,0)),
#                          Segments()))
#        self.assertEqual(pg.intersect_segment(Segment3D(Point3D(1,0,0),
#                                                        Point3D(2,0,0))),
#                         (Points(Point3D(1,0,0)),
#                          Segments()))
#        self.assertEqual(pg.intersect_segment(Segment3D(Point3D(0.5,0.5,0),
#                                                        Point3D(1.5,0.5,0))),
#                         (Points(),
#                          Segments(Segment3D(Point3D(0.5,0.5,0),
#                                             Point3D(1,0.5,0)))))
#        self.assertEqual(pg.intersect_segment(Segment3D(Point3D(-0.5,0.5,0),
#                                                        Point3D(0.5,0.5,0))),
#                         (Points(),
#                          Segments(Segment3D(Point3D(0,0.5,0),
#                                             Point3D(0.5,0.5,0)))))
#        self.assertEqual(pg.intersect_segment(Segment3D(Point3D(0,0.25,0),
#                                                        Point3D(0,0.75,0))),
#                         (Points(),
#                          Segments(Segment3D(Point3D(0,0.25,0),
#                                             Point3D(0,0.75,0)))))
#        
#    
    def test_intersect_simple_convex_polygon(self):
        ""
        pg=SimpleConvexPolygon3D(*points)
        
        # no intersection - parallel but not coplanar
        pg1=SimpleConvexPolygon3D(Point3D(0,0,1),
                                  Point3D(1,0,1),
                                  Point3D(1,1,1),
                                  Point3D(0,1,1))
        self.assertEqual(pg.intersect_simple_convex_polygon(pg1),
                         None)
        
        # no intersection - coplanar
        pg1=SimpleConvexPolygon3D(Point3D(-2,0,0),
                                  Point3D(-1,0,0),
                                  Point3D(-1,1,0),
                                  Point3D(-2,1,0))
        self.assertEqual(pg.intersect_simple_convex_polygon(pg1),
                         None)
        
        # no intersection - skew
        pg1=SimpleConvexPolygon3D(Point3D(-1,0,0),
                                  Point3D(-1,1,0),
                                  Point3D(-1,1,1),
                                  Point3D(-1,0,1))
        self.assertEqual(pg.intersect_simple_convex_polygon(pg1),
                         None)
        
        # point intersection - coplanar
        pg1=SimpleConvexPolygon3D(Point3D(-1,-1,0),
                                  Point3D(0,-1,0),
                                  Point3D(0,0,0),
                                  Point3D(-1,0,0))
        self.assertEqual(pg.intersect_simple_convex_polygon(pg1),
                         Point3D(0,0,0))
        
        # point intersection - skew
        pg1=SimpleConvexPolygon3D(Point3D(0,0,0),
                            Point3D(0,-1,0),
                            Point3D(0,-1,-1),
                            Point3D(0,0,-1))
        self.assertEqual(pg.intersect_simple_convex_polygon(pg1),
                         Point3D(0,0,0))
    
        # edge intersection - coplanar
        pg1=SimpleConvexPolygon3D(Point3D(-1,0,0),
                                  Point3D(0,0,0),
                                  Point3D(0,1,0),
                                  Point3D(-1,1,0))
        self.assertEqual(pg.intersect_simple_convex_polygon(pg1),
                         Segment3D(Point3D(0,0,0),
                                   Point3D(0,1,0)))
        
        # edge intersection - skew
        pg1=SimpleConvexPolygon3D(Point3D(0,0,0),
                                  Point3D(0,1,0),
                                  Point3D(0,1,1),
                                  Point3D(0,0,1))
        self.assertEqual(pg.intersect_simple_convex_polygon(pg1),
                         Segment3D(Point3D(0,0,0),
                                   Point3D(0,1,0)))
        
        # overlap intersection - same polygon
        self.assertEqual(pg.intersect_simple_convex_polygon(pg),
                         pg)
    
        
        # overlap intersection - coplanar
        pg1=SimpleConvexPolygon3D(Point3D(-0.5,-0.5,0),
                                  Point3D(0.5,-0.5,0),
                                  Point3D(0.5,0.5,0),
                                  Point3D(-0.5,0.5,0))
        self.assertEqual(pg.intersect_simple_convex_polygon(pg1),
                         SimpleConvexPolygon3D(Point3D(0,0,0.0),
                                               Point3D(0.5,0.0,0.0),
                                               Point3D(0.5,0.5,0.0),
                                               Point3D(0.0,0.5,0.0)))
        
        self.assertEqual(pg1.intersect_simple_convex_polygon(pg),
                         SimpleConvexPolygon3D(Point3D(0,0,0.0),
                                               Point3D(0.5,0.0,0.0),
                                               Point3D(0.5,0.5,0.0),
                                               Point3D(0.0,0.5,0.0)))


        # overlap intersection - skew - segment
        pg1=SimpleConvexPolygon3D(Point3D(0.5,0,-1),
                                  Point3D(0.5,0,1),
                                  Point3D(0.5,0.5,1),
                                  Point3D(0.5,0.5,-1))
        self.assertEqual(pg.intersect_simple_convex_polygon(pg1),
                         Segment3D(Point3D(0.5,0,0),
                                   Point3D(0.5,0.5,0)))
        self.assertEqual(pg1.intersect_simple_convex_polygon(pg),
                         Segment3D(Point3D(0.5,0,0),
                                   Point3D(0.5,0.5,0)))

    
        # overlap intersection - skew - segment
        pg1=SimpleConvexPolygon3D(Point3D(0.5,-0.5,-1),
                            Point3D(0.5,-0.5,1),
                            Point3D(0.5,0.5,1),
                            Point3D(0.5,0.5,-1))
        self.assertEqual(pg.intersect_simple_convex_polygon(pg1),
                         Segment3D(Point3D(0.5,0,0),
                                   Point3D(0.5,0.5,0)))

    
if __name__=='__main__':
    
    points=(Point2D(0,0),Point2D(1,0),Point2D(1,1),Point2D(0,1))
    unittest.main(Test_SimpleConvexPolygon2D())
    
    points=(Point3D(0,0,0),Point3D(1,0,0),Point3D(1,1,0),Point3D(0,1,0))
    unittest.main(Test_SimpleConvexPolygon3D())
    
    