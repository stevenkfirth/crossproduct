# -*- coding: utf-8 -*-

import itertools

from .point import Point
from .segment import Segment, Segment2D, Segment3D
from .segments import Segments


class Polyline():
    """A n-D polyline
    
    """
    
    def __init__(self,*points):
        """
        
        param points: an array of points 
                    
        """
        
        for pt in points:
            if not isinstance(pt,Point):
                raise TypeError
        
        self.points=tuple(points)
        
        
    def __eq__(self,polyline):
        """Tests if this polyline and the supplied polyline are equal
        
        :param polyline Polyline: a  polyline
        
        :return result: 
            - True if 
                - it has the same points, and the points are in the same order, 
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
        
        
    def intersect_polyline(self,polyline):
        """Returns the interesection of this polyline and another polyline
        
        :param polyline Polyline: a polyline
        
        :return (ipts,isegments): (tuple of intersetion points, 
                                   tuple of intersection segments)
        :rtype tuple:
            
        """
        return self.segments.intersect_segments(polyline.segments)
    
    
    def intersect_segment(self,segment):
        """Returns the interesection of this polyline and a segment
        
        :param segment Segment: a segment
        
        :return (ipts,isegments): (tuple of intersetion points, 
                                   tuple of intersection segments)
        :rtype tuple:
            
        """
        return self.segments.intersect_segment(segment)
    
        
    @property
    def is_intersecting(self):
        """Tests to see if the polyline is self intersecting
        
        :return result:
            - True if a polyline segment intersects another segment, 
                except for adjacent start and end points intersection
                and except for the start and end points of the polyline intersection
            - False otherwise
        :rtype bool:
        
        """
        for s in itertools.combinations(self.segments,2):
            result=s[0].intersect_segment(s[1])
            if isinstance(result,Segment):
                return True
            elif isinstance(result,Point):
                if result==s[0].P0 or result==s[0].P1:
                    pass
                else:
                    return True
        return False
        
        
    @property
    def reverse(self):
        """Return a polyline with the points reversed
        
        :return polyline:
        :rtype SimplePolyline:
        """
        points=[self.points[i] 
                for i in range(len(self.points)-1,-1,-1)]
        return self.__class__(*points)
    
    
    def union(self,polyline):
        """Returns the union of this polyline and another polyline
        
        :param polyline SimplePolyline: a polyline
            - for the union of a polyline and a segment, first convert the segment to a 1-item polyline
        
        :return result:
            - Polyline, the union of the polylines if they have 
                a same start point or end point
            - None, for polylines that don't have a union        
        
        Note: - this may return a polyline with two adjacent segments that are collinear
        
        """
        
        
        if self.points[-1]==polyline.points[0]:
            return self.__class__(*self.points,*polyline.points[1:])
        elif self.points[-1]==polyline.points[-1]:
            return self.__class__(*self.points,*polyline.reverse.points[1:])
        elif self.points[0]==polyline.points[-1]:
            return self.__class__(*polyline.points,*self.points[1:])
        elif self.points[0]==polyline.points[0]:
            return self.__class__(*polyline.reverse.points,*self.points[1:])
        else:
            return None
        
        
    
    
    
class Polyline2D(Polyline):
    """A 2D polyline
    
    """
    
    def __repr__(self):
        """The string of this polyline for printing
        
        :return result:
        :rtype str:
            
        """
        return 'Polyline2D(%s)' % ','.join([str(p) for p in self.points])
    
    
    def plot(self,ax,**kwargs):
        """Plots the polyline on the supplied axes
        
        :param ax matplotlib.axes.Axes: an Axes instance
        :param **kwargs: keyword arguments to be supplied to the Axes.plot call
                    
        
        """
        x=[p.x for p in self.points]
        y=[p.y for p in self.points]
        ax.plot(x,y,**kwargs)
        
    
    @property
    def segments(self):
        """Returns a Segments sequence of the segments in the polyline
        
        :return result: 
        :rtype Segments:
        
        """
        n=len(self.points)
        return Segments(*[Segment2D(self.points[i],self.points[i+1]) for i in range(n-1)])
    
    
    
class Polyline3D(Polyline):
    """A 3D polyline
    
    """
    
    def __repr__(self):
        """The string of this polyline for printing
        
        :return result:
        :rtype str:
            
        """
        return 'Polyline3D(%s)' % ','.join([str(p) for p in self.points])
    
    
    def plot(self,ax,**kwargs):
        """Plots the segment on the supplied axes
        
        :param ax mpl_toolkits.mplot3d.axes3d.Axes3D: an Axes3D instance
        :param **kwargs: keyword arguments to be supplied to the Axes3D.plot call
                    
        
        """
        x=[p.x for p in self.points]
        y=[p.y for p in self.points]
        z=[p.z for p in self.points]
        ax.plot(x,y,z,**kwargs)


    @property
    def segments(self):
        """Returns a Segments sequence of the segments in the polyline
        
        :return result: 
        :rtype Segments:
        
        """
        n=len(self.points)
        return Segments(*[Segment3D(self.points[i],self.points[i+1]) for i in range(n-1)])
    
    
    
    
    
    