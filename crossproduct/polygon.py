# -*- coding: utf-8 -*-

from .simple_polygon import SimplePolygon2D, SimplePolygon3D

class Polygon():
    """A n-D polygon
    
    Polygon cannot self intersect but it can have holes
    
    """
    
    def __init__(self,points,holes):
        """
        
        param points: an array of points 
            - the first point is not repeated at the end of the array
        Param holes SimplePolygons: a sequence of simple polygons
        
        """
        
        for pt in points:
            if pt.classname=='Point':
                raise TypeError
        
        self.points=tuple(points)
        
        self.triangles=self.triangulate
        
        for h in holes:
            if not h.classname=='SimplePolygon':
                raise TypeError
                    
        self.holes=holes
        
        
    @property
    def area(self):
        """
        """
        a=self.simple_polygon.area
        for h in self.holes:
            a-=h.area
        return a
        
    
    
class Polygon2D(Polygon,SimplePolygon2D):
    """A 2D polygon
    """
    
    @property
    def simple_polygon(self):
        """
        """
        return Polygon2D(*self.points)
    
    
    
class Polygon3D(Polygon,SimplePolygon3D):
    """A 3D Polygon
    """
    
    @property
    def simple_polygon(self):
        """
        """
        return Polygon3D(*self.points)
    
    
    
    