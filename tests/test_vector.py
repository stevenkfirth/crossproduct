# -*- coding: utf-8 -*-

import unittest
import math
from crossproduct import Vector


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
    
    








class Test_Vector2D(unittest.TestCase):
    
    def test___init__(self):
        ""
        v=Vector2D(1,0)
        self.assertIsInstance(v,Vector2D)
        self.assertEqual(v.x,1)
        self.assertEqual(v.y,0)
        
        
    def test___add__(self):
        ""
        v1=Vector2D(1,0)
        v2=Vector2D(2,0)
        self.assertEqual(v1+v2,
                         Vector2D(3,0))
    
    
    def test___eq__(self):
        ""
        v=Vector2D(1,0)
        self.assertTrue(v==v)
        
        v2=Vector2D(2,0)
        self.assertFalse(v==v2)
        
        
    def test___repr__(self):
        ""
        v=Vector2D(1,0)
        self.assertEqual(str(v),
                         'Vector2D(1,0)')
        
        
    def test___mul__(self):
        ""
        v=Vector2D(1,0)
        self.assertEqual(v*2,
                         Vector2D(2,0))
        
        
    def test___sub__(self):
        ""
        v1=Vector2D(1,0)
        v2=Vector2D(2,0)
        self.assertEqual(v1-v2,
                         Vector2D(-1,0))
        
        
    def test_coordinates(self):
        ""
        v=Vector2D(1,0)
        self.assertEqual(v.coordinates,
                         (1,0))
        
        
    def test_dot(self):
        ""
        v=Vector2D(1,0)
        self.assertEqual(v.dot(v),
                         1)
        self.assertEqual(v.dot(v.perp_vector),
                         0)
        self.assertEqual(v.dot(v.opposite),
                         -1)
        
        
    def test_is_codirectional(self):
        ""
        v=Vector2D(1,0)
        self.assertTrue(v.is_codirectional(v))
        self.assertFalse(v.is_codirectional(v.perp_vector))
        self.assertFalse(v.is_codirectional(v.opposite))
        
        
    def test_is_collinear(self):
        ""
        v=Vector2D(1,0)
        self.assertTrue(v.is_collinear(v))
        self.assertFalse(v.is_collinear(v.perp_vector))
        self.assertTrue(v.is_collinear(v.opposite))
        
        
        
    def test_is_opposite(self):
        ""
        v=Vector2D(1,0)
        self.assertFalse(v.is_opposite(v))
        self.assertFalse(v.is_opposite(v.perp_vector))
        self.assertTrue(v.is_opposite(v.opposite))
        
        
    def test_is_perpendicular(self):
        ""
        v=Vector2D(1,0)
        self.assertFalse(v.is_perpendicular(v))
        self.assertTrue(v.is_perpendicular(v.perp_vector))
        
        
    def test_length(self):
        ""
        v=Vector2D(1,0)
        self.assertEqual(v.length,
                         1)
        
        
    def test_normalise(self):
        ""
        v=Vector2D(2,0)
        self.assertEqual(v.normalise,
                         Vector2D(1,0))
        
        
    def test_opposite(self):
        ""
        v=Vector2D(1,0)
        self.assertEqual(v.opposite,
                         Vector2D(-1,0))
        
        
    def test_perp_product(self):
        ""
        v=Vector2D(1,0)
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
        v=Vector2D(1,0)
        self.assertEqual(v.perp_vector,
                         Vector2D(0,1))
        
        
        
class Test_Vector3D(unittest.TestCase):
    
    def test___init__(self):
        ""
        v=Vector3D(1,0,0)
        self.assertIsInstance(v,Vector3D)
        self.assertEqual(v.x,1)
        self.assertEqual(v.y,0)
        self.assertEqual(v.z,0)
        
        
    def test___add__(self):
        ""
        v1=Vector3D(1,0,0)
        v2=Vector3D(2,0,0)
        self.assertEqual(v1+v2,
                         Vector3D(3,0,0))
    
    
    def test___eq__(self):
        ""
        v=Vector3D(1,0,0)
        self.assertTrue(v==v)
        
        v2=Vector3D(2,0,0)
        self.assertFalse(v==v2)
        
        
    def test___repr__(self):
        ""
        v=Vector3D(1,0,0)
        self.assertEqual(str(v),
                         'Vector3D(1,0,0)')
        
        
    def test___mul__(self):
        ""
        v=Vector3D(1,0,0)
        self.assertEqual(v*2,
                         Vector3D(2,0,0))
        
        
    def test___sub__(self):
        ""
        v1=Vector3D(1,0,0)
        v2=Vector3D(2,0,0)
        self.assertEqual(v1-v2,
                         Vector3D(-1,0,0))
        
        
    def test_cross_product(self):
        ""
        v1=Vector3D(1,0,0)
        v2=Vector3D(0,1,0)
        self.assertEqual(v1.cross_product(v1),
                         Vector3D(0,0,0))
        self.assertEqual(v1.cross_product(v1.opposite),
                         Vector3D(0,0,0))
        self.assertEqual(v1.cross_product(v2),
                         Vector3D(0,0,1))
        
        
    def test_coordinates(self):
        ""
        v=Vector3D(1,0,0)
        self.assertEqual(v.coordinates,
                         (1,0,0))
        
        
    def test_dot(self):
        ""
        v=Vector3D(1,0,0)
        self.assertEqual(v.dot(v),
                         1)
        self.assertEqual(v.dot(Vector3D(0,1,0)),
                         0)
        self.assertEqual(v.dot(v.opposite),
                         -1)
        
        
    def test_is_codirectional(self):
        ""
        v=Vector3D(1,0,0)
        self.assertTrue(v.is_codirectional(v))
        self.assertFalse(v.is_codirectional(Vector3D(0,1,0)))
        self.assertFalse(v.is_codirectional(v.opposite))
        
        
    def test_is_collinear(self):
        ""
        v=Vector3D(1,0,0)
        self.assertTrue(v.is_collinear(v))
        self.assertFalse(v.is_collinear(Vector3D(0,1,0)))
        self.assertTrue(v.is_collinear(v.opposite))
        
        
    def test_is_opposite(self):
        ""
        v=Vector3D(1,0,0)
        self.assertFalse(v.is_opposite(v))
        self.assertFalse(v.is_opposite(Vector3D(0,1,0)))
        self.assertTrue(v.is_opposite(v.opposite))
        
        
    def test_is_perpendicular(self):
        ""
        v=Vector3D(1,0,0)
        self.assertFalse(v.is_perpendicular(v))
        self.assertTrue(v.is_perpendicular(Vector3D(0,1,0)))
        
        
    def test_length(self):
        ""
        v=Vector3D(1,0,0)
        self.assertEqual(v.length,
                         1)
        
        
    def test_normalise(self):
        ""
        v=Vector3D(2,0,0)
        self.assertEqual(v.normalise,
                         Vector3D(1,0,0))
        
        
    def test_opposite(self):
        ""
        v=Vector3D(1,0,0)
        self.assertEqual(v.opposite,
                         Vector3D(-1,0,0))
        
        
    def test_triple_product(self):
        ""
        v1=Vector3D(1,0,0)
        v2=Vector3D(0,1,0)
        v3=Vector3D(0,0,1)
        self.assertEqual(v1.triple_product(v2,v3),
                         1)
    
    
if __name__=='__main__':
    
    unittest.main(Test_Vector())
    #unittest.main(Test_Vector2D())
    #unittest.main(Test_Vector3D())
    
    
    