# -*- coding: utf-8 -*-

import unittest
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d

from crossproduct import Point2D, Point3D, Segment2D, Segment3D, Points, Segments, \
    Polyline2D, Polylines


plot=True
        
class Test_Polylines(unittest.TestCase):
    """
    
    """
    
    def test___init__(self):
        ""
        pls=Polylines(*polylines)
        self.assertIsInstance(pls,Polylines)
        self.assertEqual(pls._polylines,
                         list(polylines))
        
        
    def test___eq__(self):
        ""
        pls=Polylines(*polylines)
        self.assertTrue(pls==pls)
        
        pls1=Polylines(*polylines)
        pls1.append(Polyline2D(Point2D(1,1),
                               Point2D(0,1)))
        self.assertFalse(pls==pls1)
        
        
    def test___repr__(self):
        ""
        pls=Polylines(*polylines)
        self.assertEqual(str(pls),
                        'Polylines(Polyline2D(Point2D(0,0),Point2D(1,0)), Polyline2D(Point2D(1,0),Point2D(1,1)))')
        
        
    def test_add_all(self):
        
        pls=Polylines(*polylines)
        
        # no additions
        self.assertEqual(pls.add_all,
                         Polylines(Polyline2D(Point2D(0,0),
                                              Point2D(1,0),
                                              Point2D(1,1))))
        
        pls=Polylines(Polyline2D(Point2D(0,0),Point2D(1,0)), 
                      Polyline2D(Point2D(1,0),Point2D(1,1)),
                      Polyline2D(Point2D(10,0),Point2D(11,0)),
                      Polyline2D(Point2D(11,0),Point2D(11,1)))
        self.assertEqual(pls.add_all,
                         Polylines(Polyline2D(Point2D(0,0),
                                              Point2D(1,0),
                                              Point2D(1,1)), 
                                   Polyline2D(Point2D(10,0),
                                              Point2D(11,0),
                                              Point2D(11,1))))
        
        pls=Polylines(Polyline2D(Point2D(0,0),Point2D(1,0)), 
                      Polyline2D(Point2D(1,0),Point2D(1,1)), 
                      Polyline2D(Point2D(1,1),Point2D(0,1)), 
                      Polyline2D(Point2D(0,1),Point2D(0,0)))
        self.assertEqual(pls.add_all,
                         Polylines(Polyline2D(Point2D(0,0),
                                              Point2D(1,0),
                                              Point2D(1,1),
                                              Point2D(0,1),
                                              Point2D(0,0))))
        
        
    def test_add_first(self):
        ""
        pls=Polylines(*polylines)
        
        self.assertEqual(pls.add_first(Polyline2D(Point2D(-1,0), 
                                                  Point2D(0,0))),
                         (Polyline2D(Point2D(-1,0),
                                     Point2D(0,0),
                                     Point2D(1,0)), 
                          0))
        
        
        self.assertEqual(pls.add_first(Polyline2D(Point2D(0,0), 
                                                  Point2D(-1,0))),
                         (Polyline2D(Point2D(-1,0),
                                     Point2D(0,0),
                                     Point2D(1,0)), 
                          0))
        
        
        self.assertEqual(pls.add_first(Polyline2D(Point2D(1,1), 
                                                  Point2D(1,2))),
                         (Polyline2D(Point2D(1,0),
                                     Point2D(1,1),
                                     Point2D(1,2)), 
                          1))
        
        
        self.assertEqual(pls.add_first(Polyline2D(Point2D(1,2), 
                                                  Point2D(1,1))),
                         (Polyline2D(Point2D(1,0),
                                     Point2D(1,1),
                                     Point2D(1,2)), 
                          1))
        
        
    def test_append(self):
        ""
        pls=Polylines(*polylines)
        
        pls.append(Polyline2D(Point2D(1,1),
                              Point2D(0,1)))
        self.assertEqual(len(pls),3)
        
        pls.append(Polyline2D(Point2D(1,1),
                              Point2D(0,1)))
        self.assertEqual(len(pls),4)
        
        pls.append(Polyline2D(Point2D(0,1),
                              Point2D(1,1)),
                 unique=True)
        self.assertEqual(len(pls),4)
        
    
    def test_segments(self):
        ""
        pls=Polylines(*polylines)
        self.assertEqual(pls.segments,
                         Segments(Segment2D(Point2D(0,0),Point2D(1,0)),
                                  Segment2D(Point2D(1,0),Point2D(1,1))))
    


if __name__=='__main__':
    
    polylines=(Polyline2D(Point2D(0,0),
                          Point2D(1,0)),
               Polyline2D(Point2D(1,0),
                          Point2D(1,1)))
    unittest.main(Test_Polylines())
    
    