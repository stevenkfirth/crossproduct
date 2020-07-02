# -*- coding: utf-8 -*-

from .point import Point
from .polyline import Polyline2D, Polyline3D


class SimplePolyline():
    """A n-D non-inersecting polyline
        
    """
    
    def __init__(self,*points):
        """
        
        param points: an array of points 
                    
        """
        
        for pt in points:
            if not isinstance(pt,Point):
                raise TypeError
        
        self.points=tuple(points)
        
        if self.is_intersecting:
            raise ValueError('A simple polyline cannot have self intersecting points')
                
    
        
class SimplePolyline2D(SimplePolyline,Polyline2D):
    """A 2-D polyline
    """
    
    def __repr__(self):
        """The string of this polyline for printing
        
        :return result:
        :rtype str:
            
        """
        return 'SimplePolyline2D(%s)' % ','.join([str(p) for p in self.points])
    
    
    
class SimplePolyline3D(SimplePolyline,Polyline3D):
    """A 3-D polyline
    """
    
    def __repr__(self):
        """The string of this polyline for printing
        
        :return result:
        :rtype str:
            
        """
        return 'SimplePolyline3D(%s)' % ','.join([str(p) for p in self.points])


    