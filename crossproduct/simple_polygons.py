# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d

from collections.abc import Sequence
from .segments import Segments


class SimplePolygons(Sequence):
    """A sequence of simple polygons   
    
    """
    
    def __init__(self,*simple_polygons,validate=False):
        """
        """
    
        if validate:
            for pg in simple_polygons:
                print(pg.classname)
                if not pg.classname in ['Triangle',
                                        'Quadrilateral',
                                        'Parallelogram',
                                        'SimpleConvexPolygon',
                                        'SimplePolygon']:
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
        
        
        
        
    
    def append(self,simple_polygon,unique=False):
        """
        """
        if simple_polygon.classname in ['Triangle','Quadrilateral','Parallelogram','SimpleConvexPolygon','SimplePolygon']:
            if unique:
                if not simple_polygon in self:
                    self.simple_polygons.append(simple_polygon)
            else:
                self.simple_polygons.append(simple_polygon)
                
        else:
            raise TypeError
    
    
    def plot(self,ax=None,color='blue',**kwargs):
        ""
        if not ax:
            if self[0].__class__.__name__.endswith('2D'):
                fig, ax = plt.subplots()
            else:
                fig = plt.figure()
                ax = fig.add_subplot(111, projection='3d')
        for tr in self:
            tr.plot(ax,color=color,**kwargs)
    
    
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
        pg=self[0]
        remaining_polygons=SimplePolygons(*self[1:])
        while True:
            #print('---')
            #print('i',i)
            #print('pg',pg)
            #print('remaining_polygons',remaining_polygons)
            #print('result',result)
            try:
                pg,remaining_polygons=remaining_polygons.union_adjacent_simple_polygon(pg)
                
            except TypeError:
                result.append(pg)
                try:
                    pg=remaining_polygons[0]
                except IndexError:
                    break
                remaining_polygons=SimplePolygons(*remaining_polygons[1:])
        return result
    
    
    def union_adjacent_simple_polygon(self,polygon):
        """Returns the first adjacent union of a polygon in the sequence with the polyline
        
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
        
        
        
        
        
        
        
        
        
        
        
    