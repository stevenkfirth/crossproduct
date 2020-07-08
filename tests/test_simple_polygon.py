# -*- coding: utf-8 -*-

import unittest
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d

from crossproduct import Point2D, Point3D, \
    Vector2D, Vector3D, Line2D, SimplePolygon2D, SimplePolygon3D, Plane3D, Triangle2D, Triangle3D, \
    Segment2D, Segment3D, Halfline2D, Points, Segments, SimplePolygons, SimpleConvexPolygon2D, \
    Parallelogram2D, Triangles

plot=False # Set to true to see the test plots

class Test_SimplePolygon2D(unittest.TestCase):
    """
    points=(Point2D(0,0),Point2D(1,0),Point2D(1,1),Point2D(0,1))
    """
    
    def test___init__(self):
        ""
        pg=SimplePolygon2D(*points)
        self.assertIsInstance(pg,SimplePolygon2D)
        self.assertEqual(pg.points,points)
        
        #print('--start--')
        pts2=Point2D(0,0),Point2D(1,0),Point2D(1,1),Point2D(0,1),Point2D(-1,1),Point2D(-1,0)
        pg=SimplePolygon2D(*pts2)
        #print('--end--')
        
        
    def test___contains__(self):
        ""
        pg=SimplePolygon2D(*points)
        
        # Point
        self.assertTrue(Point2D(0.5,0.5) in pg)
        
        # Segment
        
        # SimplePolygon
        
        
    def test___eq__(self):
        ""
        pg=SimplePolygon2D(*points)
        self.assertTrue(pg==pg)
        
        pg2=SimplePolygon2D(Point2D(0,0),Point2D(1,0),Point2D(0,1))
        self.assertFalse(pg==pg2)
        
        
    def test___repr__(self):
        ""
        pg=SimplePolygon2D(*points)
        self.assertEqual(str(pg),
                         'SimplePolygon2D(Point2D(0,0),Point2D(1,0),Point2D(1,1),Point2D(0,1))')
        
        
    def test_area(self):
        ""
        pg=SimplePolygon2D(*points)
        self.assertEqual(pg.area, # ccw
                         1)
        self.assertEqual(pg.reverse.area, # cw
                         1)
        
        
    def test_centroid(self):
        ""
        pg=SimplePolygon2D(*points)
        self.assertEqual(pg.centroid, 
                         Point2D(0.5,0.5))
        
        
    def test_closed_points(self):
        ""
        pg=SimplePolygon2D(*points)
        self.assertEqual(pg.closed_points,
                         tuple(list(points)+[points[0]]))
        
        
    def test_crossing_number(self):
        ""
        pg=SimplePolygon2D(*points)
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
        
        
    def test_is_adjacent(self):
        ""
        pr=Parallelogram2D(Point2D(0,0),Vector2D(1,0),Vector2D(0,1))
        
        # no intersection
        pr1=Parallelogram2D(Point2D(0,10), Vector2D(1,0), Vector2D(0,1))
        self.assertFalse(pr.is_adjacent(pr1))
        
        # point intersection
        pr1=Parallelogram2D(Point2D(1,1), Vector2D(1,0), Vector2D(0,1))
        self.assertFalse(pr.is_adjacent(pr1))
        
        # segment intersection
        pr1=Parallelogram2D(Point2D(0,1), Vector2D(1,0), Vector2D(0,1))
        self.assertTrue(pr.is_adjacent(pr1))
                
        
        
    def test_intersect_simple_polygon__triangle(self):
        ""
        tr=Triangle2D(Point2D(0,0),Vector2D(1,0),Vector2D(0.5,1))
        
        # no intersection
        tr1=Triangle2D(Point2D(0,10), Vector2D(1,10), Vector2D(0.5,10))
        self.assertEqual(tr.intersect_simple_polygon(tr1),
                         (Points(), 
                          Segments(), 
                          SimplePolygons()))
        
        # point intersection
        tr1=Triangle2D(Point2D(1,0), Vector2D(2,0), Vector2D(1.5,1))
        self.assertEqual(tr.intersect_simple_polygon(tr1),
                         (Points(Point2D(1,0)), 
                          Segments(), 
                          SimplePolygons()))
                
        # segment intersection
        tr1=Triangle2D(Point2D(0,0), Vector2D(1,0), Vector2D(0.5,-1))
        self.assertEqual(tr.intersect_simple_polygon(tr1),
                         (Points(), 
                          Segments(Segment2D(Point2D(0,0),
                                             Point2D(1,0))), 
                          SimplePolygons()))
        
        # polygon intersetion - self
        self.assertEqual(tr.intersect_simple_polygon(tr),
                         (Points(), 
                          Segments(), 
                          SimplePolygons(tr)))
        
        # polygon intersetion - overlap - result is a triangle
        tr1=Triangle2D(Point2D(0.5,0), Vector2D(1,0), Vector2D(0.5,1))
        self.assertEqual(tr.intersect_simple_polygon(tr1),
                         (Points(), 
                          Segments(), 
                          SimplePolygons(SimpleConvexPolygon2D(Point2D(0.75,0.5),
                                                               Point2D(0.5,0.0),
                                                               Point2D(1.0,0.0)))))
        
        # polygon intersetion - overlap - result is a parallelogram
        tr1=Triangle2D(Point2D(0,1), Vector2D(1,0), Vector2D(0.5,-1))
        self.assertEqual(tr.intersect_simple_polygon(tr1),
                         (Points(), 
                          Segments(), 
                          SimplePolygons(SimpleConvexPolygon2D(Point2D(0.25,0.5),
                                               Point2D(0.5,0.0),
                                               Point2D(0.75,0.5),
                                               Point2D(0.5,1.0)))))
        
    def test_intersect_simple_polygon__parallelogram(self):
        ""
        pr=Parallelogram2D(Point2D(0,0),Vector2D(1,0),Vector2D(0,1))
        
        # no intersection
        pr1=Parallelogram2D(Point2D(0,10), Vector2D(1,0), Vector2D(0,1))
        self.assertEqual(pr.intersect_simple_polygon(pr1),
                         (Points(), 
                          Segments(), 
                          SimplePolygons()))
        
        # point intersection
        pr1=Parallelogram2D(Point2D(1,1), Vector2D(1,0), Vector2D(0,1))
        self.assertEqual(pr.intersect_simple_polygon(pr1),
                         (Points(Point2D(1,1)), 
                          Segments(), 
                          SimplePolygons()))
        
        # segment intersection
        pr1=Parallelogram2D(Point2D(0,1), Vector2D(1,0), Vector2D(0,1))
        self.assertEqual(pr.intersect_simple_polygon(pr1),
                         (Points(), 
                          Segments(Segment2D(Point2D(0,1),
                                             Point2D(1,1))), 
                          SimplePolygons()))
        
        # polygon intersection - self
        #print(pr.intersect_simple_polygon(pr))
        return
        self.assertEqual(pr.intersect_simple_polygon(pr),
                         (Points(), 
                          Segments(), 
                          SimplePolygons(pr)))
        
        
#    def test_intersect_halfline(self):
#        ""
#        pg=SimplePolygon2D(*points)
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
#        pg=SimplePolygon2D(Point2D(0,0),
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
#        pg=SimplePolygon2D(*points)
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
#        pg=SimplePolygon2D(Point2D(0,0),
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
#    def test_intersect_segment(self):
#        ""
#        pg=SimplePolygon2D(*points)
#        
#        # convex polygon
#        self.assertEqual(pg.intersect_segment(Segment2D(Point2D(0,0),
#                                                        Point2D(1,1))),
#                         ([], 
#                          [Segment2D(Point2D(0.0,0.0), 
#                                     Point2D(1.0,1.0))]))        
#        
#        self.assertEqual(pg.intersect_segment(Segment2D(Point2D(0,0),
#                                                        Point2D(1,-1))),
#                         ([Point2D(0,0)], 
#                          []))     
#    
#        self.assertEqual(pg.intersect_segment(Segment2D(Point2D(0.5,0.5),
#                                                        Point2D(1,1))),
#                         ([], 
#                          [Segment2D(Point2D(0.5,0.5), 
#                                     Point2D(1.0,1.0))]))    
#            
#        # concave polygon
#        pg=SimplePolygon2D(Point2D(0,0),
#                     Point2D(2,0),
#                     Point2D(1,1),
#                     Point2D(2,2),
#                     Point2D(0,2))
#        
#        self.assertEqual(pg.intersect_segment(Segment2D(Point2D(1.5,0),
#                                                        Point2D(1.5,10))),
#                         ([], 
#                          [Segment2D(Point2D(1.5,0), 
#                                     Point2D(1.5,0.5)),
#                           Segment2D(Point2D(1.5,1.5), 
#                                     Point2D(1.5,2))]))  
#    
#        self.assertEqual(pg.intersect_segment(Segment2D(Point2D(2,0),
#                                                        Point2D(2,10))),
#                         ([Point2D(2,0),
#                           Point2D(2,2)], 
#                          []))  
#    
#        self.assertEqual(pg.intersect_segment(Segment2D(Point2D(1,0),
#                                                        Point2D(1,10))),
#                         ([], 
#                          [Segment2D(Point2D(1,0), 
#                                     Point2D(1,2))]))  
#    
#        self.assertEqual(pg.intersect_segment(Segment2D(Point2D(0,0),
#                                                        Point2D(0,10))),
#                         ([], 
#                          [Segment2D(Point2D(0,0), 
#                                     Point2D(0,2))]))  
#    
#        self.assertEqual(pg.intersect_segment(Segment2D(Point2D(0,0.5),
#                                                        Point2D(10,0.5))),
#                         ([], 
#                          [Segment2D(Point2D(0,0.5), 
#                                     Point2D(1.5,0.5))]))  
#    
#    
#    def test_intersect_polygon(self):
#        ""
#        pg=SimplePolygon2D(*points)
#        
#        # no intersection
#        pg1=SimplePolygon2D(Point2D(-2,0),
#                       Point2D(-1,0),
#                       Point2D(-1,1),
#                       Point2D(-2,1))
#        self.assertEqual(pg.intersect_polygon(pg1),
#                         ([],
#                          []))
#        
#        # point intersection
#        pg1=SimplePolygon2D(Point2D(-1,-1),
#                      Point2D(0,-1),
#                      Point2D(0,0),
#                      Point2D(-1,0))
#        self.assertEqual(pg.intersect_polygon(pg1),
#                         ([Point2D(0,0)],
#                         []))
#    
#        # edge intersection
#        pg1=SimplePolygon2D(Point2D(-1,0),
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
#        pg1=SimplePolygon2D(Point2D(-0.5,-0.5),
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
#    def test_union_polygon(self):
#        ""
#        pg=SimplePolygon2D(*points)
#        
#        # no intersection
#        pg1=SimplePolygon2D(Point2D(-2,0),
#                      Point2D(-1,0),
#                      Point2D(-1,1),
#                      Point2D(-2,1))
#        self.assertEqual(pg.union_polygon(pg1),
#                         ((),
#                          (),
#                          ()))
#        
#        # point intersection
#        pg1=SimplePolygon2D(Point2D(-1,-1),
#                       Point2D(0,-1),
#                        Point2D(0,0),
#                        Point2D(-1,0))
#        self.assertEqual(pg.union_polygon(pg1),
#                         ((Point2D(0,0),),
#                           (),
#                           ()))
#        
#        # edge intersection
#        pg1=SimplePolygon2D(Point2D(-1,0),
#                        Point2D(0,0),
#                        Point2D(0,1),
#                        Point2D(-1,1))
#        self.assertEqual(pg.union_polygon(pg1),
#                         ((),
#                          (Segment2D(Point2D(0,0),
#                                     Point2D(0,1)),),
#                          ()))
#                         
#        
#        # overlap intersection - same polygon
#        self.assertEqual(pg.union_polygon(pg),
#                         pg)
#
#        # overlap intersection
#        pg1=SimplePolygon2D(Point2D(-0.5,-0.5),
#                            Point2D(0.5,-0.5),
#                            Point2D(0.5,0.5),
#                            Point2D(-0.5,0.5))
#        self.assertEqual(pg.union_polygon(pg1),
#                         ((), 
#                          (), 
#                          (SimplePolygon2D(Point2D(0.0,0.0),
#                                     Point2D(0.0,0.5),
#                                     Point2D(0.5,0.5),
#                                     Point2D(0.5,0.0)),)))
#    
        
    def test_next_index(self):
        ""
        pg=SimplePolygon2D(*points)
        self.assertEqual(pg.next_index(0),
                         1)
        self.assertEqual(pg.next_index(3),
                         0)
        
        
    def test_orientation(self):
        ""
        pg=SimplePolygon2D(*points)
        self.assertTrue(pg.orientation>0)
        self.assertTrue(pg.reverse.orientation<0)
        
        
    def test_prevous_index(self):
        ""
        pg=SimplePolygon2D(*points)
        self.assertEqual(pg.previous_index(0),
                         3)
        self.assertEqual(pg.previous_index(3),
                         2)
        
        
    def test_plot(self):
        ""
        if plot:
            
            pg=SimplePolygon2D(*points)
            fig, ax = plt.subplots()
            pg.plot(ax)
            
            # concave polygon
            pg=SimplePolygon2D(Point2D(0,0),
                         Point2D(2,0),
                         Point2D(1,1),
                         Point2D(2,2),
                         Point2D(0,2))
            fig, ax = plt.subplots()
            pg.plot(ax)
        
        
    def test_reorder(self):
        ""
        pg=SimplePolygon2D(*points)
        self.assertEqual(pg.reorder(1),
                         SimplePolygon2D(Point2D(1,0),
                                   Point2D(1,1),
                                   Point2D(0,1),
                                   Point2D(0,0)))
        
        
    def test_reverse(self):
        ""
        pg=SimplePolygon2D(*points)
        self.assertEqual(pg.reverse,
                         SimplePolygon2D(Point2D(0,1),
                                   Point2D(1,1),
                                   Point2D(1,0),
                                   Point2D(0,0)))
        
        
    def test_rightmost_lowest_vertex(self):
        ""
        pg=SimplePolygon2D(*points)
        self.assertEqual(pg.rightmost_lowest_vertex, 
                         1)
        
        
    def test_signed_area(self):
        ""
        pg=SimplePolygon2D(*points)
        self.assertEqual(pg.signed_area, # ccw
                         1)
        self.assertEqual(pg.reverse.signed_area, # cw
                         -1)
        
        
    def test_triangulate(self):
        ""
        # convex polygon
        pg=SimplePolygon2D(*points)
        self.assertEqual(pg.triangulate,
                         Triangles(*[Triangle2D(Point2D(0,0), Vector2D(1,0), Vector2D(0,1)), 
                                     Triangle2D(Point2D(1,0), Vector2D(0,1), Vector2D(-1,1))]))
        
        # concave polygon
        pg=SimplePolygon2D(Point2D(0,0),
                     Point2D(2,0),
                     Point2D(1,1),
                     Point2D(2,2),
                     Point2D(0,2))
        self.assertEqual(pg.triangulate,
                         Triangles(*[Triangle2D(Point2D(2,0), Vector2D(-1,1), Vector2D(-2,0)), 
                                     Triangle2D(Point2D(0,0), Vector2D(1,1), Vector2D(0,2)), 
                                     Triangle2D(Point2D(1,1), Vector2D(1,1), Vector2D(-1,1))]))
    
        
    def test_winding_number(self):
        ""
        pg=SimplePolygon2D(*points)
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
        
    
        
class Test_SimplePolygon3D(unittest.TestCase):
    """
    points=(Point3D(0,0,0),Point3D(1,0,0),Point3D(1,1,0),Point3D(0,1,0))
    """
    
    def test___init__(self):
        ""
        pg=SimplePolygon3D(*points)
        self.assertIsInstance(pg,SimplePolygon3D)
        self.assertEqual(pg.points,points)
        
        
    def test___contains__(self):
        ""
        pg=SimplePolygon3D(*points)
        
        # Point
        
        # --> TO DO
        
        # Segment
        
        # SimplePolygon
        
        
    def test___eq__(self):
        ""
        pg=SimplePolygon3D(*points)
        self.assertTrue(pg==pg)
        
        pg2=SimplePolygon3D(Point3D(0,0,0),Point3D(1,0,0),Point3D(0,1,0))
        self.assertFalse(pg==pg2)
        
        
    def test___repr__(self):
        ""
        pg=SimplePolygon3D(*points)
        self.assertEqual(str(pg),
                         'SimplePolygon3D(Point3D(0,0,0),Point3D(1,0,0),Point3D(1,1,0),Point3D(0,1,0))')
        
    def test_area(self):
        ""
        pg=SimplePolygon3D(*points)
        self.assertEqual(pg.area, # ccw
                         1)
        self.assertEqual(pg.reverse.area, # cw
                         1)
        
        
    def test_centroid(self):
        ""
        pg=SimplePolygon3D(*points)
        self.assertEqual(pg.centroid, 
                         Point3D(0.5,0.5,0))
        
        
    def test_next_index(self):
        ""
        pg=SimplePolygon3D(*points)
        self.assertEqual(pg.next_index(0),
                         1)
        self.assertEqual(pg.next_index(3),
                         0)
        
    
    def test_plane(self):
        ""
        pg=SimplePolygon3D(*points)
        self.assertEqual(pg.plane,
                         Plane3D(Point3D(0,0,0),Vector3D(0,0,1)))
        
        
    def test_plot(self):
        ""
        
        if plot:
        
            pg=SimplePolygon3D(*points)
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            pg.plot(ax)
            
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            pg.plot(ax,normal=True)
            
        
        
    def test_prevous_index(self):
        ""
        pg=SimplePolygon3D(*points)
        self.assertEqual(pg.previous_index(0),
                         3)
        self.assertEqual(pg.previous_index(3),
                         2)
        
        
    def test_project_2D(self):
        ""
        pg=SimplePolygon3D(*points)
        self.assertEqual(pg.project_2D,
                         (2,SimplePolygon2D(Point2D(0,0),Point2D(1,0),Point2D(1,1),Point2D(0,1))))
        
        
    def test_reorder(self):
        ""
        pg=SimplePolygon3D(*points)
        self.assertEqual(pg.reorder(1),
                         SimplePolygon3D(Point3D(1,0,0),
                                   Point3D(1,1,0),
                                   Point3D(0,1,0),
                                   Point3D(0,0,0)))
        
        
    def test_reverse(self):
        ""
        pg=SimplePolygon3D(*points)
        self.assertEqual(pg.reverse,
                         SimplePolygon3D(Point3D(0,1,0),
                                   Point3D(1,1,0),
                                   Point3D(1,0,0),
                                   Point3D(0,0,0)))
        
        
    def test_triangulate(self):
        ""
        # convex polygon
        pg=SimplePolygon3D(*points)
        self.assertEqual(pg.triangulate,
                         Triangles(*[Triangle3D(Point3D(0,0,0), Vector3D(1,0,0), Vector3D(0,1,0)), 
                                     Triangle3D(Point3D(1,0,0), Vector3D(0,1,0), Vector3D(-1,1,0))]))
        
        # concave polygon
        pg=SimplePolygon3D(Point3D(0,0,2),
                     Point3D(2,0,2),
                     Point3D(1,1,2),
                     Point3D(2,2,2),
                     Point3D(0,2,2))
        self.assertEqual(pg.triangulate,
                         Triangles(*[Triangle3D(Point3D(2,0,2), Vector3D(-1,1,0), Vector3D(-2,0,0)), 
                                     Triangle3D(Point3D(0,0,2), Vector3D(1,1,0), Vector3D(0,2,0)), 
                                     Triangle3D(Point3D(1,1,2), Vector3D(1,1,0), Vector3D(-1,1,0))]))
        
        
    
if __name__=='__main__':
    
    points=(Point2D(0,0),Point2D(1,0),Point2D(1,1),Point2D(0,1))
    unittest.main(Test_SimplePolygon2D())
    
    points=(Point3D(0,0,0),Point3D(1,0,0),Point3D(1,1,0),Point3D(0,1,0))
    unittest.main(Test_SimplePolygon3D())
    
    