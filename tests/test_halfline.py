# -*- coding: utf-8 -*-

import unittest
from bspy.geometry import Point2D, Point3D,Vector2D, Vector3D, \
    HalfLine2D, HalfLine3D, Line2D, Line3D, Segment2D, Segment3D



class Test_HalfLine2D(unittest.TestCase):
    """
    P0=Point2D(0,0)
    vL=Vector2D(1,1)
    """
    
    def test___init__(self):
        ""
        hl=HalfLine2D(P0,vL)
        self.assertIsInstance(hl,HalfLine2D)
        self.assertEqual(hl.P0,Point2D(0,0))
        self.assertEqual(hl.vL,Vector2D(1,1))
          
        
    def test___contains__(self):
        ""
        hl=HalfLine2D(P0,vL)
        
        # point
        self.assertTrue(P0 in hl)
        self.assertTrue(P0+vL in hl)
        self.assertTrue(P0+vL*10 in hl)
        self.assertFalse(P0+vL.opposite in hl)
        self.assertFalse(P0+vL.perp_vector in hl)
        
        # segment
        self.assertTrue(Segment2D(P0,P0+vL) in hl)
        self.assertTrue(Segment2D(P0+vL,P0+vL*2) in hl)
        self.assertFalse(Segment2D(P0+vL*-1,P0) in hl)
        self.assertFalse(Segment2D(P0+vL*-2,P0+vL*-1) in hl)
        self.assertFalse(Segment2D(P0+vL.perp_vector,P0+vL+vL.perp_vector) in hl)
        
        
    def test___eq__(self):
        ""
        hl=HalfLine2D(P0,vL)
        self.assertTrue(hl==hl)
        
        
    def test___repr__(self):
        ""
        hl=HalfLine2D(P0,vL)
        self.assertEqual(str(hl),'HalfLine2D(Point2D(0,0), Vector2D(1,1))')
        
    
    def test_calculate_point(self):
        ""
        hl=HalfLine2D(P0,vL)
        self.assertEqual(hl.calculate_point(2),
                         P0+vL*2)
        
        
    def test_calculate_t_from_point(self):
        ""
        hl=HalfLine2D(P0,vL)
        self.assertEqual(hl.calculate_t_from_point(P0+vL*2),
                         2)
    

    def test_calculate_t_from_x(self):
        ""
        hl=HalfLine2D(P0,vL)
        self.assertEqual(hl.calculate_t_from_x(2),
                         2)
        
                
    def test_calculate_t_from_y(self):
        ""
        hl=HalfLine2D(P0,vL)
        self.assertEqual(hl.calculate_t_from_y(3),
                         3)    
    

    def test_distance_point(self):
        ""
        hl=HalfLine2D(P0,vL)
        
        # point
        self.assertEqual(hl.distance_point(P0),
                         0)
        self.assertEqual(hl.distance_point(P0-vL),
                         vL.length)
        self.assertEqual(hl.distance_point(P0+vL),
                         0)
        self.assertEqual(hl.distance_point(P0+Vector2D(1,-1)),
                         Vector2D(1,-1).length)
        
        
    def test_intersect_halfline(self):
        ""
        hl=HalfLine2D(P0,vL)
        
        # same
        self.assertEqual(hl.intersect_halfline(hl),
                         hl)
        
        # codirectional
        self.assertEqual(hl.intersect_halfline(HalfLine2D(P0+vL,
                                                          vL)),
                         HalfLine2D(P0+vL,vL))
        
        self.assertEqual(hl.intersect_halfline(HalfLine2D(P0+vL*-1,
                                                          vL)),
                         hl)
        
        # parallel
        self.assertEqual(hl.intersect_halfline(HalfLine2D(P0+vL.perp_vector,
                                                          vL)),
                         None)
        
        # collinear but not codirectinal
        self.assertEqual(hl.intersect_halfline(HalfLine2D(P0,
                                                          vL*-1)),
                         hl.P0)
        
        self.assertEqual(hl.intersect_halfline(HalfLine2D(P0+vL,
                                                          vL*-1)),
                         Segment2D(P0,P0+vL))
        
        # skew
        self.assertEqual(hl.intersect_halfline(HalfLine2D(P0,
                                                          vL.perp_vector)),
                         hl.P0)
        
        self.assertEqual(hl.intersect_halfline(HalfLine2D(P0+vL,
                                                          vL.perp_vector)),
                         P0+vL)
        
        self.assertEqual(hl.intersect_halfline(HalfLine2D(P0+vL*-1,
                                                          vL.perp_vector)),
                         None)
        
        
    def test_intersect_line(self):
        ""
        hl=HalfLine2D(P0,vL)
        
        # collinear
        self.assertEqual(hl.intersect_line(Line2D(P0,
                                                  vL)),
                         hl)
        
        # parallel
        self.assertEqual(hl.intersect_line(Line2D(Point2D(0,1),
                                                  vL)),
                         None)
        
        # skew - same P0s
        self.assertEqual(hl.intersect_line(Line2D(P0,
                                                  Vector2D(0,1))),
                         P0)
        
        # skew - different P0s
        self.assertEqual(hl.intersect_line(Line2D(Point2D(0.5,0),
                                                  Vector2D(0,1))),
                         Point2D(0.5,0.5))
        

    def test_is_codirectional(self):
        ""
        hl=HalfLine2D(P0,vL)
        self.assertTrue(hl.is_codirectional(hl))
        self.assertTrue(hl.is_codirectional(HalfLine2D(P0+vL.perp_vector,vL)))
        self.assertFalse(hl.is_codirectional(HalfLine2D(P0,vL.opposite)))
        
    
    
    def test_line(self):
        hl=HalfLine2D(P0,vL)
        self.assertEqual(hl.line,
                         Line2D(P0,vL))
    
    
    
class Test_HalfLine3D(unittest.TestCase):
    """
    P0=Point3D(0,0,0)
    vL=Vector3D(1,1,1)
    """
    
    def test___init__(self):
        ""
        hl=HalfLine3D(P0,vL)
        self.assertIsInstance(hl,HalfLine3D)
        self.assertEqual(hl.P0,Point3D(0,0,0))
        self.assertEqual(hl.vL,Vector3D(1,1,1))
          
        
    def test___contains__(self):
        ""
        hl=HalfLine3D(P0,vL)
        
        # point
        self.assertTrue(P0 in hl)
        self.assertTrue(P0+vL in hl)
        self.assertTrue(P0+vL*10 in hl)
        self.assertFalse(P0+vL.opposite in hl)
        self.assertFalse(P0+Vector3D(1,-1,0) in hl)
        
        # segment
        self.assertTrue(Segment3D(P0,P0+vL) in hl)
        self.assertTrue(Segment3D(P0+vL,P0+vL*2) in hl)
        self.assertFalse(Segment3D(P0+vL*-1,P0) in hl)
        self.assertFalse(Segment3D(P0+vL*-2,P0+vL*-1) in hl)
        self.assertFalse(Segment3D(P0+Vector3D(1,-1,0),P0+vL+Vector3D(1,-1,0)) in hl)
        
        
    def test___eq__(self):
        ""
        hl=HalfLine3D(P0,vL)
        self.assertTrue(hl==hl)
        
        
    def test___repr__(self):
        ""
        hl=HalfLine3D(P0,vL)
        self.assertEqual(str(hl),'HalfLine3D(Point3D(0,0,0), Vector3D(1,1,1))')
        
    
    def test_calculate_point(self):
        ""
        hl=HalfLine3D(P0,vL)
        self.assertEqual(hl.calculate_point(2),
                         P0+vL*2)
        
        
    def test_calculate_t_from_point(self):
        ""
        hl=HalfLine3D(P0,vL)
        self.assertEqual(hl.calculate_t_from_point(P0+vL*2),
                         2)
    

    def test_calculate_t_from_x(self):
        ""
        hl=HalfLine3D(P0,vL)
        self.assertEqual(hl.calculate_t_from_x(2),
                         2)
        
                
    def test_calculate_t_from_y(self):
        ""
        hl=HalfLine3D(P0,vL)
        self.assertEqual(hl.calculate_t_from_y(3),
                         3)    
        
        
    def test_distance_point(self):
        ""
        hl=HalfLine3D(P0,vL)
        
        # point
        self.assertEqual(hl.distance_point(P0),
                         0)
        self.assertEqual(hl.distance_point(P0-vL),
                         vL.length)
        self.assertEqual(hl.distance_point(P0+vL),
                         0)
        self.assertEqual(hl.distance_point(P0+Vector3D(1,-1,0)),
                         Vector3D(1,-1,0).length)
        
        
    def test_is_codirectional(self):
        ""
        hl=HalfLine3D(P0,vL)
        self.assertTrue(hl.is_codirectional(hl))
        self.assertFalse(hl.is_codirectional(HalfLine3D(P0,vL.opposite)))
        self.assertTrue(hl.is_codirectional(HalfLine3D(P0+Vector3D(1,-1,0),vL)))
    
    
    def test_line(self):
        hl=HalfLine3D(P0,vL)
        self.assertEqual(hl.line,
                         Line3D(P0,vL))
    
    
if __name__=='__main__':
    
    P0=Point2D(0,0)
    vL=Vector2D(1,1)
    unittest.main(Test_HalfLine2D())
    
    P0=Point3D(0,0,0)
    vL=Vector3D(1,1,1)
    unittest.main(Test_HalfLine3D())
    
    
    
    