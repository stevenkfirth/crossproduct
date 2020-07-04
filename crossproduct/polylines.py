# -*- coding: utf-8 -*-

import itertools

from collections.abc import Sequence
from .segment import Segment
from .point import Point
from .points import Points
#from .simple_polygons import SimplePolygons


class Polylines(Sequence):
    """A sequence of polylines   
    
    """
    
    def __init__(self,*polylines):
        """
        """
    
        self.polylines=list(polylines)
        
        
    def __eq__(self,obj):
        """
        """
        if isinstance(obj,Polylines) and self.polylines==obj.polylines:
            return True
        else:
            return False
        
        
    def __getitem__(self,i):
        """
        """
        return self.polylines[i]
        
    
    def __len__(self):
        """
        """
        return len(self.polylines)
    
    
    def __repr__(self):
        """The string of this polyline for printing
        
        :return result:
        :rtype str:
            
        """
        return 'Polylines(%s)' % ', '.join([str(s) for s in self.polylines])
    
    
    def append(self,polyline,unique=False):
        """
        """
        if isinstance(polyline,polyline):
            if unique:
                if not polyline in self:
                    self.polylines.append(polyline)
            else:
                self.polylines.append(polyline)
                
        else:
            raise TypeError
    
    
    @property
    def consolidate(self):    
        """Returns a Polylines sequence with the same segments but a minimum number of polylines
        
        :return result: 
            - each polyline can have one or more segments
            - note there may be multiple solutions, only the first solution is returned
        
        :rtype Polylines
        
        """
        polylines=[pl for pl in self]
        n=len(polylines)
        i=0
        
        while i<n-1:
            
            pl=polylines[i]
            j=i+1
            
            while j<n:
                
                u=pl.union(polylines[j])
                
                if not u is None:
                    polylines[i]=u
                    polylines.pop(j)
                    break
                
                j+=1

            else:
                i+=1
                    
            n=len(polylines)
           
        return Polylines(*polylines)
        
    
    @property
    def simple_polygons(self):
        """Returns any polygons that exist in the Polylines sequence
        
        :return result: - a tuple of zero or more polygons
            - each polyline can have one or more than one segments
        
        """
        n=len(self)
        
        
        
        
        
        
        
        
        
        