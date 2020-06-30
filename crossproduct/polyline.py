# -*- coding: utf-8 -*-

from .point import Point
from .segment import Segment, Segment2D, Segment3D



class Polyline():
    """A n-D polyline
    """
    
    def __init__(self,*points):
        """
        
        param points: an array of points 
            - the first point is not repeated at the end of the array
        
        """
        
        for pt in points:
            if not isinstance(pt,Point):
                raise TypeError
        
        self.points=tuple(points)
        
        
    def __eq__(self,polyline):
        """Tests if this polygon and the supplied polygon are equal
        
        :param line Polygon2D: a 2D polygon
        
        :return result: 
            - True if 
                - it has the same points, and
                - the points are in the same order (from an arbitrary start point), 
                    either forward or reversed      
            - otherwise False
        :rtype bool:
            
        """
        if isinstance(polyline,Polyline):
            
            if self.points==polyline.points or self.points==polyline.reverse.points:
                
                return True
            
            else:
            
                return False
            
            
        else:
            return False
        
        
    @property
    def reverse(self):
        """Return a polyline with the points reversed
        
        :return polyline:
        :rtype Polyline:
        """
        points=[self.points[i] 
                for i in range(len(self.points)-1,-1,-1)]
        return self.__class__(*points)
    
        
        
class Polyline2D(Polyline):
    """A 2-D polyline
    """
    
    def __repr__(self):
        """The string of this polyline for printing
        
        :return result:
        :rtype str:
            
        """
        return 'Polyline2D(%s)' % ','.join([str(p) for p in self.points])
    
    @property
    def segments(self):
        """Returns a list of segments in the polyline
        
        :return list: a list of segments
        """
        n=len(self.points)
        return tuple(Segment2D(self.points[i],self.points[i+1]) for i in range(n-1))
        
    
class Polyline3D(Polyline):
    """A 3-D polyline
    """
    
    def __repr__(self):
        """The string of this polyline for printing
        
        :return result:
        :rtype str:
            
        """
        return 'Polyline3D(%s)' % ','.join([str(p) for p in self.points])


    @property
    def segments(self):
        """Returns a list of segments in the polyline
        
        :return list: a list of segments
        """
        n=len(self.points)
        return tuple(Segment3D(self.points[i],self.points[i+1]) for i in range(n-1))