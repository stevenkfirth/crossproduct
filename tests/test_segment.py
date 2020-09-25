# -*- coding: utf-8 -*-

import unittest
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d

from crossproduct import Point2D, Point3D,Vector2D, Vector3D, \
    Halfline2D, Halfline3D, Line2D, Line3D, Segment2D, Segment3D, \
    Polyline2D, Segments, Points

plot=False

class Test_Segment2D(unittest.TestCase):
    """
    P0=Point2D(0,0)
    P1=Point2D(1,1)
    """

    def test___init__(self):
        ""
        s=Segment2D(P0,P1)
        self.assertIsInstance(s,Segment2D)
        self.assertEqual(s.P0,Point2D(0,0))
        self.assertEqual(s.P1,Point2D(1,1))
          
        
    def test___add__(self):
        ""
        s=Segment2D(P0,P1)
        
        s1=Segment2D(Point2D(1,1), Point2D(2,2))
        self.assertEqual(s+s1,
                         Segment2D(Point2D(0,0), Point2D(2,2)))
        
        self.assertEqual(Segment2D(Point2D(1,1), Point2D(1,2))+Segment2D(Point2D(1,0), Point2D(1,1)),
                         Segment2D(Point2D(1.0,0.0), Point2D(1.0,2.0)))
        
        
    def test___contains__(self):
        ""
        s=Segment2D(P0,P1)
        
        # point
        self.assertTrue(P0 in s)
        self.assertTrue(P1 in s)
        self.assertTrue(P0+s.line.vL*0.5 in s) # segment midpoint
        self.assertFalse(P0+s.line.vL*-0.5 in s) 
        self.assertFalse(P0+s.line.vL*1.5 in s) 
        
        # segment
        self.assertTrue(s in s)
        self.assertTrue(Segment2D(P0,P0+s.line.vL*0.5) in s)
        self.assertTrue(Segment2D(P0+s.line.vL*0.5,P1) in s)
        self.assertFalse(Segment2D(P0+s.line.vL*-0.5,P1) in s)
        self.assertFalse(Segment2D(P0,P1+s.line.vL*0.5) in s)
        self.assertFalse(Segment2D(P0,P0+s.line.vL.perp_vector) in s)
        
        
    def test___eq__(self):
        ""
        s=Segment2D(P0,P1)
        self.assertTrue(s==s)
        self.assertFalse(Segment2D(P0,P0+s.line.vL*0.5)==s)
        
        
    def test___repr__(self):
        ""
        s=Segment2D(P0,P1)
        self.assertEqual(str(s),'Segment2D(Point2D(0,0), Point2D(1,1))')
        
        
    def test_calculate_point(self):
        ""
        s=Segment2D(P0,P1)
        self.assertEqual(s.calculate_point(0.5),
                         P0+s.line.vL*0.5)
        
        
    def test_difference_segment(self):
        ""
        s=Segment2D(P0,P1)
        
        # no intersection, difference is self
        self.assertEqual(s.difference_segment(Segment2D(Point2D(5,5),Point2D(6,6))),
                         Segments(s))
        
        # point intersection, difference is self
        self.assertEqual(s.difference_segment(Segment2D(Point2D(1,1),Point2D(2,2))),
                         Segments(s))
        
        # segment intersection, difference is remaining segment part
        self.assertEqual(s.difference_segment(Segment2D(Point2D(0.5,0.5),Point2D(2,2))),
                         Segments(Segment2D(Point2D(0,0),Point2D(0.5,0.5)),))
        
        
        # self intersection, difference is None
        self.assertEqual(s.difference_segment(s),
                         Segments())
        
        # segment intersection, inside original
        # segment intersection, difference is remaining segment part
        self.assertEqual(s.difference_segment(Segment2D(Point2D(0.25,0.25),Point2D(0.75,0.75))),
                         Segments(Segment2D(Point2D(0,0),Point2D(0.25,0.25)),
                                  Segment2D(Point2D(0.75,0.75),Point2D(1,1))))
        
        # segment intersection, outside both start and end point
        self.assertEqual(s.difference_segment(Segment2D(Point2D(-1,-1),Point2D(2,2))),
                         Segments())
        
        
    def test_difference_segments(self):
        ""
        
        s=Segment2D(P0,P1)
        
        # self intersection - intersection first
        s1=Segments(Segment2D(Point2D(0,0), Point2D(1,1)), 
                    Segment2D(Point2D(1,1), Point2D(2,1)),
                    Segment2D(Point2D(4,1), Point2D(5,1)))
        self.assertEqual(s.difference_segments(s1),
                         Segments())
        
        # self intersection - intersection last
        s1=Segments(Segment2D(Point2D(4,1), Point2D(5,1)), 
                    Segment2D(Point2D(1,1), Point2D(2,1)),
                    Segment2D(Point2D(0,0), Point2D(1,1)))
        self.assertEqual(s.difference_segments(s1),
                         Segments())
                
        # no intersection
        s1=Segments(Segment2D(Point2D(0,0), Point2D(1,0)), 
                    Segment2D(Point2D(1,1), Point2D(2,1)))
        self.assertEqual(s.difference_segments(s1),
                         Segments(s))
        
        # mid intersection
        s1=Segments(Segment2D(Point2D(0,0), Point2D(0.5,0.5)), 
                    Segment2D(Point2D(1,1), Point2D(2,1)))
        self.assertEqual(s.difference_segments(s1),
                         Segments(Segment2D(Point2D(0.5,0.5), Point2D(1,1))))
        
        # full intersection using two segments
        s1=Segments(Segment2D(Point2D(0,0), Point2D(0.5,0.5)), 
                    Segment2D(Point2D(0.5,0.5), Point2D(1,1)))
        self.assertEqual(s.difference_segments(s1),
                         Segments())
        
        # intersection inside original
        s1=Segments(Segment2D(Point2D(0.25,0.25),Point2D(0.75,0.75)), 
                    Segment2D(Point2D(1,1), Point2D(2,2)))
        self.assertEqual(s.difference_segments(s1),
                         Segments(Segment2D(Point2D(0,0), 
                                            Point2D(0.25,0.25)), 
                                  Segment2D(Point2D(0.75,0.75), 
                                            Point2D(1,1))))
        
        # intersection inside original
        s1=Segments(Segment2D(Point2D(0.2,0.2),Point2D(0.4,0.4)), 
                    Segment2D(Point2D(0.6,0.6), Point2D(0.8,0.8)))
        self.assertEqual(s.difference_segments(s1),
                         Segments(Segment2D(Point2D(0,0), 
                                            Point2D(0.2,0.2)), 
                                  Segment2D(Point2D(0.4,0.4), 
                                            Point2D(0.6,0.6)), 
                                  Segment2D(Point2D(0.8,0.8), 
                                            Point2D(1.0,1.0))))
        
        
    def test_distance_to_point(self):
        ""
        s=Segment2D(P0,P1)
        self.assertEqual(s.distance_to_point(Point2D(-2,0)),
                         2) 
        self.assertEqual(s.distance_to_point(Point2D(2,1)),
                         1) 
        self.assertEqual(s.distance_to_point(Point2D(0,1)),
                         0.5**0.5) 
        self.assertEqual(s.distance_to_point(Point2D(1,0)),
                         0.5**0.5) 
        
        
    def test_intersect_halfline(self):
        ""
        s=Segment2D(P0,P1)
        
        # collinear - same start point
        self.assertEqual(s.intersect_halfline(Halfline2D(P0,
                                                         s.line.vL)),
                         s)
        
        # collinear - halfline start point is segment end point
        self.assertEqual(s.intersect_halfline(Halfline2D(P1,
                                                         s.line.vL)),
                         P1)
        
        # collinear - halfline start point is segment mid point
        self.assertEqual(s.intersect_halfline(Halfline2D(P0+s.line.vL*0.5,
                                                         s.line.vL)),
                         Segment2D(P0+s.line.vL*0.5,P1))

        self.assertEqual(s.intersect_halfline(Halfline2D(P0+s.line.vL*0.5,
                                                         s.line.vL*-1)),
                         Segment2D(P0,P0+s.line.vL*0.5))


    def test_intersect_line(self):
        ""
        s=Segment2D(P0,P1)
        
        # collinear
        self.assertEqual(s.intersect_line(Line2D(P0,
                                                 s.line.vL)),
                         s)
        
        # parallel
        self.assertEqual(s.intersect_line(Line2D(P0+s.line.vL.perp_vector,
                                                 s.line.vL)),
                         None)
        
        # skew - same P0s
        self.assertEqual(s.intersect_line(Line2D(P0,
                                                 s.line.vL.perp_vector)),
                         P0)
        
        # skew - different P0s
        self.assertEqual(s.intersect_line(Line2D(Point2D(0.5,0),
                                                 s.line.vL.perp_vector)),
                         Point2D(0.25,0.25))
        
        # skew - no intersection
        self.assertEqual(s.intersect_line(Line2D(P0+s.line.vL*-1,
                                                 s.line.vL.perp_vector)),
                         None)
        
    def test_intersect_segment(self):
        ""
        s=Segment2D(P0,P1)
        
        # collinear - same segment
        self.assertEqual(s.intersect_segment(s),
                         s)
    
        # collinear - different start point inside segment
        self.assertEqual(s.intersect_segment(Segment2D(P0+s.line.vL*0.5,
                                                       P1)),
                         Segment2D(P0+s.line.vL*0.5,
                                   P1))
        
        # collinear - different start point outside segment
        self.assertEqual(s.intersect_segment(Segment2D(P0+s.line.vL*-0.5,
                                                       P1)),
                         s)

        # collinear - different end point inside segment
        self.assertEqual(s.intersect_segment(Segment2D(P0,
                                                       P1+s.line.vL*-0.5)),
                         Segment2D(P0,
                                   P1+s.line.vL*-0.5))
        
        # collinear - different start point outside segment
        self.assertEqual(s.intersect_segment(Segment2D(P0,
                                                       P1+s.line.vL*0.5)),
                         s)
        
        # collinear - start point and end point inside segment
        self.assertEqual(s.intersect_segment(Segment2D(P0+s.line.vL*0.25,
                                                       P1+s.line.vL*-0.25)),
                         Segment2D(P0+s.line.vL*0.25,
                                   P1+s.line.vL*-0.25))
        
        # collinear - start point and end point outside segment
        self.assertEqual(s.intersect_segment(Segment2D(P0+s.line.vL*-0.25,
                                                       P1+s.line.vL*0.25)),
                         s)
        
        # collinear - but no intersection
        self.assertEqual(s.intersect_segment(Segment2D(P0+s.line.vL*2,
                                                       P1+s.line.vL*2)),
                         None)
        
        # parallel
        self.assertEqual(s.intersect_segment(Segment2D(P0+s.line.vL.perp_vector,
                                                       P1+s.line.vL.perp_vector)),
                         None)
        
        # skew - intersecting at start point
        self.assertEqual(s.intersect_segment(Segment2D(P0,
                                                       P1+s.line.vL.perp_vector)),
                         P0)
        
        # skew - intersecting at end point
        self.assertEqual(s.intersect_segment(Segment2D(P1+s.line.vL.perp_vector*-1,
                                                       P1+s.line.vL.perp_vector)),
                         P1)
        
        # skew - intersecting at mid points
        self.assertEqual(s.intersect_segment(Segment2D(P0+s.line.vL*0.5+s.line.vL.perp_vector*-0.5,
                                                       P0+s.line.vL*0.5+s.line.vL.perp_vector*0.5)),
                         P0+s.line.vL*0.5)
        
        # skew - no intersection
        self.assertEqual(s.intersect_segment(Segment2D(P0+s.line.vL.perp_vector*0.5,
                                                       P0+s.line.vL.perp_vector*1.5)),
                         None)
        
        
    def test_line(self):
        ""
        s=Segment2D(P0,P1)
        self.assertEqual(s.line,
                         Line2D(P0,s.line.vL))
        
        
    def test_plot(self):
        ""
        if plot:
            s=Segment2D(P0,P1)
            fig, ax = plt.subplots()
            s.plot(ax)
    
    
    def test_points(self):
        ""
        s=Segment2D(P0,P1)
        self.assertEqual(s.points,
                         Points(P0,P1))
        
        
    def reverse(self):
        ""
        s=Segment2D(P0,P1)
        self.assertEqual(s.reverse,
                         Segment2D(P1,P0))
        
        
        
class Test_Segment3D(unittest.TestCase):
    """
    P0=Point3D(0,0,0)
    P1=Point3D(1,1,1)
    """

    def test___init__(self):
        ""
        s=Segment3D(P0,P1)
        self.assertIsInstance(s,Segment3D)
        self.assertEqual(s.P0,Point3D(0,0,0))
        self.assertEqual(s.P1,Point3D(1,1,1))
          
        
    def test___contains__(self):
        ""
        s=Segment3D(P0,P1)
        
        # point
        self.assertTrue(P0 in s)
        self.assertTrue(P1 in s)
        self.assertTrue(P0+s.line.vL*0.5 in s) # segment midpoint
        self.assertFalse(P0+s.line.vL*-0.5 in s) 
        self.assertFalse(P0+s.line.vL*1.5 in s) 
        
        # segment
        self.assertTrue(s in s)
        self.assertTrue(Segment3D(P0,P0+s.line.vL*0.5) in s)
        self.assertTrue(Segment3D(P0+s.line.vL*0.5,P1) in s)
        self.assertFalse(Segment3D(P0+s.line.vL*-0.5,P1) in s)
        self.assertFalse(Segment3D(P0,P1+s.line.vL*0.5) in s)
        self.assertFalse(Segment3D(P0,P0+Vector3D(1,-1,0)) in s)
        
        
    def test___eq__(self):
        ""
        s=Segment3D(P0,P1)
        self.assertTrue(s==s)
        self.assertFalse(Segment3D(P0,P0+s.line.vL*0.5)==s)
        
        
    def test___repr__(self):
        ""
        s=Segment3D(P0,P1)
        self.assertEqual(str(s),'Segment3D(Point3D(0,0,0), Point3D(1,1,1))')
        
        
    def test_calculate_point(self):
        ""
        s=Segment3D(P0,P1)
        self.assertEqual(s.calculate_point(0.5),
                         P0+s.line.vL*0.5)
        
        
    def test_distance_to_point(self):
        ""
        s=Segment3D(P0,P1)
        self.assertEqual(s.distance_to_point(Point3D(-2,0,0)),
                         2) 
        self.assertEqual(s.distance_to_point(Point3D(1,1,2)),
                         1) 
        self.assertEqual(s.distance_to_point(Point3D(0,0,0)),
                         0) 
        self.assertEqual(s.distance_to_point(Point3D(1,-1,0)),
                         (s.P0-Point3D(1,-1,0)).length) 
        
        
    def test_distance_to_segment(self):
        ""
        s=Segment3D(P0,P1)
        
        # line
        self.assertEqual(s.distance_to_segment(s),
                         0)
        self.assertEqual(s.distance_to_segment(Segment3D(P0+Vector3D(1,-1,0),
                                                         P1+Vector3D(1,-1,0))),
                         Vector3D(1,-1,0).length)
        self.assertEqual(s.distance_to_segment(Segment3D(P0,
                                                         Point3D(1,-1,0))), 
                         0)
        self.assertEqual(s.distance_to_segment(Segment3D(Point3D(-2,-2,-2),
                                                         Point3D(-1,-1,-1))),
                         Vector3D(1,1,1).length)
        
        
    def test_intersect_segment(self):
        ""
        s1=Segment3D(Point3D(0,0,0), Point3D(0,1,0))
        s2=Segment3D(Point3D(0,1,0), Point3D(1,1,0))
        
        self.assertEqual(s1.intersect_segment(s2),
                         Point3D(0,1,0))
        
        
    def test_line(self):
        ""
        s=Segment3D(P0,P1)
        self.assertEqual(s.line,
                         Line3D(P0,P1-P0))
        
        
    def test_order(self):
        ""
        s=Segment3D(P0,P1)
        self.assertEqual(s.order.points,
                         s.points)
        
        s=Segment3D(P1,P0)
        self.assertEqual(s.order.points,
                        Points(Point3D(0,0,0), Point3D(1,1,1)))
        
        
    def test_plot(self):
        ""
        if plot:
            s=Segment3D(P0,P1)
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            s.plot(ax)
        
        
    def test_points(self):
        ""
        s=Segment3D(P0,P1)
        self.assertEqual(s.points,
                         Points(P0,P1))
        
        
    def reverse(self):
        ""
        s=Segment3D(P0,P1)
        self.assertEqual(s.reverse,
                         Segment3D(P1,P0))
        
        
    
        
        
    
if __name__=='__main__':
    
    P0=Point2D(0,0)
    P1=Point2D(1,1)
    unittest.main(Test_Segment2D())
    
    P0=Point3D(0,0,0)
    P1=Point3D(1,1,1)
    unittest.main(Test_Segment3D())