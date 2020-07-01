# -*- coding: utf-8 -*-

import unittest
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d

from crossproduct import Point2D, Point3D,Vector2D, Vector3D, \
    Halfline2D, Halfline3D, Line2D, Line3D, Segment2D, Segment3D, \
    SimplePolyline2D, SimplePolyline3D

plot=False

class Test_SimplePolyline2D(unittest.TestCase):
    """
    points(Point2D(0,0),
            Point2D(0,1),
            Point2D(1,1))
    """

    def test___init__(self):
        ""
        pl=SimplePolyline2D(*points)
        self.assertIsInstance(pl,SimplePolyline2D)
        self.assertEqual(pl.points,points)
        
        
    def test___eq__(self):
        ""
        pl=SimplePolyline2D(*points)
        
        self.assertTrue(pl==pl)
        self.assertTrue(pl==SimplePolyline2D(Point2D(1,1),
                                       Point2D(0,1),
                                       Point2D(0,0)))
        
        
    def test_plot(self):
        ""
        if plot:
            pl=SimplePolyline2D(*points)
            fig, ax = plt.subplots()
            pl.plot(ax)
        
        
          
    def test___repr__(self):
        ""
        pl=SimplePolyline2D(*points)
        self.assertEqual(str(pl),'SimplePolyline2D(Point2D(0,0),Point2D(0,1),Point2D(1,1))')
    

    def test_reverse(self):
        ""
        pl=SimplePolyline2D(*points)
        
        self.assertEqual(pl.reverse,
                         SimplePolyline2D(Point2D(1,1),
                                    Point2D(0,1),
                                    Point2D(0,0)))
    
    
    def test_segments(self):
        ""
        pl=SimplePolyline2D(*points)
        self.assertEqual(pl.segments,
                         (Segment2D(Point2D(0,0),
                                    Point2D(0,1)),
                          Segment2D(Point2D(0,1),
                                    Point2D(1,1))))
    
    
    def test_union(self):
        ""
        pl=SimplePolyline2D(*points)
        
        # no union
        self.assertEqual(pl.union(SimplePolyline2D(Point2D(2,2),
                                             Point2D(3,3))),
                         None)
    
        # union
        self.assertEqual(pl.union(SimplePolyline2D(Point2D(1,1),
                                             Point2D(1,2),
                                             Point2D(2,2))),
                         SimplePolyline2D(Point2D(0,0),
                                    Point2D(0,1),
                                    Point2D(1,1),
                                    Point2D(1,2),
                                    Point2D(2,2)))
        
        self.assertEqual(pl.union(SimplePolyline2D(Point2D(2,2),
                                             Point2D(1,2),
                                             Point2D(1,1))),
                         SimplePolyline2D(Point2D(0,0),
                                    Point2D(0,1),
                                    Point2D(1,1),
                                    Point2D(1,2),
                                    Point2D(2,2)))
            
        self.assertEqual(pl.union(SimplePolyline2D(Point2D(1,0),
                                             Point2D(0,0))),
                         SimplePolyline2D(Point2D(1,0),
                                    Point2D(0,0),
                                    Point2D(0,1),
                                    Point2D(1,1)))
            
        self.assertEqual(pl.union(SimplePolyline2D(Point2D(0,0),
                                             Point2D(1,0))),
                         SimplePolyline2D(Point2D(1,0),
                                    Point2D(0,0),
                                    Point2D(0,1),
                                    Point2D(1,1)))
        
            
class Test_SimplePolyline3D(unittest.TestCase):
    """
    points=(Point2D(0,0,0),
            Point2D(0,1,0),
            Point2D(1,1,0))
    """

#    def test___init__(self):
#        ""
#        pl=SimplePolyline3D(*points)
#        self.assertIsInstance(pl,SimplePolyline3D)
#        self.assertEqual(pl.points,points)
#    
#    
#    def test___eq__(self):
#        ""
#        pl=SimplePolyline3D(*points)
#        
#        self.assertTrue(pl==pl)
#        self.assertTrue(pl==SimplePolyline3D(Point3D(1,1,0),
#                                       Point3D(0,1,0),
#                                       Point3D(0,0,0)))
#    
#    
#    def test_plot(self):
#        ""
#        if plot:
#            pl=SimplePolyline3D(*points)
#            fig = plt.figure()
#            ax = fig.add_subplot(111, projection='3d')
#            pl.plot(ax)
#    
#        
#    def test___repr__(self):
#        ""
#        pl=SimplePolyline3D(*points)
#        self.assertEqual(str(pl),'SimplePolyline3D(Point3D(0,0,0),Point3D(0,1,0),Point3D(1,1,0))')
#        
#        
#    def test_reverse(self):
#        ""
#        pl=SimplePolyline3D(*points)
#        
#        self.assertEqual(pl.reverse,
#                         SimplePolyline3D(Point3D(1,1,0),
#                                    Point3D(0,1,0),
#                                    Point3D(0,0,0)))
#        
#        
#    def test_segments(self):
#        ""
#        pl=SimplePolyline3D(*points)
#        self.assertEqual(pl.segments,
#                         (Segment3D(Point3D(0,0,0),
#                                    Point3D(0,1,0)),
#                          Segment3D(Point3D(0,1,0),
#                                    Point3D(1,1,0))))
#        
        
    
if __name__=='__main__':
    
    points=(Point2D(0,0),
            Point2D(0,1),
            Point2D(1,1))
    unittest.main(Test_SimplePolyline2D())
    
    points=(Point3D(0,0,0),
            Point3D(0,1,0),
            Point3D(1,1,0))
    unittest.main(Test_SimplePolyline3D())