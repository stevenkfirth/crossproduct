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
            

        
    def test__intersect_line(self):
        ""
        P0,vL=Point(0,0),Vector(1,1) 
        l=Line(P0,vL)        
        # collinear
        self.assertEqual(l._intersect_line(l),
                         l)        
        # parallel
        self.assertEqual(l._intersect_line(Line(P0+vL.perp_vector,vL)),
                         None)        
        # skew
        self.assertEqual(l._intersect_line(Line(P0,vL.perp_vector)),
                         P0)        
        # skew - different P0s
        self.assertEqual(l._intersect_line(Line(P0+vL,vL.perp_vector)),
                         P0+vL)
        
        P0,vL=Point(0,0,0),Vector(1,1,1) 
        l=Line(P0,vL)
        # collinear
        self.assertEqual(l._intersect_line(l),
                         l)
        # parallel
        self.assertEqual(l._intersect_line(Line(P0+Vector(1,-1,0),vL)),
                         None)
        #skew
        self.assertEqual(l._intersect_line(Line(P0,Vector(1,-1,0))),
                         P0)
        self.assertEqual(l._intersect_line(Line(P0+vL,Vector(1,-1,0))),
                         P0+vL)
        self.assertEqual(l._intersect_line(Line(Point(0,0,1),Vector(1,-1,0))),
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
    





    
    
    
    
if __name__=='__main__':
    
    unittest.main()