# -*- coding: utf-8 -*-

import unittest
from crossproduct import Point2D, Vector2D, Line2D, Halfline2D, Segment2D, \
    Point3D, Vector3D, Line3D, Halfline3D, Segment3D


class Test_Line2D(unittest.TestCase):
    """
    P0=Point2D(0,0)
    vL=Vector2D(1,1)
    """
    
    def test___init__(self):
        ""
        l=Line2D(P0,vL)
        self.assertIsInstance(l,
                              Line2D)
        self.assertEqual(l.P0,
                         P0)
        self.assertEqual(l.vL,
                         vL)
        
        
    def test___contains__(self):
        ""
        l=Line2D(P0,vL)
        
        # point
        self.assertTrue(P0 in l)
        self.assertTrue(P0+vL in l)
        self.assertFalse(P0+vL.perp_vector in l)
        
        # halfline
        self.assertTrue(Halfline2D(P0,vL) in l)
        self.assertTrue(Halfline2D(P0+vL,vL) in l)
        self.assertFalse(Halfline2D(P0+vL.perp_vector,vL) in l)
        self.assertFalse(Halfline2D(P0,vL.perp_vector) in l)
        
        # segment
        self.assertTrue(Segment2D(P0,P0+vL) in l)
        self.assertTrue(Segment2D(P0,P0+vL*10) in l)
        self.assertFalse(Segment2D(P0+vL.perp_vector,P0+vL) in l)
        self.assertFalse(Segment2D(P0+vL.perp_vector,P0+vL+vL.perp_vector) in l)
        
        
    def test___eq__(self):
        ""
        l=Line2D(P0,vL)
        self.assertTrue(l==Line2D(P0,vL*2))
        self.assertTrue(l==Line2D(P0,vL.opposite))
        self.assertTrue(l==Line2D(P0+vL,vL))
        self.assertFalse(l==Line2D(P0,vL.perp_vector))
        self.assertFalse(l==Line2D(P0+vL.perp_vector,vL))
        
        
    def test___repr__(self):
        ""
        l=Line2D(P0,vL)
        self.assertEqual(str(l),
                         'Line2D(Point2D(0,0), Vector2D(1,1))')
        
        
    def test_calculate_point(self):
        ""
        l=Line2D(P0,vL)
        self.assertEqual(l.calculate_point(2),
                         P0+vL*2)
        
        
    def test_calculate_t_from_point(self):
        ""
        l=Line2D(P0,vL)
        self.assertEqual(l.calculate_t_from_point(P0+vL*2),
                         2)
    

    def test_calculate_t_from_x(self):
        ""
        l=Line2D(P0,vL)
        self.assertEqual(l.calculate_t_from_x(2),
                         2)
        
                
    def test_calculate_t_from_y(self):
        ""
        l=Line2D(P0,vL)
        self.assertEqual(l.calculate_t_from_y(3),
                         3)    
    

    def test_distance_to_point(self):
        ""
        l=Line2D(P0,vL)
        
        self.assertEqual(l.distance_to_point(P0),
                         0)
        self.assertEqual(l.distance_to_point(P0+vL),
                         0)
        self.assertEqual(l.distance_to_point(P0+vL.perp_vector),
                         vL.length)

    def test_distance_to_line(self):
        ""
        l=Line2D(P0,vL)
        
        self.assertEqual(l.distance_to_line(l),
                         0)
        self.assertEqual(l.distance_to_line(Line2D(P0+vL.perp_vector,vL)),
                         vL.length)
        self.assertEqual(l.distance_to_line(Line2D(P0,vL.perp_vector)), 
                         0)
        
        
    def test_intersect_line(self):
        ""
        l=Line2D(P0,vL)
        
        # collinear
        self.assertEqual(l.intersect_line(l),
                         l)
        
        # parallel
        self.assertEqual(l.intersect_line(Line2D(P0+vL.perp_vector,vL)),
                         None)
        
        # skew
        self.assertEqual(l.intersect_line(Line2D(P0,vL.perp_vector)),
                         P0)
        
        # skew - different P0s
        self.assertEqual(l.intersect_line(Line2D(P0+vL,vL.perp_vector)),
                         P0+vL)
        
        
    def test__intersect_line_skew(self):
        ""
        l=Line2D(P0,vL)
        self.assertEqual(l._intersect_line_skew(Line2D(P0,vL.perp_vector)),
                         P0)
        self.assertEqual(l._intersect_line_skew(Line2D(P0+vL,vL.perp_vector)),
                         P0+vL)
    
        
    def test_is_parallel(self):
        ""
        l=Line2D(P0,vL)
        self.assertTrue(l.is_parallel(l))
        self.assertTrue(l.is_parallel(Line2D(P0,vL.opposite)))
        self.assertTrue(l.is_parallel(Line2D(P0+vL.perp_vector,vL)))
        
        
        
class Test_Line3D(unittest.TestCase):
    """
    P0=Point2D(0,0,0)
    vL=Vector2D(1,1,1)
    """
    
    def test___init__(self):
        ""
        l=Line3D(P0,vL)
        self.assertIsInstance(l,
                              Line3D)
        self.assertEqual(l.P0,
                         P0)
        self.assertEqual(l.vL,
                         vL)
        
        
    def test___contains__(self):
        ""
        l=Line3D(P0,vL)
        
        # point
        self.assertTrue(P0 in l)
        self.assertTrue(P0+vL in l)
        self.assertFalse(P0+Vector3D(1,-1,0) in l)
        
#        # halfline
#        self.assertTrue(Halfline3D(P0,vL) in l)
#        self.assertTrue(Halfline3D(P0+vL,vL) in l)
#        self.assertFalse(Halfline3D(P0+Vector3D(1,-1,0),vL) in l)
#        self.assertFalse(Halfline3D(P0,Vector3D(1,-1,0)) in l)
#        
#        # segment
#        self.assertTrue(Segment3D(P0,P0+vL) in l)
#        self.assertTrue(Segment3D(P0,P0+vL*10) in l)
#        self.assertFalse(Segment3D(P0+Vector3D(1,-1,0),P0+vL) in l)
#        self.assertFalse(Segment3D(P0+Vector3D(1,-1,0),P0+vL+Vector3D(1,-1,0)) in l)
        
        
    def test___eq__(self):
        ""
        l=Line3D(P0,vL)
        self.assertTrue(l==Line3D(P0,vL*2))
        self.assertTrue(l==Line3D(P0,vL.opposite))
        self.assertTrue(l==Line3D(P0+vL,vL))
        self.assertFalse(l==Line3D(P0,Vector3D(1,-1,0)))
        self.assertFalse(l==Line3D(P0+Vector3D(1,-1,0),vL))
        
        
    def test___repr__(self):
        ""
        l=Line3D(P0,vL)
        self.assertEqual(str(l),
                         'Line3D(Point3D(0,0,0), Vector3D(1,1,1))')
        
        
    def test_calculate_point(self):
        ""
        l=Line3D(P0,vL)
        self.assertEqual(l.calculate_point(2),
                         P0+vL*2)
        
        
    def test_calculate_t_from_point(self):
        ""
        l=Line3D(P0,vL)
        self.assertEqual(l.calculate_t_from_point(P0+vL*2),
                         2)
    

    def test_calculate_t_from_x(self):
        ""
        l=Line3D(P0,vL)
        self.assertEqual(l.calculate_t_from_x(2),
                         2)
        
                
    def test_calculate_t_from_y(self):
        ""
        l=Line3D(P0,vL)
        self.assertEqual(l.calculate_t_from_y(3),
                         3)    
    

    def test_distance_to_point(self):
        ""
        l=Line3D(P0,vL)
        
        # point
        self.assertEqual(l.distance_to_point(P0),
                         0)
        self.assertEqual(l.distance_to_point(P0+Vector3D(1,-1,0)),
                         Vector3D(1,-1,0).length)


    def test_distance_to_line(self):
        ""
        l=Line3D(P0,vL)
        
        # line
        self.assertEqual(l.distance_to_line(l),
                         0)
        self.assertEqual(l.distance_to_line(Line3D(P0+Vector3D(1,-1,0),vL)),
                         Vector3D(1,-1,0).length)
        self.assertEqual(l.distance_to_line(Line3D(P0,Vector3D(1,-1,0))), 
                         0)
        
        self.assertEqual(Line3D(Point3D(0,0,0),
                                Vector3D(1,0,0)).distance_to_line(Line3D(Point3D(0,0,1),
                                         Vector3D(0,1,0))),
                        1)
                
                
        
    def test_intersect_line(self):
        ""
        l=Line3D(P0,vL)
        
        # collinear
        self.assertEqual(l.intersect_line(l),
                         l)
        
        # parallel
        self.assertEqual(l.intersect_line(Line3D(P0+Vector3D(1,-1,0),vL)),
                         None)
        
        #skew
        self.assertEqual(l.intersect_line(Line3D(P0,
                                                      Vector3D(1,-1,0))),
                         P0)
        self.assertEqual(l.intersect_line(Line3D(P0+vL,
                                                      Vector3D(1,-1,0))),
                         P0+vL)
        self.assertEqual(l.intersect_line(Line3D(Point3D(0,0,1),
                                                      Vector3D(1,-1,0))),
                         None)
        
        
    def test__intersect_line_skew(self):
        ""
        l=Line3D(P0,vL)
        self.assertEqual(l._intersect_line_skew(Line3D(P0,
                                                      Vector3D(1,-1,0))),
                         P0)
        self.assertEqual(l._intersect_line_skew(Line3D(Point3D(0,0,1),
                                                      Vector3D(1,-1,0))),
                         None)
    
        
    def test_is_parallel(self):
        ""
        l=Line3D(P0,vL)
        self.assertTrue(l.is_parallel(l))
        self.assertTrue(l.is_parallel(Line3D(P0,vL.opposite)))
        self.assertTrue(l.is_parallel(Line3D(P0+Vector3D(1,-1,0),vL)))
        
        
    def test_project_2D(self):
        ""
        l=Line3D(P0,vL)
        self.assertEqual(l.project_2D(0),
                         Line2D(Point2D(0,0),Vector2D(1,1)))
        self.assertEqual(l.project_2D(1),
                         Line2D(Point2D(0,0),Vector2D(1,1)))
        self.assertEqual(l.project_2D(2),
                         Line2D(Point2D(0,0),Vector2D(1,1)))
    
        
        
    
    
if __name__=='__main__':
    
    P0=Point2D(0,0)
    vL=Vector2D(1,1)
    unittest.main(Test_Line2D())
    
    P0=Point3D(0,0,0)
    vL=Vector3D(1,1,1)
    unittest.main(Test_Line3D())
    
    