# -*- coding: utf-8 -*-

import unittest

import shapely.geometry

from crossproduct import Point, Points
from crossproduct import Vector
from crossproduct import Line
from crossproduct import Polyline, Polylines
from crossproduct import Plane
from crossproduct import Polygon, Polygons
from crossproduct import Tetrahedron, tetrahedron_from_points
from crossproduct import ExtrudedPolyhedron
from crossproduct import GeometryObjects


class Test_Point(unittest.TestCase):
    ""
    
    def test_difference(self):
        ""
        pt=Point(0.5,0.5)
        pg=Polygon(Point(0,0),Point(1,0),Point(1,1),Point(0,1))
        #print(pt.difference(pg)); return
        self.assertEqual(pt.difference(pg),
                         GeometryObjects())
        
        
    def test_intersection(self):
        ""
        pt=Point(0.5,0.5)
        pg=Polygon(Point(0,0),Point(1,0),Point(1,1),Point(0,1))
        #print(pt.intersection(pg)); return
        self.assertEqual(pt.intersection(pg),
                         GeometryObjects(Point(0.5,0.5)))
        
        
    def test_plot(self):
        ""
        return
        pt=Point(0.5,0.5)
        pt.plot()
        
        pt=Point(0.5,0.5,0.5)
        pt.plot()
    

class Test_Points(unittest.TestCase):
    ""
    def test_plot(self):
        ""
        return
        pts=Points(Point(0.5,0.5),Point(1.5,0.5))
        pts.plot()
        
        
class Test_Polyline(unittest.TestCase):
    ""
    
    def test_plot(self):
        ""
        return
        pl=Polyline(Point(0.5,0.5),Point(1.5,0.5))
        pl.plot()


class Test_Polylines(unittest.TestCase):
    ""
    
    def test_plot(self):
        ""
        return
        pls=Polylines(Polyline(Point(0.5,0.5),Point(1.5,0.5)),
                      Polyline(Point(0.5,1.5),Point(1.5,1.5)))
        pls.plot()



class Test_Plane(unittest.TestCase):
    ""
    
    def test_intersection_plane(self):
        ""
        P0,N=Point(0,0,0),Vector(0,0,1)
        pl=Plane(P0,N)
        
        # coplanar plane
        self.assertEqual(pl.intersection(pl),
                         GeometryObjects(pl))
        
        # parallel, non-coplanar planes
        self.assertEqual(pl.intersection(Plane(P0+N,N)),
                         GeometryObjects())
        
        # intersecting planes - same P0
        self.assertEqual(pl.intersection(Plane(P0,Vector(1,0,0))),
                         GeometryObjects(Line(Point(0,0,0), Vector(0,1,0))))
        
        self.assertEqual(pl.intersection(Plane(P0,Vector(0,1,0))),
                         GeometryObjects(Line(Point(0,0,0), Vector(-1,0,0))))
        
        self.assertEqual(pl.intersection(Plane(P0,Vector(1,1,0))),
                         GeometryObjects(Line(Point(0,0,0), Vector(-1,1,0))))
        
        self.assertEqual(pl.intersection(Plane(P0,Vector(0,1,1))),
                         GeometryObjects(Line(Point(0,0,0), Vector(-1,0,0))))
        
        # intersecting planes - different P0
        self.assertEqual(pl.intersection(Plane(P0+ Vector(1,0,0),
                                         Vector(1,0,0))),
                         GeometryObjects(Line(Point(1,0,0), Vector(0,1,0))))
        


class Test_Polygon(unittest.TestCase):
    ""
    
    def test___eq__(self):
        ""
        pg=Polygon(Point(0,0),Point(1,0),Point(1,1),Point(0,1))
        self.assertTrue(pg==pg)
        
        pg1=Polygon(Point(0,1),Point(0,0),Point(1,0),Point(1,1))
        self.assertFalse(pg==pg1)
        
        pg2=Polygon(Point(0,0),Point(1,0),Point(0,1))
        self.assertFalse(pg==pg2)
        
        # polygon with hole is equivalent to polygon of same shape without hole
        hole=Polygon(Point(0,0),Point(0.5,0),Point(0.5,0.5),Point(0,0.5))
        pg3=Polygon(Point(0,0),Point(1,0),Point(1,1),Point(0,1),
                    holes=[hole])
        pg4=Polygon(Point(0.5,0),Point(1,0),Point(1,1),Point(0,1),Point(0,0.5),Point(0.5,0.5))
        self.assertFalse(pg3==pg4)
        
    
    def test___init__(self):
        ""
        pg=Polygon(Point(0,0),Point(1,0),Point(1,1),Point(0,1))
        self.assertIsInstance(pg,Polygon)
        self.assertEqual(pg.points,
                         Points(Point(0,0),Point(1,0),Point(1,1),Point(0,1)))
        
        
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
        
        
    def test_coordinates(self):
        ""
        pg=Polygon(Point(0,0),Point(1,0),Point(1,1),Point(0,1))
        #print(pg.coordinates); return
        self.assertEqual(pg.coordinates,
                         (((0, 0), (1, 0), (1, 1), (0, 1)), ()))
        
        pg=Polygon(Point(0,0),Point(1,0),Point(1,1),Point(0,1),
                    holes=[Polygon(Point(0,0),Point(0.5,0),Point(0.5,0.5),Point(0,0.5))])
        #print(pg.coordinates); return
        self.assertEqual(pg.coordinates,
                         (((0, 0), (1, 0), (1, 1), (0, 1)), 
                          (((0, 0), (0.5, 0), (0.5, 0.5), (0, 0.5)),))
                         )
        
        
    def test_difference_polygon_2d(self):
        ""
        # 2D
        pg=Polygon(Point(0,0),Point(1,0),Point(1,1),Point(0,1))
        # no intersection
        pg1=Polygon(Point(0,2),Point(1,2),Point(1,3),Point(0,3))
        #print(pg.difference(pg1)); return
        self.assertEqual(pg.difference(pg1),
                         GeometryObjects(Polygon(Point(0,0),
                                  Point(0,1),
                                  Point(1,1),
                                  Point(1,0)),))
        # point intersection
        pg1=Polygon(Point(1,1),Point(2,1),Point(2,2),Point(1,2))
        #print(pg.difference(pg1)); return
        self.assertEqual(pg.difference(pg1),
                         GeometryObjects(Polygon(Point(1,1),
                                  Point(1,0),
                                  Point(0,0),
                                  Point(0,1)),))
        # full edge intersection
        pg1=Polygon(Point(0,1),Point(1,1),Point(1,2),Point(0,2))
        #print(pg.difference(pg1)); return
        self.assertEqual(pg.difference(pg1),
                         GeometryObjects(Polygon(Point(1,1),
                                  Point(1,0),
                                  Point(0,0),
                                  Point(0,1)),))
        # half edge overlap intersection
        pg1=Polygon(Point(0.5,1),Point(1.5,1),Point(1.5,2),Point(0.5,2))
        #print(pg.difference(pg1)); return
        self.assertEqual(pg.difference(pg1),
                         GeometryObjects(Polygon(Point(1,1),
                                  Point(1,0),
                                  Point(0,0),
                                  Point(0,1),
                                  Point(0.5,1)),))
        # partial internal edge intersection
        pg1=Polygon(Point(0.25,1),Point(0.75,1),Point(0.75,2),Point(0.25,2))
        #print(pg.difference(pg1)); return
        self.assertEqual(pg.difference(pg1),
                         GeometryObjects(Polygon(Point(0.75,1),
                                  Point(1,1),
                                  Point(1,0),
                                  Point(0,0),
                                  Point(0,1),
                                  Point(0.25,1)),))
        # full intersection
        pg1=pg
        #print(pg.difference(pg1)); return
        self.assertEqual(pg.difference(pg1),
                         GeometryObjects())
        # half intersection
        pg1=Polygon(Point(0.5,0),Point(1.5,0),Point(1.5,1),Point(0.5,1))
        #print(pg.difference(pg1)); return
        self.assertEqual(pg.difference(pg1),
                         GeometryObjects(Polygon(Point(0.5,0),
                                  Point(0,0),
                                  Point(0,1),
                                  Point(0.5,1)),))
        # quarter intersection
        pg1=Polygon(Point(0.5,0.5),Point(1.5,0.5),Point(1.5,1.5),Point(0.5,1.5))
        #print(pg.difference(pg1)); return
        self.assertEqual(pg.difference(pg1),
                         GeometryObjects(Polygon(Point(1.0,0.5),
                                  Point(1.0,0.0),
                                  Point(0.0,0.0),
                                  Point(0.0,1.0),
                                  Point(0.5,1.0),
                                  Point(0.5,0.5)),))
        # internal intersection, 2 edges
        pg1=Polygon(Point(0.25,0),Point(0.75,0),Point(0.75,1),Point(0.25,1))
        #print(pg.difference(pg1)); return
        self.assertEqual(pg.difference(pg1),
                         GeometryObjects(Polygon(Point(0.25,0),
                                  Point(0,0),
                                  Point(0,1),
                                  Point(0.25,1)), 
                          Polygon(Point(0.75,1),
                                  Point(1,1),
                                  Point(1,0),
                                  Point(0.75,0))))
        # internal intersection, 1 edges
        pg1=Polygon(Point(0.25,0),Point(0.75,0),Point(0.75,0.5),Point(0.25,0.5))
        #print(pg.difference(pg1)); return
        self.assertEqual(pg.difference(pg1),
                         GeometryObjects(Polygon(Point(0.25,0.0),
                                  Point(0.0,0.0),
                                  Point(0.0,1.0),
                                  Point(1.0,1.0),
                                  Point(1.0,0.0),
                                  Point(0.75,0.0),
                                  Point(0.75,0.5),
                                  Point(0.25,0.5)),))
        
        #
        pg=Polygon(Point(1.0,0.25),Point(1.0,1.0),Point(0.0,1.0),Point(0.0,0.25))
        pg1=Polygon(Point(0.25,0.25),
                    Point(0.75,0.25),
                    Point(0.75,0.75),
                    Point(0.25,0.75))
        #print('---return---\n',pg.difference(pg1)); return
        self.assertEqual(pg.difference(pg1),
                         GeometryObjects(Polygon(Point(0.25,0.25),
                                  Point(0.0,0.25),
                                  Point(0.0,1.0),
                                  Point(1.0,1.0),
                                  Point(1.0,0.25),
                                  Point(0.75,0.25),
                                  Point(0.75,0.75),
                                  Point(0.25,0.75)),))
        
        
        # internal intersection, no edges
        pg=Polygon(Point(0,0),Point(1,0),Point(1,1),Point(0,1))
        pg1=Polygon(Point(0.25,0.25),
                          Point(0.75,0.25),
                          Point(0.75,0.75),
                          Point(0.25,0.75))
        #print('---return---\n',pg.difference(pg1)); return
        self.assertEqual(pg.difference(pg1),
                         GeometryObjects(Polygon(Point(0.0,0.0),
                                  Point(0.0,1.0),
                                  Point(1.0,1.0),
                                  Point(1.0,0.0), 
                                  holes=Polygons(Polygon(Point(0.25,0.25),
                                                         Point(0.75,0.25),
                                                         Point(0.75,0.75),
                                                         Point(0.25,0.75)))),))
    
        # external intersection, no edges
        pg1=Polygon(Point(-1,-1),Point(2,-1),Point(2,2),Point(-1,2))
        #print(pg.difference(pg1)); return
        self.assertEqual(pg.difference(pg1),
                         GeometryObjects())
        
        
    def test_intersection_polygon_2d(self):
        ""
        # concave polygon
        # 2D
        pg=Polygon(Point(0,0),Point(1,0),Point(1,1),Point(0,1))
        # no intersection
        pg1=Polygon(Point(0,2),Point(1,2),Point(1,3),Point(0,3))
        #print(pg.intersection(pg1)); return
        self.assertEqual(pg.intersection(pg1),
                         GeometryObjects())
        # point intersection
        pg1=Polygon(Point(1,1),Point(2,1),Point(2,2),Point(1,2))
        #print(pg.intersection(pg1)); return
        self.assertEqual(pg.intersection(pg1),
                         GeometryObjects(Point(1,1),))
        # full edge intersection
        pg1=Polygon(Point(0,1),Point(1,1),Point(1,2),Point(0,2))
        #print(pg.intersection(pg1)); return
        self.assertEqual(pg.intersection(pg1),
                         GeometryObjects(Polyline(Point(1,1),Point(0,1)),))
        # half edge overlap intersection
        pg1=Polygon(Point(0.5,1),Point(1.5,1),Point(1.5,2),Point(0.5,2))
        #print(pg.intersection(pg1)); return
        self.assertEqual(pg.intersection(pg1),
                         GeometryObjects(Polyline(Point(1,1),Point(0.5,1)),))
        # partial internal edge intersection
        pg1=Polygon(Point(0.25,1),Point(0.75,1),Point(0.75,2),Point(0.25,2))
        #print(pg.intersection(pg1)); return
        self.assertEqual(pg.intersection(pg1),
                         GeometryObjects(Polyline(Point(0.75,1),Point(0.25,1)),))
        # full intersection
        pg1=pg
        #print(pg.intersection(pg1)); return
        self.assertEqual(pg.intersection(pg1),
                         GeometryObjects(Polygon(Point(1,0),
                                  Point(0,0),
                                  Point(0,1),
                                  Point(1,1)),))
        # half intersection
        pg1=Polygon(Point(0.5,0),Point(1.5,0),Point(1.5,1),Point(0.5,1))
        #print(pg.intersection(pg1)); return
        self.assertEqual(pg.intersection(pg1),
                         GeometryObjects(Polygon(Point(1,0),
                                  Point(0.5,0),
                                  Point(0.5,1),
                                  Point(1,1)),))
        # quarter intersection
        pg1=Polygon(Point(0.5,0.5),Point(1.5,0.5),Point(1.5,1.5),Point(0.5,1.5))
        #print(pg.intersection(pg1)); return
        self.assertEqual(pg.intersection(pg1),
                         GeometryObjects(Polygon(Point(0.5,1),
                                  Point(1,1),
                                  Point(1,0.5),
                                  Point(0.5,0.5)),))
        # internal intersection, 2 edges
        pg1=Polygon(Point(0.25,0),Point(0.75,0),Point(0.75,1),Point(0.25,1))
        #print(pg.intersection(pg1)); return
        self.assertEqual(pg.intersection(pg1),
                         GeometryObjects(Polygon(Point(0.75,0.0),
                                  Point(0.25,0.0),
                                  Point(0.25,1.0),
                                  Point(0.75,1.0)),))
    
        # convex polygon
        # 2D
        pg=Polygon(Point(0,0),Point(1,0),Point(0.5,0.5),Point(1,1),Point(0,1))
        
        # 2 point intersection
        pg1=Polygon(Point(1,0),Point(2,0),Point(2,1),Point(1,1))
        #print(pg.intersection(pg1)); return
        self.assertEqual(pg.intersection(pg1),
                         GeometryObjects(Point(1.0,0.0),Point(1.0,1.0)))
        
        # 2 polyline intersection
        pg1=Polygon(Point(1,0),Point(1,1),Point(0.5,0.5))
        #print(pg.intersection(pg1)); return
        self.assertEqual(pg.intersection(pg1),
                         GeometryObjects(Polyline(Point(1.0,0.0),
                                   Point(0.5,0.5)),
                          Polyline(Point(0.5,0.5),
                                   Point(1.0,1.0))))
        
        # 2 polygon intersection
        pg1=Polygon(Point(0.5,0),Point(1,0),Point(1,1),Point(0.5,1))
        #print(pg.intersection(pg1)); return
        self.assertEqual(pg.intersection(pg1),
                         GeometryObjects(Polygon(Point(1.0,0.0),
                                  Point(0.5,0.0),
                                  Point(0.5,0.5)),
                          Polygon(Point(1.0,1.0),
                                  Point(0.5,0.5),
                                  Point(0.5,1.0))))
        
        # point and polyline intersection
        pg=Polygon(Point(0,0),Point(1,0),Point(0.5,0.5),
                   Point(1,1),Point(1,2),Point(0,2))
        pg1=Polygon(Point(1,0),Point(2,0),Point(2,2),Point(1,2))
        #print(pg.intersection(pg1)); return
        self.assertEqual(pg.intersection(pg1),
                         GeometryObjects(Point(1.0,0.0), 
                          Polyline(Point(1.0,1.0),
                                   Point(1.0,2.0))))
        
        
    def test_intersection_polygon_3d(self):
        ""
        pg=Polygon(Point(0,0,0),Point(1,0,0),Point(1,1,0),Point(0,1,0))
        # in-plane half intersection
        pg1=Polygon(Point(0.5,0,0),Point(1.5,0,0),Point(1.5,1,0),Point(0.5,1,0))
        #print(pg.intersection(pg1)); return
        self.assertEqual(pg.intersection(pg1),
                         (Polygon(Point(1,0,0),
                                  Point(0.5,0,0),
                                  Point(0.5,1,0),
                                  Point(1,1,0)),))
        # parallel plane no intersection
        pg1=Polygon(Point(0,0,1),Point(1,0,1),Point(1,1,1),Point(0,1,1))
        #print(pg.intersection(pg1)); return
        self.assertEqual(pg.intersection(pg1),
                         tuple())
        # skew plane point intersection
        pg1=Polygon(Point(0,0,0),Point(1,0,1),Point(0,0,1))
        #print(pg.intersection(pg1)); return
        self.assertEqual(pg.intersection(pg1),
                         (Point(0,0,0),))
        # skew plane full edge intersection
        pg1=Polygon(Point(0,0,0),Point(1,0,0),Point(0,0,1))
        #print(pg.intersection(pg1)); return
        self.assertEqual(pg.intersection(pg1),
                         (Polyline(Point(0,0,0),Point(1,0,0)),))
        # skew plane edge-t0-edge internal intersection
        pg1=Polygon(Point(0,0.5,0),Point(1,0.5,0),Point(0,0.5,1))
        #print(pg.intersection(pg1)); return
        self.assertEqual(pg.intersection(pg1),
                         (Polyline(Point(0,0.5,0),Point(1,0.5,0)),))
        # skew plane internal intersection
        pg1=Polygon(Point(0.25,0.5,0),Point(0.75,0.5,0),Point(0.25,0.5,1))
        #print(pg.intersection(pg1)); return
        self.assertEqual(pg.intersection(pg1),
                         (Polyline(Point(0.25,0.5,0),Point(0.75,0.5,0)),))
        # skew plane in-out internal intersection
        pg1=Polygon(Point(0.5,0.5,0),Point(1.5,0.5,0),Point(0.5,0.5,1))
        #print(pg.intersection(pg1)); return
        self.assertEqual(pg.intersection(pg1),
                         (Polyline(Point(0.5,0.5,0),Point(1,0.5,0)),))
        # skew plane point intersection
        pg1=Polygon(Point(1,0.5,0),Point(2,0.5,0),Point(1,0.5,1))
        #print(pg.intersection(pg1)); return
        self.assertEqual(pg.intersection(pg1),
                         (Point(1,0.5,0),))       
        
        
    def test_plot(self):
        ""
        return
        pg=Polygon(Point(0,0),Point(1,0),Point(1,1),Point(0,1))
        pg.plot()
        
        pg=Polygon(Point(0,0,0),Point(1,0,0),Point(1,1,0),Point(0,1,0))
        pg.plot()
        
        
        
    def test_polygons(self):
        ""
        pg=Polygon(Point(0,0),Point(1,0),Point(1,1),Point(0,1))
        #print(pg.polygons); return
        self.assertEqual(pg.polygons,
                         Polygons(Polygon(Point(0.0,0.0),
                                          Point(1.0,0.0),
                                          Point(1.0,1.0),
                                          Point(0.0,1.0))))
        
        hole=Polygon(Point(0,0),Point(0.5,0),Point(0.5,0.5),Point(0,0.5))
        pg=Polygon(Point(0,0),Point(1,0),Point(1,1),Point(0,1),
                   holes=[hole])
        #print(pg.polygons); return
        self.assertEqual(pg.polygons,
                         Polygons(Polygon(Point(1.0, 0.0),
                                          Point(0.5, 0.0),
                                          Point(0.5, 0.5),
                                          Point(0.0, 0.5),
                                          Point(0.0, 1.0),
                                          Point(1.0, 1.0))))
        
        hole=Polygon(Point(0.25,0.25),Point(0.75,0.25),Point(0.75,0.75),Point(0.25,0.75))
        pg=Polygon(Point(0,0),Point(1,0),Point(1,1),Point(0,1),
                   holes=[hole])
        #print(pg.polygons); return
        self.assertEqual(pg.polygons,
                         Polygons(Polygon(Point(1.0, 0.25),
                                          Point(1.0, 0.0),
                                          Point(0.0, 0.0),
                                          Point(0.0, 0.25),
                                          Point(0.25, 0.25),
                                          Point(0.75, 0.25)), 
                                  Polygon(Point(0.0, 0.25),
                                          Point(0.0, 1.0),
                                          Point(1.0, 1.0),
                                          Point(1.0, 0.25),
                                          Point(0.75, 0.25),
                                          Point(0.75, 0.75),
                                          Point(0.25, 0.75),
                                          Point(0.25, 0.25))))
        
        
        
        
    def test_split(self):
        ""
        # 2d
        pg=Polygon(Point(0,0),Point(1,0),Point(1,1),Point(0,1))
        pl=Polyline(Point(0.5,0),Point(0.5,1))
        self.assertEqual(pg.split(pl),
                         GeometryObjects(Polygon(Point(0.5, 0.0),
                                                 Point(0.0, 0.0),
                                                 Point(0.0, 1.0),
                                                 Point(0.5, 1.0)), 
                                         Polygon(Point(0.5, 1.0),
                                                 Point(1.0, 1.0),
                                                 Point(1.0, 0.0),
                                                 Point(0.5, 0.0))))
        
        pg=Polygon(Point(0,0),Point(1,0),Point(1,1),Point(0,1))
        l=Line(Point(0.5,0),Vector(0,1))
        self.assertEqual(pg.split(l),
                         GeometryObjects(Polygon(Point(0.5, 0.0),
                                                 Point(0.0, 0.0),
                                                 Point(0.0, 1.0),
                                                 Point(0.5, 1.0)), 
                                         Polygon(Point(0.5, 1.0),
                                                 Point(1.0, 1.0),
                                                 Point(1.0, 0.0),
                                                 Point(0.5, 0.0))))
        
        # 3d
        pg=Polygon(Point(0,0,1),Point(1,0,1),Point(1,1,1),Point(0,1,1))
        l=Line(Point(0.5,0,1),Vector(0,1,0))
        #print(pg.split(l)); return
        self.assertEqual(pg.split(l),
                         GeometryObjects(Polygon(Point(0.5, 0.0, 1.0),
                                                 Point(0.0, 0.0, 1.0),
                                                 Point(0.0, 1.0, 1.0),
                                                 Point(0.5, 1.0, 1.0)), 
                                         Polygon(Point(0.5, 1.0, 1.0),
                                                 Point(1.0, 1.0, 1.0),
                                                 Point(1.0, 0.0, 1.0),
                                                 Point(0.5, 0.0, 1.0))))
        
        
        
        
    def test_triangles(self):
        ""
        # convex polygon
        pg=Polygon(Point(0,0),Point(1,0),Point(1,1),Point(0,1))
        #print(pg.triangles); return
        self.assertEqual(pg.triangles,
                         Polygons(Polygon(Point(0,1),
                                          Point(0,0),
                                          Point(1,0)), 
                                   Polygon(Point(1,0),
                                           Point(1,1),
                                           Point(0,1))))
        # concave polygon
        pg=Polygon(Point(0,0),
                         Point(2,0),
                         Point(1,1),
                         Point(2,2),
                         Point(0,2))
        #print(pg.triangles); return
        self.assertEqual(pg.triangles,
                         Polygons(Polygon(Point(0.0,2.0),
                                          Point(0.0,0.0),
                                          Point(1.0,1.0)), 
                                   Polygon(Point(2.0,0.0),
                                           Point(1.0,1.0),
                                           Point(0.0,0.0)), 
                                   Polygon(Point(1.0,1.0),
                                           Point(2.0,2.0),
                                           Point(0.0,2.0))))
        
        #return
        # example
        #print('test')
        pg=Polygon(Point(221.7423, -84.20669, 6.0),
                   Point(221.7423, -53.63377, 6.0),
                   Point(221.7423, -53.63377, 14.0),
                   Point(221.7423, -54.0921, 14.0),
                   Point(221.7423, -54.0921, 9.02132),
                   Point(221.7423, -60.6546, 9.02132),
                   Point(221.7423, -60.6546, 14.0),
                   Point(221.7423, -63.91502, 14.0),
                   Point(221.7423, -63.91502, 9.02132),
                   Point(221.7423, -70.83169, 9.02132),
                   Point(221.7423, -70.83169, 14.0),
                   Point(221.7423, -73.91502, 14.0),
                   Point(221.7423, -73.91502, 9.02132),
                   Point(221.7423, -80.83169, 9.02132),
                   Point(221.7423, -80.83169, 14.0),
                   Point(221.7423, -84.20669, 14.0), 
           holes=Polygons(Polygon(Point(221.7423, -80.68064, 8.969236),
                                  Point(221.7423, -74.06606, 8.969236),
                                  Point(221.7423, -74.06606, 9.02132),
                                  Point(221.7423, -80.68064, 9.02132)), 
                          Polygon(Point(221.7423, -70.68064, 8.969236),
                                  Point(221.7423, -64.06606, 8.969236),
                                  Point(221.7423, -64.06606, 9.02132),
                                  Point(221.7423, -70.68064, 9.02132)), 
                          Polygon(Point(221.7423, -60.68064, 8.969236),
                                  Point(221.7423, -54.06606, 8.969236),
                                  Point(221.7423, -54.06606, 14.0),
                                  Point(221.7423, -54.0921, 14.0),
                                  Point(221.7423, -54.0921, 9.02132),
                                  Point(221.7423, -60.6546, 9.02132),
                                  Point(221.7423, -60.6546, 14.0),
                                  Point(221.7423, -60.68064, 14.0))))
        return
        pg.plot(set_lims=True)
        pg.triangles.plot(set_lims=True)
        print(pg.triangles); return
        return
        pg.polylines[0].plot()
        pg.holes[0].polylines.plot()
        pg.holes[1].polylines.plot()
        pg.holes[2].polylines.plot()
        
        print(pg.holes[0].reverse.area)
        print(pg.holes[1].area)
        print(pg.holes[2].area)
        
        
        print(pg.holes[0].intersection(pg.exterior)[0].area)
        print(pg.holes[1].intersection(pg.exterior)[0].area)
        print(pg.holes[2].intersection(pg.exterior)[0].area)
        
        return
        
        
        #return
        
        pg=Polygon(Point(220.7528, -63.91502, 9.02132),
                   Point(221.7423, -63.91502, 9.02132),
                   Point(221.7423, -63.91502, 14.0),
                   Point(220.7528, -63.91502, 14.0))
        #print(pg.triangles); return
        
        pg=Polygon(Point(221.7423, -84.20669, 6.0),Point(221.7423, -53.63377, 6.0),Point(221.7423, -53.63377, 14.0),Point(221.7423, -54.0921, 14.0),Point(221.7423, -54.0921, 9.02132),Point(221.7423, -60.6546, 9.02132),Point(221.7423, -60.6546, 14.0),Point(221.7423, -63.91502, 14.0),Point(221.7423, -63.91502, 9.02132),Point(221.7423, -70.83169, 9.02132),Point(221.7423, -70.83169, 14.0),Point(221.7423, -73.91502, 14.0),Point(221.7423, -73.91502, 9.02132),Point(221.7423, -80.83169, 9.02132),Point(221.7423, -80.83169, 14.0),Point(221.7423, -84.20669, 14.0), holes=Polygons(Polygon(Point(221.7423, -80.68064, 8.969236),Point(221.7423, -74.06606, 8.969236),Point(221.7423, -74.06606, 9.02132),Point(221.7423, -80.68064, 9.02132)), Polygon(Point(221.7423, -70.68064, 8.969236),Point(221.7423, -64.06606, 8.969236),Point(221.7423, -64.06606, 9.02132),Point(221.7423, -70.68064, 9.02132)), Polygon(Point(221.7423, -60.68064, 8.969236),Point(221.7423, -54.06606, 8.969236),Point(221.7423, -54.06606, 14.0),Point(221.7423, -54.0921, 14.0),Point(221.7423, -54.0921, 9.02132),Point(221.7423, -60.6546, 9.02132),Point(221.7423, -60.6546, 14.0),Point(221.7423, -60.68064, 14.0))))
        print(pg.triangles); return
        
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
        pgs=Polygons(Polygon(Point(0,0),Point(1,0),Point(1,1)),
                     Polygon(Point(2,0),Point(1,0),Point(1,1))
                     )
        #print(pgs._shapely); return
        self.assertEqual(pgs._shapely,
            shapely.geometry.MultiPolygon([shapely.geometry.Polygon(((0,0),
                                                                     (1,0),
                                                                     (1,1))),
                                           shapely.geometry.Polygon(((2,0),
                                                                     (1,0),
                                                                     (1,1)))
                                           ]))
        
        
    def test_bounds(self):
        ""
        pgs=Polygons(Polygon(Point(0,0),Point(1,0),Point(1,1)),
                     Polygon(Point(2,0),Point(2,1),Point(1,0))
                     )
        self.assertEqual(pgs.bounds,
                         (0.0, 0.0, 2.0, 1.0))
        
        pgs=Polygons(Polygon(Point(0,0,0),Point(1,0,0),Point(1,1,0)),
                     Polygon(Point(0,0,1),Point(0,1,1),Point(1,1,1))
                     )
        self.assertEqual(pgs.bounds,
                         (0.0, 0.0, 0.0, 1.0, 1.0, 1.0))
        
        
    def test_plot(self):
        ""
        return
        pgs=Polygons(Polygon(Point(0,0),Point(1,0),Point(1,1)),
                     Polygon(Point(2,0),Point(2,1),Point(1,0))
                     )
        pgs.plot()
        
        pgs=Polygons(Polygon(Point(0,0,0),Point(1,0,0),Point(1,1,0)),
                     Polygon(Point(0,0,1),Point(0,1,1),Point(1,1,1))
                     )
        pgs.plot()
        
        
class Test_Tetrahedron(unittest.TestCase):
    ""
    
    def test_tetrahedron_from_points(self):
        ""
        t=tetrahedron_from_points(Point(0,0,0),Point(1,1,0),Point(0,1,0),Point(0,1,1))
        self.assertIsInstance(t,
                              Tetrahedron)
        self.assertEqual(t.polygons,
                         Polygons(Polygon(Point(0,1,0),Point(1,1,0),Point(0,0,0)),
                                  Polygon(Point(0,0,0),Point(1,1,0),Point(0,1,1)),
                                  Polygon(Point(0,1,1),Point(0,1,0),Point(0,0,0)),
                                  Polygon(Point(1,1,0),Point(0,1,0),Point(0,1,1))))
        
        
class Test_ExtrudedPolyhedron(unittest.TestCase):
    ""
    
    def test___init__(self):
        ""
        ep=ExtrudedPolyhedron(Polygon(Point(0,0,0),
                                      Point(1,0,0),
                                      Point(1,1,0),
                                      Point(0,1,0)),
                              Vector(0,0,1))
        self.assertEqual(ep.polygons,
                         Polygons(Polygon(Point(0,1,0),
                                            Point(1,1,0),
                                            Point(1,0,0),
                                            Point(0,0,0)),
                                    Polygon(Point(0,0,1),
                                            Point(1,0,1),
                                            Point(1,1,1),
                                            Point(0,1,1)),
                                    Polygon(Point(0,1,1),
                                            Point(1,1,1),
                                            Point(1,1,0),
                                            Point(0,1,0)),
                                    Polygon(Point(1,1,1),
                                            Point(1,0,1),
                                            Point(1,0,0),
                                            Point(1,1,0)),
                                    Polygon(Point(1,0,1),
                                            Point(0,0,1),
                                            Point(0,0,0),
                                            Point(1,0,0)),
                                    Polygon(Point(0,0,1),
                                            Point(0,1,1),
                                            Point(0,1,0),
                                            Point(0,0,0))))
        self.assertEqual(len(ep.base_polygon.triangles),
                         2)
        self.assertEqual(len(ep.tetrahedrons),
                         6)
        
        
        
        
if __name__=='__main__':
    
    unittest.main()
    #unittest.main(Test_Polygon,'test_polygons')
    #unittest.main(Test_Polygon,'test_split')
    #unittest.main(Test_Polygon,'test_triangles')
    #unittest.main(Test_Polygons,'test__shapely')
        