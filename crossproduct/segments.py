# -*- coding: utf-8 -*-

import itertools

from collections.abc import Sequence
from .segment import Segment
from .point import Point
from .points import Points
from .polyline import Polyline


class Segments(Sequence):
    """A sequence of segments    
    
    """
    
    def __init__(self,*segments):
        """
        """
    
        self.segments=list(segments)
        
        
    def __eq__(self,obj):
        """
        """
        if isinstance(obj,Segments) and self.segments==obj.segments:
            return True
        else:
            return False
        
        
        
    def __getitem__(self,i):
        """
        """
        return self.segments[i]
        
    
    def __len__(self):
        """
        """
        return len(self.segments)
    
    
    def __repr__(self):
        """The string of this segment for printing
        
        :return result:
        :rtype str:
            
        """
        return 'Segments(%s)' % ', '.join([str(s) for s in self.segments])
    
    
    def append(self,segment,unique=False):
        """
        """
        if isinstance(segment,Segment):
            if unique:
                if not segment in self:
                    self.segments.append(segment)
            else:
                self.segments.append(segment)
                
        else:
            raise TypeError
    
    
    def intersect_halfline(self,halfline):
        """Returns the intersection of this segments sequence and a halfline
        
        :param halfline Halfline: a halfline
        
        :return (ipts,isegments): (tuple of intersetion points, 
                                   tuple of intersection segments)
        :rtype tuple:
            
        """
        ipts=Points()
        isegments=Segments()
        for s in self:
            result=s.intersect_halfline(halfline)
            if isinstance(result,Point):
                ipts.append(result,unique=True)
            if isinstance(result,Segment):
                isegments.append(result,unique=True)
        
        # remove points which exist in the segments
        ipts.remove_points_in_segments(isegments)
        
        return ipts, isegments
    
    
    def intersect_line(self,line):
        """Returns the intersection of this segments sequence and a line
        
        :param line Line: a line
        
        :return (ipts,isegments): (tuple of intersetion points, 
                                   tuple of intersection segments)
        :rtype tuple:
            
        """
        ipts=Points()
        isegments=Segments()
        for s in self:
            result=s.intersect_line(line)
            if isinstance(result,Point):
                ipts.append(result,unique=True)
            if isinstance(result,Segment):
                isegments.append(result,unique=True)
        
        # remove points which exist in the segments
        ipts.remove_points_in_segments(isegments)
        
        return ipts, isegments
    
    
    def intersect_point(self,point):
        """Test if the point intersects with any of the segments
        
        :return result:
        :rtype bool:        
        
        """
        for s in self:
            if point in s:
                return True
        return False
    
    
    def intersect_segment(self,segment):
        """Returns the intersection of this segments sequence and a segment
        
        :param segment Segment: a segment
        
        :return (ipts,isegments): (tuple of intersetion points, 
                                   tuple of intersection segments)
        :rtype tuple:
            
        """
        ipts=Points()
        isegments=Segments()
        for s in self:
            result=s.intersect_segment(segment)
            if isinstance(result,Point):
                ipts.append(result,unique=True)
            if isinstance(result,Segment):
                isegments.append(result,unique=True)
        
        # remove points which exist in the segments
        ipts.remove_points_in_segments(isegments)
        
        return ipts, isegments
        
    
    def intersect_segments(self,segments):
        """Returns the intersection of this segments sequence and another segments sequence
        
        :param segments Segments: a segments sequence
        
        :return (ipts,isegments): (tuple of intersetion points, 
                                   tuple of intersection segments)
        :rtype tuple:
            
        """
        ipts=Points()
        isegments=Segments()
        for s in segments:
            result_ipts,result_isegments=self.intersect_segment(s)
            for pt in result_ipts:
                ipts.append(pt,unique=True)
            for s1 in result_isegments:
                isegments.append(s1,unique=True)
        
        # remove points which exist in the segments
        ipts.remove_points_in_segments(isegments)
        
        return ipts, isegments
    
    
    @property
    def polyline(self):
        """Returns a polyline of the segments
        
        :return result:
        :rtype: Polyline or None
        
        """
#        # first union
#        s=self[0]
#        try:
#            pl,remaining_segments=Segments(*self[1:]).union_segment(s)
#        except TypeError:
#            return None
        
        pl=self[0].polyline
        remaining_segments=Segments(*self[1:])
        
        while len(remaining_segments)>0:
            try:
                pl,remaining_segments=remaining_segments.union_polyline(pl)
            except TypeError:
                return None
            
        return pl
    
    
    def union_polyline(self,polyline):
        """Returns the first union of a segment in the sequence with the polyline
        
        :return result: (union_result (Polyline),
                         Segments sequence of remaining segments)
        
        """
        segments=[s for s in self]
        for i in range(len(segments)):
            u=polyline.union(segments[i].polyline)
            if u:
                segments.pop(i)
                return u,Segments(*segments)
    
        return None
    
    
    def union_segment(self,segment):
        """Returns the first union of a segment in the sequence with the supplied segment
        
        :return result: (union_result (Polyline),
                         Segments sequence of remaining segments)
        
        """
        segments=[s for s in self]
        for i in range(len(segments)):
            u=segments[i].union(segment)
            if u:
                segments.pop(i)
                return u,Segments(*segments)
    
        return None
    
    
    
#    @property
#    def polylines(self):    
#        """Returns the polylines that exist in the Segments sequence
#        
#        :return result: - 
#            - each polyline can have one or more than one segments
#        :rtype Polylines:
#        
#        """
#        
#        p=Polylines(*[s.polyline for s in self])
#        return p.consolidate
#    
#        
#        polylines=[s.polyline for s in self]
#        n=len(polylines)
#        i=0
#        
#        while i<n-1:
#            
#            pl=polylines[i]
#            j=i+1
#            
#            while j<n:
#                
#                u=pl.union(polylines[j])
#                
#                if not u is None:
#                    polylines[i]=u
#                    polylines.pop(j)
#                    break
#                
#                j+=1
#
#            else:
#                i+=1
#                    
#            n=len(polylines)
#           
#        return tuple(polylines)
#        
#    
#    @property
#    def polygons(self):
#        """Returns any polygons that exist in the Segments sequence
#        
#        :return result: - a tuple of zero or more polygons
#            - each polyline can have one or more than one segments
#        
#        """
#        
#        
#    @property
#    def self_union(self):
#        """Returns a new Segments sequence with the union of any segments if possible
#        
#        """
#        
        
        
        
        
        
        
        