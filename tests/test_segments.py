# -*- coding: utf-8 -*-

import unittest
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d

from crossproduct import Point, Points, Segment, Segments


plot=True
        
class Test_Segments(unittest.TestCase):
    """
    segments=(Segment(Point(0,0),
                        Point(1,0)),
              Segment(Point(1,0),
                        Point(1,1)))
    """
    
    def test___init__(self):
        ""
        s=Segments(*segments)
        self.assertIsInstance(s,Segments)
        self.assertEqual(s._segments,
                         list(segments))
        
        
    def test___eq__(self):
        ""
        s=Segments(*segments)
        self.assertTrue(s==s)
        
        s1=Segments(*segments)
        s1.append(Segment(Point(1,1),
                            Point(0,1)))
        self.assertFalse(s==s1)
        
                
        
    def test_add_all(self):
        ""
        # no additions
        s=Segments(*segments)
        s.add_all()
        self.assertEqual(s,
                         Segments(*segments))
        # an addition
        s=Segments(Segment(Point(0,0), Point(1,0)), 
                   Segment(Point(1,0), Point(2,0)))
        s.add_all()
        self.assertEqual(s,
                         Segments(Segment(Point(0,0), 
                                            Point(2,0))))
        # reversed
        s=Segments(Segment(Point(1,0), Point(2,0)), 
                   Segment(Point(0,0), Point(1,0)))
        s.add_all()
        self.assertEqual(s,
                         Segments(Segment(Point(0,0), 
                                            Point(2,0))))
        # gap
        s=Segments(Segment(Point(0,0), Point(1,0)), 
                   Segment(Point(2,0), Point(3,0)))
        s.add_all()
        self.assertEqual(s,
                         Segments(Segment(Point(0,0), Point(1,0)), 
                                  Segment(Point(2,0), Point(3,0))))
        # an gap and an addition
        s=Segments(Segment(Point(0,0), Point(1,0)), 
                   Segment(Point(2,0), Point(3,0)),
                   Segment(Point(3,0), Point(4,0)))
        s.add_all()
        self.assertEqual(s,
                         Segments(Segment(Point(0,0), 
                                            Point(1,0)), 
                                  Segment(Point(2.0,0.0), 
                                            Point(4.0,0.0))))
        
        
    def test_add_first(self):
        ""
        s=Segments(*segments)
        self.assertEqual(s.add_first(Segment(Point(-1,0), 
                                             Point(0,0))),
                         (Segment(Point(-1.0,0.0), 
                                  Point(1.0,0.0)), 
                          0))
        
        self.assertEqual(s.add_first(Segment(Point(1,1), 
                                             Point(1,2))),
                         (Segment(Point(1.0,0.0), 
                                  Point(1.0,2.0)), 
                          1))
        
        
    # def _test_append(self):
    #     ""
    #     s=Segments(*segments)
        
    #     s.append(Segment2D(Point2D(1,1),
    #                        Point2D(0,1)))
    #     self.assertEqual(len(s),3)
        
    #     s.append(Segment2D(Point2D(1,1),
    #                        Point2D(0,1)))
    #     self.assertEqual(len(s),4)
        
    #     s.append(Segment2D(Point2D(0,1),
    #                        Point2D(1,1)),
    #              unique=True)
    #     self.assertEqual(len(s),4)
    
    
    def test_contains(self):
        ""
        s=Segments(*segments)
        
        # point
        self.assertTrue(s.contains(Point(0,0)))
        self.assertTrue(s.contains(Point(0.5,0)))
        self.assertFalse(s.contains(Point(-1,0)))
        
    
    def _test_difference_segments(self):
        ""
        s=Segments(*segments)
        
        # no intersection
        s1=Segments(Segment2D(Point2D(0,5),
                              Point2D(0,6)))
        self.assertEqual(s.difference_segments(s1),
                          s)
    
        # edge intersection - single edge
        s1=Segments(Segment2D(Point2D(0,0),
                              Point2D(1,0)))
        self.assertEqual(s.difference_segments(s1),
                          Segments(Segment2D(Point2D(1,0), 
                                            Point2D(1,1))))
        
        # edge intersection - mid to end single edge
        s1=Segments(Segment2D(Point2D(0,0),
                              Point2D(0.5,0)))
        self.assertEqual(s.difference_segments(s1),
                          Segments(Segment2D(Point2D(0.5,0), 
                                            Point2D(1,0)), 
                                  Segment2D(Point2D(1,0), 
                                            Point2D(1,1))))
        
        # edge intersection - start to mid single edge
        s1=Segments(Segment2D(Point2D(0.5,0),
                              Point2D(1,0)))
        self.assertEqual(s.difference_segments(s1),
                          Segments(Segment2D(Point2D(0,0), 
                                            Point2D(0.5,0)), 
                                  Segment2D(Point2D(1,0), 
                                            Point2D(1,1))))
        
        # self intersection
        self.assertEqual(s.difference_segments(s),
                         Segments())
        
        #
        s1=Segments(Segment2D(Point2D(1.0,1.0), Point2D(0.5,1)), 
                    Segment2D(Point2D(0.5,1), Point2D(0.5,0.0)), 
                    Segment2D(Point2D(0.5,0.0), Point2D(1.0,0.0)), 
                    Segment2D(Point2D(1.0,0.0), Point2D(1.0,1.0)))
        s2=Segments(Segment2D(Point2D(0,0), Point2D(1,0)), 
                    Segment2D(Point2D(1,0), Point2D(1,1)), 
                    Segment2D(Point2D(1,1), Point2D(0,1)), 
                    Segment2D(Point2D(0,1), Point2D(0,0)))
        self.assertEqual(s1.difference_segments(s2),
                          Segments(Segment2D(Point2D(0.5,1), 
                                            Point2D(0.5,0.0))))
    
        #
        s1=Segments(Segment2D(Point2D(0,0), Point2D(2,0)), 
                    Segment2D(Point2D(2,0), Point2D(2,1)), 
                    Segment2D(Point2D(2,1), Point2D(0,1)), 
                    Segment2D(Point2D(0,1), Point2D(0,0)))
        s2=Segments(Segment2D(Point2D(0.5,0), Point2D(1.5,0)), 
                    Segment2D(Point2D(1.5,0), Point2D(1.5,1)), 
                    Segment2D(Point2D(1.5,1), Point2D(0.5,1)), 
                    Segment2D(Point2D(0.5,1), Point2D(0.5,0)))
        self.assertEqual(s1.difference_segments(s2),
                          Segments(Segment2D(Point2D(0,0), Point2D(0.5,0.0)), 
                                  Segment2D(Point2D(1.5,0.0), Point2D(2,0)), 
                                  Segment2D(Point2D(2,0), Point2D(2,1)), 
                                  Segment2D(Point2D(2,1), Point2D(1.5,1.0)), 
                                  Segment2D(Point2D(0.5,1.0), Point2D(0,1)), 
                                  Segment2D(Point2D(0,1), Point2D(0,0))))
    
        
    def _test_intersect_segment(self):
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
        
            
    def _test_intersect_segments(self):
        ""
        s=Segments(*segments)
        
        self.assertEqual(s.intersect_segments(s),
                          (Points(),
                          s))
            
        
    
if __name__=='__main__':
    
    segments=(Segment(Point(0,0),
                      Point(1,0)),
              Segment(Point(1,0),
                      Point(1,1)))
    unittest.main(Test_Segments())
    
    