# -*- coding: utf-8 -*-

from .point import Point, Point2D, Point3D
from .convex_polygon import ConvexPolygon2D, ConvexPolygon3D
from .vector import Vector, Vector2D, Vector3D
from .quadrilateral import Quadrilateral2D, Quadrilateral3D


class Parallelogram():
    """A n-D parallelogram
    """
    
    def __init__(self,P0,v,w):
        """
        
        :param P0 Point: a point on the quadrilateral
        :param v Vector: a vector on the quadrilateral from P0 to P1
        :param w Vector: a vector on the quadrilateral from P0 to P3
        
        """
        
        if isinstance(P0,Point):
            self.P0=P0
        else:
            raise TypeError
            
        if isinstance(v,Vector):
            self.v=v
        else:
            raise TypeError
        
        if isinstance(w,Vector):
            self.w=w
        else:
            raise TypeError


    @property
    def P1(self):
        """Returns point P1
        
        :return point:
        :rtype Point2D
        
        """
        return self.P0+self.v
    
    
    @property
    def P2(self):
        """Returns point P2
        
        :return point:
        :rtype Point2D
        
        """
        return self.P0+self.v+self.w
    
    
    @property
    def P3(self):
        """Returns point P3
        
        :return point:
        :rtype Point2D
        
        """
        return self.P0+self.w
    
    
    def reorder(self,i):
        """Returns a triangle with reordered points
        
        :param i: the index of the start point
        
        """
        points=[]
        for _ in range(len(self.points)):
            points.append(self.points[i])
            i=self.next_index(i)
        return self.__class__(points[0],
                              points[1]-points[0],
                              points[3]-points[0])
        
    
    @property
    def reverse(self):
        """Return a polygon with the points reversed
        
        :return polygon:
        :rtype Polygon:
        """
        points=[self.points[i] 
                for i in range(len(self.points)-1,-1,-1)]
        return self.__class__(points[0],
                              points[1]-points[0],
                              points[3]-points[0])
        


class Parallelogram2D(Parallelogram,Quadrilateral2D):
    """A 2D parallelogram
    """
        
    def __repr__(self):
        """The string of this parallelogram for printing
        
        :return result:
        :rtype str:
            
        """
        return 'Parallelogram2D(%s, %s, %s)' % (self.P0,self.v,self.w)
        
    
    @property
    def signed_area(self):
        """Returns the signed area of the parallelogram
        
        :return result:
            - return value >0 if parallelogram points are ordered counterclockwise
            - return value <0 if parallelogram points are ordered clockwise
        :rtype float:
        
        
        """
        return self.v.x*self.w.y - self.w.x*self.v.y
    
    
    
    
class Parallelogram3D(Parallelogram,Quadrilateral3D):
    """A 3D parallelogram
    """
    
    def __repr__(self):
        """The string of this parallelogram for printing
        
        :return result:
        :rtype str:
            
        """
        return 'Parallelogram3D(%s, %s, %s)' % (self.P0,self.v,self.w)
        
    
    @property
    def area(self):
        """Returns the area of the parallelogram
        
        :return result:
        :rtype float:

        """
        return self.v.cross_product(self.w).length
        
    
    @property
    def class_2D(self):
        return Parallelogram2D  
    
    
    
        
        