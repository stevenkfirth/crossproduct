# -*- coding: utf-8 -*-

import unittest
from crossproduct import Point, Vector


class Test_Point(unittest.TestCase):
    
    
    def test___add__(self):
        ""
        pt=Point(0,0)
        v=Vector(1,0)
        self.assertEqual(pt+v,
                         Point(1,0))
 
        pt=Point(0,0,0)
        v=Vector(1,0,0)
        self.assertEqual(pt+v,
                         Point(1,0,0))
    
    
    def test___eq__(self):
        ""
        pt=Point(0,0)
        self.assertTrue(pt==pt)
        
        pt1=Point(1,0)
        self.assertFalse(pt==pt1)
    
        pt2=Point(0,1,2)
        self.assertRaises(ValueError,
                          pt.__eq__,pt2)
    
        pt3=(0,0.0000000000001)
        self.assertTrue(pt==pt3)    
        
    
    def test___init__(self):
        ""
        pt=Point(0,1)
        self.assertIsInstance(pt,Point)
        self.assertEqual(list(pt),
                         [0,1])
        self.assertEqual(pt[1],
                         1)
        
        pt=Point(0,1,2)
        self.assertEqual(list(pt),
                         [0,1,2])
        
        
    def test___lt__(self):
        ""
        
        pt=Point(0,0)
        self.assertFalse(pt<Point(0,0))
        self.assertTrue(pt<Point(1,0))
        self.assertFalse(pt<Point(-1,0))
        self.assertTrue(pt<Point(0,1))
        self.assertFalse(pt<Point(0,-1))
        self.assertFalse(pt<Point(-1,1))
        
        pt=Point(0,0,0)
        self.assertFalse(pt<Point(0,0,0))
        self.assertTrue(pt<Point(1,0,0))
        self.assertFalse(pt<Point(-1,0,0))
        self.assertTrue(pt<Point(0,1,0))
        self.assertFalse(pt<Point(0,-1,0))
        self.assertTrue(pt<Point(0,0,1))
        self.assertFalse(pt<Point(0,0,-1))
        
        pt=Point(0,0)
        
        
    def test___repr__(self):
        ""
        pt=Point(0,0)
        self.assertEqual(str(pt),
                         'Point(0.0,0.0)')
    
    
    def test___sub__(self):
        ""
        pt1=Point(0,0)
        pt2=Point(1,0)
        self.assertEqual(pt2-pt1,
                         Vector(1,0))
        
        v=Vector(1,0)
        self.assertEqual(pt2-v,
                         pt1)
        
        pt1=Point(0,0,0)
        pt2=Point(1,0,0)
        self.assertEqual(pt2-pt1,
                         Vector(1,0,0))
        
        v=Vector(1,0,0)
        self.assertEqual(pt2-v,
                         pt1)
        
        
    def test_distance_to_point(self):
        ""
        pt1=Point(0,0)
        pt2=Point(1,0)
        self.assertEqual(pt1.distance_to_point(pt2),
                         1)
   
        pt1=Point(0,0,0)
        pt2=Point(1,0,0)
        self.assertEqual(pt1.distance_to_point(pt2),
                         1)
        
    
    def test_project_2D(self):
        ""
        pt=Point(1,2,3)
        self.assertEqual(pt.project_2D(0),
                         Point(2,3))
    
    # TO DO WHEN PLANE IS AVAILABLE
    # def test_project_3D(self):
    #     ""
    #     pl=Plane3D(Point3D(0,0,1),Vector3D(0,0,1))
    #     pt=Point2D(2,2)
    #     self.assertEqual(pt.project_3D(pl,2),
    #                       Point3D(2,2,1.0))
    


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
        
        
    def test_distance_to_point(self):
        ""
        pt1=Point3D(0,0,0)
        pt2=Point3D(1,0,0)
        self.assertEqual(pt1.distance_to_point(pt2),
                         1)
        
        
    def test_project_2D(self):
        ""
        pt=Point3D(1,2,3)
        self.assertEqual(pt.project_2D(0),
                         Point2D(2,3))
        
    
if __name__=='__main__':
    
    unittest.main(Test_Point())
    #unittest.main(Test_Point3D())
    
    