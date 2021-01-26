# -*- coding: utf-8 -*-

import unittest
from crossproduct import Point, Vector, Line, Plane, Halfline, Segment


class Test_Plane(unittest.TestCase):
    """
    P0=Point(0,0,0)
    N=Vector(0,0,1)
    """
    
    def test___init__(self):
        ""
        pl=Plane(P0,N)
        self.assertIsInstance(pl,
                              Plane)
        self.assertEqual(pl.P0,
                         P0)
        self.assertEqual(pl.N,
                         N)
        
        
    def test___contains__(self):
        ""
        pl=Plane(P0,N)
        
        # point
        self.assertTrue(pl.contains(P0))
        self.assertTrue(pl.contains(Point(10,10,0)))
        self.assertFalse(pl.contains(Point(0,0,1)))
        
        # line
        self.assertTrue(pl.contains(Line(P0,Vector(1,0,0))))
        self.assertFalse(pl.contains(Line(P0+N,Vector(1,0,0))))
        self.assertFalse(pl.contains(Line(P0,N)))
        
        # halfline
        # segment
        # polygon
    
    
    def test___eq__(self):
        ""
        pl=Plane(P0,N)
        self.assertTrue(pl==pl)
        self.assertTrue(pl==Plane(P0,N.opposite))
        self.assertFalse(pl==Plane(P0,Vector(1,0,0)))
    
    
    def test___repr__(self):
        ""
        pl=Plane(P0,N)
        self.assertEqual(str(pl),
                         'Plane(Point(0.0,0.0,0.0), Vector(0.0,0.0,1.0))')
        
        
    def test_distance_to_point(self):
        ""
        pl=Plane(P0,N)
        self.assertEqual(pl.distance_to_point(Point(0,0,1)),
                         1)
        self.assertEqual(pl.distance_to_point(Point(0,0,-1)),
                         1)
        
        
    def test_intersect_halfline(self):
        ""
        pl=Plane(P0,N)
        
        # halfline in plane
        self.assertEqual(pl.intersect_halfline(Halfline(P0,
                                                          Vector(1,0,0))),
                         Halfline(P0,
                                    Vector(1,0,0)))
            
        # parallel halfline not in plane
        self.assertEqual(pl.intersect_halfline(Halfline(P0+N,
                                                          Vector(1,0,0))),
                         None)
            
        # perpendicular halfline passing through P0
        self.assertEqual(pl.intersect_halfline(Halfline(P0,
                                                          N)),
                         P0)
        self.assertEqual(pl.intersect_halfline(Halfline(P0+N,
                                                          N.opposite)),
                         P0)
        
        # perpendicular line not passing through plane
        self.assertEqual(pl.intersect_halfline(Halfline(P0+N,
                                                          N)),
                         None)
        
        
    def test_intersect_line(self):
        ""
        pl=Plane(P0,N)
        
        # line in plane
        self.assertEqual(pl.intersect_line(Line(P0,
                                                  Vector(1,0,0))),
                         Line(P0,
                                Vector(1,0,0)))
            
        # parallel line not in plane
        self.assertEqual(pl.intersect_line(Line(P0+N,
                                                  Vector(1,0,0))),
                         None)
            
        
        # perpendicular line passing through P0
        self.assertEqual(pl.intersect_line(Line(P0,
                                                  N)),
                         P0)
        self.assertEqual(pl.intersect_line(Line(P0+N,
                                                  N)),
                         P0)
        
        # non perpendicular line not passing through P0
        self.assertEqual(pl.intersect_line(Line(Point(0,0,1),
                                                  Vector(1,0,-1))),
                         Point(1,0,0))
        
            
    def test_intersect_segment(self):
        ""
        pl=Plane(P0,N)
        
        # segment in plane
        self.assertEqual(pl.intersect_segment(Segment(P0,
                                                        Point(1,0,0))),
                         Segment(P0,
                                   Point(1,0,0)))
            
        # parallel segment not in plane
        self.assertEqual(pl.intersect_segment(Segment(P0+N,
                                                        Point(1,0,0)+N)),
                         None)
            
        # perpendicular segment passing through P0
        self.assertEqual(pl.intersect_segment(Segment(P0,
                                                        P0+N)),
                         P0)
        self.assertEqual(pl.intersect_segment(Segment(P0-N,
                                                        P0)),
                         P0)
            

        # perpendicular segment not passing through plane
        self.assertEqual(pl.intersect_segment(Segment(P0+N,
                                                        P0+N*2)),
                         None)
        self.assertEqual(pl.intersect_segment(Segment(P0-N,
                                                        P0-N*2)),
                         None)
            
    
    def test__intersect_line_skew(self):
        ""
        pl=Plane(P0,N)
        
        # perpendicular line passing through P0
        self.assertEqual(pl._intersect_line_skew(Line(P0,
                                                        N)),
                         P0)
        self.assertEqual(pl._intersect_line_skew(Line(P0+N,
                                                        N)),
                         P0)
        
        # non perpendicular line not passing through P0
        self.assertEqual(pl._intersect_line_skew(Line(Point(0,0,1),
                                                        Vector(1,0,-1))),
                         Point(1,0,0))
            
            
    def test_intersect_plane(self):
        ""
        pl=Plane(P0,N)
        
        # coplanar plane
        self.assertEqual(pl.intersect_plane(pl),
                         pl)
        
        # parallel, non-coplanar planes
        self.assertEqual(pl.intersect_plane(Plane(P0+N,
                                                    N)),
                         None)
        
        # intersecting planes - same P0
        self.assertEqual(pl.intersect_plane(Plane(P0,
                                                    Vector(1,0,0))),
                         Line(Point(0,0,0), Vector(0,1,0)))
        
        self.assertEqual(pl.intersect_plane(Plane(P0,
                                                    Vector(0,1,0))),
                         Line(Point(0,0,0), Vector(1,0,0)))
        
        self.assertEqual(pl.intersect_plane(Plane(P0,
                                                    Vector(1,1,0))),
                         Line(Point(0,0,0), Vector(-1,1,0)))
        
        self.assertEqual(pl.intersect_plane(Plane(P0,
                                                    Vector(0,1,1))),
                         Line(Point(0,0,0), Vector(1,0,0)))
        
        # intersecting planes - different P0
        self.assertEqual(pl.intersect_plane(Plane(P0+ Vector(1,0,0),
                                                    Vector(1,0,0))),
                         Line(Point(1,0,0), Vector(0,1,0)))
        
        
    def test_plot(self):
        ""
        P0=Point(0,0,0)
        N=Vector(1,0,0)
        pl=Plane(P0,N)
        import matplotlib.pyplot as plt
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        pl.plot(ax)
        
        
    def test_point_xy(self):
        ""
        P0=Point(0,0,10)
        N=Vector(0,0,1)
        pl=Plane(P0,N)
        
        self.assertEqual(pl.point_xy(1,1),
                         Point(1,1,10))
        
        P0=Point(0,0,0)
        N=Vector(0,1,0)
        pl=Plane(P0,N)
        self.assertRaises(ValueError,
                          pl.point_xy,1,1)
        
        #print(pl.point_xy(0,0))
        
        
        
        
        
        
    def test_signed_distance_to_point(self):
        ""
        pl=Plane(P0,N)
        self.assertEqual(pl.signed_distance_to_point(Point(0,0,1)),
                         1)
        self.assertEqual(pl.signed_distance_to_point(Point(0,0,-1)),
                         -1)



class Test_Plane3D(unittest.TestCase):
    """
    P0=Point3D(0,0,0)
    N=Vector3D(0,0,1)
    """
    
    def test___init__(self):
        ""
        pl=Plane3D(P0,N)
        self.assertIsInstance(pl,
                              Plane3D)
        self.assertEqual(pl.P0,
                         P0)
        self.assertEqual(pl.N,
                         N)
        
        
    def test___contains__(self):
        ""
        pl=Plane3D(P0,N)
        
        # point
        self.assertTrue(P0 in pl)
        self.assertTrue(Point3D(10,10,0) in pl)
        self.assertFalse(Point3D(0,0,1) in pl)
        
        # line
        self.assertTrue(Line3D(P0,Vector3D(1,0,0)) in pl)
        self.assertFalse(Line3D(P0+N,Vector3D(1,0,0)) in pl)
        self.assertFalse(Line3D(P0,N) in pl)
        
        # halfline
        # segment
        # polygon
    
    
    def test___eq__(self):
        ""
        pl=Plane3D(P0,N)
        self.assertTrue(pl==pl)
        self.assertTrue(pl==Plane3D(P0,N.opposite))
        self.assertFalse(pl==Plane3D(P0,Vector3D(1,0,0)))
    
    
    def test___repr__(self):
        ""
        pl=Plane3D(P0,N)
        self.assertEqual(str(pl),
                         'Plane3D(Point3D(0,0,0), Vector3D(0,0,1))')
        
        
    def test_distance_to_point(self):
        ""
        pl=Plane3D(P0,N)
        self.assertEqual(pl.distance_to_point(Point3D(0,0,1)),
                         1)
        self.assertEqual(pl.distance_to_point(Point3D(0,0,-1)),
                         1)
        
        
    def test_intersect_halfline(self):
        ""
        pl=Plane3D(P0,N)
        
        # halfline in plane
        self.assertEqual(pl.intersect_halfline(Halfline3D(P0,
                                                          Vector3D(1,0,0))),
                         Halfline3D(P0,
                                    Vector3D(1,0,0)))
            
        # parallel halfline not in plane
        self.assertEqual(pl.intersect_halfline(Halfline3D(P0+N,
                                                          Vector3D(1,0,0))),
                         None)
            
        # perpendicular halfline passing through P0
        self.assertEqual(pl.intersect_halfline(Halfline3D(P0,
                                                          N)),
                         P0)
        self.assertEqual(pl.intersect_halfline(Halfline3D(P0+N,
                                                          N.opposite)),
                         P0)
        
        # perpendicular line not passing through plane
        self.assertEqual(pl.intersect_halfline(Halfline3D(P0+N,
                                                          N)),
                         None)
        
        
    def test_intersect_line(self):
        ""
        pl=Plane3D(P0,N)
        
        # line in plane
        self.assertEqual(pl.intersect_line(Line3D(P0,
                                                  Vector3D(1,0,0))),
                         Line3D(P0,
                                Vector3D(1,0,0)))
            
        # parallel line not in plane
        self.assertEqual(pl.intersect_line(Line3D(P0+N,
                                                  Vector3D(1,0,0))),
                         None)
            
        
        # perpendicular line passing through P0
        self.assertEqual(pl.intersect_line(Line3D(P0,
                                                  N)),
                         P0)
        self.assertEqual(pl.intersect_line(Line3D(P0+N,
                                                  N)),
                         P0)
        
        # non perpendicular line not passing through P0
        self.assertEqual(pl.intersect_line(Line3D(Point3D(0,0,1),
                                                  Vector3D(1,0,-1))),
                         Point3D(1,0,0))
        
            
    def test_intersect_segment(self):
        ""
        pl=Plane3D(P0,N)
        
        # segment in plane
        self.assertEqual(pl.intersect_segment(Segment3D(P0,
                                                        Point3D(1,0,0))),
                         Segment3D(P0,
                                   Point3D(1,0,0)))
            
        # parallel segment not in plane
        self.assertEqual(pl.intersect_segment(Segment3D(P0+N,
                                                        Point3D(1,0,0)+N)),
                         None)
            
        # perpendicular segment passing through P0
        self.assertEqual(pl.intersect_segment(Segment3D(P0,
                                                        P0+N)),
                         P0)
        self.assertEqual(pl.intersect_segment(Segment3D(P0-N,
                                                        P0)),
                         P0)
            

        # perpendicular segment not passing through plane
        self.assertEqual(pl.intersect_segment(Segment3D(P0+N,
                                                        P0+N*2)),
                         None)
        self.assertEqual(pl.intersect_segment(Segment3D(P0-N,
                                                        P0-N*2)),
                         None)
            
    
    def test__intersect_line_skew(self):
        ""
        pl=Plane3D(P0,N)
        
        # perpendicular line passing through P0
        self.assertEqual(pl._intersect_line_skew(Line3D(P0,
                                                        N)),
                         P0)
        self.assertEqual(pl._intersect_line_skew(Line3D(P0+N,
                                                        N)),
                         P0)
        
        # non perpendicular line not passing through P0
        self.assertEqual(pl._intersect_line_skew(Line3D(Point3D(0,0,1),
                                                        Vector3D(1,0,-1))),
                         Point3D(1,0,0))
            
            
    def test_intersect_plane(self):
        ""
        pl=Plane3D(P0,N)
        
        # coplanar plane
        self.assertEqual(pl.intersect_plane(pl),
                         pl)
        
        # parallel, non-coplanar planes
        self.assertEqual(pl.intersect_plane(Plane3D(P0+N,
                                                    N)),
                         None)
        
        # intersecting planes - same P0
        self.assertEqual(pl.intersect_plane(Plane3D(P0,
                                                    Vector3D(1,0,0))),
                         Line3D(Point3D(0,0,0), Vector3D(0,1,0)))
        
        self.assertEqual(pl.intersect_plane(Plane3D(P0,
                                                    Vector3D(0,1,0))),
                         Line3D(Point3D(0,0,0), Vector3D(1,0,0)))
        
        self.assertEqual(pl.intersect_plane(Plane3D(P0,
                                                    Vector3D(1,1,0))),
                         Line3D(Point3D(0,0,0), Vector3D(-1,1,0)))
        
        self.assertEqual(pl.intersect_plane(Plane3D(P0,
                                                    Vector3D(0,1,1))),
                         Line3D(Point3D(0,0,0), Vector3D(1,0,0)))
        
        # intersecting planes - different P0
        self.assertEqual(pl.intersect_plane(Plane3D(P0+ Vector3D(1,0,0),
                                                    Vector3D(1,0,0))),
                         Line3D(Point3D(1,0,0), Vector3D(0,1,0)))
        
        
        
    def test_point_xy(self):
        ""
        P0=Point3D(0,0,10)
        N=Vector3D(0,0,1)
        pl=Plane3D(P0,N)
        
        self.assertEqual(pl.point_xy(1,1),
                         Point3D(1,1,10))
        
        
    def test_signed_distance_to_point(self):
        ""
        pl=Plane3D(P0,N)
        self.assertEqual(pl.signed_distance_to_point(Point3D(0,0,1)),
                         1)
        self.assertEqual(pl.signed_distance_to_point(Point3D(0,0,-1)),
                         -1)
        
    
if __name__=='__main__':
    
    P0=Point(0,0,0)
    N=Vector(0,0,1)
    unittest.main(Test_Plane())
    #unittest.main(Test_Plane3D())
    
    
    