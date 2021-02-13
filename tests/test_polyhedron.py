# -*- coding: utf-8 -*-

import unittest
from crossproduct import Point, Vector, Polygon, Polyhedron

class Test_Polyhedron(unittest.TestCase):
    
    def test___eq__(self):
        ""
        ph=Polyhedron(Polygon(Point(0.0,0.0,3.0),Point(0.0,10.0,3.0),Point(10.0,10.0,3.0),Point(10.0,0.0,3.0)),
                      Polygon(Point(10.0,0.0,6.0),Point(10.0,10.0,6.0),Point(0.0,10.0,6.0),Point(0.0,0.0,6.0)),
                      Polygon(Point(0.0,0.0,6.0),Point(0.0,10.0,6.0),Point(0.0,10.0,3.0),Point(0.0,0.0,3.0)),
                      Polygon(Point(0.0,10.0,6.0),Point(10.0,10.0,6.0),Point(10.0,10.0,3.0),Point(0.0,10.0,3.0)),
                      Polygon(Point(10.0,10.0,6.0),Point(10.0,0.0,6.0),Point(10.0,0.0,3.0),Point(10.0,10.0,3.0)),
                      Polygon(Point(10.0,0.0,6.0),Point(0.0,0.0,6.0),Point(0.0,0.0,3.0),Point(10.0,0.0,3.0)))
        
        print(ph==ph)
        
        

        
        
if __name__=='__main__':
    
    unittest.main(Test_Polyhedron())