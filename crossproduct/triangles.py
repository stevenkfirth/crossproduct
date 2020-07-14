# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d

from collections.abc import Sequence
from .segments import Segments
from .points import Points
from .simple_polygons import SimplePolygons


class Triangles(Sequence):
    """A sequence of triangles   
    
    """
    
    def __init__(self,*triangles):
        """
        """
    
#        for tr in triangles:
#            if not isinstance(tr,Triangle):
#                raise TypeError
    
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
        return 'Triangles(%s)' % ', '.join([str(s) for s in self.triangles])
    
    
    def intersect_plane(self,plane):
        """Returns the intersection of this Triangles sequence with a plane
        """
        ipts=Points()
        isegments=Segments()
        
        for tr in self:
            
            result=tr.intersect_plane(plane)
            if result is None:
                continue
            elif result.classname=='Point':
                ipts.append(result,unique=True)
            elif result.classname=='Segment':
                isegments.append(result,unique=True)
            else:
                raise Exception
                
        return ipts, isegments
    
    
    def intersect_halfline(self,halfline):
        ""
        ipts=Points()
        isegments=Segments()
        
        for tr in self:
            result=tr.intersect_halfline(halfline)
            if result is None:
                continue
            if result.classname=='Point':
                ipts.append(result,unique=True)
            elif result.classname=='Segment':
                isegments.append(result,unique=True)
        
        return ipts, isegments
    
    
    def intersect_segment(self,segment):
        ""
        ipts=Points()
        isegments=Segments()
        
        for tr in self:
            result=tr.intersect_segment(segment)
            if result is None:
                continue
            if result.classname=='Point':
                ipts.append(result,unique=True)
            elif result.classname=='Segment':
                isegments.append(result,unique=True)
        
        return ipts, isegments
    
    
    def intersect_segments(self,segments):
        """Returns the intersection of this Triangles sequence with a Segments sequence
        """
        ipts=Points()
        isegments=Segments()
        
        for s in segments:
            result=self.intersect_segment(s)
            for pt in result[0]:
                ipts.append(pt,unique=True)
            for s in result[1]:
                isegments.append(s,unique=True)
                
        return ipts, isegments
        
    
    def intersect_simple_convex_polygon(self,simple_convex_polygon):
        """Returns the intersection of this Triangles sequence with a simple convex polygon
        """
        ipts=Points()
        isegments=Segments()
        isimplepolygons=SimplePolygons()
        
        for tr in self:
            #print('tr',tr)
            result=tr.intersect_simple_convex_polygon(simple_convex_polygon) # returns None, Point, Segment, SimpleConvexPolygon
            #print('result',result)
            if result is None:
                continue
            if result.classname=='Point':
                ipts.append(result,unique=True)
            elif result.classname=='Segment':
                isegments.append(result,unique=True)
            elif result.classname=='SimpleConvexPolygon':
                isimplepolygons.append(result)
                
        return ipts, isegments, isimplepolygons
    
            
    
    def intersect_triangle(self,triangle):
        """Returns the intersection of this Triangles sequence with another triangle
        """
        ipts=Points()
        isegments=Segments()
        isimplepolygons=SimplePolygons()
        
        for tr in self:
            result=tr.intersect_simple_convex_polygon(triangle) # returns None, Point, Segment, SimpleConvexPolygon
            if result is None:
                continue
            if result.classname=='Point':
                ipts.append(result,unique=True)
            elif result.classname=='Segment':
                isegments.append(result,unique=True)
            elif result.classname=='SimpleConvexPolygon':
                isimplepolygons.append(result)
                
        return ipts, isegments, isimplepolygons
        
        
    def intersect_triangles(self,triangles):
        """Returns the intersection of this Triangles sequence with another triangle sequence
        """
        ipts=Points()
        isegments=Segments()
        isimplepolygons=SimplePolygons()
        
        for tr in triangles:
            result=self.intersect_triangle(tr)
            for pt in result[0]:
                ipts.append(pt,unique=True)
            for s in result[1]:
                isegments.append(s,unique=True)
            for pg in result[2]:
                isimplepolygons.append(pg)
                
        return ipts, isegments, isimplepolygons
        
    
    def plot(self,ax=None,color='blue',**kwargs):
        ""
        if not ax:
            if self[0].__class__.__name__=='Triangle2D':
                fig, ax = plt.subplots()
            else:
                fig = plt.figure()
                ax = fig.add_subplot(111, projection='3d')
        for tr in self:
            tr.plot(ax,color=color,**kwargs)
        
        
    
        
        
        
        
        
        
        
        