# -*- coding: utf-8 -*-

import unittest

from crossproduct import Point, Points, Vector, Line, Halfline, Segment, Segments
from crossproduct import Polyline, Polylines, Plane
from crossproduct import Polygon, SimplePolygon, ConvexSimplePolygon
from crossproduct import Polyhedron

class Test_Point(unittest.TestCase):
    ""
    
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
        
        
    def test__distance_to_point(self):
        ""
        pt1=Point(0,0)
        pt2=Point(1,0)
        self.assertEqual(pt1._distance_to_point(pt2),
                         1)
   
        pt1=Point(0,0,0)
        pt2=Point(1,0,0)
        self.assertEqual(pt1._distance_to_point(pt2),
                         1)
        
        
    def test_distance(self):
        ""
        pt1=Point(0,0)
        pt2=Point(1,0)
        self.assertEqual(pt1.distance(pt2),
                         1)
   
        pt1=Point(0,0,0)
        pt2=Point(1,0,0)
        self.assertEqual(pt1.distance(pt2),
                         1)
        
        
    def test_nD(self):
        ""
        pt=Point(0,0)
        self.assertEqual(pt.nD,
                         2)
        pt=Point(0,0,0)
        self.assertEqual(pt.nD,
                         3)
        
    
    def test_project_2D(self):
        ""
        pt=Point(1,2,3)
        self.assertEqual(pt.project_2D(0),
                         Point(2,3))
    
    def test_project_3D(self):
        ""
        pl=Plane(Point(0,0,1),Vector(0,0,1))
        pt=Point(2,2)
        self.assertEqual(pt.project_3D(pl,2),
                         Point(2,2,1.0))



class Test_Points(unittest.TestCase):
    
    def test___init__(self):
        ""
        # creation
        pt=Point(0,0)
        pts=Points(pt)
        self.assertIsInstance(pts,
                              Points)
        self.assertEqual(pts[0],
                         pt)
        self.assertEqual(len(pts),
                         1)
        
        # append
        pt1=Point(1,1)
        pts.append(pt1)
        self.assertEqual(pts[1],
                         pt1)
        self.assertEqual(len(pts),
                         2)
        
        # insert
        pt2=Point(2,2)
        pts.insert(0,pt2)
        self.assertEqual(pts[0],
                         pt2)
        self.assertEqual(len(pts),
                         3)
        
        # del
        del pts[0]
        self.assertEqual(pts[0],
                         pt)
        
        
    def test_remove_points_in_segments(self):
        ""
        pts = Points(Point(0,0), Point(1,0))
        segments = Segments(Segment(Point(0,0), Point(0,1)))
        pts.remove_points_in_segments(segments)
        self.assertEqual(pts,
                         Points(Point(1.0,0.0)))
            
        

class Test_Vector(unittest.TestCase):
    
    def test___add__(self):
        ""
        v1=Vector(1,0)
        v2=Vector(2,0)
        self.assertEqual(v1+v2,
                         Vector(3,0))
    
        v1=Vector(1,0,0)
        v2=Vector(2,0,0)
        self.assertEqual(v1+v2,
                         Vector(3,0,0))
    
    
    def test___eq__(self):
        ""
        v=Vector(0,0)
        self.assertTrue(v==v)
        
        v1=Vector(1,0)
        self.assertFalse(v==v1)
    
        v2=Vector(0,1,2)
        self.assertRaises(ValueError,
                          v.__eq__,v2)
    
        v3=(0,0.0000000000001)
        self.assertTrue(v==v3)    
    
    
    def test___init__(self):
        ""
        v=Vector(1,0)
        self.assertIsInstance(v,
                              Vector)
        self.assertEqual(v[0],
                         1)
        self.assertEqual(v[1],
                         0)
        
        v=Vector(1,0,0)
        self.assertIsInstance(v,Vector)
        self.assertEqual(list(v),
                         [1.0,0.0,0.0])
        
        
    def test___mul__(self):
        ""
        v=Vector(1,0)
        self.assertEqual(v*2,
                         Vector(2,0))
        
        v=Vector(1,0,0)
        self.assertEqual(v*2,
                         Vector(2,0,0))
        
    
    def test___sub__(self):
        ""
        v1=Vector(1,0)
        v2=Vector(2,0)
        self.assertEqual(v1-v2,
                         Vector(-1,0))
        
        v1=Vector(1,0,0)
        v2=Vector(2,0,0)
        self.assertEqual(v1-v2,
                         Vector(-1,0,0))
        

    def test_angle(self):
        ""
        v1=Vector(1,0)
        self.assertEqual(v1.angle(v1),
                         0)
        self.assertEqual(v1.angle(Vector(0,1)),
                         90)
        self.assertAlmostEqual(v1.angle(Vector(1,1)), 
                               45)
        self.assertAlmostEqual(v1.angle(Vector(-1,0)), 
                               180)
        
        v1=Vector(1,0,0)
        self.assertEqual(v1.angle(v1),
                         0)
        self.assertEqual(v1.angle(Vector(0,1,0)),
                         90)
        self.assertAlmostEqual(v1.angle(Vector(1,1,0)), 
                               45)
        self.assertAlmostEqual(v1.angle(Vector(-1,0,0)), 
                               180)
        
    
    
    
    def test_cross_product(self):
        ""
        v1=Vector(1,0,0)
        v2=Vector(0,1,0)
        self.assertEqual(v1.cross_product(v1),
                         Vector(0,0,0))
        self.assertEqual(v1.cross_product(v1.opposite),
                         Vector(0,0,0))
        self.assertEqual(v1.cross_product(v2),
                         Vector(0,0,1))    
    

    def test_dot(self):
        ""
        v=Vector(1,0)
        self.assertEqual(v.dot(v),
                         1)
        self.assertEqual(v.dot(v.perp_vector),
                         0)
        self.assertEqual(v.dot(v.opposite),
                         -1)
    
        v=Vector(1,0,0)
        self.assertEqual(v.dot(v),
                         1)
        self.assertEqual(v.dot(Vector(0,1,0)),
                         0)
        self.assertEqual(v.dot(v.opposite),
                         -1)
        
    

    def test_index_largest_absolute_coordinate(self):
        ""
        v=Vector(1,2)
        self.assertTrue(v.index_largest_absolute_coordinate,
                        1)


    def test_is_codirectional(self):
        ""
        v=Vector(1,0)
        self.assertTrue(v.is_codirectional(v))
        self.assertFalse(v.is_codirectional(v.perp_vector))
        self.assertFalse(v.is_codirectional(v.opposite))

        v=Vector(1,0,0)
        self.assertTrue(v.is_collinear(v))
        self.assertFalse(v.is_collinear(Vector(0,1,0)))
        self.assertTrue(v.is_collinear(v.opposite))
    
    
    def test_is_collinear(self):
        ""
        v=Vector(1,0)
        self.assertTrue(v.is_collinear(v))
        self.assertFalse(v.is_collinear(v.perp_vector))
        self.assertTrue(v.is_collinear(v.opposite))
    
        v=Vector(1,0,0)
        self.assertTrue(v.is_collinear(v))
        self.assertFalse(v.is_collinear(Vector(0,1,0)))
        self.assertTrue(v.is_collinear(v.opposite))
       
        
    def test_is_opposite(self):
        ""
        v=Vector(1,0)
        self.assertFalse(v.is_opposite(v))
        self.assertFalse(v.is_opposite(v.perp_vector))
        self.assertTrue(v.is_opposite(v.opposite))
        
        v=Vector(1,0,0)
        self.assertFalse(v.is_opposite(v))
        self.assertFalse(v.is_opposite(Vector(0,1,0)))
        self.assertTrue(v.is_opposite(v.opposite))
        
            
    def test_is_perpendicular(self):
        ""
        v=Vector(1,0)
        self.assertFalse(v.is_perpendicular(v))
        self.assertTrue(v.is_perpendicular(v.perp_vector))
    
        v=Vector(1,0,0)
        self.assertFalse(v.is_perpendicular(v))
        self.assertTrue(v.is_perpendicular(Vector(0,1,0)))
        
        
    def test_length(self):
        ""
        v=Vector(1,0)
        self.assertEqual(v.length,
                         1)
        
        v=Vector(1,0,0)
        self.assertEqual(v.length,
                         1)
        
        
    def test_normalise(self):
        ""
        v=Vector(2,0)
        self.assertEqual(v.normalise,
                         Vector(1,0))
        
        v=Vector(2,0,0)
        self.assertEqual(v.normalise,
                         Vector(1,0,0))
        
        
    def test_opposite(self):
        ""
        v=Vector(1,0)
        self.assertEqual(v.opposite,
                         Vector(-1,0))
        
        v=Vector(1,0,0)
        self.assertEqual(v.opposite,
                         Vector(-1,0,0))
        

    def test_perp_product(self):
        ""
        v=Vector(1,0)
        self.assertEqual(v.perp_product(v),
                         0)
        self.assertEqual(v.perp_product(v.perp_vector),
                         1)
        self.assertEqual(v.perp_product(v.opposite),
                         0)
        self.assertEqual(v.perp_product(v.perp_vector.opposite),
                         -1)


    def test_perp_vector(self):
        ""
        v=Vector(1,0)
        self.assertEqual(v.perp_vector,
                         Vector(0,1))
        
        
    def test_triple_product(self):
        ""
        v1=Vector(1,0,0)
        v2=Vector(0,1,0)
        v3=Vector(0,0,1)
        self.assertEqual(v1.triple_product(v2,v3),
                         1)
    
    
    
if __name__=='__main__':
    
    unittest.main()