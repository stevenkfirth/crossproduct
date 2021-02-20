# -*- coding: utf-8 -*-

import unittest, math

from crossproduct import Point, Points, Vector, Line, Halfline, Segment, Segments
from crossproduct import Polyline, Polylines, Plane
from crossproduct import Polygon, SimplePolygon, ConvexSimplePolygon
from crossproduct import Polyhedron

class Test_Point(unittest.TestCase):
    ""
    
    def test___add__(self):
        ""
        pt=Point(0,0)
        v=Vector(1,0)
        self.assertEqual(pt+v,
                         Point(1,0))
 
        pt=Point(0,0,0)
        v=Vector(1,0,0)
        self.assertEqual(pt+v,
                         Point(1,0,0))
    
    
    def test___eq__(self):
        ""
        pt=Point(0,0)
        self.assertTrue(pt==pt)
        
        pt1=Point(1,0)
        self.assertFalse(pt==pt1)
    
        pt2=Point(0,1,2)
        self.assertRaises(ValueError,
                          pt.__eq__,pt2)
    
        pt3=(0,0.0000000000001)
        self.assertTrue(pt==pt3)    
        
    
    def test___init__(self):
        ""
        pt=Point(0,1)
        self.assertIsInstance(pt,Point)
        self.assertEqual(list(pt),
                         [0,1])
        self.assertEqual(pt[1],
                         1)
        
        pt=Point(0,1,2)
        self.assertEqual(list(pt),
                         [0,1,2])
        
        
    def test___lt__(self):
        ""
        pt=Point(0,0)
        self.assertFalse(pt<Point(0,0))
        self.assertTrue(pt<Point(1,0))
        self.assertFalse(pt<Point(-1,0))
        self.assertTrue(pt<Point(0,1))
        self.assertFalse(pt<Point(0,-1))
        self.assertFalse(pt<Point(-1,1))
        
        pt=Point(0,0,0)
        self.assertFalse(pt<Point(0,0,0))
        self.assertTrue(pt<Point(1,0,0))
        self.assertFalse(pt<Point(-1,0,0))
        self.assertTrue(pt<Point(0,1,0))
        self.assertFalse(pt<Point(0,-1,0))
        self.assertTrue(pt<Point(0,0,1))
        self.assertFalse(pt<Point(0,0,-1))
        
        
    def test___repr__(self):
        ""
        pt=Point(0,0)
        self.assertEqual(str(pt),
                         'Point(0.0,0.0)')
    
    
    def test___sub__(self):
        ""
        pt1=Point(0,0)
        pt2=Point(1,0)
        self.assertEqual(pt2-pt1,
                         Vector(1,0))
        
        v=Vector(1,0)
        self.assertEqual(pt2-v,
                         pt1)
        
        pt1=Point(0,0,0)
        pt2=Point(1,0,0)
        self.assertEqual(pt2-pt1,
                         Vector(1,0,0))
        
        v=Vector(1,0,0)
        self.assertEqual(pt2-v,
                         pt1)
        
        
    def test__distance_to_point(self):
        ""
        pt1=Point(0,0)
        pt2=Point(1,0)
        self.assertEqual(pt1._distance_to_point(pt2),
                         1)
   
        pt1=Point(0,0,0)
        pt2=Point(1,0,0)
        self.assertEqual(pt1._distance_to_point(pt2),
                         1)
        
        
    def test_distance(self):
        ""
        pt1=Point(0,0)
        pt2=Point(1,0)
        self.assertEqual(pt1.distance(pt2),
                         1)
   
        pt1=Point(0,0,0)
        pt2=Point(1,0,0)
        self.assertEqual(pt1.distance(pt2),
                         1)
        
        
    def test_nD(self):
        ""
        pt=Point(0,0)
        self.assertEqual(pt.nD,
                         2)
        pt=Point(0,0,0)
        self.assertEqual(pt.nD,
                         3)
        
    
    def test_project_2D(self):
        ""
        pt=Point(1,2,3)
        self.assertEqual(pt.project_2D(0),
                         Point(2,3))
    
    def test_project_3D(self):
        ""
        pl=Plane(Point(0,0,1),Vector(0,0,1))
        pt=Point(2,2)
        self.assertEqual(pt.project_3D(pl,2),
                         Point(2,2,1.0))



class Test_Points(unittest.TestCase):
    ""
    
    def test___eq__(self):
        ""
        pts1=Points(Point(0,0),Point(1,1))
        pts2=Points(Point(0,0),Point(1,1))
        self.assertTrue(pts1==pts2)
        
    
    def test___init__(self):
        ""
        # creation
        pt=Point(0,0)
        pts=Points(pt)
        self.assertIsInstance(pts,
                              Points)
        self.assertEqual(pts[0],
                         pt)
        self.assertEqual(len(pts),
                         1)
        
        # append
        pt1=Point(1,1)
        pts.append(pt1)
        self.assertEqual(pts[1],
                         pt1)
        self.assertEqual(len(pts),
                         2)
        
        # insert
        pt2=Point(2,2)
        pts.insert(0,pt2)
        self.assertEqual(pts[0],
                         pt2)
        self.assertEqual(len(pts),
                         3)
        
        # del
        del pts[0]
        self.assertEqual(pts[0],
                         pt)
        
        
    def test_remove_points_in_segments(self):
        ""
        pts = Points(Point(0,0), Point(1,0))
        segments = Segments(Segment(Point(0,0), Point(0,1)))
        pts.remove_points_in_segments(segments)
        self.assertEqual(pts,
                         Points(Point(1.0,0.0)))
            
        

class Test_Vector(unittest.TestCase):
    
    def test___add__(self):
        ""
        v1=Vector(1,0)
        v2=Vector(2,0)
        self.assertEqual(v1+v2,
                         Vector(3,0))
    
        v1=Vector(1,0,0)
        v2=Vector(2,0,0)
        self.assertEqual(v1+v2,
                         Vector(3,0,0))
    
    
    def test___eq__(self):
        ""
        v=Vector(0,0)
        self.assertTrue(v==v)
        
        v1=Vector(1,0)
        self.assertFalse(v==v1)
    
        v2=Vector(0,1,2)
        self.assertRaises(ValueError,
                          v.__eq__,v2)
    
        v3=(0,0.0000000000001)
        self.assertTrue(v==v3)    
    
    
    def test___init__(self):
        ""
        v=Vector(1,0)
        self.assertIsInstance(v,
                              Vector)
        self.assertEqual(v[0],
                         1)
        self.assertEqual(v[1],
                         0)
        
        v=Vector(1,0,0)
        self.assertIsInstance(v,Vector)
        self.assertEqual(list(v),
                         [1.0,0.0,0.0])
        
        
    def test___mul__(self):
        ""
        v=Vector(1,0)
        self.assertEqual(v*2,
                         Vector(2,0))
        
        v=Vector(1,0,0)
        self.assertEqual(v*2,
                         Vector(2,0,0))
        
    
    def test___sub__(self):
        ""
        v1=Vector(1,0)
        v2=Vector(2,0)
        self.assertEqual(v1-v2,
                         Vector(-1,0))
        
        v1=Vector(1,0,0)
        v2=Vector(2,0,0)
        self.assertEqual(v1-v2,
                         Vector(-1,0,0))
        

    def test_angle(self):
        ""
        v1=Vector(1,0)
        self.assertEqual(v1.angle(v1),
                         0)
        self.assertEqual(v1.angle(Vector(0,1)),
                         math.pi/2)
        self.assertAlmostEqual(v1.angle(Vector(1,1)), 
                               math.pi/4)
        self.assertAlmostEqual(v1.angle(Vector(-1,0)), 
                               math.pi)
        
        v1=Vector(1,0,0)
        self.assertEqual(v1.angle(v1),
                         0)
        self.assertEqual(v1.angle(Vector(0,1,0)),
                         math.pi/2)
        self.assertAlmostEqual(v1.angle(Vector(1,1,0)), 
                               math.pi/4)
        self.assertAlmostEqual(v1.angle(Vector(-1,0,0)), 
                               math.pi)
        
    
    
    
    def test_cross_product(self):
        ""
        v1=Vector(1,0,0)
        v2=Vector(0,1,0)
        self.assertEqual(v1.cross_product(v1),
                         Vector(0,0,0))
        self.assertEqual(v1.cross_product(v1.opposite),
                         Vector(0,0,0))
        self.assertEqual(v1.cross_product(v2),
                         Vector(0,0,1))    
    

    def test_dot(self):
        ""
        v=Vector(1,0)
        self.assertEqual(v.dot(v),
                         1)
        self.assertEqual(v.dot(v.perp_vector),
                         0)
        self.assertEqual(v.dot(v.opposite),
                         -1)
    
        v=Vector(1,0,0)
        self.assertEqual(v.dot(v),
                         1)
        self.assertEqual(v.dot(Vector(0,1,0)),
                         0)
        self.assertEqual(v.dot(v.opposite),
                         -1)
        
    

    def test_index_largest_absolute_coordinate(self):
        ""
        v=Vector(1,2)
        self.assertTrue(v.index_largest_absolute_coordinate,
                        1)


    def test_is_codirectional(self):
        ""
        v=Vector(1,0)
        self.assertTrue(v.is_codirectional(v))
        self.assertFalse(v.is_codirectional(v.perp_vector))
        self.assertFalse(v.is_codirectional(v.opposite))

        v=Vector(1,0,0)
        self.assertTrue(v.is_collinear(v))
        self.assertFalse(v.is_collinear(Vector(0,1,0)))
        self.assertTrue(v.is_collinear(v.opposite))
    
    
    def test_is_collinear(self):
        ""
        v=Vector(1,0)
        self.assertTrue(v.is_collinear(v))
        self.assertFalse(v.is_collinear(v.perp_vector))
        self.assertTrue(v.is_collinear(v.opposite))
    
        v=Vector(1,0,0)
        self.assertTrue(v.is_collinear(v))
        self.assertFalse(v.is_collinear(Vector(0,1,0)))
        self.assertTrue(v.is_collinear(v.opposite))
       
        
    def test_is_opposite(self):
        ""
        v=Vector(1,0)
        self.assertFalse(v.is_opposite(v))
        self.assertFalse(v.is_opposite(v.perp_vector))
        self.assertTrue(v.is_opposite(v.opposite))
        
        v=Vector(1,0,0)
        self.assertFalse(v.is_opposite(v))
        self.assertFalse(v.is_opposite(Vector(0,1,0)))
        self.assertTrue(v.is_opposite(v.opposite))
        
            
    def test_is_perpendicular(self):
        ""
        v=Vector(1,0)
        self.assertFalse(v.is_perpendicular(v))
        self.assertTrue(v.is_perpendicular(v.perp_vector))
    
        v=Vector(1,0,0)
        self.assertFalse(v.is_perpendicular(v))
        self.assertTrue(v.is_perpendicular(Vector(0,1,0)))
        
        
    def test_length(self):
        ""
        v=Vector(1,0)
        self.assertEqual(v.length,
                         1)
        
        v=Vector(1,0,0)
        self.assertEqual(v.length,
                         1)
        
        
    def test_normalise(self):
        ""
        v=Vector(2,0)
        self.assertEqual(v.normalise,
                         Vector(1,0))
        
        v=Vector(2,0,0)
        self.assertEqual(v.normalise,
                         Vector(1,0,0))
        
        
    def test_opposite(self):
        ""
        v=Vector(1,0)
        self.assertEqual(v.opposite,
                         Vector(-1,0))
        
        v=Vector(1,0,0)
        self.assertEqual(v.opposite,
                         Vector(-1,0,0))
        

    def test_perp_product(self):
        ""
        v=Vector(1,0)
        self.assertEqual(v.perp_product(v),
                         0)
        self.assertEqual(v.perp_product(v.perp_vector),
                         1)
        self.assertEqual(v.perp_product(v.opposite),
                         0)
        self.assertEqual(v.perp_product(v.perp_vector.opposite),
                         -1)


    def test_perp_vector(self):
        ""
        v=Vector(1,0)
        self.assertEqual(v.perp_vector,
                         Vector(0,1))
        
        
    def test_triple_product(self):
        ""
        v1=Vector(1,0,0)
        v2=Vector(0,1,0)
        v3=Vector(0,0,1)
        self.assertEqual(v1.triple_product(v2,v3),
                         1)
    
    
    
class Test_Line(unittest.TestCase):
    
    def test___eq__(self):
        ""
        P0,vL=Point(0,0),Vector(1,1) 
        l=Line(P0,vL)
        self.assertTrue(l==Line(P0,vL*2))
        self.assertTrue(l==Line(P0,vL.opposite))
        self.assertTrue(l==Line(P0+vL,vL))
        self.assertFalse(l==Line(P0,vL.perp_vector))
        self.assertFalse(l==Line(P0+vL.perp_vector,vL))
        
        P0,vL=Point(0,0,0),Vector(1,1,1)
        l=Line(P0,vL)
        self.assertTrue(l==Line(P0,vL*2))
        self.assertTrue(l==Line(P0,vL.opposite))
        self.assertTrue(l==Line(P0+vL,vL))
        self.assertFalse(l==Line(P0,Vector(1,-1,0)))
        self.assertFalse(l==Line(P0+Vector(1,-1,0),vL))
        
    
    
    def test___init__(self):
        ""
        P0,vL=Point(0,0),Vector(1,1) 
        l=Line(P0,vL)
        self.assertIsInstance(l,
                              Line)
        self.assertEqual(l.P0,
                         P0)
        self.assertEqual(l.vL,
                         vL)
        
        
    def test__distance_to_line(self):
        ""
        P0,vL=Point(0,0),Vector(1,1) 
        l=Line(P0,vL)
        self.assertEqual(l._distance_to_line(l),
                         0)
        self.assertEqual(l._distance_to_line(Line(P0+vL.perp_vector,vL)),
                         vL.length)
        self.assertEqual(l._distance_to_line(Line(P0,vL.perp_vector)), 
                         0)

        P0,vL=Point(0,0,0),Vector(1,1,1) 
        l=Line(P0,vL)
        self.assertEqual(l._distance_to_line(l),
                         0)
        self.assertEqual(l._distance_to_line(Line(P0+Vector(1,-1,0),vL)),
                         Vector(1,-1,0).length)
        self.assertEqual(l._distance_to_line(Line(P0,Vector(1,-1,0))), 
                         0)
        
        self.assertEqual(Line(Point(0,0,0),
                              Vector(1,0,0))._distance_to_line(Line(Point(0,0,1),
                                                                    Vector(0,1,0))),
                        1)
        
        
    def test__distance_to_point(self):
        ""
        P0,vL=Point(0,0),Vector(1,1) 
        l=Line(P0,vL)
        self.assertEqual(l._distance_to_point(P0),
                         0)
        self.assertEqual(l._distance_to_point(P0+vL),
                         0)
        self.assertEqual(l._distance_to_point(P0+vL.perp_vector),
                         vL.length)
                

        P0,vL=Point(0,0,0),Vector(1,1,1) 
        l=Line(P0,vL)
        self.assertEqual(l._distance_to_point(P0),
                         0)
        self.assertEqual(l._distance_to_point(P0+Vector(1,-1,0)),
                         Vector(1,-1,0).length)
            

        
    def test_intersect_line(self):
        ""
        P0,vL=Point(0,0),Vector(1,1) 
        l=Line(P0,vL)        
        # collinear
        self.assertEqual(l.intersect_line(l),
                         l)        
        # parallel
        self.assertEqual(l.intersect_line(Line(P0+vL.perp_vector,vL)),
                         None)        
        # skew
        self.assertEqual(l.intersect_line(Line(P0,vL.perp_vector)),
                         P0)        
        # skew - different P0s
        self.assertEqual(l.intersect_line(Line(P0+vL,vL.perp_vector)),
                         P0+vL)
        
        P0,vL=Point(0,0,0),Vector(1,1,1) 
        l=Line(P0,vL)
        # collinear
        self.assertEqual(l.intersect_line(l),
                         l)
        # parallel
        self.assertEqual(l.intersect_line(Line(P0+Vector(1,-1,0),vL)),
                         None)
        #skew
        self.assertEqual(l.intersect_line(Line(P0,Vector(1,-1,0))),
                         P0)
        self.assertEqual(l.intersect_line(Line(P0+vL,Vector(1,-1,0))),
                         P0+vL)
        self.assertEqual(l.intersect_line(Line(Point(0,0,1),Vector(1,-1,0))),
                         None)
        
        
    def test__intersect_line_skew_2D(self):
        ""
        P0,vL=Point(0,0),Vector(1,1) 
        l=Line(P0,vL)
        self.assertEqual(l._intersect_line_skew_2D(Line(P0,vL.perp_vector)),
                         P0)
        self.assertEqual(l._intersect_line_skew_2D(Line(P0+vL,vL.perp_vector)),
                         P0+vL)

        
    def test__intersect_line_skew_3D(self):
        ""
        P0,vL=Point(0,0,0),Vector(1,1,1)
        l=Line(P0,vL)
        self.assertEqual(l._intersect_line_skew_3D(Line(P0,
                                                        Vector(1,-1,0))),
                         P0)
        self.assertEqual(l._intersect_line_skew_3D(Line(Point(0,0,1),
                                                        Vector(1,-1,0))),
                         None)

        
    def test_calculate_point(self):
        ""
        P0,vL=Point(0,0),Vector(1,1) 
        l=Line(P0,vL)
        self.assertEqual(l.calculate_point(2),
                         P0+vL*2)
        
        P0,vL=Point(0,0,0),Vector(1,1,1)
        l=Line(P0,vL)
        self.assertEqual(l.calculate_point(2),
                         P0+vL*2)
        
        
        
    def test_calculate_t_from_coordinates(self):
        ""
        P0,vL=Point(0,0),Vector(1,1) 
        l=Line(P0,vL)
        self.assertEqual(l.calculate_t_from_coordinates(*(P0+vL*2)),
                         2)
        self.assertEqual(l.calculate_t_from_coordinates(2,0),
                         2)
        
        
        
        P0,vL=Point(0,0,0),Vector(1,1,1) 
        l=Line(P0,vL)
        self.assertEqual(l.calculate_t_from_coordinates(*(P0+vL*2)),
                         2)
    
    
    def test_contains(self):
        ""
        P0,vL=Point(0,0),Vector(1,1) 
        l=Line(P0,vL)
        
        # point
        self.assertTrue(l.contains(P0))
        self.assertTrue(l.contains(P0+vL))
        self.assertFalse(l.contains(P0+vL.perp_vector))
        
        # # halfline
        self.assertTrue(l.contains(Halfline(P0,vL)))
        self.assertTrue(l.contains(Halfline(P0+vL,vL)))
        self.assertFalse(l.contains(Halfline(P0+vL.perp_vector,vL)))
        self.assertFalse(l.contains(Halfline(P0,vL.perp_vector)))
        
        # segment
        self.assertTrue(l.contains(Segment(P0,P0+vL)))
        self.assertTrue(l.contains(Segment(P0,P0+vL*10)))
        self.assertFalse(l.contains(Segment(P0+vL.perp_vector,P0+vL)))
        self.assertFalse(l.contains(Segment(P0+vL.perp_vector,P0+vL+vL.perp_vector)))
    
        P0,vL=Point(0,0,0),Vector(1,1,1) 
        l=Line(P0,vL)
        
        # point
        self.assertTrue(l.contains(P0))
        self.assertTrue(l.contains(P0+vL))
        self.assertFalse(l.contains(P0+Vector(1,-1,0)))
        
        # halfline
        self.assertTrue(l.contains(Halfline(P0,vL)))
        self.assertTrue(l.contains(Halfline(P0+vL,vL)))
        self.assertFalse(l.contains(Halfline(P0+Vector(1,-1,0),vL)))
        self.assertFalse(l.contains(Halfline(P0,Vector(1,-1,0))))
        
        # segment
        self.assertTrue(l.contains(Segment(P0,P0+vL)))
        self.assertTrue(l.contains(Segment(P0,P0+vL*10)))
        self.assertFalse(l.contains(Segment(P0+Vector(1,-1,0),P0+vL)))
        self.assertFalse(l.contains(Segment(P0+Vector(1,-1,0),P0+vL+Vector(1,-1,0))))
        
    
    
    
        
    
    def test_is_parallel(self):
        ""
        P0,vL=Point(0,0),Vector(1,1) 
        l=Line(P0,vL)
        self.assertTrue(l.is_parallel(l))
        self.assertTrue(l.is_parallel(Line(P0,vL.opposite)))
        self.assertTrue(l.is_parallel(Line(P0+vL.perp_vector,vL)))
        
        P0,vL=Point(0,0,0),Vector(1,1,1) 
        l=Line(P0,vL)
        self.assertTrue(l.is_parallel(l))
        self.assertTrue(l.is_parallel(Line(P0,vL.opposite)))
        self.assertTrue(l.is_parallel(Line(P0+Vector(1,-1,0),vL)))
        

    def test_project_2D(self):
        ""
        P0,vL=Point(0,0,0),Vector(1,1,1) 
        l=Line(P0,vL)
        self.assertEqual(l.project_2D(0),
                         Line(Point(0,0),Vector(1,1)))
        self.assertEqual(l.project_2D(1),
                         Line(Point(0,0),Vector(1,1)))
        self.assertEqual(l.project_2D(2),
                         Line(Point(0,0),Vector(1,1)))
    


class Test_Halfline(unittest.TestCase):
    
    def test___eq__(self):
        ""
        P0,vL=Point(0,0),Vector(1,1) 
        hl=Halfline(P0,vL)
        self.assertTrue(hl==hl)
    
        P0,vL=Point(0,0,0),Vector(1,1,1)
        hl=Halfline(P0,vL)
        self.assertTrue(hl==hl)
        
        
    def test___init__(self):
        ""
        P0,vL=Point(0,0),Vector(1,1) 
        hl=Halfline(P0,vL)
        self.assertIsInstance(hl,Halfline)
        self.assertEqual(hl.P0,Point(0,0))
        self.assertEqual(hl.vL,Vector(1,1))
        
        P0,vL=Point(0,0,0),Vector(1,1,1)
        hl=Halfline(P0,vL)
        self.assertIsInstance(hl,Halfline)
        self.assertEqual(hl.P0,Point(0,0,0))
        self.assertEqual(hl.vL,Vector(1,1,1))
        
    
    def test_calculate_point(self):
        ""
        P0,vL=Point(0,0),Vector(1,1) 
        hl=Halfline(P0,vL)
        self.assertEqual(hl.calculate_point(2),
                         P0+vL*2)

        P0,vL=Point(0,0,0),Vector(1,1,1)
        hl=Halfline(P0,vL)
        self.assertEqual(hl.calculate_point(2),
                         P0+vL*2)


    def test_contains(self):
        ""
        P0,vL=Point(0,0),Vector(1,1) 
        hl=Halfline(P0,vL)
        # point
        self.assertTrue(hl.contains(P0))
        self.assertTrue(hl.contains(P0+vL))
        self.assertTrue(hl.contains(P0+vL*10))
        self.assertFalse(hl.contains(P0+vL.opposite))
        self.assertFalse(hl.contains(P0+vL.perp_vector))
        # segment
        self.assertTrue(hl.contains(Segment(P0,P0+vL)))
        self.assertTrue(hl.contains(Segment(P0+vL,P0+vL*2)))
        self.assertFalse(hl.contains(Segment(P0+vL*-1,P0)))
        self.assertFalse(hl.contains(Segment(P0+vL*-2,P0+vL*-1)))
        self.assertFalse(hl.contains(Segment(P0+vL.perp_vector,P0+vL+vL.perp_vector)))

        P0,vL=Point(0,0,0),Vector(1,1,1)
        hl=Halfline(P0,vL)
        # point
        self.assertTrue(hl.contains(P0))
        self.assertTrue(hl.contains(P0+vL))
        self.assertTrue(hl.contains(P0+vL*10))
        self.assertFalse(hl.contains(P0+vL.opposite))
        self.assertFalse(hl.contains(P0+Vector(1,-1,0)))
        # segment
        self.assertTrue(hl.contains(Segment(P0,P0+vL)))
        self.assertTrue(hl.contains(Segment(P0+vL,P0+vL*2)))
        self.assertFalse(hl.contains(Segment(P0+vL*-1,P0)))
        self.assertFalse(hl.contains(Segment(P0+vL*-2,P0+vL*-1)))
        self.assertFalse(hl.contains(Segment(P0+Vector(1,-1,0),P0+vL+Vector(1,-1,0))))
        
        
    def test__distance_to_point(self):
        ""
        P0,vL=Point(0,0),Vector(1,1) 
        hl=Halfline(P0,vL)
        self.assertEqual(hl._distance_to_point(P0),
                         0)
        self.assertEqual(hl._distance_to_point(P0-vL),
                         vL.length)
        self.assertEqual(hl._distance_to_point(P0+vL),
                         0)
        self.assertEqual(hl._distance_to_point(P0+Vector(1,-1)),
                         Vector(1,-1).length)


        P0,vL=Point(0,0,0),Vector(1,1,1)
        hl=Halfline(P0,vL)
        self.assertEqual(hl._distance_to_point(P0),
                         0)
        self.assertEqual(hl._distance_to_point(P0-vL),
                         vL.length)
        self.assertEqual(hl._distance_to_point(P0+vL),
                         0)
        self.assertEqual(hl._distance_to_point(P0+Vector(1,-1,0)),
                         Vector(1,-1,0).length)


    def test_intersect_halfline(self):
        ""
        P0,vL=Point(0,0),Vector(1,1) 
        hl=Halfline(P0,vL)
        # same
        self.assertEqual(hl.intersect_halfline(hl),
                         hl)
        # codirectional
        self.assertEqual(hl.intersect_halfline(Halfline(P0+vL,vL)),
                         Halfline(P0+vL,vL))
        self.assertEqual(hl.intersect_halfline(Halfline(P0+vL*-1,vL)),
                         hl)
        # parallel
        self.assertEqual(hl.intersect_halfline(Halfline(P0+vL.perp_vector,vL)),
                         None)
        # collinear but not codirectinal
        self.assertEqual(hl.intersect_halfline(Halfline(P0,vL*-1)),
                         hl.P0)
        self.assertEqual(hl.intersect_halfline(Halfline(P0+vL,vL*-1)),
                         Segment(P0,P0+vL))
        # skew
        self.assertEqual(hl.intersect_halfline(Halfline(P0,vL.perp_vector)),
                         hl.P0)
        self.assertEqual(hl.intersect_halfline(Halfline(P0+vL,vL.perp_vector)),
                         P0+vL)
        self.assertEqual(hl.intersect_halfline(Halfline(P0+vL*-1,vL.perp_vector)),
                         None)


    def test_intersect_line(self):
        ""
        P0,vL=Point(0,0),Vector(1,1) 
        hl=Halfline(P0,vL)
        # collinear
        self.assertEqual(hl.intersect_line(Line(P0,vL)),
                         hl)
        # parallel
        self.assertEqual(hl.intersect_line(Line(Point(0,1),vL)),
                         None)
        # skew - same P0s
        self.assertEqual(hl.intersect_line(Line(P0,Vector(0,1))),
                         P0)
        # skew - different P0s
        self.assertEqual(hl.intersect_line(Line(Point(0.5,0),Vector(0,1))),
                         Point(0.5,0.5))


    def test_line(self):
        P0,vL=Point(0,0),Vector(1,1) 
        hl=Halfline(P0,vL)
        self.assertEqual(hl.line,
                         Line(P0,vL))
    
        P0,vL=Point(0,0,0),Vector(1,1,1)
        hl=Halfline(P0,vL)
        self.assertEqual(hl.line,
                         Line(P0,vL))



class Test_Segment(unittest.TestCase):
    
    def test___add__(self):
        ""
        P0,P1=Point(0,0), Point(1,1)
        s=Segment(P0,P1)
        s1=Segment(Point(1,1), Point(2,2))
        self.assertEqual(s+s1,
                         Segment(Point(0,0), Point(2,2)))
        self.assertEqual(Segment(Point(1,1), Point(1,2))+Segment(Point(1,0), Point(1,1)),
                         Segment(Point(1.0,0.0), Point(1.0,2.0)))

        
    def test___eq__(self):
        ""
        P0,P1=Point(0,0), Point(1,1)
        s=Segment(P0,P1)
        self.assertTrue(s==s)
        self.assertFalse(Segment(P0,P0+s.line.vL*0.5)==s)
    
        P0, P1=Point(0,0,0), Point(1,1,1)
        s=Segment(P0,P1)
        self.assertTrue(s==s)
        self.assertFalse(Segment(P0,P0+s.line.vL*0.5)==s)
        
        
    def test___init__(self):
        ""
        P0,P1=Point(0,0), Point(1,1)
        s=Segment(P0,P1)
        self.assertIsInstance(s,Segment)
        self.assertEqual(s.P0,Point(0,0))
        self.assertEqual(s.P1,Point(1,1))

        P0, P1=Point(0,0,0), Point(1,1,1)
        s=Segment(P0,P1)
        self.assertIsInstance(s,Segment)
        self.assertEqual(s.P0,Point(0,0,0))
        self.assertEqual(s.P1,Point(1,1,1))
        
    
    def test_calculate_point(self):
        ""
        P0,P1=Point(0,0), Point(1,1)
        s=Segment(P0,P1)
        self.assertEqual(s.calculate_point(0.5),
                         P0+s.line.vL*0.5)

        P0, P1=Point(0,0,0), Point(1,1,1)
        s=Segment(P0,P1)
        self.assertEqual(s.calculate_point(0.5),
                         P0+s.line.vL*0.5)
        

    def test_contains(self):
        ""
        P0,P1=Point(0,0), Point(1,1)
        s=Segment(P0,P1)        
        # point
        self.assertTrue(s.contains(P0))
        self.assertTrue(s.contains(P1))
        self.assertTrue(s.contains(P0+s.line.vL*0.5)) # segment midpoint
        self.assertFalse(s.contains(P0+s.line.vL*-0.5)) 
        self.assertFalse(s.contains(P0+s.line.vL*1.5))         
        # segment
        self.assertTrue(s.contains(s))
        self.assertTrue(s.contains(Segment(P0,P0+s.line.vL*0.5)))
        self.assertTrue(s.contains(Segment(P0+s.line.vL*0.5,P1)))
        self.assertFalse(s.contains(Segment(P0+s.line.vL*-0.5,P1)))
        self.assertFalse(s.contains(Segment(P0,P1+s.line.vL*0.5)))
        self.assertFalse(s.contains(Segment(P0,P0+s.line.vL.perp_vector)))
    
    
        P0, P1=Point(0,0,0), Point(1,1,1)
        s=Segment(P0,P1)        
        # point
        self.assertTrue(s.contains(P0))
        self.assertTrue(s.contains(P1))
        self.assertTrue(s.contains(P0+s.line.vL*0.5)) # segment midpoint
        self.assertFalse(s.contains(P0+s.line.vL*-0.5)) 
        self.assertFalse(s.contains(P0+s.line.vL*1.5))         
        # segment
        self.assertTrue(s.contains(s))
        self.assertTrue(s.contains(Segment(P0,P0+s.line.vL*0.5)))
        self.assertTrue(s.contains(Segment(P0+s.line.vL*0.5,P1)))
        self.assertFalse(s.contains(Segment(P0+s.line.vL*-0.5,P1)))
        self.assertFalse(s.contains(Segment(P0,P1+s.line.vL*0.5)))
        self.assertFalse(s.contains(Segment(P0,P0+Vector(1,-1,0))))
        
        
    def test__distance_to_point(self):
        ""
        P0,P1=Point(0,0), Point(1,1)
        s=Segment(P0,P1)
        self.assertEqual(s._distance_to_point(Point(-2,0)),
                         2) 
        self.assertEqual(s._distance_to_point(Point(2,1)),
                         1) 
        self.assertEqual(s._distance_to_point(Point(0,1)),
                         0.5**0.5) 
        self.assertEqual(s._distance_to_point(Point(1,0)),
                         0.5**0.5) 
        
        P0, P1=Point(0,0,0), Point(1,1,1)
        s=Segment(P0,P1)
        self.assertEqual(s._distance_to_point(Point(-2,0,0)),
                         2) 
        self.assertEqual(s._distance_to_point(Point(1,1,2)),
                         1) 
        self.assertEqual(s._distance_to_point(Point(0,0,0)),
                         0) 
        self.assertEqual(s._distance_to_point(Point(1,-1,0)),
                         (s.P0-Point(1,-1,0)).length) 

    
    def test__distance_to_segment(self):
        ""
        P0, P1=Point(0,0,0), Point(1,1,1)
        s=Segment(P0,P1)        
        self.assertEqual(s._distance_to_segment(s),
                         0)
        self.assertEqual(s._distance_to_segment(Segment(P0+Vector(1,-1,0),
                                                         P1+Vector(1,-1,0))),
                         Vector(1,-1,0).length)
        self.assertEqual(s._distance_to_segment(Segment(P0,
                                                         Point(1,-1,0))), 
                         0)
        self.assertEqual(s._distance_to_segment(Segment(Point(-2,-2,-2),
                                                         Point(-1,-1,-1))),
                         Vector(1,1,1).length)

        
    def test_difference_segment(self):
        ""
        P0,P1=Point(0,0), Point(1,1)
        s=Segment(P0,P1)        
        # no intersection, difference is self
        self.assertEqual(s.difference_segment(Segment(Point(5,5),Point(6,6))),
                         Segments(s))        
        # point intersection, difference is self
        self.assertEqual(s.difference_segment(Segment(Point(1,1),Point(2,2))),
                         Segments(s))        
        # segment intersection, difference is remaining segment part
        self.assertEqual(s.difference_segment(Segment(Point(0.5,0.5),Point(2,2))),
                         Segments(Segment(Point(0,0),Point(0.5,0.5)),))
        # self intersection, difference is None
        self.assertEqual(s.difference_segment(s),
                         Segments())        
        # segment intersection, inside original
        # segment intersection, difference is remaining segment part
        self.assertEqual(s.difference_segment(Segment(Point(0.25,0.25),Point(0.75,0.75))),
                         Segments(Segment(Point(0,0),Point(0.25,0.25)),
                                  Segment(Point(0.75,0.75),Point(1,1))))        
        # segment intersection, outside both start and end point
        self.assertEqual(s.difference_segment(Segment(Point(-1,-1),Point(2,2))),
                         Segments())

        
    def test_difference_segments(self):
        ""        
        P0,P1=Point(0,0), Point(1,1)
        s=Segment(P0,P1)        
        # self intersection - intersection first
        s1=Segments(Segment(Point(0,0), Point(1,1)), 
                    Segment(Point(1,1), Point(2,1)),
                    Segment(Point(4,1), Point(5,1)))
        self.assertEqual(s.difference_segments(s1),
                         Segments())        
        # self intersection - intersection last
        s1=Segments(Segment(Point(4,1), Point(5,1)), 
                    Segment(Point(1,1), Point(2,1)),
                    Segment(Point(0,0), Point(1,1)))
        self.assertEqual(s.difference_segments(s1),
                         Segments())                
        # no intersection
        s1=Segments(Segment(Point(0,0), Point(1,0)), 
                    Segment(Point(1,1), Point(2,1)))
        self.assertEqual(s.difference_segments(s1),
                         Segments(s))        
        # mid intersection
        s1=Segments(Segment(Point(0,0), Point(0.5,0.5)), 
                    Segment(Point(1,1), Point(2,1)))
        self.assertEqual(s.difference_segments(s1),
                         Segments(Segment(Point(0.5,0.5), Point(1,1))))        
        # full intersection using two segments
        s1=Segments(Segment(Point(0,0), Point(0.5,0.5)), 
                    Segment(Point(0.5,0.5), Point(1,1)))
        self.assertEqual(s.difference_segments(s1),
                         Segments())        
        # intersection inside original
        s1=Segments(Segment(Point(0.25,0.25),Point(0.75,0.75)), 
                    Segment(Point(1,1), Point(2,2)))
        self.assertEqual(s.difference_segments(s1),
                         Segments(Segment(Point(0,0), 
                                            Point(0.25,0.25)), 
                                  Segment(Point(0.75,0.75), 
                                            Point(1,1))))        
        # intersection inside original
        s1=Segments(Segment(Point(0.2,0.2),Point(0.4,0.4)), 
                    Segment(Point(0.6,0.6), Point(0.8,0.8)))
        self.assertEqual(s.difference_segments(s1),
                         Segments(Segment(Point(0,0), 
                                            Point(0.2,0.2)), 
                                  Segment(Point(0.4,0.4), 
                                            Point(0.6,0.6)), 
                                  Segment(Point(0.8,0.8), 
                                            Point(1.0,1.0))))
        

    def test_intersect_halfline(self):
        ""
        P0,P1=Point(0,0), Point(1,1)
        s=Segment(P0,P1)        
        # collinear - same start point
        self.assertEqual(s.intersect_halfline(Halfline(P0,s.line.vL)),
                         s)        
        # collinear - halfline start point is segment end point
        self.assertEqual(s.intersect_halfline(Halfline(P1,s.line.vL)),
                         P1)
        # collinear - halfline start point is segment mid point
        self.assertEqual(s.intersect_halfline(Halfline(P0+s.line.vL*0.5,
                                                       s.line.vL)),
                         Segment(P0+s.line.vL*0.5,P1))
        self.assertEqual(s.intersect_halfline(Halfline(P0+s.line.vL*0.5,
                                                       s.line.vL*-1)),
                         Segment(P0,P0+s.line.vL*0.5))


    def test_intersect_line(self):
        ""
        P0,P1=Point(0,0), Point(1,1)
        s=Segment(P0,P1)        
        # collinear
        self.assertEqual(s.intersect_line(Line(P0,s.line.vL)),
                         s)
        # parallel
        self.assertEqual(s.intersect_line(Line(P0+s.line.vL.perp_vector,
                                               s.line.vL)),
                         None)
        # skew - same P0s
        self.assertEqual(s.intersect_line(Line(P0,s.line.vL.perp_vector)),
                         P0)
        # skew - different P0s
        self.assertEqual(s.intersect_line(Line(Point(0.5,0),
                                               s.line.vL.perp_vector)),
                         Point(0.25,0.25))
        # skew - no intersection
        self.assertEqual(s.intersect_line(Line(P0+s.line.vL*-1,
                                               s.line.vL.perp_vector)),
                         None)
        
        
    def test_intersect_segment(self):
        ""
        P0,P1=Point(0,0), Point(1,1)
        s=Segment(P0,P1)
        # collinear - same segment
        self.assertEqual(s.intersect_segment(s),
                         s)
        # collinear - different start point inside segment
        self.assertEqual(s.intersect_segment(Segment(P0+s.line.vL*0.5,P1)),
                         Segment(P0+s.line.vL*0.5,
                                   P1))
        # collinear - different start point outside segment
        self.assertEqual(s.intersect_segment(Segment(P0+s.line.vL*-0.5,P1)),
                         s)
        # collinear - different end point inside segment
        self.assertEqual(s.intersect_segment(Segment(P0,P1+s.line.vL*-0.5)),
                         Segment(P0,P1+s.line.vL*-0.5))
        # collinear - different start point outside segment
        self.assertEqual(s.intersect_segment(Segment(P0,P1+s.line.vL*0.5)),
                         s)
        # collinear - start point and end point inside segment
        self.assertEqual(s.intersect_segment(Segment(P0+s.line.vL*0.25,
                                                     P1+s.line.vL*-0.25)),
                         Segment(P0+s.line.vL*0.25,
                                 P1+s.line.vL*-0.25))
        # collinear - start point and end point outside segment
        self.assertEqual(s.intersect_segment(Segment(P0+s.line.vL*-0.25,
                                                     P1+s.line.vL*0.25)),
                         s)
        # collinear - but no intersection
        self.assertEqual(s.intersect_segment(Segment(P0+s.line.vL*2,
                                                     P1+s.line.vL*2)),
                         None)
        # parallel
        self.assertEqual(s.intersect_segment(Segment(P0+s.line.vL.perp_vector,
                                                     P1+s.line.vL.perp_vector)),
                         None)
        # skew - intersecting at start point
        self.assertEqual(s.intersect_segment(Segment(P0,P1+s.line.vL.perp_vector)),
                         P0)
        # skew - intersecting at end point
        self.assertEqual(s.intersect_segment(Segment(P1+s.line.vL.perp_vector*-1,
                                                     P1+s.line.vL.perp_vector)),
                         P1)
        # skew - intersecting at mid points
        self.assertEqual(s.intersect_segment(Segment(P0+s.line.vL*0.5+s.line.vL.perp_vector*-0.5,
                                                     P0+s.line.vL*0.5+s.line.vL.perp_vector*0.5)),
                         P0+s.line.vL*0.5)
        # skew - no intersection
        self.assertEqual(s.intersect_segment(Segment(P0+s.line.vL.perp_vector*0.5,
                                                     P0+s.line.vL.perp_vector*1.5)),
                         None)
        
        s1=Segment(Point(0,0,0), Point(0,1,0))
        s2=Segment(Point(0,1,0), Point(1,1,0))
        self.assertEqual(s1.intersect_segment(s2),
                         Point(0,1,0))
        
        
    def test_line(self):
        ""
        P0,P1=Point(0,0), Point(1,1)
        s=Segment(P0,P1)
        self.assertEqual(s.line,
                         Line(P0,s.line.vL))
        
        P0, P1=Point(0,0,0), Point(1,1,1)
        s=Segment(P0,P1)
        self.assertEqual(s.line,
                         Line(P0,P1-P0))
        
        
    def test_order(self):
        ""
        P0, P1=Point(0,0,0), Point(1,1,1)
        s=Segment(P0,P1)
        self.assertEqual(s.order.points,
                         s.points)
        
        s=Segment(P1,P0)
        self.assertEqual(s.order.points,
                        Points(Point(0,0,0), Point(1,1,1)))

        
    # def test_plot(self):
    #     ""
    #     if plot:
    #         P0,P1=Point(0,0), Point(1,1)
    #         s=Segment(P0,P1)
    #         fig, ax = plt.subplots()
    #         s.plot(ax)
            
    #     if plot:
    #         P0, P1=Point(0,0,0), Point(1,1,1)
    #         s=Segment(P0,P1)
    #         fig = plt.figure()
    #         ax = fig.add_subplot(111, projection='3d')
    #         s.plot(ax)
        
    
    def test_points(self):
        ""
        P0,P1=Point(0,0), Point(1,1)
        s=Segment(P0,P1)
        self.assertEqual(s.points,
                         Points(P0,P1))
        
        P0, P1=Point(0,0,0), Point(1,1,1)
        s=Segment(P0,P1)
        self.assertEqual(s.points,
                         Points(P0,P1))
        
        
    def test_project_2D(self):
        ""
        
        
    def test_project_3D(self):
        ""
        
        
    def reverse(self):
        ""
        P0,P1=Point(0,0), Point(1,1)
        s=Segment(P0,P1)
        self.assertEqual(s.reverse,
                         Segment(P1,P0))
        
        P0, P1=Point(0,0,0), Point(1,1,1)
        s=Segment(P0,P1)
        self.assertEqual(s.reverse,
                         Segment(P1,P0))
        

class Test_Segments(unittest.TestCase):
    ""
    
    def test___init__(self):
        ""
        s=Segments(Segment(Point(0,0),Point(1,0)),
                   Segment(Point(1,0),Point(1,1)))
        self.assertIsInstance(s,Segments)
        self.assertEqual(s._segments,
                         list((Segment(Point(0,0),Point(1,0)),
                               Segment(Point(1,0),Point(1,1)))))
        
        
    def test___eq__(self):
        ""
        s=Segments(Segment(Point(0,0),Point(1,0)),
                   Segment(Point(1,0),Point(1,1)))
        self.assertTrue(s==s)
        
        s1=Segments(Segment(Point(0,0),Point(1,0)),
                    Segment(Point(1,0),Point(1,1)))
        s1.append(Segment(Point(1,1),
                            Point(0,1)))
        self.assertFalse(s==s1)
        
                
        
    def test_add_all(self):
        ""
        # no additions
        s=Segments(Segment(Point(0,0),Point(1,0)),
                   Segment(Point(1,0),Point(1,1)))
        s.add_all()
        self.assertEqual(s,
                         Segments(Segment(Point(0,0),Point(1,0)),
                                  Segment(Point(1,0),Point(1,1))))
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
        s=Segments(Segment(Point(0,0),Point(1,0)),
                   Segment(Point(1,0),Point(1,1)))
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

    
    
    
    
if __name__=='__main__':
    
    unittest.main()