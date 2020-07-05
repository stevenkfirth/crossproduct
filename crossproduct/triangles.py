# -*- coding: utf-8 -*-


from collections.abc import Sequence
from .segment import Segment
from .point import Point
from .points import Points
#from .simple_polygons import SimplePolygons


class Triangles(Sequence):
    """A sequence of triangles   
    
    """
    
    def __init__(self,*triangles):
        """
        """
    
        self.triangles=list(triangles)
        
        
    def __eq__(self,obj):
        """
        """
        if isinstance(obj,Triangles) and self.triangles==obj.triangles:
            return True
        else:
            return False
        
        
    def __getitem__(self,i):
        """
        """
        return self.triangles[i]
        
    
    def __len__(self):
        """
        """
        return len(self.triangles)
    
    
    def __repr__(self):
        """The string of this triangle for printing
        
        :return result:
        :rtype str:
            
        """
        return 'Truangles(%s)' % ', '.join([str(s) for s in self.triangles])
    
    
    def intersect_triangle(self):
        """Returns the intersection of this Triangles sequence with another triangle
        """
        
    def intersect_triangles(self):
        """Returns the intersection of this Triangles sequence with another triangle sequence
        """
        
    def union(self):
        """Returns the union of all triangles in the Triangles sequence
        """
    
        
        
        
        
        
        
        
        
        