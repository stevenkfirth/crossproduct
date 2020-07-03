# -*- coding: utf-8 -*-

import unittest
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d

from crossproduct import Point2D, Point3D, Segment2D, Segment3D, Points, Segments, \
    SimplePolyline2D


plot=True
        
class Test_Polylines(unittest.TestCase):
    """
    
    """
    
    def test___init__(self):
        ""
        s=Segments(*segments)
        self.assertIsInstance(s,Segments)
        self.assertEqual(s.segments,
                         list(segments))
        
        
    def test___eq__(self):
        ""
        s=Segments(*segments)
        self.assertTrue(s==s)
        
        s1=Segments(*segments)
        s1.append(Segment2D(Point2D(1,1),
                            Point2D(0,1)))
        self.assertFalse(s==s1)
        
        
    def test___repr__(self):
        ""
        s=Segments(*segments)
        self.assertEqual(str(s),
                         'Segments(Segment2D(Point2D(0,0), Point2D(1,0)), Segment2D(Point2D(1,0), Point2D(1,1)))')
        
        
    def test_append(self):
        ""
        s=Segments(*segments)
        
        s.append(Segment2D(Point2D(1,1),
                           Point2D(0,1)))
        self.assertEqual(len(s),3)
        
        s.append(Segment2D(Point2D(1,1),
                           Point2D(0,1)))
        self.assertEqual(len(s),4)
        
        s.append(Segment2D(Point2D(0,1),
                           Point2D(1,1)),
                 unique=True)
        self.assertEqual(len(s),4)
    
    
    def test_intersect_point(self):
        ""
        s=Segments(*segments)
        self.assertTrue(s.intersect_point(Point2D(0,0)))
        self.assertTrue(s.intersect_point(Point2D(0.5,0)))
        self.assertFalse(s.intersect_point(Point2D(-0.5,0)))
        
        
    def test_intersect_segment(self):
        ""
        s=Segments(*segments)
        
        # no intersection
        self.assertEqual(s.intersect_segment(Segment2D(Point2D(-1,0),
                                                       Point2D(-0.5,0))),
                         (Points(),
                          Segments()))
    
        # single point intersection
        self.assertEqual(s.intersect_segment(Segment2D(Point2D(-1,0),
                                                       Point2D(0,0))),
                         (Points(Point2D(0,0)),
                          Segments()))
            
        # two point intersection
        self.assertEqual(s.intersect_segment(Segment2D(Point2D(0,0),
                                                       Point2D(1,1))),
                         (Points(Point2D(0,0),
                                 Point2D(1,1)),
                          Segments()))
            
        # segment intersection
        self.assertEqual(s.intersect_segment(Segment2D(Point2D(0,0),
                                                       Point2D(1,0))),
                         (Points(),
                          Segments(Segment2D(Point2D(0,0),
                                                       Point2D(1,0)))))
            
        self.assertEqual(s.intersect_segment(Segment2D(Point2D(-1,0),
                                                       Point2D(1,0))),
                         (Points(),
                          Segments(Segment2D(Point2D(0,0),
                                                       Point2D(1,0)))))
            
        self.assertEqual(s.intersect_segment(Segment2D(Point2D(0,0),
                                                       Point2D(2,0))),
                         (Points(),
                          Segments(Segment2D(Point2D(0,0),
                                                       Point2D(1,0)))))
            
        self.assertEqual(s.intersect_segment(Segment2D(Point2D(-1,0),
                                                       Point2D(2,0))),
                         (Points(),
                          Segments(Segment2D(Point2D(0,0),
                                                       Point2D(1,0)))))
        
            
    def test_intersect_segments(self):
        ""
        s=Segments(*segments)
        
        self.assertEqual(s.intersect_segments(s),
                         (Points(),
                          s))
            
        
    def test_polylines(self):
        ""
        s=Segments(*segments)
        self.assertEqual(s.polylines,
                         (SimplePolyline2D(Point2D(0,0),
                                           Point2D(1,0),
                                           Point2D(1,1)),))
        
        s.append(Segment2D(Point2D(2,2),
                           Point2D(3,3)))     
        self.assertEqual(s.polylines,
                         (SimplePolyline2D(Point2D(0,0),
                                           Point2D(1,0),
                                           Point2D(1,1)), 
                          SimplePolyline2D(Point2D(2,2),
                                           Point2D(3,3))))
        
    
if __name__=='__main__':
    
    segments=(Segment2D(Point2D(0,0),
                        Point2D(1,0)),
              Segment2D(Point2D(1,0),
                        Point2D(1,1)))
    unittest.main(Test_Segments())
    
    