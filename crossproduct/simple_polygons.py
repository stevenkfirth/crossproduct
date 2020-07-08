# -*- coding: utf-8 -*-

from collections.abc import Sequence
from .segment import Segment
from .point import Point
from .points import Points
from .simple_polygon import SimplePolygon
from .segments import Segments


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
        return 'SimplePolygons(%s)' % ', '.join([str(pg) for pg in self.simple_polygons])
    
    
    @property
    def adjacent_polygons(self):
        """Returns a list of SimplePolygon sequences containing polygons that are adjacent to each other
        
        
        """
        
        
        
        
    
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
    
    @property
    def segments(self):
        """Returns a Segments sequence of all the segments of the polygons
        """
        segments=Segments()
        for pg in self:
            for s in pg.polyline.segments:
                segments.append(s,unique=True)
        return segments
    
    
    @property
    def union_adjacent(self):
        """Returns the adjacent unions of the simple polygons
        
        :rtype: SimplePolygons
        """
        if len(self)==0:
            return self        
        
        result=SimplePolygons()
        i=0
        pg=self[0]
        remaining_polygons=SimplePolygons(*self[i+1:])
        while True:
            try:
                pg,remaining_polygons=remaining_polygons.union_adjacent_simple_polygon(pg)
            except TypeError:
                result.append(pg)
                i+=1
                try:
                    pg=remaining_polygons[i]
                except IndexError:
                    break
        return result
    
    
    def union_adjacent_simple_polygon(self,polygon):
        """Returns the first union of a polygon in the sequence with the polyline
        
        :return result: (union_result (SimplePolygon),
                         SimplePolygons sequence of remaining polygons)
        
        """
        pgs=[pg for pg in self]
        for i in range(len(pgs)):
            u=polygon.union_adjacent_simple_polygon(pgs[i])
            if u:
                pgs.pop(i)
                return u,SimplePolygons(*pgs)
    
        return None
        
        
        
        
        
        
        
        
        
        
        
    