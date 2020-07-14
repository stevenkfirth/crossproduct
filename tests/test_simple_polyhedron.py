# -*- coding: utf-8 -*-

import unittest
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d

from crossproduct import Point2D, Point3D, \
    Vector2D, Vector3D, Line2D, SimplePolygon2D, SimplePolygon3D, Plane3D, Triangle2D, Triangle3D, \
    Segment2D, Segment3D, SimplePolyhedron3D


plot=True
        
class Test_SimplePolyhedron3D(unittest.TestCase):
    """
    
    """
    
    def test___init__(self):
        ""
        ph=SimplePolyhedron3D(*polygons)
        self.assertIsInstance(ph,SimplePolyhedron3D)
        self.assertEqual(ph.polygons,polygons)
        print(ph.polygons)
        print(ph.polygons[0].plane.N)
        print(ph.polygons[1].plane.N)
        
    def test___contains__(self):
        ""
        
        
    def test___eq__(self):
        ""
        
        
        
    def test___repr__(self):
        ""
        
        
    def test_plot(self):
        ""
                
        if plot:
        
            ph=SimplePolyhedron3D(*polygons)
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            ph.plot(ax,normal=True)
        
        
    
if __name__=='__main__':
    
    P0=Point3D(0,0,0)
    P1=Point3D(1,0,0)
    P2=Point3D(1,1,0)
    P3=Point3D(0,1,0)
    P4=Point3D(0,0,1)
    P5=Point3D(1,0,1)
    P6=Point3D(1,1,1)
    P7=Point3D(0,1,1)
    
    polygons=(SimplePolygon3D(P0,P1,P2,P3),
              SimplePolygon3D(P0,P1,P5,P4),
              SimplePolygon3D(P1,P2,P6,P5),
              SimplePolygon3D(P2,P3,P7,P6),
              SimplePolygon3D(P3,P0,P4,P7),
              SimplePolygon3D(P5,P4,P7,P6))
    unittest.main(Test_SimplePolyhedron3D())
    
    