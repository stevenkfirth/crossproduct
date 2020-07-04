# -*- coding: utf-8 -*-

from collections.abc import Sequence
from .segment import Segment
from .point import Point
from .points import Points
from .simple_polygon import SimplePolygon


class SimplePolygons(Sequence):
    """A sequence of simple polygons   
    
    """
    
    def __init__(self,*simple_polygons):
        """
        """
    
        for pg in simple_polygons:
            if not isinstance(pg,SimplePolygon):
                raise TypeError
    
        self.simple_polygons=list(simple_polygons)
        
        
    def __eq__(self,obj):
        """
        """
        if isinstance(obj,SimplePolygons) and self.simple_polygons==obj.simple_polygons:
            return True
        else:
            return False
        
        
    def __getitem__(self,i):
        """
        """
        return self.simple_polygons[i]
        
    
    def __len__(self):
        """
        """
        return len(self.simple_polygons)
    
    
    def __repr__(self):
        """The string of this segment for printing
        
        :return result:
        :rtype str:
            
        """
        return 'SimplePolygons(%s)' % ', '.join([str(pg) for g in self.simple_polygons])
    
    
    def append(self,simple_polygons,unique=False):
        """
        """
        if isinstance(simple_polygons,SimplePolygon):
            if unique:
                if not simple_polygons in self:
                    self.simple_polygons.append(simple_polygons)
            else:
                self.simple_polygons.append(simple_polygons)
                
        else:
            raise TypeError
    
    
    
    
    
    