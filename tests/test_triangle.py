# -*- coding: utf-8 -*-

import unittest
from crossproduct import Point2D, Point3D, Vector2D, Vector3D, \
    Line2D, Line3D, Triangle2D, Triangle3D, Plane3D, Segment2D, Segment3D

class Test_Triangle2D(unittest.TestCase):
    """
    P0=Point2D(0,0)
    v=Vector2D(1,0)
    w=Vector2D(0.5,1)
    """
    
    def test___init__(self):
        ""
        tr=Triangle2D(P0,v,w)
        self.assertIsInstance(tr,Triangle2D)
        
        
    def test___repr__(self):
        ""
        tr=Triangle2D(P0,v,w)
        self.assertEqual(str(tr),
                         'Triangle2D(Point2D(0,0), Vector2D(1,0), Vector2D(0.5,1))')
        
        
    def test_area(self):
        ""
        tr=Triangle2D(P0,v,w) #ccw
        self.assertEqual(tr.area,0.5)
        
        tr=Triangle2D(P0,w,v) #cw
        self.assertEqual(tr.area,0.5)
        
        
    def test_intersect_segment(self):
        
        tr=Triangle2D(Point2D(1,1), Vector2D(1,1), Vector2D(-1,1))
        s=Segment2D(Point2D(1.5,0), Point2D(1.5,10))
        
#        print(tr)
#        print(s)
#        print(s.vL)
#        print(tr.intersect_segment(s))
        
        
    def test_intersect_line(self):
        ""
        tr=Triangle2D(Point2D(0,0), Vector2D(1,1), Vector2D(0,2))
        l=Line2D(Point2D(1.5,0), Vector2D(0,1))
#        print(tr.intersect_line(l))
        
    def test_orientation(self):
        ""
        tr=Triangle2D(P0,v,w) #ccw
        self.assertTrue(tr.orientation>0)
    
        tr=Triangle2D(P0,w,v) #cw
        self.assertTrue(tr.orientation<0)
        
        
    def test_P1(self):
        ""
        tr=Triangle2D(P0,v,w)
        self.assertEqual(tr.P1,
                         P0+v)
        
        
    def test_P2(self):
        ""
        tr=Triangle2D(P0,v,w)
        self.assertEqual(tr.P2,
                         P0+w)
        
        
    def test_points(self):
        ""
        tr=Triangle2D(P0,v,w)
        self.assertEqual(tr.points,
                         (P0, tr.P1, tr.P2))
        
        
    def test_signed_area(self):
        ""
        tr=Triangle2D(P0,v,w) #ccw
        self.assertEqual(tr.signed_area,0.5)
        
        tr=Triangle2D(P0,w,v) #cw
        self.assertEqual(tr.signed_area,-0.5)
    
    
    
class Test_Triangle3D(unittest.TestCase):
    """
    P0=Point3D(0,0,0)
    v=Vector3D(1,0,0)
    w=Vector3D(0.5,1,0)
    """
    
    def test___init__(self):
        ""
        tr=Triangle3D(P0,v,w)
        self.assertIsInstance(tr,Triangle3D)
        
        
    def test___contains__(self):
        ""
        tr=Triangle3D(P0,v,w)
        
        #point
        self.assertTrue(P0 in tr)
        self.assertTrue(P0+v in tr)
        self.assertTrue(P0+w in tr)
        self.assertTrue(P0+v*0.5+w*0.5 in tr)
        self.assertFalse(P0+v*2 in tr)
        self.assertFalse(P0-v in tr)
        self.assertFalse(P0+w*2 in tr)
        self.assertFalse(P0-w in tr)
        self.assertFalse(P0+v*2 in tr)
        self.assertFalse(P0+tr.plane.N in tr)
        
        self.assertTrue(Point2D(1,1) in Triangle2D(Point2D(0,0), Vector2D(2,0), Vector2D(0,2)))

        
        #segment
        
        #polygon
        
        
    def test___repr__(self):
        ""
        tr=Triangle3D(P0,v,w)
        self.assertEqual(str(tr),
                         'Triangle3D(Point3D(0,0,0), Vector3D(1,0,0), Vector3D(0.5,1,0))')
        
        
    def test_area(self):
        ""
        tr=Triangle3D(P0,v,w) #ccw
        self.assertEqual(tr.area,0.5)
        
        tr=Triangle3D(P0,w,v) #cw
        self.assertEqual(tr.area,0.5)
        
    
    def test_intersect_halfline(self):
        ""
        
        
    def test_intersect_line(self):
        ""
        tr=Triangle3D(P0,v,w) #ccw
        
        # skew triangle plane and line, point intersection
        self.assertEqual(tr.intersect_line(Line3D(P0,
                                                  tr.plane.N)),
                         P0)
        
        # skew triangle plane and line, no intersection
        self.assertEqual(tr.intersect_line(Line3D(P0-v,
                                                  tr.plane.N)),
                         None)
        
        # parallel, non-coplanar triangle plane and line
        self.assertEqual(tr.intersect_line(Line3D(P0+tr.plane.N,
                                                  v)),
                         None)
    

    def test_intersect_plane(self):
        ""
        tr=Triangle3D(P0,v,w) #ccw
        
        # parallel triangle and plane
        self.assertEqual(tr.intersect_plane(Plane3D(P0+tr.plane.N,
                                                    tr.plane.N)),
                         None)
        
        # coplanar triangle and plane
        self.assertEqual(tr.intersect_plane(Plane3D(P0,
                                                    tr.plane.N)),
                         tr)
        
        # skew 3D triangle and plane - no intersection
        self.assertEqual(tr.intersect_plane(Plane3D(P0+v*2,
                                                    v)),
                         None)
        
        # skew 3D triangle and plane - point intersection
        self.assertEqual(tr.intersect_plane(Plane3D(P0,
                                                    v)),
                         P0)
        self.assertEqual(tr.intersect_plane(Plane3D(P0,
                                                    w)),
                         P0)
        self.assertEqual(tr.intersect_plane(Plane3D(P0+v,
                                                    v)),
                         P0+v)
        self.assertEqual(tr.intersect_plane(Plane3D(P0+w,
                                                    w)),
                         P0+w)
        
        # skew 3D triangle and plane - segment intersection
        self.assertEqual(tr.intersect_plane(Plane3D(P0+v*0.5,
                                                    v)),
                         Segment3D(P0+v*0.5,
                                   P0+w))
            
            # ... could test other variations here...
        
    
        
    def test_intersect_segment(self):
        ""
        
        
    def test_intersect_triangle(self):
        ""
        tr=Triangle3D(P0,v,w) #ccw
        
        # parallel triangle planes
        self.assertEqual(tr.intersect_triangle(Triangle3D(P0+tr.plane.N,
                                                          v,
                                                          w)),
                         None)
        
        # skew triangles, point intersection
        self.assertEqual(tr.intersect_triangle(Triangle3D(P0,
                                                          Vector3D(-1,0,1),
                                                          Vector3D(1,0,1))),
                         P0)
        self.assertEqual(tr.intersect_triangle(Triangle3D(P0+v,
                                                          Vector3D(-1,0,1),
                                                          Vector3D(1,0,1))),
                         P0+v)
            
        # skew triangles, segment intersection
        self.assertEqual(tr.intersect_triangle(Triangle3D(P0,
                                                          v,
                                                          Vector3D(0,0,1))),
                         Segment3D(P0,P0+v))
            
        self.assertEqual(tr.intersect_triangle(Triangle3D(P0+v*0.5,
                                                          Vector3D(0,2,2),
                                                          Vector3D(0,2,-2))),
                         Segment3D(P0+v*0.5,P0+w))
        
        # skew triangles, no intersection
        self.assertEqual(tr.intersect_triangle(Triangle3D(P0-v,
                                                          Vector3D(-1,0,1),
                                                          Vector3D(1,0,1))),
                         None)
        
                
    def test_P1(self):
        ""
        tr=Triangle3D(P0,v,w)
        self.assertEqual(tr.P1,
                         P0+v)
        
        
    def test_P2(self):
        ""
        tr=Triangle3D(P0,v,w)
        self.assertEqual(tr.P2,
                         P0+w)
        
        
    def test_points(self):
        ""
        tr=Triangle3D(P0,v,w)
        self.assertEqual(tr.points,
                         (P0, tr.P1, tr.P2))
        
        
    
    
if __name__=='__main__':
    
    P0=Point2D(0,0)
    v=Vector2D(1,0)
    w=Vector2D(0.5,1)
    unittest.main(Test_Triangle2D())
    
    P0=Point3D(0,0,0)
    v=Vector3D(1,0,0)
    w=Vector3D(0.5,1,0)
    unittest.main(Test_Triangle3D())
    
    
    
    
#    def test_intersection_halfline(self):
#        ""
#        # intersection of triangle and a halfline running along its base to the right
#        tr=Triangle2D(P0,v,w)
#        hl=Halfline2D(P0,v)
#        result=tr.intersect_halfline(hl)
#        self.assertEqual(result,[Segment2D(P0,P0+v)])
#        
#        # intersection of triangle and a halfline running along its base to the left
#        tr=Triangle2D(P0,v,w)
#        hl=Halfline2D(tr.P1,v*-1)
#        result=tr.intersect_halfline(hl)
#        self.assertEqual(result,[Segment2D(P0+v,P0)])
#        
#        # intersection of triangle and a Halfline running across the top
#        tr=Triangle2D(P0,v,w)
#        hl=Halfline2D(tr.P2,v)
#        result=tr.intersect_halfline(hl)
#        self.assertEqual(result,[tr.P2])
#        
#        # intersection of triangle and a horizontal Halfline running through the middle
#        tr=Triangle2D(P0,v,w)
#        hl=Halfline2D(P0+w*0.5,v)
#        result=tr.intersect_halfline(hl)
#        self.assertEqual(result,[Segment2D(P0+w*0.5,P0+(v+w)*0.5)])
#        
#        # intersection of triangle and a vertical Halfline running through the middle
#        tr=Triangle2D(P0,v,w)
#        hl=Halfline2D(P0+v*0.5,Vector2D(0,1))
#        result=tr.intersect_halfline(hl)
#        self.assertEqual(result,[Segment2D(P0+v*0.5,tr.P2)])
#        
#        # intersection of triangle and a Halfline running through a vertex to the middle of the opposite side
#        tr=Triangle2D(P0,v,w)
#        hl=Halfline2D(P0,Vector2D(0.75,0.5))
#        result=tr.intersect_halfline(hl)
#        self.assertEqual(result,[Segment2D(P0,P0+(v+w)*0.5)])
#        
#        # intersection of triangle and horizontal halfline starting inside triangle
#        tr=Triangle2D(P0,v,w)
#        hl=Halfline2D(Point2D(0.5,0.5),Vector2D(1,0))
#        result=tr.intersect_halfline(hl)
#        self.assertEqual(result,[Segment2D(Point2D(0.5,0.5), Point2D(0.75,0.5))])
#        
#        # intersection of triangle and vertical halfline starting inside triangle
#        tr=Triangle2D(P0,v,w)
#        hl=Halfline2D(Point2D(0.5,0.5),Vector2D(0,1))
#        result=tr.intersect_halfline(hl)
#        self.assertEqual(result,[Segment2D(Point2D(0.5,0.5), Point2D(0.5,1.0))])
#        
#        
#    def test_intersection_line(self):
#        ""
#        # intersection of triangle and a line running along it's base
#        tr=Triangle2D(P0,v,w)
#        l=Line2D(P0,v)
#        result=tr.intersect_line(l)
#        self.assertEqual(result,[Segment2D(P0,P0+v)])
#        
#        # intersection of triangle and a line running across the top
#        tr=Triangle2D(P0,v,w)
#        l=Line2D(tr.P2,v)
#        result=tr.intersect_line(l)
#        self.assertEqual(result,[tr.P2])
#        
#        # intersection of triangle and a horizontal line running through the middle
#        tr=Triangle2D(P0,v,w)
#        l=Line2D(P0+w*0.5,v)
#        result=tr.intersect_line(l)
#        self.assertEqual(result,[Segment2D(P0+w*0.5,P0+(v+w)*0.5)])
#        
#        # intersection of triangle and a vertical line running through the middle
#        tr=Triangle2D(P0,v,w)
#        l=Line2D(P0+v*0.5,Vector2D(0,1))
#        result=tr.intersect_line(l)
#        self.assertEqual(result,[Segment2D(P0+v*0.5,tr.P2)])
#        
#        # intersection of triangle and a line running through a vertex to the middle of the opposite side
#        tr=Triangle2D(P0,v,w)
#        l=Line2D(P0,Vector2D(0.75,0.5))
#        result=tr.intersect_line(l)
#        self.assertEqual(result,[Segment2D(P0,P0+(v+w)*0.5)])
#        
#    
#    def test_intersection_segment(self):
#        ""
#        # intersection of triangle and a segment matching it's base
#        tr=Triangle2D(P0,v,w)
#        s=Segment2D(P0,P0+v)
#        result=tr.intersect_segment(s)
#        self.assertEqual(result,[s])
#        
#        # intersection of triangle and a segment matching it's base and extending on either side
#        tr=Triangle2D(P0,v,w)
#        s=Segment2D(P0+v*-1,P0+v*2)
#        result=tr.intersect_segment(s)
#        self.assertEqual(result,[tr.polygon_segment(0)])
#        
#        # intersection of triangle and a segment starting at the base mid point and extending to the right
#        tr=Triangle2D(P0,v,w)
#        s=Segment2D(P0+v*0.5,P0+v*2)
#        result=tr.intersect_segment(s)
#        self.assertEqual(result,[Segment2D(P0+v*0.5,tr.P1)])
#        
#        # intersection of triangle and a segment starting at the base mid point and extending to the left
#        tr=Triangle2D(P0,v,w)
#        s=Segment2D(P0+v*0.5,P0+v*-2)
#        result=tr.intersect_segment(s)
#        self.assertEqual(result,[Segment2D(P0+v*0.5,P0)])
#        
#        # intersection of triangle and a segment starting at the base mid point and extending up
#        tr=Triangle2D(P0,v,w)
#        s=Segment2D(P0+v*0.5,Point2D(0.5,10))
#        result=tr.intersect_segment(s)
#        self.assertEqual(result,[Segment2D(P0+v*0.5,Point2D(0.5,1))])
#        
#        # intersection of triangle and a segment starting at P0 and extending to the middle
#        tr=Triangle2D(P0,v,w)
#        s=Segment2D(P0+v*0.5,Point2D(0.5,0.5))
#        result=tr.intersect_segment(s)
#        self.assertEqual(result,[s])
#        
#        # intersection of triangle and a segment starting at the middle and extending up
#        tr=Triangle2D(P0,v,w)
#        s=Segment2D(Point2D(0.5,0.5),Point2D(0.5,10))
#        result=tr.intersect_segment(s)
#        self.assertEqual(result,[Segment2D(Point2D(0.5,0.5),Point2D(0.5,1))])
        
    
    