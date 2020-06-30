# -*- coding: utf-8 -*-

import unittest
from crossproduct import Point2D, Point3D, HalfLine2D, HalfLine3D, \
    Vector2D, Vector3D, Line2D, Line3D, ConvexPolygon2D, ConvexPolygon3D, Plane3D, Segment2D, Segment3D, \
    Polyline2D, Polyline3D
    

class Test_ConvexPolygon2D(unittest.TestCase):
    """
    points=(Point2D(0,0),Point2D(1,0),Point2D(1,1),Point2D(0,1))
    """
    
    def test___init__(self):
        ""
        pg=ConvexPolygon2D(*points)
        self.assertIsInstance(pg,ConvexPolygon2D)
        self.assertEqual(pg.points,points)
        
        
    def test_intersect_halfline(self):
        ""
        pg=ConvexPolygon2D(*points)
        
        self.assertEqual(pg.intersect_halfline(HalfLine2D(Point2D(0,0),
                                                          Vector2D(1,0))),
                         Segment2D(Point2D(0,0),
                                   Point2D(1,0)))
        self.assertEqual(pg.intersect_halfline(HalfLine2D(Point2D(-1,0.5),
                                                          Vector2D(1,0))),
                         Segment2D(Point2D(0,0.5),
                                   Point2D(1,0.5)))
        self.assertEqual(pg.intersect_halfline(HalfLine2D(Point2D(0,-0.5),
                                                          Vector2D(1,0))),
                         None)
        self.assertEqual(pg.intersect_halfline(HalfLine2D(Point2D(0,0),
                                                          Vector2D(-1,1))),
                         Point2D(0,0))  
        self.assertEqual(pg.intersect_halfline(HalfLine2D(Point2D(2,0),
                                                          Vector2D(1,0))),
                         None)
        self.assertEqual(pg.intersect_halfline(HalfLine2D(Point2D(0.5,0.5),
                                                          Vector2D(1,0))),
                         Segment2D(Point2D(0.5,0.5),
                                   Point2D(1,0.5)))
        self.assertEqual(pg.intersect_halfline(HalfLine2D(Point2D(-1,1),
                                                          Vector2D(-1,1))),
                         None)  
    
        
    def test_intersect_line(self):
        ""
        pg=ConvexPolygon2D(*points)
        
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
        pg=ConvexPolygon2D(*points)
        
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
        pg=ConvexPolygon2D(*points)
        
        self.assertEqual(pg.intersect_segment(Segment2D(Point2D(0,0),
                                                        Point2D(1,0))),
                         Segment2D(Point2D(0,0),
                                   Point2D(1,0)))
        self.assertEqual(pg.intersect_segment(Segment2D(Point2D(-1,0.5),
                                                        Point2D(2,0.5))),
                         Segment2D(Point2D(0,0.5),
                                   Point2D(1,0.5)))
        self.assertEqual(pg.intersect_segment(Segment2D(Point2D(0,-0.5),
                                                        Point2D(1,-0.5))),
                         None)
        self.assertEqual(pg.intersect_segment(Segment2D(Point2D(0,0),
                                                        Point2D(-1,1))),
                         Point2D(0,0))  
        self.assertEqual(pg.intersect_segment(Segment2D(Point2D(1,0),
                                                        Point2D(2,0))),
                         Point2D(1,0))
        self.assertEqual(pg.intersect_segment(Segment2D(Point2D(0.5,0.5),
                                                        Point2D(1.5,0.5))),
                         Segment2D(Point2D(0.5,0.5),
                                   Point2D(1,0.5)))
        self.assertEqual(pg.intersect_segment(Segment2D(Point2D(-0.5,0.5),
                                                        Point2D(0.5,0.5))),
                         Segment2D(Point2D(0,0.5),
                                   Point2D(0.5,0.5)))
        self.assertEqual(pg.intersect_segment(Segment2D(Point2D(0,0.25),
                                                        Point2D(0,0.75))),
                         Segment2D(Point2D(0,0.25),
                                   Point2D(0,0.75)))
    
    
    def test_intersect_convex_polygon(self):
        ""
        pg=ConvexPolygon2D(*points)
        
        # no intersection
        pg1=ConvexPolygon2D(Point2D(-2,0),
                            Point2D(-1,0),
                            Point2D(-1,1),
                            Point2D(-2,1))
        self.assertEqual(pg.intersect_convex_polygon(pg1),
                         None)
        
        # point intersection
        pg1=ConvexPolygon2D(Point2D(-1,-1),
                            Point2D(0,-1),
                            Point2D(0,0),
                            Point2D(-1,0))
        self.assertEqual(pg.intersect_convex_polygon(pg1),
                         Point2D(0,0))
    
        # edge intersection
        pg1=ConvexPolygon2D(Point2D(-1,0),
                            Point2D(0,0),
                            Point2D(0,1),
                            Point2D(-1,1))
        self.assertEqual(pg.intersect_convex_polygon(pg1),
                         Polyline2D(Point2D(0,0),Point2D(0,1)))
        
        # overlap intersection - same polygon
        self.assertEqual(pg.intersect_convex_polygon(pg),
                         pg.polyline)
    
        
        # overlap intersection
        pg1=ConvexPolygon2D(Point2D(-0.5,-0.5),
                            Point2D(0.5,-0.5),
                            Point2D(0.5,0.5),
                            Point2D(-0.5,0.5))
        self.assertEqual(pg.intersect_convex_polygon(pg1),
                         Polyline2D(Point2D(0.5,0),
                                    Point2D(0.5,0.5),
                                    Point2D(0,0.5)))
        self.assertEqual(pg1.intersect_convex_polygon(pg),
                         Polyline2D(Point2D(0,0.5),
                                    Point2D(0,0),
                                    Point2D(0.5,0)))
        
        
        
    def test_union_convex_polygon(self):
        ""
        pg=ConvexPolygon2D(*points)
        
        # no intersection
        pg1=ConvexPolygon2D(Point2D(-2,0),
                            Point2D(-1,0),
                            Point2D(-1,1),
                            Point2D(-2,1))
        self.assertEqual(pg.union_convex_polygon(pg1),
                         None)

        # point intersection
        pg1=ConvexPolygon2D(Point2D(-1,-1),
                            Point2D(0,-1),
                            Point2D(0,0),
                            Point2D(-1,0))
        self.assertEqual(pg.union_convex_polygon(pg1),
                         Point2D(0,0))
        
        # edge intersection
        pg1=ConvexPolygon2D(Point2D(-1,0),
                            Point2D(0,0),
                            Point2D(0,1),
                            Point2D(-1,1))
        self.assertEqual(pg.union_convex_polygon(pg1),
                         Polyline2D(Point2D(0,0),Point2D(0,1)))
        
        # overlap intersection - same polygon
        self.assertEqual(pg.union_convex_polygon(pg),
                         pg)

        # overlap intersection
        pg1=ConvexPolygon2D(Point2D(-0.5,-0.5),
                            Point2D(0.5,-0.5),
                            Point2D(0.5,0.5),
                            Point2D(-0.5,0.5))
        self.assertEqual(pg.union_convex_polygon(pg1),
                         ConvexPolygon2D(Point2D(0.5,0.0),
                                         Point2D(0.5,0.5),
                                         Point2D(0.0,0.5),
                                         Point2D(0,0)))
        
        
        
class Test_ConvexPolygon3D(unittest.TestCase):
    """
    points=(Point3D(0,0,0),Point3D(1,0,0),Point3D(1,1,0),Point3D(0,1,0))
    """
    
    def test___init__(self):
        ""
        pg=ConvexPolygon3D(*points)
        self.assertIsInstance(pg,ConvexPolygon3D)
        self.assertEqual(pg.points,points)
        
        
    def test_intersect_line(self):
        ""
        pg=ConvexPolygon3D(*points)
        
        # no intersection -> parallel, non-coplanar
        self.assertEqual(pg.intersect_line(Line3D(Point3D(0,0,1),
                                                  Vector3D(1,0,0))),
                         None)
        
        # no intersection -> skew, non-intersecting
        self.assertEqual(pg.intersect_line(Line3D(Point3D(-1,0,0),
                                                  Vector3D(0,0,1))),
                         None)
    
        # segment intersection -> coplanar, intersects at 2 points
        self.assertEqual(pg.intersect_line(Line3D(Point3D(0,0,0),
                                                  Vector3D(1,1,0))),
                         Segment3D(Point3D(0,0,0),
                                   Point3D(1,1,0)))
            
        # point intersection -> skew plane and line
        self.assertEqual(pg.intersect_line(Line3D(Point3D(0.5,0.5,0),
                                                  Vector3D(0,0,1))),
                         Point3D(0.5,0.5,0))
            
        # -- note that this 'point intersection' returns None, as the 
        #   point is not considered inside the polygon if it's on the top or
        #   righthand edge
        self.assertEqual(pg.intersect_line(Line3D(Point3D(1,1,0),
                                                  Vector3D(0,0,1))),
                         None)
            
            
        # point intersection -> coplanar, intersects at 1 point
        self.assertEqual(pg.intersect_line(Line3D(Point3D(1,1,0),
                                                  Vector3D(-1,1,0))),
                         Point3D(1,1,0))
    
    
    def test_intersect_convex_polygon(self):
        ""
        pg=ConvexPolygon3D(*points)
        
        # no intersection - parallel but not coplanar
        pg1=ConvexPolygon3D(Point3D(0,0,1),
                            Point3D(1,0,1),
                            Point3D(1,1,1),
                            Point3D(0,1,1))
        self.assertEqual(pg.intersect_convex_polygon(pg1),
                         None)
        
        # no intersection - coplanar
        pg1=ConvexPolygon3D(Point3D(-2,0,0),
                            Point3D(-1,0,0),
                            Point3D(-1,1,0),
                            Point3D(-2,1,0))
        self.assertEqual(pg.intersect_convex_polygon(pg1),
                         None)
        
        # no intersection - skew
        pg1=ConvexPolygon3D(Point3D(-1,0,0),
                            Point3D(-1,1,0),
                            Point3D(-1,1,1),
                            Point3D(-1,0,1))
        self.assertEqual(pg.intersect_convex_polygon(pg1),
                         None)
        
        # point intersection - coplanar
        pg1=ConvexPolygon3D(Point3D(-1,-1,0),
                            Point3D(0,-1,0),
                            Point3D(0,0,0),
                            Point3D(-1,0,0))
        self.assertEqual(pg.intersect_convex_polygon(pg1),
                         Point3D(0,0,0))
        
        # point intersection - skew
        pg1=ConvexPolygon3D(Point3D(0,0,0),
                            Point3D(0,-1,0),
                            Point3D(0,-1,-1),
                            Point3D(0,0,-1))
        self.assertEqual(pg.intersect_convex_polygon(pg1),
                         Point3D(0,0,0))
    
        # edge intersection - coplanar
        pg1=ConvexPolygon3D(Point3D(-1,0,0),
                            Point3D(0,0,0),
                            Point3D(0,1,0),
                            Point3D(-1,1,0))
        self.assertEqual(pg.intersect_convex_polygon(pg1),
                         Polyline3D(Point3D(0,0,0),
                                    Point3D(0,1,0)))
        
        # edge intersection - skew
        pg1=ConvexPolygon3D(Point3D(0,0,0),
                            Point3D(0,1,0),
                            Point3D(0,1,1),
                            Point3D(0,0,1))
        self.assertEqual(pg.intersect_convex_polygon(pg1),
                         Polyline3D(Point3D(0,0,0),
                                    Point3D(0,1,0)))
        
        # overlap intersection - same polygon
        self.assertEqual(pg.intersect_convex_polygon(pg),
                         pg.polyline)
    
        
        # overlap intersection - coplanar
        pg1=ConvexPolygon3D(Point3D(-0.5,-0.5,0),
                            Point3D(0.5,-0.5,0),
                            Point3D(0.5,0.5,0),
                            Point3D(-0.5,0.5,0))
        self.assertEqual(pg.intersect_convex_polygon(pg1),
                         Polyline3D(Point3D(0.5,0,0),
                                    Point3D(0.5,0.5,0),
                                    Point3D(0,0.5,0)))
        self.assertEqual(pg1.intersect_convex_polygon(pg),
                         Polyline3D(Point3D(0,0.5,0),
                                    Point3D(0,0,0),
                                    Point3D(0.5,0,0)))

        # overlap intersection - skew - segment
        pg1=ConvexPolygon3D(Point3D(0.5,0,-1),
                            Point3D(0.5,0,1),
                            Point3D(0.5,0.5,1),
                            Point3D(0.5,0.5,-1))
        self.assertEqual(pg.intersect_convex_polygon(pg1),
                         Polyline3D(Point3D(0.5,0,0),
                                    Point3D(0.5,0.5,0)))
    
        # overlap intersection - skew - point
        pg1=ConvexPolygon3D(Point3D(0.5,-0.5,-1),
                            Point3D(0.5,-0.5,1),
                            Point3D(0.5,0.5,1),
                            Point3D(0.5,0.5,-1))
        self.assertEqual(pg.intersect_convex_polygon(pg1),
                         Point3D(0.5,0.5,0))
    
    
    def test_union_convex_polygon(self):
        ""
        pg=ConvexPolygon3D(*points)
        
        # no union - parallel but not coplanar
        pg1=ConvexPolygon3D(Point3D(0,0,1),
                            Point3D(1,0,1),
                            Point3D(1,1,1),
                            Point3D(0,1,1))
        self.assertEqual(pg.union_convex_polygon(pg1),
                         None)
        
        # no union - coplanar
        pg1=ConvexPolygon3D(Point3D(-2,0,0),
                            Point3D(-1,0,0),
                            Point3D(-1,1,0),
                            Point3D(-2,1,0))
        self.assertEqual(pg.union_convex_polygon(pg1),
                         None)
        
        # no union - skew
        pg1=ConvexPolygon3D(Point3D(-1,0,0),
                            Point3D(-1,1,0),
                            Point3D(-1,1,1),
                            Point3D(-1,0,1))
        self.assertEqual(pg.union_convex_polygon(pg1),
                         None)
        
        # point union - coplanar
        pg1=ConvexPolygon3D(Point3D(-1,-1,0),
                            Point3D(0,-1,0),
                            Point3D(0,0,0),
                            Point3D(-1,0,0))
        self.assertEqual(pg.union_convex_polygon(pg1),
                         Point3D(0,0,0))
        
        # point union - skew
        pg1=ConvexPolygon3D(Point3D(0,0,0),
                            Point3D(0,-1,0),
                            Point3D(0,-1,-1),
                            Point3D(0,0,-1))
        self.assertEqual(pg.union_convex_polygon(pg1),
                         Point3D(0,0,0))
    
        # edge union - coplanar
        pg1=ConvexPolygon3D(Point3D(-1,0,0),
                            Point3D(0,0,0),
                            Point3D(0,1,0),
                            Point3D(-1,1,0))
        self.assertEqual(pg.union_convex_polygon(pg1),
                         Polyline3D(Point3D(0,0,0),
                                    Point3D(0,1,0)))
        
        # edge union - skew
        pg1=ConvexPolygon3D(Point3D(0,0,0),
                            Point3D(0,1,0),
                            Point3D(0,1,1),
                            Point3D(0,0,1))
        self.assertEqual(pg.union_convex_polygon(pg1),
                         Polyline3D(Point3D(0,0,0),
                                    Point3D(0,1,0)))
        
        # overlap union - same polygon
        self.assertEqual(pg.union_convex_polygon(pg),
                         pg)
        
        # overlap union - coplanar
        pg1=ConvexPolygon3D(Point3D(-0.5,-0.5,0),
                            Point3D(0.5,-0.5,0),
                            Point3D(0.5,0.5,0),
                            Point3D(-0.5,0.5,0))
        self.assertEqual(pg.union_convex_polygon(pg1),
                         ConvexPolygon3D(Point3D(0.5,0,0),
                                         Point3D(0.5,0.5,0),
                                         Point3D(0,0.5,0),
                                         Point3D(0,0,0)))
        
        self.assertEqual(pg1.union_convex_polygon(pg),
                         ConvexPolygon3D(Point3D(0.5,0,0),
                                         Point3D(0.5,0.5,0),
                                         Point3D(0,0.5,0),
                                         Point3D(0,0,0)))
    
        # overlap union - skew - segment
        pg1=ConvexPolygon3D(Point3D(0.5,0,-1),
                            Point3D(0.5,0,1),
                            Point3D(0.5,0.5,1),
                            Point3D(0.5,0.5,-1))
        self.assertEqual(pg.union_convex_polygon(pg1),
                         Polyline3D(Point3D(0.5,0,0),
                                    Point3D(0.5,0.5,0)))
        
        # overlap union - skew - point
        pg1=ConvexPolygon3D(Point3D(0.5,-0.5,-1),
                            Point3D(0.5,-0.5,1),
                            Point3D(0.5,0.5,1),
                            Point3D(0.5,0.5,-1))
        self.assertEqual(pg.union_convex_polygon(pg1),
                         Polyline3D(Point3D(0.5,0,0),
                                    Point3D(0.5,0.5,0)))
    
    
if __name__=='__main__':
    
    points=(Point2D(0,0),Point2D(1,0),Point2D(1,1),Point2D(0,1))
    unittest.main(Test_ConvexPolygon2D())
    
    points=(Point3D(0,0,0),Point3D(1,0,0),Point3D(1,1,0),Point3D(0,1,0))
    unittest.main(Test_ConvexPolygon3D())
    
    