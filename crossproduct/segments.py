# -*- coding: utf-8 -*-

from collections.abc import Sequence
from .segment import Segment
from .point import Point
from .points import Points


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
    
    
    
    