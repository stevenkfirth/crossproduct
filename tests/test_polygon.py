# -*- coding: utf-8 -*-

import unittest
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d

from crossproduct import Point2D, Point3D, \
    Vector2D, Vector3D, Line2D, Polygon2D, Polygon3D, Plane3D, Triangle2D, Triangle3D, \
    Segment2D, Segment3D, HalfLine2D

plot=False # Set to true to see the test plots

class Test_Polygon2D(unittest.TestCase):
    """
    points=(Point2D(0,0),Point2D(1,0),Point2D(1,1),Point2D(0,1))
    """
    
    def test___init__(self):
        ""
        pg=Polygon2D(*points)
        self.assertIsInstance(pg,Polygon2D)
        self.assertEqual(pg.points,points)
        
        
    def test___contains__(self):
        ""
        pg=Polygon2D(*points)
        
        # Point
        self.assertTrue(Point2D(0.5,0.5) in pg)
        
        # Segment
        
        # Polygon
        
        
    def test___eq__(self):
        ""
        pg=Polygon2D(*points)
        self.assertTrue(pg==pg)
        
        pg2=Polygon2D(Point2D(0,0),Point2D(1,0),Point2D(0,1))
        self.assertFalse(pg==pg2)
        
        
    def test___repr__(self):
        ""
        pg=Polygon2D(*points)
        self.assertEqual(str(pg),
                         'Polygon2D(Point2D(0,0),Point2D(1,0),Point2D(1,1),Point2D(0,1))')
        
        
    def test_area(self):
        ""
        pg=Polygon2D(*points)
        self.assertEqual(pg.area, # ccw
                         1)
        self.assertEqual(pg.reverse.area, # cw
                         1)
        
        
    def test_closed_points(self):
        ""
        pg=Polygon2D(*points)
        self.assertEqual(pg.closed_points,
                         tuple(list(points)+[points[0]]))
        
        
    def test_crossing_number(self):
        ""
        pg=Polygon2D(*points)
        self.assertEqual(pg.crossing_number(pg.points[0]),
                         1)
        self.assertEqual(pg.crossing_number(pg.points[1]),
                         0)
        self.assertEqual(pg.crossing_number(pg.points[2]),
                         0)
        self.assertEqual(pg.crossing_number(pg.points[3]),
                         0) 
        self.assertEqual(pg.crossing_number(Point2D(-0.5,0.5)),
                         2)
        self.assertEqual(pg.crossing_number(Point2D(0.5,0.5)),
                         1)
        
        
    def test_intersect_halfline(self):
        ""
        pg=Polygon2D(*points)
        
        # convex polygon
        self.assertEqual(pg.intersect_halfline(HalfLine2D(Point2D(0,0),
                                                          Vector2D(1,1))),
                         ([], 
                          [Segment2D(Point2D(0.0,0.0), 
                                     Point2D(1.0,1.0))]))        
        
        self.assertEqual(pg.intersect_halfline(HalfLine2D(Point2D(0,0),
                                                          Vector2D(1,-1))),
                         ([Point2D(0,0)], 
                          []))     
    
        self.assertEqual(pg.intersect_halfline(HalfLine2D(Point2D(0.5,0.5),
                                                          Vector2D(1,1))),
                         ([], 
                          [Segment2D(Point2D(0.5,0.5), 
                                     Point2D(1.0,1.0))]))    
            
        # concave polygon
        pg=Polygon2D(Point2D(0,0),
                     Point2D(2,0),
                     Point2D(1,1),
                     Point2D(2,2),
                     Point2D(0,2))
        
        self.assertEqual(pg.intersect_halfline(HalfLine2D(Point2D(1.5,0),
                                                          Vector2D(0,1))),
                         ([], 
                          [Segment2D(Point2D(1.5,0), 
                                     Point2D(1.5,0.5)),
                           Segment2D(Point2D(1.5,1.5), 
                                     Point2D(1.5,2))]))  
    
        self.assertEqual(pg.intersect_halfline(HalfLine2D(Point2D(2,0),
                                                          Vector2D(0,1))),
                         ([Point2D(2,0),
                           Point2D(2,2)], 
                          []))  
    
        self.assertEqual(pg.intersect_halfline(HalfLine2D(Point2D(1,0),
                                                          Vector2D(0,1))),
                         ([], 
                          [Segment2D(Point2D(1,0), 
                                     Point2D(1,2))]))  
    
        self.assertEqual(pg.intersect_halfline(HalfLine2D(Point2D(0,0),
                                                          Vector2D(0,1))),
                         ([], 
                          [Segment2D(Point2D(0,0), 
                                     Point2D(0,2))]))  
    
        self.assertEqual(pg.intersect_halfline(HalfLine2D(Point2D(0,0.5),
                                                          Vector2D(1,0))),
                         ([], 
                          [Segment2D(Point2D(0,0.5), 
                                     Point2D(1.5,0.5))]))  
        
        
    def test_intersect_line(self):
        ""
        pg=Polygon2D(*points)
        
        # convex polygon
        self.assertEqual(pg.intersect_line(Line2D(Point2D(0,0),
                                                  Vector2D(1,1))),
                         ([], 
                          [Segment2D(Point2D(0.0,0.0), 
                                     Point2D(1.0,1.0))]))        
        
        self.assertEqual(pg.intersect_line(Line2D(Point2D(0,0),
                                                  Vector2D(1,-1))),
                         ([Point2D(0,0)], 
                          []))     
        
            
        # concave polygon
        pg=Polygon2D(Point2D(0,0),
                     Point2D(2,0),
                     Point2D(1,1),
                     Point2D(2,2),
                     Point2D(0,2))
        
        self.assertEqual(pg.intersect_line(Line2D(Point2D(1.5,0),
                                                  Vector2D(0,1))),
                         ([], 
                          [Segment2D(Point2D(1.5,0), 
                                     Point2D(1.5,0.5)),
                           Segment2D(Point2D(1.5,1.5), 
                                     Point2D(1.5,2))]))  
    
        self.assertEqual(pg.intersect_line(Line2D(Point2D(2,0),
                                                  Vector2D(0,1))),
                         ([Point2D(2,0),
                           Point2D(2,2)], 
                          []))  
    
        self.assertEqual(pg.intersect_line(Line2D(Point2D(1,0),
                                                  Vector2D(0,1))),
                         ([], 
                          [Segment2D(Point2D(1,0), 
                                     Point2D(1,2))]))  
    
        self.assertEqual(pg.intersect_line(Line2D(Point2D(0,0),
                                                  Vector2D(0,1))),
                         ([], 
                          [Segment2D(Point2D(0,0), 
                                     Point2D(0,2))]))  
    
        self.assertEqual(pg.intersect_line(Line2D(Point2D(0,0.5),
                                                  Vector2D(1,0))),
                         ([], 
                          [Segment2D(Point2D(0,0.5), 
                                     Point2D(1.5,0.5))]))  
    
    
    def test_intersect_segment(self):
        ""
        pg=Polygon2D(*points)
        
        # convex polygon
        self.assertEqual(pg.intersect_segment(Segment2D(Point2D(0,0),
                                                        Point2D(1,1))),
                         ([], 
                          [Segment2D(Point2D(0.0,0.0), 
                                     Point2D(1.0,1.0))]))        
        
        self.assertEqual(pg.intersect_segment(Segment2D(Point2D(0,0),
                                                        Point2D(1,-1))),
                         ([Point2D(0,0)], 
                          []))     
    
        self.assertEqual(pg.intersect_segment(Segment2D(Point2D(0.5,0.5),
                                                        Point2D(1,1))),
                         ([], 
                          [Segment2D(Point2D(0.5,0.5), 
                                     Point2D(1.0,1.0))]))    
            
        # concave polygon
        pg=Polygon2D(Point2D(0,0),
                     Point2D(2,0),
                     Point2D(1,1),
                     Point2D(2,2),
                     Point2D(0,2))
        
        self.assertEqual(pg.intersect_segment(Segment2D(Point2D(1.5,0),
                                                        Point2D(1.5,10))),
                         ([], 
                          [Segment2D(Point2D(1.5,0), 
                                     Point2D(1.5,0.5)),
                           Segment2D(Point2D(1.5,1.5), 
                                     Point2D(1.5,2))]))  
    
        self.assertEqual(pg.intersect_segment(Segment2D(Point2D(2,0),
                                                        Point2D(2,10))),
                         ([Point2D(2,0),
                           Point2D(2,2)], 
                          []))  
    
        self.assertEqual(pg.intersect_segment(Segment2D(Point2D(1,0),
                                                        Point2D(1,10))),
                         ([], 
                          [Segment2D(Point2D(1,0), 
                                     Point2D(1,2))]))  
    
        self.assertEqual(pg.intersect_segment(Segment2D(Point2D(0,0),
                                                        Point2D(0,10))),
                         ([], 
                          [Segment2D(Point2D(0,0), 
                                     Point2D(0,2))]))  
    
        self.assertEqual(pg.intersect_segment(Segment2D(Point2D(0,0.5),
                                                        Point2D(10,0.5))),
                         ([], 
                          [Segment2D(Point2D(0,0.5), 
                                     Point2D(1.5,0.5))]))  
    
    
    def test_intersect_polygon(self):
        ""
        pg=Polygon2D(*points)
        
        # no intersection
        pg1=Polygon2D(Point2D(-2,0),
                            Point2D(-1,0),
                            Point2D(-1,1),
                            Point2D(-2,1))
        self.assertEqual(pg.intersect_polygon(pg1),
                         None)
        
#        # point intersection
#        pg1=Polygon2D(Point2D(-1,-1),
#                            Point2D(0,-1),
#                            Point2D(0,0),
#                            Point2D(-1,0))
#        self.assertEqual(pg.intersect_polygon(pg1),
#                         Point2D(0,0))
#    
#        # edge intersection
#        pg1=Polygon2D(Point2D(-1,0),
#                            Point2D(0,0),
#                            Point2D(0,1),
#                            Point2D(-1,1))
#        self.assertEqual(pg.intersect_polygon(pg1),
#                         Polyline2D(Point2D(0,0),Point2D(0,1)))
#        
#        # overlap intersection - same polygon
#        self.assertEqual(pg.intersect_polygon(pg),
#                         pg.polyline)
#    
#        
#        # overlap intersection
#        pg1=Polygon2D(Point2D(-0.5,-0.5),
#                            Point2D(0.5,-0.5),
#                            Point2D(0.5,0.5),
#                            Point2D(-0.5,0.5))
#        self.assertEqual(pg.intersect_polygon(pg1),
#                         Polyline2D(Point2D(0.5,0),
#                                    Point2D(0.5,0.5),
#                                    Point2D(0,0.5)))
#        self.assertEqual(pg1.intersect_polygon(pg),
#                         Polyline2D(Point2D(0,0.5),
#                                    Point2D(0,0),
#                                    Point2D(0.5,0)))
    
    
        
    def test_next_index(self):
        ""
        pg=Polygon2D(*points)
        self.assertEqual(pg.next_index(0),
                         1)
        self.assertEqual(pg.next_index(3),
                         0)
        
        
    def test_orientation(self):
        ""
        pg=Polygon2D(*points)
        self.assertTrue(pg.orientation>0)
        self.assertTrue(pg.reverse.orientation<0)
        
        
    def test_prevous_index(self):
        ""
        pg=Polygon2D(*points)
        self.assertEqual(pg.previous_index(0),
                         3)
        self.assertEqual(pg.previous_index(3),
                         2)
        
        
    def test_plot(self):
        ""
        if plot:
            
            pg=Polygon2D(*points)
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
        
        
    def test_reorder(self):
        ""
        pg=Polygon2D(*points)
        self.assertEqual(pg.reorder(1),
                         Polygon2D(Point2D(1,0),
                                   Point2D(1,1),
                                   Point2D(0,1),
                                   Point2D(0,0)))
        
        
    def test_reverse(self):
        ""
        pg=Polygon2D(*points)
        self.assertEqual(pg.reverse,
                         Polygon2D(Point2D(0,1),
                                   Point2D(1,1),
                                   Point2D(1,0),
                                   Point2D(0,0)))
        
        
    def test_rightmost_lowest_vertex(self):
        ""
        pg=Polygon2D(*points)
        self.assertEqual(pg.rightmost_lowest_vertex, 
                         1)
        
        
    def test_signed_area(self):
        ""
        pg=Polygon2D(*points)
        self.assertEqual(pg.signed_area, # ccw
                         1)
        self.assertEqual(pg.reverse.signed_area, # cw
                         -1)
        
        
    def test_triangulate(self):
        ""
        # convex polygon
        pg=Polygon2D(*points)
        self.assertEqual(pg.triangulate,
                         [Triangle2D(Point2D(0,0), Vector2D(1,0), Vector2D(0,1)), 
                          Triangle2D(Point2D(1,0), Vector2D(0,1), Vector2D(-1,1))])
        
        # concave polygon
        pg=Polygon2D(Point2D(0,0),
                     Point2D(2,0),
                     Point2D(1,1),
                     Point2D(2,2),
                     Point2D(0,2))
        self.assertEqual(pg.triangulate,
                         [Triangle2D(Point2D(2,0), Vector2D(-1,1), Vector2D(-2,0)), 
                          Triangle2D(Point2D(0,0), Vector2D(1,1), Vector2D(0,2)), 
                          Triangle2D(Point2D(1,1), Vector2D(1,1), Vector2D(-1,1))])
    
        
    def test_winding_number(self):
        ""
        pg=Polygon2D(*points)
        self.assertEqual(pg.winding_number(pg.points[0]),
                         1)
        self.assertEqual(pg.winding_number(pg.points[1]),
                         0)
        self.assertEqual(pg.winding_number(pg.points[2]),
                         0)
        self.assertEqual(pg.winding_number(pg.points[3]),
                         0) 
        self.assertEqual(pg.winding_number(Point2D(-0.5,0.5)),
                         0)
        self.assertEqual(pg.winding_number(Point2D(0.5,0.5)),
                         1)
        
    
        
class Test_Polygon3D(unittest.TestCase):
    """
    points=(Point3D(0,0,0),Point3D(1,0,0),Point3D(1,1,0),Point3D(0,1,0))
    """
    
    def test___init__(self):
        ""
        pg=Polygon3D(*points)
        self.assertIsInstance(pg,Polygon3D)
        self.assertEqual(pg.points,points)
        
        
    def test___contains__(self):
        ""
        pg=Polygon3D(*points)
        
        # Point
        
        # --> TO DO
        
        # Segment
        
        # Polygon
        
        
    def test___eq__(self):
        ""
        pg=Polygon3D(*points)
        self.assertTrue(pg==pg)
        
        pg2=Polygon3D(Point3D(0,0,0),Point3D(1,0,0),Point3D(0,1,0))
        self.assertFalse(pg==pg2)
        
        
    def test___repr__(self):
        ""
        pg=Polygon3D(*points)
        self.assertEqual(str(pg),
                         'Polygon3D(Point3D(0,0,0),Point3D(1,0,0),Point3D(1,1,0),Point3D(0,1,0))')
        
    def test_area(self):
        ""
        pg=Polygon3D(*points)
        self.assertEqual(pg.area, # ccw
                         1)
        self.assertEqual(pg.reverse.area, # cw
                         1)
        
        
    def test_next_index(self):
        ""
        pg=Polygon3D(*points)
        self.assertEqual(pg.next_index(0),
                         1)
        self.assertEqual(pg.next_index(3),
                         0)
        
    
    def test_plane(self):
        ""
        pg=Polygon3D(*points)
        self.assertEqual(pg.plane,
                         Plane3D(Point3D(0,0,0),Vector3D(0,0,1)))
        
        
    def test_plot(self):
        ""
        
        if plot:
        
            pg=Polygon3D(*points)
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            pg.plot(ax)
        
        
    def test_prevous_index(self):
        ""
        pg=Polygon3D(*points)
        self.assertEqual(pg.previous_index(0),
                         3)
        self.assertEqual(pg.previous_index(3),
                         2)
        
        
    def test_project_2D(self):
        ""
        pg=Polygon3D(*points)
        self.assertEqual(pg.project_2D,
                         (2,Polygon2D(Point2D(0,0),Point2D(1,0),Point2D(1,1),Point2D(0,1))))
        
        
    def test_reorder(self):
        ""
        pg=Polygon3D(*points)
        self.assertEqual(pg.reorder(1),
                         Polygon3D(Point3D(1,0,0),
                                   Point3D(1,1,0),
                                   Point3D(0,1,0),
                                   Point3D(0,0,0)))
        
        
    def test_reverse(self):
        ""
        pg=Polygon3D(*points)
        self.assertEqual(pg.reverse,
                         Polygon3D(Point3D(0,1,0),
                                   Point3D(1,1,0),
                                   Point3D(1,0,0),
                                   Point3D(0,0,0)))
        
        
    def test_triangulate(self):
        ""
        # convex polygon
        pg=Polygon3D(*points)
        self.assertEqual(pg.triangulate,
                         [Triangle3D(Point3D(0,0,0), Vector3D(1,0,0), Vector3D(0,1,0)), 
                          Triangle3D(Point3D(1,0,0), Vector3D(0,1,0), Vector3D(-1,1,0))])
        
        # concave polygon
        pg=Polygon3D(Point3D(0,0,2),
                     Point3D(2,0,2),
                     Point3D(1,1,2),
                     Point3D(2,2,2),
                     Point3D(0,2,2))
        self.assertEqual(pg.triangulate,
                         [Triangle3D(Point3D(2,0,2), Vector3D(-1,1,0), Vector3D(-2,0,0)), 
                          Triangle3D(Point3D(0,0,2), Vector3D(1,1,0), Vector3D(0,2,0)), 
                          Triangle3D(Point3D(1,1,2), Vector3D(1,1,0), Vector3D(-1,1,0))])
        
        
    
if __name__=='__main__':
    
    points=(Point2D(0,0),Point2D(1,0),Point2D(1,1),Point2D(0,1))
    unittest.main(Test_Polygon2D())
    
    points=(Point3D(0,0,0),Point3D(1,0,0),Point3D(1,1,0),Point3D(0,1,0))
    unittest.main(Test_Polygon3D())
    
    