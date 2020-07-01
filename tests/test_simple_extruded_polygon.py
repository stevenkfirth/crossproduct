# -*- coding: utf-8 -*-

import unittest
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d

from crossproduct import Point2D, Point3D, \
    Vector2D, Vector3D, Line2D, SimplePolygon2D, SimplePolygon3D, Plane3D, Triangle2D, Triangle3D, \
    Segment2D, Segment3D, Halfline2D, SimpleExtrudedPolyhedron3D

plot=True # Set to true to see the test plots

class Test_SimpleExtrudedPolyhedron3D(unittest.TestCase):
    """
    points=(Point2D(0,0),Point2D(1,0),Point2D(1,1),Point2D(0,1))
    """
    
    def test___init__(self):
        ""
        ph=SimpleExtrudedPolyhedron3D(polygon,Vector3D(1,0,1))
        self.assertIsInstance(ph,SimpleExtrudedPolyhedron3D)
        #print(ph.polygons)
        #print([pg.plane.N for pg in ph.polygons])
        #self.assertEqual(pg.points,points)
        print(ph.volume)
        
        
        if plot:
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            ph.plot(ax,normal=True)
        
        
        
#    def test_plot(self):
#        ""
#        if plot:
#            ph=SimpleExtrudedPolyhedron3D(polygon,Vector3D(0,0,1))
#            fig = plt.figure()
#            ax = fig.add_subplot(111, projection='3d')
#            ph.plot(ax,normal=True)
        
        
if __name__=='__main__':
    
    polygon=SimplePolygon3D(Point3D(0,0,0),
                            Point3D(1,0,0),
                            Point3D(1,1,0),
                            Point3D(0,1,0))
    unittest.main(Test_SimpleExtrudedPolyhedron3D())