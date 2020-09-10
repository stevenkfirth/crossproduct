# -*- coding: utf-8 -*-

import unittest
from crossproduct import Point3D, Vector3D, Line3D, Plane3D, Halfline3D, \
    Segment3D, PlaneVolume3D, Polyline3D, Points, Polylines


class Test_PlaneVolume3D(unittest.TestCase):
    """
    P0=Point3D(0,0,0)
    N=Vector3D(0,0,1)
    """
    
    def test___init__(self):
        ""
        pl=PlaneVolume3D(P0,N)
        self.assertIsInstance(pl,
                              PlaneVolume3D)
        self.assertEqual(pl.P0,
                         P0)
        self.assertEqual(pl.N,
                         N)
        
        
    def test___contains__(self):
        ""
        pl=PlaneVolume3D(P0,N)
        
        # point
        self.assertTrue(P0 in pl)
        self.assertTrue(Point3D(10,10,0) in pl)
        self.assertFalse(Point3D(0,0,1) in pl)
        self.assertTrue(Point3D(0,0,-1) in pl)
        
        # line
        self.assertTrue(Line3D(P0,Vector3D(1,0,0)) in pl)
        self.assertFalse(Line3D(P0+N,Vector3D(1,0,0)) in pl)
        self.assertTrue(Line3D(P0-N,Vector3D(1,0,0)) in pl)
        self.assertFalse(Line3D(P0,N) in pl)
        
        # polyline
        self.assertFalse(Polyline3D(P0,P0+N,Point3D(1,0,0)+N) in pl)
        self.assertTrue(Polyline3D(P0,P0-N,Point3D(1,0,0)-N,Point3D(1,0,0)) in pl)
    
    
    def test___eq__(self):
        ""
        pl=PlaneVolume3D(P0,N)
        self.assertTrue(pl==pl)
        self.assertFalse(pl==PlaneVolume3D(P0,N.opposite))
        self.assertFalse(pl==PlaneVolume3D(P0,Vector3D(1,0,0)))
    
    
    def test___repr__(self):
        ""
        pl=PlaneVolume3D(P0,N)
        self.assertEqual(str(pl),
                         'PlaneVolume3D(Point3D(0,0,0), Vector3D(0,0,1))')
        
        
    def test__intersect_line_skew(self):
        ""
        pl=PlaneVolume3D(P0,N)
        
        # perpendicular line passing through P0
        self.assertEqual(pl._intersect_line_skew(Line3D(P0,
                                                        N)),
                         Halfline3D(Point3D(0.0,0.0,0.0), 
                                    Vector3D(0,0,-1)))
        self.assertEqual(pl._intersect_line_skew(Line3D(P0+N,
                                                        N)),
                         Halfline3D(Point3D(0.0,0.0,0.0), 
                                    Vector3D(0,0,-1)))
        
        # non perpendicular line not passing through P0
        self.assertEqual(pl._intersect_line_skew(Line3D(Point3D(0,0,1),
                                                        Vector3D(1,0,-1))),
                         Halfline3D(Point3D(1.0,0.0,0.0), 
                                    Vector3D(1,0,-1)))
            
        
    def test_intersect_polyline(self):
        ""
        pv=PlaneVolume3D(P0,N)
        
        # single point intersection
        pl=Polyline3D(P0,P0+N,Point3D(1,0,0)+N)
        self.assertEqual(pv.intersect_polyline(pl),
                         (Points(Point3D(0,0,0)), 
                          Polylines()))
        
        # two point intersection
        pl=Polyline3D(P0,P0+N,Point3D(1,0,0)+N,Point3D(1,0,0))
        self.assertEqual(pv.intersect_polyline(pl),
                         (Points(Point3D(0,0,0),
                                 Point3D(1,0,0)), 
                          Polylines()))
        
        # full intersection
        pl=Polyline3D(P0,P0-N,Point3D(1,0,0)-N,Point3D(1,0,0))
        self.assertEqual(pv.intersect_polyline(pl),
                         (Points(), 
                          Polylines(pl)))
        
            
    def test_intersect_segment(self):
        ""
        pl=PlaneVolume3D(P0,N)
        
        # segment in plane of plane volume
        self.assertEqual(pl.intersect_segment(Segment3D(P0,
                                                        Point3D(1,0,0))),
                          Segment3D(P0,
                                    Point3D(1,0,0)))
            
        # parallel segment not in plane volume
        self.assertEqual(pl.intersect_segment(Segment3D(P0+N,
                                                        Point3D(1,0,0)+N)),
                          None)
            
        # perpendicular segment with start point at P0 and end point outside plane volume
        self.assertEqual(pl.intersect_segment(Segment3D(P0,
                                                        P0+N)),
                          P0)
        
        # perpendicular segment with end point at P0 and start point outside plane volume
        self.assertEqual(pl.intersect_segment(Segment3D(P0+N,
                                                        P0)),
                          P0)
        
        # perpendicular segment fully intersecting plane volume
        s=Segment3D(P0-N,
                    P0-N*2)
        self.assertEqual(pl.intersect_segment(s),
                         s)
            
        # parallel segment fully intersecting plane volume
        s=Segment3D(P0-N,
                    Point3D(1,0,0)-N)
        self.assertEqual(pl.intersect_segment(s),
                         s)
        
        # perpendicular segment parially intersecting plane volume
        self.assertEqual(pl.intersect_segment(Segment3D(P0+N,
                                                        P0-N)),
                         Segment3D(P0,
                                   P0-N))
        
        
    def test_plane(self):
        ""
        pl=PlaneVolume3D(P0,N)
        
        self.assertEqual(pl.plane,
                         Plane3D(P0,N))
    
    
if __name__=='__main__':
    
    P0=Point3D(0,0,0)
    N=Vector3D(0,0,1)
    unittest.main(Test_PlaneVolume3D())
    
    
    