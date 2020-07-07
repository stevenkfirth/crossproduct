# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

from collections.abc import Sequence
from .simple_convex_polygon import SimpleConvexPolygon
from .simple_polygons import SimplePolygons


class SimpleConvexPolygons(SimplePolygons):
    """A sequence of simple convex polygons   
    
    """
    
    def __init__(self,*simple_convex_polygons):
        """
        """
    
        for pg in simple_convex_polygons:
            if not isinstance(pg,SimpleConvexPolygon):
                raise TypeError
    
        self.simple_convex_polygons=list(simple_convex_polygons)
        
        
    def __eq__(self,obj):
        """
        """
        if isinstance(obj,SimpleConvexPolygons) and self.simple_convex_polygons==obj.simple_convex_polygons:
            return True
        else:
            return False
        
        
    def __getitem__(self,i):
        """
        """
        return self.simple_convex_polygons[i]
        
    
    def __len__(self):
        """
        """
        return len(self.simple_convex_polygons)
    
    
    def __repr__(self):
        """The string of this segment for printing
        
        :return result:
        :rtype str:
            
        """
        return 'SimpleConvexPolygons(%s)' % ', '.join([str(pg) for pg in self.simple_convex_polygons])
    
    
    
    
    