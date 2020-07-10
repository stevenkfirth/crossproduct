# -*- coding: utf-8 -*-

import unittest
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d

from crossproduct import Point2D, Point3D, Segment2D, Segment3D, Points, Segments, \
    SimplePolyline2D, Polyline2D, Polylines


plot=True
        
class Test_Segments(unittest.TestCase):
    """
    segments=(Segment2D(Point2D(0,0),
                        Point2D(1,0)),
              Segment2D(Point2D(1,0),
                        Point2D(1,1)))
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
    
    
    def test_difference_segments(self):
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
                         None)
        
        
        
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
            
        
    def test_polyline(self):
        ""
        # two segment polyline
        s=Segments(*segments)
        self.assertEqual(s.polyline,
                         Polyline2D(Point2D(0,0),
                                     Point2D(1,0),
                                     Point2D(1,1)))
        
        # three segment polyline
        s=Segments(Segment2D(Point2D(0,0),
                             Point2D(1,0)),
                   Segment2D(Point2D(1,0), 
                             Point2D(1,1)),
                   Segment2D(Point2D(1,1), 
                             Point2D(2,1)))
        self.assertEqual(s.polyline,
                         Polyline2D(Point2D(0,0),
                                    Point2D(1,0),
                                    Point2D(1,1),
                                    Point2D(2,1)))
        
        # no polyline
        s=Segments(Segment2D(Point2D(0,0),
                             Point2D(1,0)),
                   Segment2D(Point2D(1,1), 
                             Point2D(2,1)))
        self.assertEqual(s.polyline,
                         None)
    

    def test_polylines(self):
        #
        s=Segments(Segment2D(Point2D(0,0), Point2D(0.5,0.0)), 
                   Segment2D(Point2D(1.5,0.0), Point2D(2,0)), 
                   Segment2D(Point2D(2,0), Point2D(2,1)), 
                   Segment2D(Point2D(2,1), Point2D(1.5,1.0)), 
                   Segment2D(Point2D(0.5,1.0), Point2D(0,1)), 
                   Segment2D(Point2D(0,1), Point2D(0,0)))
        self.assertEqual(s.polylines,
                         Polylines(Polyline2D(Point2D(0.5,1.0),
                                              Point2D(0,1),
                                              Point2D(0,0),
                                              Point2D(0.5,0.0)), 
                                   Polyline2D(Point2D(1.5,0.0),
                                              Point2D(2,0),
                                              Point2D(2,1),
                                              Point2D(1.5,1.0))))


    def test_union(self):
        ""
        s=Segments(*segments)
        
        # no unions
        self.assertEqual(s.union,
                         s)
            
        # a union
        s=Segments(Segment2D(Point2D(0,0), Point2D(1,0)), 
                   Segment2D(Point2D(1,0), Point2D(2,0)))
        self.assertEqual(s.union,
                         Segments(Segment2D(Point2D(0,0), 
                                            Point2D(2,0))))
        
        # reversed
        s=Segments(Segment2D(Point2D(1,0), Point2D(2,0)), 
                   Segment2D(Point2D(0,0), Point2D(1,0)))
        self.assertEqual(s.union,
                         Segments(Segment2D(Point2D(0,0), 
                                            Point2D(2,0))))
        
        # gap
        # a union
        s=Segments(Segment2D(Point2D(0,0), Point2D(1,0)), 
                   Segment2D(Point2D(2,0), Point2D(3,0)))
        self.assertEqual(s.union,
                         s)
        
        
        
    def test_union_polyline(self):
        ""
        s=Segments(*segments)
        
        # no union
        self.assertEqual(s.union_polyline(Polyline2D(Point2D(3,1),
                                                   Point2D(4,1))),
                         None)
        
        # segment union
        self.assertEqual(s.union_polyline(Polyline2D(Point2D(1,1),
                                                   Point2D(1,2))),
                         (Polyline2D(Point2D(1,0),
                                     Point2D(1,1),
                                     Point2D(1,2)), 
                          Segments(Segment2D(Point2D(0,0), 
                                             Point2D(1,0)))))
        
        # polyline union
        self.assertEqual(s.union_polyline(Polyline2D(Point2D(1,1),
                                                   Point2D(2,1))),
                         (Polyline2D(Point2D(1,0),
                                     Point2D(1,1),
                                     Point2D(2,1)), 
                          Segments(Segment2D(Point2D(0,0), 
                                             Point2D(1,0)))))
        
        
        
    def test_union_segment(self):
        ""
        s=Segments(*segments)
        
        # no union
        self.assertEqual(s.union_segment(Segment2D(Point2D(3,1),
                                                   Point2D(4,1))),
                         None)
        
        # segment union
        self.assertEqual(s.union_segment(Segment2D(Point2D(1,1),
                                                   Point2D(1,2))),
                         (Polyline2D(Point2D(1,0),
                                     Point2D(1,1),
                                     Point2D(1,2)), 
                          Segments(Segment2D(Point2D(0,0), 
                                             Point2D(1,0)))))
        
        # polyline union
        self.assertEqual(s.union_segment(Segment2D(Point2D(1,1),
                                                   Point2D(2,1))),
                         (Polyline2D(Point2D(1,0),
                                     Point2D(1,1),
                                     Point2D(2,1)), 
                          Segments(Segment2D(Point2D(0,0), 
                                             Point2D(1,0)))))
        
        
        
        
        
#    def test_polylines(self):
#        ""
#        s=Segments(*segments)
#        self.assertEqual(s.polylines,
#                         (SimplePolyline2D(Point2D(0,0),
#                                           Point2D(1,0),
#                                           Point2D(1,1)),))
#        
#        s.append(Segment2D(Point2D(2,2),
#                           Point2D(3,3)))     
#        self.assertEqual(s.polylines,
#                         (SimplePolyline2D(Point2D(0,0),
#                                           Point2D(1,0),
#                                           Point2D(1,1)), 
#                          SimplePolyline2D(Point2D(2,2),
#                                           Point2D(3,3))))
        
    
if __name__=='__main__':
    
    segments=(Segment2D(Point2D(0,0),
                        Point2D(1,0)),
              Segment2D(Point2D(1,0),
                        Point2D(1,1)))
    unittest.main(Test_Segments())
    
    