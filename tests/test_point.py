# -*- coding: utf-8 -*-

import unittest
from crossproduct import Point2D, Point3D, Vector2D, Vector3D


class Test_Point2D(unittest.TestCase):
    
    def test___init__(self):
        ""
        pt=Point2D(0,0)
        self.assertIsInstance(pt,Point2D)
        self.assertEqual(pt.x,0)
        self.assertEqual(pt.y,0)
    
    
    def test___add__(self):
        ""
        pt=Point2D(0,0)
        v=Vector2D(1,0)
        self.assertEqual(pt+v,
                         Point2D(1,0))
    
    
    def test___eq__(self):
        ""
        pt=Point2D(0,0)
        self.assertTrue(pt==pt)
        
        pt1=Point2D(1,0)
        self.assertFalse(pt==pt1)
        
        
    def test___lt__(self):
        ""
        pt=Point2D(0,0)
        self.assertFalse(pt<Point2D(0,0))
        self.assertTrue(pt<Point2D(1,0))
        self.assertFalse(pt<Point2D(-1,0))
        self.assertTrue(pt<Point2D(0,1))
        self.assertFalse(pt<Point2D(0,-1))
        
        
    def test___repr__(self):
        ""
        pt=Point2D(0,0)
        self.assertEqual(str(pt),
                         'Point2D(0,0)')
        
        
    def test___sub__(self):
        ""
        pt1=Point2D(0,0)
        pt2=Point2D(1,0)
        self.assertEqual(pt2-pt1,
                         Vector2D(1,0))
        
        v=Vector2D(1,0)
        self.assertEqual(pt2-v,
                         pt1)
        
    def test_coordinates(self):
        ""
        pt=Point2D(0,0)
        self.assertEqual(pt.coordinates,
                         (0,0))
        
        
    def test_distance_point(self):
        ""
        pt1=Point2D(0,0)
        pt2=Point2D(1,0)
        self.assertEqual(pt1.distance_point(pt2),
                         1)
   

class Test_Point3D(unittest.TestCase):
    
    def test___init__(self):
        ""
        pt=Point3D(0,0,0)
        self.assertIsInstance(pt,Point3D)
        self.assertEqual(pt.x,0)
        self.assertEqual(pt.y,0)
        self.assertEqual(pt.z,0)
    
    
    def test___add__(self):
        ""
        pt=Point3D(0,0,0)
        v=Vector3D(1,0,0)
        self.assertEqual(pt+v,
                         Point3D(1,0,0))
    
    
    def test___eq__(self):
        ""
        pt=Point3D(0,0,0)
        self.assertTrue(pt==pt)
        
        pt1=Point3D(1,0,0)
        self.assertFalse(pt==pt1)
        
        
    def test___lt__(self):
        ""
        pt=Point3D(0,0,0)
        self.assertFalse(pt<Point3D(0,0,0))
        self.assertTrue(pt<Point3D(1,0,0))
        self.assertFalse(pt<Point3D(-1,0,0))
        self.assertTrue(pt<Point3D(0,1,0))
        self.assertFalse(pt<Point3D(0,-1,0))
        self.assertTrue(pt<Point3D(0,0,1))
        self.assertFalse(pt<Point3D(0,0,-1))
        
        
    def test___repr__(self):
        ""
        pt=Point3D(0,0,0)
        self.assertEqual(str(pt),
                         'Point3D(0,0,0)')
        
        
    def test___sub__(self):
        ""
        pt1=Point3D(0,0,0)
        pt2=Point3D(1,0,0)
        self.assertEqual(pt2-pt1,
                         Vector3D(1,0,0))
        
        v=Vector3D(1,0,0)
        self.assertEqual(pt2-v,
                         pt1)
        
        
    def test_coordinates(self):
        ""
        pt=Point3D(0,0,0)
        self.assertEqual(pt.coordinates,
                         (0,0,0))
        
        
    def test_distance_point(self):
        ""
        pt1=Point3D(0,0,0)
        pt2=Point3D(1,0,0)
        self.assertEqual(pt1.distance_point(pt2),
                         1)
        
        
    def test_project_2D(self):
        ""
        pt=Point3D(1,2,3)
        self.assertEqual(pt.project_2D(0),
                         Point2D(2,3))
        
    
if __name__=='__main__':
    
    unittest.main(Test_Point2D())
    unittest.main(Test_Point3D())
    
    