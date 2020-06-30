# -*- coding: utf-8 -*-

from .point import Point, Point2D, Point3D
from .convex_polygon import ConvexPolygon2D, ConvexPolygon3D
from .vector import Vector2D, Vector3D


class Quadrilateral():
    """A n-D quadrilateral
    """
    
    def __init__(self,P0,P1,P2,P3):
        """
        
        :param P0 Point2D: point P0 on the quadrilateral
        :param P1 Point2D: point P1 on the quadrilateral
        :param P2 Point2D: point P2 on the quadrilateral
        :param P3 Point2D: point P3 on the quadrilateral
        
        """
        
        if isinstance(P0,Point):
            self.P0=P0
        else:
            raise TypeError
            
        if isinstance(P1,Point):
            self.P1=P1
        else:
            raise TypeError
            
        if isinstance(P2,Point):
            self.P2=P2
        else:
            raise TypeError
            
        if isinstance(P3,Point):
            self.P3=P3
        else:
            raise TypeError
            
    
    @property
    def points(self):
        """Returns point P0, P1, P2 and P3
        
        :return result:
        :rtype tuple:
        
        """
        return (self.P0,
                self.P1,
                self.P2,
                self.P3)
    


class Quadrilateral2D(Quadrilateral,ConvexPolygon2D):
    """"A 2D Quadrilateral
    """
        
    def __repr__(self):
        return 'Quadrilateral2D(%s, %s, %s, %s)' % (self.P0,self.P1,self.P2,self.P3)
        
        
    @property
    def area(self):
        """Returns the area of the quadrilateral
        
        :return result:
        :rtype float:

        """
        return abs(self.signed_area)
            
        
    @property
    def orientation(self):
        """Returns the orientation of a 2D quadrilateral
        
        :return result: 
            - >0 for counterclockwise
            - =0 for none (degenerate)
            - <0 for clockwise
        :rtype float: 
        """
        return self.signed_area
    
    
    @property
    def signed_area(self):
        """Returns the signed area of the quadrilateral
        
        :return result:
            - return value >0 if quadrilateral points are ordered counterclockwise
            - return value <0 if quadrilateral points are ordered clockwise
        :rtype float:
        
        
        """
        return 0.5* ((self.P2.x-self.P0.x)*(self.P3.y-self.P1.y) 
                     - (self.P3.x-self.P1.x)*(self.P2.y-self.P0.y))
        
        
        
class Quadrilateral3D(Quadrilateral,ConvexPolygon3D):
    """"A 3D Quadrilateral
    """        
        
    def __repr__(self):
        return 'Quadrilateral3D(%s, %s, %s, %s)' % (self.P0,self.P1,self.P2,self.P3)
        
        
    @property
    def area(self):
        """Returns the area of the quadrilateral
        
        :return result:
        :rtype float:

        """
        return 0.5 * (self.P2-self.P0).cross_product(self.P3-self.P1).length
               
   
    @property
    def class_2D(self):
        return Quadrilateral2D  
        