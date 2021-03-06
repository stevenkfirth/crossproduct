# -*- coding: utf-8 -*-

import unittest
from crossproduct import Point, Vector, Line, Halfline, Segment
import matplotlib.pyplot as plt


class Test_Halfline(unittest.TestCase):
    
    def test___eq__(self):
        ""
        P0,vL=Point(0,0),Vector(1,1) 
        hl=Halfline(P0,vL)
        self.assertTrue(hl==hl)
    
        P0,vL=Point(0,0,0),Vector(1,1,1)
        hl=Halfline(P0,vL)
        self.assertTrue(hl==hl)
        
        
    def test___init__(self):
        ""
        P0,vL=Point(0,0),Vector(1,1) 
        hl=Halfline(P0,vL)
        self.assertIsInstance(hl,Halfline)
        self.assertEqual(hl.P0,Point(0,0))
        self.assertEqual(hl.vL,Vector(1,1))
        
        P0,vL=Point(0,0,0),Vector(1,1,1)
        hl=Halfline(P0,vL)
        self.assertIsInstance(hl,Halfline)
        self.assertEqual(hl.P0,Point(0,0,0))
        self.assertEqual(hl.vL,Vector(1,1,1))
        
    
    def test_calculate_point(self):
        ""
        P0,vL=Point(0,0),Vector(1,1) 
        hl=Halfline(P0,vL)
        self.assertEqual(hl.calculate_point(2),
                         P0+vL*2)

        P0,vL=Point(0,0,0),Vector(1,1,1)
        hl=Halfline(P0,vL)
        self.assertEqual(hl.calculate_point(2),
                         P0+vL*2)


    def test_contains(self):
        ""
        P0,vL=Point(0,0),Vector(1,1) 
        hl=Halfline(P0,vL)
        # point
        self.assertTrue(hl.contains(P0))
        self.assertTrue(hl.contains(P0+vL))
        self.assertTrue(hl.contains(P0+vL*10))
        self.assertFalse(hl.contains(P0+vL.opposite))
        self.assertFalse(hl.contains(P0+vL.perp_vector))
        # segment
        self.assertTrue(hl.contains(Segment(P0,P0+vL)))
        self.assertTrue(hl.contains(Segment(P0+vL,P0+vL*2)))
        self.assertFalse(hl.contains(Segment(P0+vL*-1,P0)))
        self.assertFalse(hl.contains(Segment(P0+vL*-2,P0+vL*-1)))
        self.assertFalse(hl.contains(Segment(P0+vL.perp_vector,P0+vL+vL.perp_vector)))

        P0,vL=Point(0,0,0),Vector(1,1,1)
        hl=Halfline(P0,vL)
        # point
        self.assertTrue(hl.contains(P0))
        self.assertTrue(hl.contains(P0+vL))
        self.assertTrue(hl.contains(P0+vL*10))
        self.assertFalse(hl.contains(P0+vL.opposite))
        self.assertFalse(hl.contains(P0+Vector(1,-1,0)))
        # segment
        self.assertTrue(hl.contains(Segment(P0,P0+vL)))
        self.assertTrue(hl.contains(Segment(P0+vL,P0+vL*2)))
        self.assertFalse(hl.contains(Segment(P0+vL*-1,P0)))
        self.assertFalse(hl.contains(Segment(P0+vL*-2,P0+vL*-1)))
        self.assertFalse(hl.contains(Segment(P0+Vector(1,-1,0),P0+vL+Vector(1,-1,0))))
        
        
    def test_distance_to_point(self):
        ""
        P0,vL=Point(0,0),Vector(1,1) 
        hl=Halfline(P0,vL)
        self.assertEqual(hl.distance_to_point(P0),
                         0)
        self.assertEqual(hl.distance_to_point(P0-vL),
                         vL.length)
        self.assertEqual(hl.distance_to_point(P0+vL),
                         0)
        self.assertEqual(hl.distance_to_point(P0+Vector(1,-1)),
                         Vector(1,-1).length)


        P0,vL=Point(0,0,0),Vector(1,1,1)
        hl=Halfline(P0,vL)
        self.assertEqual(hl.distance_to_point(P0),
                         0)
        self.assertEqual(hl.distance_to_point(P0-vL),
                         vL.length)
        self.assertEqual(hl.distance_to_point(P0+vL),
                         0)
        self.assertEqual(hl.distance_to_point(P0+Vector(1,-1,0)),
                         Vector(1,-1,0).length)


    def test_intersect_halfline(self):
        ""
        P0,vL=Point(0,0),Vector(1,1) 
        hl=Halfline(P0,vL)
        # same
        self.assertEqual(hl.intersect_halfline(hl),
                         hl)
        # codirectional
        self.assertEqual(hl.intersect_halfline(Halfline(P0+vL,vL)),
                         Halfline(P0+vL,vL))
        self.assertEqual(hl.intersect_halfline(Halfline(P0+vL*-1,vL)),
                         hl)
        # parallel
        self.assertEqual(hl.intersect_halfline(Halfline(P0+vL.perp_vector,vL)),
                         None)
        # collinear but not codirectinal
        self.assertEqual(hl.intersect_halfline(Halfline(P0,vL*-1)),
                         hl.P0)
        self.assertEqual(hl.intersect_halfline(Halfline(P0+vL,vL*-1)),
                         Segment(P0,P0+vL))
        # skew
        self.assertEqual(hl.intersect_halfline(Halfline(P0,vL.perp_vector)),
                         hl.P0)
        self.assertEqual(hl.intersect_halfline(Halfline(P0+vL,vL.perp_vector)),
                         P0+vL)
        self.assertEqual(hl.intersect_halfline(Halfline(P0+vL*-1,vL.perp_vector)),
                         None)


    def test_intersect_line(self):
        ""
        P0,vL=Point(0,0),Vector(1,1) 
        hl=Halfline(P0,vL)
        # collinear
        self.assertEqual(hl.intersect_line(Line(P0,vL)),
                         hl)
        # parallel
        self.assertEqual(hl.intersect_line(Line(Point(0,1),vL)),
                         None)
        # skew - same P0s
        self.assertEqual(hl.intersect_line(Line(P0,Vector(0,1))),
                         P0)
        # skew - different P0s
        self.assertEqual(hl.intersect_line(Line(Point(0.5,0),Vector(0,1))),
                         Point(0.5,0.5))


    def test_line(self):
        P0,vL=Point(0,0),Vector(1,1) 
        hl=Halfline(P0,vL)
        self.assertEqual(hl.line,
                         Line(P0,vL))
    
        P0,vL=Point(0,0,0),Vector(1,1,1)
        hl=Halfline(P0,vL)
        self.assertEqual(hl.line,
                         Line(P0,vL))
    
    def test_plot(self):
        ""
        P0,vL=Point(0,0),Vector(-1,1) 
        hl=Halfline(P0,vL)
        fig, ax = plt.subplots()
        hl.plot(ax)
   


class Test_Halfline2D(unittest.TestCase):
    """
    P0=Point2D(0,0)
    vL=Vector2D(1,1)
    """
    
    def test___init__(self):
        ""
        hl=Halfline2D(P0,vL)
        self.assertIsInstance(hl,Halfline2D)
        self.assertEqual(hl.P0,Point2D(0,0))
        self.assertEqual(hl.vL,Vector2D(1,1))
          
        
    def test___contains__(self):
        ""
        hl=Halfline2D(P0,vL)
        
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
        hl=Halfline2D(P0,vL)
        self.assertTrue(hl==hl)
        
        
    def test___repr__(self):
        ""
        hl=Halfline2D(P0,vL)
        self.assertEqual(str(hl),'Halfline2D(Point2D(0,0), Vector2D(1,1))')
        
    
    def test_calculate_point(self):
        ""
        hl=Halfline2D(P0,vL)
        self.assertEqual(hl.calculate_point(2),
                         P0+vL*2)
        
 
    def test_distance_to_point(self):
        ""
        hl=Halfline2D(P0,vL)
        
        # point
        self.assertEqual(hl.distance_to_point(P0),
                         0)
        self.assertEqual(hl.distance_to_point(P0-vL),
                         vL.length)
        self.assertEqual(hl.distance_to_point(P0+vL),
                         0)
        self.assertEqual(hl.distance_to_point(P0+Vector2D(1,-1)),
                         Vector2D(1,-1).length)
        
        
    def test_intersect_halfline(self):
        ""
        hl=Halfline2D(P0,vL)
        
        # same
        self.assertEqual(hl.intersect_halfline(hl),
                         hl)
        
        # codirectional
        self.assertEqual(hl.intersect_halfline(Halfline2D(P0+vL,
                                                          vL)),
                         Halfline2D(P0+vL,vL))
        
        self.assertEqual(hl.intersect_halfline(Halfline2D(P0+vL*-1,
                                                          vL)),
                         hl)
        
        # parallel
        self.assertEqual(hl.intersect_halfline(Halfline2D(P0+vL.perp_vector,
                                                          vL)),
                         None)
        
        # collinear but not codirectinal
        self.assertEqual(hl.intersect_halfline(Halfline2D(P0,
                                                          vL*-1)),
                         hl.P0)
        
        self.assertEqual(hl.intersect_halfline(Halfline2D(P0+vL,
                                                          vL*-1)),
                         Segment2D(P0,P0+vL))
        
        # skew
        self.assertEqual(hl.intersect_halfline(Halfline2D(P0,
                                                          vL.perp_vector)),
                         hl.P0)
        
        self.assertEqual(hl.intersect_halfline(Halfline2D(P0+vL,
                                                          vL.perp_vector)),
                         P0+vL)
        
        self.assertEqual(hl.intersect_halfline(Halfline2D(P0+vL*-1,
                                                          vL.perp_vector)),
                         None)
        
        
    def test_intersect_line(self):
        ""
        hl=Halfline2D(P0,vL)
        
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
    
    
    def test_line(self):
        hl=Halfline2D(P0,vL)
        self.assertEqual(hl.line,
                         Line2D(P0,vL))
    
    
    
class Test_Halfline3D(unittest.TestCase):
    """
    P0=Point3D(0,0,0)
    vL=Vector3D(1,1,1)
    """
    
    def test___init__(self):
        ""
        hl=Halfline3D(P0,vL)
        self.assertIsInstance(hl,Halfline3D)
        self.assertEqual(hl.P0,Point3D(0,0,0))
        self.assertEqual(hl.vL,Vector3D(1,1,1))
          
        
    def test___contains__(self):
        ""
        hl=Halfline3D(P0,vL)
        
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
        hl=Halfline3D(P0,vL)
        self.assertTrue(hl==hl)
        
        
    def test___repr__(self):
        ""
        hl=Halfline3D(P0,vL)
        self.assertEqual(str(hl),'Halfline3D(Point3D(0,0,0), Vector3D(1,1,1))')
        
    
    def test_calculate_point(self):
        ""
        hl=Halfline3D(P0,vL)
        self.assertEqual(hl.calculate_point(2),
                         P0+vL*2)
        
        
    def test_distance_to_point(self):
        ""
        hl=Halfline3D(P0,vL)
        
        # point
        self.assertEqual(hl.distance_to_point(P0),
                         0)
        self.assertEqual(hl.distance_to_point(P0-vL),
                         vL.length)
        self.assertEqual(hl.distance_to_point(P0+vL),
                         0)
        self.assertEqual(hl.distance_to_point(P0+Vector3D(1,-1,0)),
                         Vector3D(1,-1,0).length)
    
    
    def test_line(self):
        hl=Halfline3D(P0,vL)
        self.assertEqual(hl.line,
                         Line3D(P0,vL))
    
    
if __name__=='__main__':
    
    
    unittest.main(Test_Halfline())
    
    # P0=Point2D(0,0)
    # vL=Vector2D(1,1)
    # unittest.main(Test_Halfline2D())
    
    # P0=Point3D(0,0,0)
    # vL=Vector3D(1,1,1)
    # unittest.main(Test_Halfline3D())
    
    
    
    