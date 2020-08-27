# -*- coding: utf-8 -*-

import unittest
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d

from crossproduct import Point2D, Point3D, Segment2D, Segment3D, Points, Segments, \
    Vector2D, Polygons, Polygon2D, Polylines, Polyline2D


plot=True
        
class Test_Polygons(unittest.TestCase):
    """
    
    """
    
    def test___init__(self):
        ""
        pgs=Polygons(*polygons)
        self.assertIsInstance(pgs,Polygons)
        self.assertEqual(pgs._polygons,
                         list(polygons))
        
        
    def test___eq__(self):
        ""
        pgs=Polygons(*polygons)
        self.assertTrue(pgs==pgs)
        
        pgs1=Polygons(polygons[0])
        self.assertFalse(pgs==pgs1)
        
        
    def test___repr__(self):
        ""
        pgs=Polygons(*polygons)
        self.assertEqual(str(pgs),
                         'Polygons(Polygon2D(Point2D(0.0,0.0),Point2D(1.0,0.0),Point2D(0.0,1.0)), Polygon2D(Point2D(1.0,0.0),Point2D(1.0,1.0),Point2D(0.0,1.0)))')
        
        
    def test_add_all(self):
        ""
        pgs=Polygons(*polygons)
        
        self.assertEqual(pgs.add_all,
                         Polygons(Polygon2D(Point2D(0.0,1.0),
                                            Point2D(0.0,0.0),
                                            Point2D(1.0,0.0),
                                            Point2D(1.0,1.0))))
        
        
    def test_add_first(self):
        ""
        pgs=Polygons(*polygons)
        
        pg=Polygon2D(Point2D(0,0),
                     Point2D(1,0),
                     Point2D(1,-1))
        self.assertEqual(pgs.add_first(pg),
                         (Polygon2D(Point2D(1,0),
                                    Point2D(1,-1),
                                    Point2D(0,0),
                                    Point2D(0.0,1.0)), 
                          0))
        
        
    def test_append(self):
        ""
        pgs=Polygons(*polygons)
        
        pgs.append(polygons[0])
        self.assertEqual(len(pgs),3)
        
        pgs.append(polygons[1])
        self.assertEqual(len(pgs),4)
        
        pgs.append(polygons[1],
                   unique=True)
        self.assertEqual(len(pgs),4)
        
    
    def test_intersect_segment(self):
        ""
        pg=Polygon2D(Point2D(0,0),
                      Point2D(2,0),
                      Point2D(1,1),
                      Point2D(2,2),
                      Point2D(0,2))
        pgs=pg._triangulate
        
        self.assertEqual(pgs.intersect_segment(Segment2D(Point2D(1.5,0),
                                                         Point2D(1.5,10))),
                        (Points(), 
                         Segments(Segment2D(Point2D(1.5,0), 
                                            Point2D(1.5,0.5)),
                                  Segment2D(Point2D(1.5,1.5), 
                                            Point2D(1.5,2)))))
        
        
    def test_plot(self):
        ""
    
    
    def test_polylines(self):
        ""
        pgs=Polygons(*polygons)
        self.assertEqual(pgs.polylines,
                         Polylines(Polyline2D(Point2D(0.0,0.0),
                                              Point2D(1.0,0.0),
                                              Point2D(0.0,1.0),
                                              Point2D(0.0,0.0)), 
                                   Polyline2D(Point2D(1.0,0.0),
                                              Point2D(1.0,1.0),
                                              Point2D(0.0,1.0),
                                              Point2D(1.0,0.0))))
    
    
    def test_project_3D(self):
        ""
        
    
    
    # def test_union_adjacent(self):
    #     ""
    #     sp=Polygons(*simple_polygons)
    #     self.assertEqual(sp.union_adjacent,
    #                      Polygons(Polygon2D(Point2D(0.0,1.0),
    #                                                     Point2D(0.0,0.0),
    #                                                     Point2D(1.0,0.0),
    #                                                     Point2D(1.0,1.0))))
    
    #     sp=Polygons(SimpleConvexPolygon2D(Point2D(1.0,0.5),Point2D(1.0,0.0),Point2D(2.0,0.0),Point2D(2.0,1.0)), 
    #                       SimpleConvexPolygon2D(Point2D(2.0,1.0),Point2D(1.0,1.0),Point2D(1.0,0.5)), 
    #                       SimpleConvexPolygon2D(Point2D(1.0,2.5),Point2D(1.0,2.0),Point2D(2.0,2.0)), 
    #                       SimpleConvexPolygon2D(Point2D(2.0,2.0),Point2D(2.0,3.0),Point2D(1,3),Point2D(1.0,2.5)))
        
    #     self.assertEqual(sp.union_adjacent,
    #                      Polygons(Polygon2D(Point2D(1.0,0.0),
    #                                                     Point2D(2.0,0.0),
    #                                                     Point2D(2.0,1.0),
    #                                                     Point2D(1.0,1.0)), 
    #                                     Polygon2D(Point2D(1.0,2.0),
    #                                                     Point2D(2.0,2.0),
    #                                                     Point2D(2.0,3.0),
    #                                                     Point2D(1,3))))
    #     #sp.plot()
    #     #sp.union_adjacent.plot()
    
    
if __name__=='__main__':
    
    polygons=(Polygon2D(Point2D(0.0,0.0),
                        Point2D(1.0,0.0),
                        Point2D(0.0,1.0)), 
              Polygon2D(Point2D(1.0,0.0),
                        Point2D(1.0,1.0),
                        Point2D(0.0,1.0)))
    unittest.main(Test_Polygons())
    
    