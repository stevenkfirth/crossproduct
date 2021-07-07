# -*- coding: utf-8 -*-

import unittest

import shapely.geometry

from crossproduct import Point, Points
from crossproduct import Polyline, Polylines
from crossproduct import Polygon, Polygons

class Test_Polygon(unittest.TestCase):
    ""
    
    def test___eq__(self):
        ""
        pg=Polygon(Point(0,0),Point(1,0),Point(1,1),Point(0,1))
        self.assertTrue(pg==pg)
        
        pg1=Polygon(Point(0,1),Point(0,0),Point(1,0),Point(1,1))
        self.assertTrue(pg==pg1)
        
        pg2=Polygon(Point(0,0),Point(1,0),Point(0,1))
        self.assertFalse(pg==pg2)
        
    
    def test___init__(self):
        ""
        pg=Polygon(Point(0,0),Point(1,0),Point(1,1),Point(0,1))
        self.assertIsInstance(pg,Polygon)
        self.assertEqual(tuple(pg),
                         (Point(0,0),Point(1,0),Point(1,1),Point(0,1)))
        
        
    def test__shapely(self):
        ""
        # convex polygon, 2d, no holes
        pg=Polygon(Point(0,0),Point(1,0),Point(1,1),Point(0,1))
        #print(pg._shapely); return
        self.assertEqual(pg._shapely,
            shapely.geometry.MultiPolygon([shapely.geometry.Polygon(((0,0),
                                                                     (1,0),
                                                                     (1,1),
                                                                     (0,1)))]))
        
        
    def test_intersection_polygon(self):
        ""
        # concave polygon
        # 2D
        pg=Polygon(Point(0,0),Point(1,0),Point(1,1),Point(0,1))
        # no intersection
        pg1=Polygon(Point(0,2),Point(1,2),Point(1,3),Point(0,3))
        #print(pg.intersection(pg1)); return
        self.assertEqual(pg.intersection(pg1),
                         (Points(), 
                          Polylines(), 
                          Polygons()))
        # point intersection
        pg1=Polygon(Point(1,1),Point(2,1),Point(2,2),Point(1,2))
        #print(pg.intersection(pg1)); return
        self.assertEqual(pg.intersection(pg1),
                         (Points(Point(1,1)), 
                          Polylines(), 
                          Polygons()))
        # full edge intersection
        pg1=Polygon(Point(0,1),Point(1,1),Point(1,2),Point(0,2))
        #print(pg.intersection(pg1)); return
        self.assertEqual(pg.intersection(pg1),
                         (Points(), 
                          Polylines(Polyline(Point(0,1),Point(1,1))), 
                          Polygons()))
        # half edge overlap intersection
        pg1=Polygon(Point(0.5,1),Point(1.5,1),Point(1.5,2),Point(0.5,2))
        #print(pg.intersection(pg1)); return
        self.assertEqual(pg.intersection(pg1),
                         (Points(), 
                          Polylines(Polyline(Point(0.5,1),Point(1,1))), 
                          Polygons()))
        # partial internal edge intersection
        pg1=Polygon(Point(0.25,1),Point(0.75,1),Point(0.75,2),Point(0.25,2))
        #print(pg.intersection(pg1)); return
        self.assertEqual(pg.intersection(pg1),
                         (Points(), 
                          Polylines(Polyline(Point(0.25,1),Point(0.75,1))), 
                          Polygons()))
        # full intersection
        pg1=pg
        #print(pg.intersection(pg1)); return
        self.assertEqual(pg.intersection(pg1),
                         (Points(), 
                          Polylines(), 
                          Polygons(pg)))
        # half intersection
        pg1=Polygon(Point(0.5,0),Point(1.5,0),Point(1.5,1),Point(0.5,1))
        #print(pg.intersection(pg1)); return
        self.assertEqual(pg.intersection(pg1),
                         (Points(), 
                          Polylines(), 
                          Polygons(Polygon(Point(0.5,0),
                                           Point(1,0),
                                           Point(1,1),
                                           Point(0.5,1)))))
        # quarter intersection
        pg1=Polygon(Point(0.5,0.5),Point(1.5,0.5),Point(1.5,1.5),Point(0.5,1.5))
        #print(pg.intersection(pg1)); return
        self.assertEqual(pg.intersection(pg1),
                         (Points(), 
                          Polylines(), 
                          Polygons(Polygon(Point(0.5,0.5),
                                           Point(1,0.5),
                                           Point(1,1),
                                           Point(0.5,1)))))
        # internal intersection, 2 edges
        pg1=Polygon(Point(0.25,0),Point(0.75,0),Point(0.75,1),Point(0.25,1))
        #print(pg.intersection(pg1)); return
        self.assertEqual(pg.intersection(pg1),
                         (Points(), 
                          Polylines(), 
                          Polygons(Polygon(Point(0.25,0.0),
                                           Point(0.75,0.0),
                                           Point(0.75,1.0),
                                           Point(0.25,1.0)))))
    
        # convex polygon
        # 2D
        pg=Polygon(Point(0,0),Point(1,0),Point(0.5,0.5),Point(1,1),Point(0,1))
        
        # 2 point intersection
        pg1=Polygon(Point(1,0),Point(2,0),Point(2,1),Point(1,1))
        #print(pg.intersection(pg1)); return
        self.assertEqual(pg.intersection(pg1),
                         (Points(Point(1.0,0.0),Point(1.0,1.0)), 
                          Polylines(), 
                          Polygons()))
        
        # 2 polyline intersection
        pg1=Polygon(Point(1,0),Point(1,1),Point(0.5,0.5))
        #print(pg.intersection(pg1)); return
        self.assertEqual(pg.intersection(pg1),
                         (Points(), 
                          Polylines(Polyline(Point(1.0,0.0),
                                             Point(0.5,0.5)),
                                    Polyline(Point(0.5,0.5),
                                             Point(1.0,1.0))), 
                          Polygons()))
        
        # 2 polygon intersection
        pg1=Polygon(Point(0.5,0),Point(1,0),Point(1,1),Point(0.5,1))
        #print(pg.intersection(pg1)); return
        self.assertEqual(pg.intersection(pg1),
                         (Points(), 
                          Polylines(), 
                          Polygons(Polygon(Point(1.0,0.0),
                                           Point(0.5,0.0),
                                           Point(0.5,0.5)),
                                   Polygon(Point(1.0,1.0),
                                           Point(0.5,0.5),
                                           Point(0.5,1.0)))))
        
        # point and polyline intersection
        pg=Polygon(Point(0,0),Point(1,0),Point(0.5,0.5),
                   Point(1,1),Point(1,2),Point(0,2))
        pg1=Polygon(Point(1,0),Point(2,0),Point(2,2),Point(1,2))
        #print(pg.intersection(pg1)); return
        self.assertEqual(pg.intersection(pg1),
                         ((Points(Point(1.0,0.0)), 
                           Polylines(Polyline(Point(1.0,1.0),
                                              Point(1.0,2.0))), 
                           Polygons())))
        
        
    def test_polygons(self):
        ""
        pg=Polygon(Point(0,0),Point(1,0),Point(1,1),Point(0,1))
        #print(pg.polygons); return
        self.assertEqual(pg.polygons,
                         Polygons(Polygon(Point(0.0,0.0),
                                          Point(1.0,0.0),
                                          Point(1.0,1.0),
                                          Point(0.0,1.0))))
        
        
        
class Test_Polygons(unittest.TestCase):
    ""
    
    def test___eq__(self):
        ""
        pg=Polygon(Point(0,0),Point(1,0),Point(1,1))
        pg1=Polygon(Point(2,0),Point(1,0),Point(1,1))
        pgs=Polygons(pg,pg1)
        
        self.assertEqual(pgs,pgs)
        
        self.assertFalse(pgs==Polygons(pg))
        
    
    def test__shapely(self):
        ""
        pg=Polygon(Point(0,0),Point(1,0),Point(1,1))
        pg1=Polygon(Point(2,0),Point(1,0),Point(1,1))
        pgs=Polygons(pg,pg1)
        #print(pgs._shapely); return
        self.assertEqual(pgs._shapely,
            shapely.geometry.MultiPolygon([shapely.geometry.Polygon(((0,0),
                                                                     (1,0),
                                                                     (1,1))),
                                           shapely.geometry.Polygon(((2,0),
                                                                     (1,0),
                                                                     (1,1)))
                                           ]))
        
        
if __name__=='__main__':
    
    unittest.main()
        
        