# -*- coding: utf-8 -*-

import unittest
from crossproduct import Point, Points


class Test_Points(unittest.TestCase):
    
    def test___init__(self):
        ""
        pt=Point(0,0)
        pts=Points(pt)
        self.assertIsInstance(pts,
                              Points)
        self.assertEqual(pts[0],
                         pt)
        self.assertEqual(len(pts),
                         1)
        
        pt1=Point(1,1)
        pts.append(pt1)
        self.assertEqual(pts[1],
                         pt1)
        
        del pts[0]
        self.assertEqual(pts[0],
                         pt1)
        
        
    
    
    
    
    
    
    
if __name__=='__main__':
    
    unittest.main(Test_Points())
