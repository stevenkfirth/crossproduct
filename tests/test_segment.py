# -*- coding: utf-8 -*-

import unittest
from crossproduct import Point2D, Point3D,Vector2D, Vector3D, \
    HalfLine2D, HalfLine3D, Line2D, Line3D, Segment2D, Segment3D



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
          
        
    def test___contains__(self):
        ""
        s=Segment2D(P0,P1)
        
        # point
        self.assertTrue(P0 in s)
        self.assertTrue(P1 in s)
        self.assertTrue(P0+s.vL*0.5 in s) # segment midpoint
        self.assertFalse(P0+s.vL*-0.5 in s) 
        self.assertFalse(P0+s.vL*1.5 in s) 
        
        # segment
        self.assertTrue(s in s)
        self.assertTrue(Segment2D(P0,P0+s.vL*0.5) in s)
        self.assertTrue(Segment2D(P0+s.vL*0.5,P1) in s)
        self.assertFalse(Segment2D(P0+s.vL*-0.5,P1) in s)
        self.assertFalse(Segment2D(P0,P1+s.vL*0.5) in s)
        self.assertFalse(Segment2D(P0,P0+s.vL.perp_vector) in s)
        
        
    def test___eq__(self):
        ""
        s=Segment2D(P0,P1)
        self.assertTrue(s==s)
        self.assertFalse(Segment2D(P0,P0+s.vL*0.5)==s)
        
        
    def test___repr__(self):
        ""
        s=Segment2D(P0,P1)
        self.assertEqual(str(s),'Segment2D(Point2D(0,0), Point2D(1,1))')
        
        
    def test_calculate_point(self):
        ""
        s=Segment2D(P0,P1)
        self.assertEqual(s.calculate_point(0.5),
                         P0+s.vL*0.5)
        
        
    def test_calculate_t_from_point(self):
        ""
        s=Segment2D(P0,P1)
        self.assertEqual(s.calculate_t_from_point(P0+s.vL*0.5),
                         0.5)
    

    def test_calculate_t_from_x(self):
        ""
        s=Segment2D(P0,P1)
        self.assertEqual(s.calculate_t_from_x(2),
                         2)
        
                
    def test_calculate_t_from_y(self):
        ""
        s=Segment2D(P0,P1)
        self.assertEqual(s.calculate_t_from_y(3),
                         3)    
        
        
    def test_distance_point(self):
        ""
        s=Segment2D(P0,P1)
        self.assertEqual(s.distance_point(Point2D(-2,0)),
                         2) 
        self.assertEqual(s.distance_point(Point2D(2,1)),
                         1) 
        self.assertEqual(s.distance_point(Point2D(0,1)),
                         0.5**0.5) 
        self.assertEqual(s.distance_point(Point2D(1,0)),
                         0.5**0.5) 
        
        
    def test_intersect_halfline(self):
        ""
        s=Segment2D(P0,P1)
        
        # collinear - same start point
        self.assertEqual(s.intersect_halfline(HalfLine2D(P0,
                                                         s.vL)),
                         s)
        
        # collinear - halfline start point is segment end point
        self.assertEqual(s.intersect_halfline(HalfLine2D(P1,
                                                         s.vL)),
                         P1)
        
        # collinear - halfline start point is segment mid point
        self.assertEqual(s.intersect_halfline(HalfLine2D(P0+s.vL*0.5,
                                                         s.vL)),
                         Segment2D(P0+s.vL*0.5,P1))

        self.assertEqual(s.intersect_halfline(HalfLine2D(P0+s.vL*0.5,
                                                         s.vL*-1)),
                         Segment2D(P0,P0+s.vL*0.5))


    def test_intersect_line(self):
        ""
        s=Segment2D(P0,P1)
        
        # collinear
        self.assertEqual(s.intersect_line(Line2D(P0,
                                                 s.vL)),
                         s)
        
        # parallel
        self.assertEqual(s.intersect_line(Line2D(P0+s.vL.perp_vector,
                                                 s.vL)),
                         None)
        
        # skew - same P0s
        self.assertEqual(s.intersect_line(Line2D(P0,
                                                 s.vL.perp_vector)),
                         P0)
        
        # skew - different P0s
        self.assertEqual(s.intersect_line(Line2D(Point2D(0.5,0),
                                                 s.vL.perp_vector)),
                         Point2D(0.25,0.25))
        
        # skew - no intersection
        self.assertEqual(s.intersect_line(Line2D(P0+s.vL*-1,
                                                 s.vL.perp_vector)),
                         None)
        
    def test_intersect_segment(self):
        ""
        s=Segment2D(P0,P1)
        
        # collinear - same segment
        self.assertEqual(s.intersect_segment(s),
                         s)
    
        # collinear - different start point inside segment
        self.assertEqual(s.intersect_segment(Segment2D(P0+s.vL*0.5,
                                                       P1)),
                         Segment2D(P0+s.vL*0.5,
                                   P1))
        
        # collinear - different start point outside segment
        self.assertEqual(s.intersect_segment(Segment2D(P0+s.vL*-0.5,
                                                       P1)),
                         s)

        # collinear - different end point inside segment
        self.assertEqual(s.intersect_segment(Segment2D(P0,
                                                       P1+s.vL*-0.5)),
                         Segment2D(P0,
                                   P1+s.vL*-0.5))
        
        # collinear - different start point outside segment
        self.assertEqual(s.intersect_segment(Segment2D(P0,
                                                       P1+s.vL*0.5)),
                         s)
        
        # collinear - start point and end point inside segment
        self.assertEqual(s.intersect_segment(Segment2D(P0+s.vL*0.25,
                                                       P1+s.vL*-0.25)),
                         Segment2D(P0+s.vL*0.25,
                                   P1+s.vL*-0.25))
        
        # collinear - start point and end point outside segment
        self.assertEqual(s.intersect_segment(Segment2D(P0+s.vL*-0.25,
                                                       P1+s.vL*0.25)),
                         s)
        
        # collinear - but no intersection
        self.assertEqual(s.intersect_segment(Segment2D(P0+s.vL*2,
                                                       P1+s.vL*2)),
                         None)
        
        # parallel
        self.assertEqual(s.intersect_segment(Segment2D(P0+s.vL.perp_vector,
                                                       P1+s.vL.perp_vector)),
                         None)
        
        # skew - intersecting at start point
        self.assertEqual(s.intersect_segment(Segment2D(P0,
                                                       P1+s.vL.perp_vector)),
                         P0)
        
        # skew - intersecting at end point
        self.assertEqual(s.intersect_segment(Segment2D(P1+s.vL.perp_vector*-1,
                                                       P1+s.vL.perp_vector)),
                         P1)
        
        # skew - intersecting at mid points
        self.assertEqual(s.intersect_segment(Segment2D(P0+s.vL*0.5+s.vL.perp_vector*-0.5,
                                                       P0+s.vL*0.5+s.vL.perp_vector*0.5)),
                         P0+s.vL*0.5)
        
        # skew - no intersection
        self.assertEqual(s.intersect_segment(Segment2D(P0+s.vL.perp_vector*0.5,
                                                       P0+s.vL.perp_vector*1.5)),
                         None)
        
        
    def test_is_collinear(self):
        ""
        s=Segment2D(P0,P1)
        
        self.assertTrue(s.is_collinear(s))
        
        self.assertFalse(s.is_collinear(Segment2D(Point2D(1,1),
                                                  Point2D(2,1))))
        
        
        
    def test_line(self):
        ""
        s=Segment2D(P0,P1)
        self.assertEqual(s.line,
                         Line2D(P0,s.vL))
        
        
    def test_points(self):
        ""
        s=Segment2D(P0,P1)
        self.assertEqual(s.points,
                         (P0,P1))
        
        
    def test_union(self):
        ""
        s=Segment2D(P0,P1)
        
        # two adjacent collinear segments
        self.assertEqual(s.union(Segment2D(Point2D(1,1),
                                           Point2D(2,2))),
                         Segment2D(Point2D(0,0),
                                   Point2D(2,2)))
            
        self.assertEqual(s.union(Segment2D(Point2D(2,2),
                                           Point2D(1,1))),
                         Segment2D(Point2D(0,0),
                                   Point2D(2,2)))
            
        # two non-collinear segment
        self.assertEqual(s.union(Segment2D(Point2D(1,1),
                                           Point2D(2,1))),
                         None)
            
        # two collinear non-adjacent segments
        self.assertEqual(s.union(Segment2D(Point2D(2,2),
                                           Point2D(3,3))),
                         None)
            
        # two collinear overlapping segments
        self.assertEqual(s.union(Segment2D(Point2D(0.5,0.5),
                                           Point2D(2,2))),
                         Segment2D(Point2D(0,0),
                                   Point2D(2,2)))
            
        
    def test_vL(self):
        ""
        s=Segment2D(P0,P1)
        
        self.assertEqual(s.vL,
                         P1-P0)
        
        
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
        self.assertTrue(P0+s.vL*0.5 in s) # segment midpoint
        self.assertFalse(P0+s.vL*-0.5 in s) 
        self.assertFalse(P0+s.vL*1.5 in s) 
        
        # segment
        self.assertTrue(s in s)
        self.assertTrue(Segment3D(P0,P0+s.vL*0.5) in s)
        self.assertTrue(Segment3D(P0+s.vL*0.5,P1) in s)
        self.assertFalse(Segment3D(P0+s.vL*-0.5,P1) in s)
        self.assertFalse(Segment3D(P0,P1+s.vL*0.5) in s)
        self.assertFalse(Segment3D(P0,P0+Vector3D(1,-1,0)) in s)
        
        
    def test___eq__(self):
        ""
        s=Segment3D(P0,P1)
        self.assertTrue(s==s)
        self.assertFalse(Segment3D(P0,P0+s.vL*0.5)==s)
        
        
    def test___repr__(self):
        ""
        s=Segment3D(P0,P1)
        self.assertEqual(str(s),'Segment3D(Point3D(0,0,0), Point3D(1,1,1))')
        
        
    def test_calculate_point(self):
        ""
        s=Segment3D(P0,P1)
        self.assertEqual(s.calculate_point(0.5),
                         P0+s.vL*0.5)
        
        
    def test_calculate_t_from_point(self):
        ""
        s=Segment3D(P0,P1)
        self.assertEqual(s.calculate_t_from_point(P0+s.vL*0.5),
                         0.5)
    

    def test_calculate_t_from_x(self):
        ""
        s=Segment3D(P0,P1)
        self.assertEqual(s.calculate_t_from_x(2),
                         2)
        
                
    def test_calculate_t_from_y(self):
        ""
        s=Segment3D(P0,P1)
        self.assertEqual(s.calculate_t_from_y(3),
                         3)    
        
        
    def test_distance_point(self):
        ""
        s=Segment3D(P0,P1)
        self.assertEqual(s.distance_point(Point3D(-2,0,0)),
                         2) 
        self.assertEqual(s.distance_point(Point3D(1,1,2)),
                         1) 
        self.assertEqual(s.distance_point(Point3D(0,0,0)),
                         0) 
        self.assertEqual(s.distance_point(Point3D(1,-1,0)),
                         (s.P0-Point3D(1,-1,0)).length) 
        
        
    def test_distance_segment(self):
        ""
        s=Segment3D(P0,P1)
        
        # line
        self.assertEqual(s.distance_segment(s),
                         0)
        self.assertEqual(s.distance_segment(Segment3D(P0+Vector3D(1,-1,0),
                                                      P1+Vector3D(1,-1,0))),
                         Vector3D(1,-1,0).length)
        self.assertEqual(s.distance_segment(Segment3D(P0,
                                                      Point3D(1,-1,0))), 
                         0)
        self.assertEqual(s.distance_segment(Segment3D(Point3D(-2,-2,-2),
                                                      Point3D(-1,-1,-1))),
                         Vector3D(1,1,1).length)
        
        
    def test_line(self):
        ""
        s=Segment3D(P0,P1)
        self.assertEqual(s.line,
                         Line3D(P0,s.vL))
        
        
    def test_points(self):
        ""
        s=Segment3D(P0,P1)
        self.assertEqual(s.points,
                         (P0,P1))
        
        
    def test_vL(self):
        ""
        s=Segment3D(P0,P1)
        self.assertEqual(s.vL,
                         s.P1-s.P0)
        
        
    
if __name__=='__main__':
    
    P0=Point2D(0,0)
    P1=Point2D(1,1)
    unittest.main(Test_Segment2D())
    
    P0=Point3D(0,0,0)
    P1=Point3D(1,1,1)
    unittest.main(Test_Segment3D())