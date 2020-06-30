# -*- coding: utf-8 -*-

import unittest
from crossproduct import Point2D, Point3D, Vector2D, Vector3D, \
    Parallelogram2D, Parallelogram3D

class Test_Parallelogram2D(unittest.TestCase):
    """
    P0=Point2D(0,0)
    v=Vector2D(1,0)
    w=Vector2D(0.5,1)
    """       
    
    def test___init__(self):
        ""
        pl=Parallelogram2D(P0,v,w)
        self.assertIsInstance(pl,Parallelogram2D)
        self.assertEqual(pl.P0,P0)
        self.assertEqual(pl.v,v)
        self.assertEqual(pl.w,w)
        
        
    def test___repr__(self):
        ""
        pl=Parallelogram2D(P0,v,w)
        self.assertEqual(str(pl),
                         'Parallelogram2D(Point2D(0,0), Vector2D(1,0), Vector2D(0.5,1))')
        
        
    def test_P1(self):
        ""
        pl=Parallelogram2D(P0,v,w)
        self.assertEqual(pl.P1,P0+v)
        
        
    def test_P2(self):
        ""
        pl=Parallelogram2D(P0,v,w)
        self.assertEqual(pl.P2,P0+v+w)
        
        
    def test_P3(self):
        ""
        pl=Parallelogram2D(P0,v,w)
        self.assertEqual(pl.P3,P0+w)
        
        
    def test_signed_area(self):
        ""
        pl=Parallelogram2D(P0,v,w) #ccw
        self.assertEqual(pl.signed_area,1)
        
        pl=Parallelogram2D(P0,w,v) #cw
        self.assertEqual(pl.signed_area,-1)
    
    
    
class Test_Parallelogram3D(unittest.TestCase):
    """
    P0=Point3D(0,0,0)
    v=Vector3D(1,0,0)
    w=Vector3D(0.5,1,0)
    """
    
    def test___init__(self):
        ""
        pl=Parallelogram3D(P0,v,w)
        self.assertIsInstance(pl,Parallelogram3D)
        self.assertEqual(pl.P0,P0)
        self.assertEqual(pl.v,v)
        self.assertEqual(pl.w,w)
    
    
    def test___repr__(self):
        ""
        pl=Parallelogram3D(P0,v,w)
        self.assertEqual(str(pl),
                         'Parallelogram3D(Point3D(0,0,0), Vector3D(1,0,0), Vector3D(0.5,1,0))')
        
        
    def test_area(self):
        ""
        pl=Parallelogram3D(P0,v,w) #ccw
        self.assertEqual(pl.area,1)
        
        pl=Parallelogram3D(P0,w,v) #cw
        self.assertEqual(pl.area,1)
        
        
    def test_P1(self):
        ""
        pl=Parallelogram3D(P0,v,w)
        self.assertEqual(pl.P1,P0+v)
        
        
    def test_P2(self):
        ""
        pl=Parallelogram3D(P0,v,w)
        self.assertEqual(pl.P2,P0+v+w)
        
        
    def test_P3(self):
        ""
        pl=Parallelogram3D(P0,v,w)
        self.assertEqual(pl.P3,P0+w)
    
    
if __name__=='__main__':
    
    P0=Point2D(0,0)
    v=Vector2D(1,0)
    w=Vector2D(0.5,1)
    unittest.main(Test_Parallelogram2D())
    
    P0=Point3D(0,0,0)
    v=Vector3D(1,0,0)
    w=Vector3D(0.5,1,0)
    unittest.main(Test_Parallelogram3D())
    
    