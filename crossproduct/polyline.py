# -*- coding: utf-8 -*-

import itertools

from .points import Points
from .segment import Segment2D, Segment3D
from .segments import Segments

class Polyline():
    """A n-D polyline
    
    """
    
    classname='Polyline'
    
    def __init__(self,*points):
        ""
        self._points=Points(*points)
        
        
    def __add__(self,polyline):
        """Returns the addition of this polyline and another polyline.
        
        :param polyline: A polyline.
        :type polyline: Polyline2D, Polyline3D
            
        :return: A new polyline which is the sum of the two polylines.
            If the polylines are not adjacent (i.e share start/end points)
            then ValueError is raised.
        :rtype: Polyline2D, Polyline3D
        
        :Example:
    
        .. code-block:: python
           
           # 2D example
           >>> pl1 = Polyline2D(Point2D(0,0), Point2D(1,0), Point2D(1,1))
           >>> pl2 = Polyline2D(Point2D(1,1), Point2D(1,2), Point2D(2,2))
           >>> result = pl1 + pl2
           >>> print(result)
           Polyline2D(Point2D(0,0), Point2D(0,1), Point2D(1,1), Point2D(1,2), Point2D(2,2))
        
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
            raise ValueError('To add two polylines, they must have a shared start or end point.')
        
        
    def __contains__(self,obj):
        """Tests if the polyline contains the geometric object.
        
        :param obj: A point. 
        :type obj: Point2D, Point3D.
            
        :return: For point, True if the point lies on one of the segments of the polyline;
            otherwise False.
        :rtype: bool
            
        """
        if obj.classname=='Point':
            
            for s in self.segments:
                
                if obj in s:
                    
                    return True
                
            return False
                    
        else:
            
            return TypeError
        
        
        
    def __eq__(self,polyline):
        """Tests if this polyline and the supplied polyline are equal.
        
        :param polyline: A polyline.
        :type polyline: Polyline2D, Polyline3D
        
        :return: True if the polylines have the same points in the same order, 
            either as supplied or in reverse;
            otherwise False.
        :rtype: bool
        
        :Example:
    
        .. code-block:: python
           
           # 2D example
           >>> pl = Polyline2D(Point2D(0,0), Point2D(1,0), Point2D(1,1))
           >>> result = pl == pl
           >>> print(result)
           True
           
           # 3D example
           >>> pl1 = Polyline3D(Point3D(0,0,0), Point3D(1,0,0))
           >>> pl2 = Polyline3D(Point3D(0,0,0), Point3D(-1,0,0))
           >>> result = pl1 == pl2
           >>> print(result)
           False
            
        """
        
        if isinstance(polyline,Polyline):
            
            if self._points==polyline._points or self._points==polyline.reverse._points:
                return True
            else:
                return False
            
        else:
            return False
    
    
    # @property
    # def merge_codirectional_segments(self):
    #     """Returns a polyline with all codirectional adjacent segments merged
        
    #     :return polyline:
    #         - looks at the segments of the polyline
    #         - if any two adjacent segments are codirectional, then these
    #             are replaced by a single segment
    #     :rtype Polyline:
            
    #     """
    #     points=[pt for pt in self.points]
    #     n=len(points)
    #     i=1
    #     while i<n-1:
    #         v=points[i]-points[i-1]
    #         w=points[i+1]-points[i]
    #         if v.is_codirectional(w):
    #             points.pop(i)
    #             n=len(points)
    #         else:
    #             i+=1
            
    #     return self.__class__(*points)
        
        
    def intersect_polyline(self,polyline):
        """Returns the intersection of this polyline and another polyline.
        
        :param polyline: A polyline.
        :type polyline: Polyline2D, Polyline3D
        
        :return: A tuple of intersection points and intersection segments 
            (Points,Segments)
        :rtype: tuple
        
        """
        return self.segments.intersect_segments(polyline.segments)
    
    
    def intersect_segment(self,segment):
        """Returns the intersection of this polyline and a segment.
        
        :param segment: A segment.
        :type segment: Segment2D, Segment3D
        
        :return: A tuple of intersection points and intersection segments 
            (Points,Segments)
        :rtype: tuple
            
        """
        return self.segments.intersect_segment(segment)
    
        
    @property
    def is_intersecting(self):
        """Tests to see if the polyline is self intersecting.
        
        :return: True if a polyline segment intersects another segment, 
            except for adjacent start and end points intersection
            and except for the start and end points of the polyline intersection;
            otherwise False.
        :rtype: bool
        
        """
        for s in itertools.combinations(self.segments,2):
            #print(s)
            result=s[0].intersect_segment(s[1])
            if result is None:
                continue
            elif result.classname=='Segment':
                return True
            elif result.classname=='Point':
                if result==s[0].P0 or result==s[0].P1:
                    pass
                else:
                    return True
        return False
        
    
    @property
    def points(self):
        """The points of the polyline.
        
        :rtype: Points
        
        """
        return self._points
    
        
    @property
    def reverse(self):
        """Return a polyline with the points reversed.
        
        :return: 
        :rtype: SimplePolyline
        
        """
        points=[self.points[i] 
                for i in range(len(self.points)-1,-1,-1)]
        return self.__class__(*points)
    
    
    
class Polyline2D(Polyline):
    """A two dimensional polyline, situated on an x, y plane.
    
    A polyline is a series of linked segments.
    
    :param points: A sequence of points.
        
    :Example:
    
    .. code-block:: python
       
       >>> pl = Polyline2D(Point2D(0,0), Point2D(1,0), Point2D(1,1))
       >>> print(pl)
       Polyline2D(Point2D(0,0), Point2D(1,0), Point2D(1,1))
    
    """
    
    def __repr__(self):
        ""
        return 'Polyline2D(%s)' % ','.join([str(p) for p in self.points])
    
    
    @property
    def dimension(self):
        """The dimension of the polyline.
        
        :return: '2D'
        :rtype: str
        
        :Example:
    
        .. code-block:: python
        
            >>> s = Polyline2D(Point2D(0,0), Point2D(1,0))
            >>> print(s.dimension)
            '2D'     
        
        """
        return '2D'
    

    def plot(self,ax,**kwargs):
        """Plots the polyline on the supplied axes.
        
        :param ax: An Axes instance.
        :type ax: matplotlib.axes.Axes
        :param kwargs: keyword arguments to be supplied to the Axes.plot call
                    
        """
        x=[p.x for p in self.points]
        y=[p.y for p in self.points]
        ax.plot(x,y,**kwargs)
        
    
    @property
    def segments(self):
        """Returns a Segments sequence of the segments in the polyline.
        
        :rtype: Segments
        
        :Example:
    
        .. code-block:: python
           
           >>> pl = Polyline2D(Point2D(0,0), Point2D(1,0), Point2D(1,1))
           >>> print(pl.segments)
           Segments(Segment2D(Point2D(0,0), Point2D(1,0)), 
                    Segment2D(Point2D(1,0), Point2D(1,1))
        
        """
        n=len(self.points)
        return Segments(*[Segment2D(self.points[i],self.points[i+1]) for i in range(n-1)])
    
    
    # def union(self,polyline):
    #     """Returns the union of this polyline and another polyline
        
    #     :param polyline SimplePolyline: a polyline
    #         - for the union of a polyline and a segment, first convert the segment to a 1-item polyline
        
    #     :return result:
    #         - Polyline, the union of the polylines if they have 
    #             a same start point or end point
    #         - None, for polylines that don't have a union        
        
    #     Note: - this may return a polyline with two adjacent segments that are collinear
        
    #     """
        
        
    #     if self.points[-1]==polyline.points[0]:
    #         return Polyline2D(*self.points,*polyline.points[1:])
    #     elif self.points[-1]==polyline.points[-1]:
    #         return Polyline2D(*self.points,*polyline.reverse.points[1:])
    #     elif self.points[0]==polyline.points[-1]:
    #         return Polyline2D(*polyline.points,*self.points[1:])
    #     elif self.points[0]==polyline.points[0]:
    #         return Polyline2D(*polyline.reverse.points,*self.points[1:])
    #     else:
    #         return None
    
    
    
class Polyline3D(Polyline):
    """A three dimensional polyline, situated on an x, y, z plane.
    
    A polyline is a series of linked segments.
    
    :param points: A sequence of points.
        
    :Example:
    
    .. code-block:: python
       
       >>> pl = Polyline3D(Point3D(0,0,0), Point3D(1,0,0), Point3D(1,1,0))
       >>> print(pl)
       Polyline3D(Point3D(0,0,0), Point3D(1,0,0), Point3D(1,1,0))
    
    """
    
    def __repr__(self):
        ""
        return 'Polyline3D(%s)' % ','.join([str(p) for p in self.points])
    
    
    @property
    def dimension(self):
        """The dimension of the polyline.
        
        :return: '3D'
        :rtype: str
        
        :Example:
    
        .. code-block:: python
        
            >>> s = Polyline3D(Point3D(0,0,0), Point3D(0,0,1))
            >>> print(s.dimension)
            '3D'     
        
        """
        return '3D'
    
    
    def plot(self,ax,**kwargs):
        """Plots the segment on the supplied axes.
        
        :param ax: An Axes3D instance.
        :type ax: mpl_toolkits.mplot3d.axes3d.Axes3D
        :param kwargs: keyword arguments to be supplied to the Axes3D.plot call
                    
        """
        x=[p.x for p in self.points]
        y=[p.y for p in self.points]
        z=[p.z for p in self.points]
        ax.plot(x,y,z,**kwargs)


    @property
    def segments(self):
        """Returns a Segments sequence of the segments in the polyline.
        
        :rtype: Segments
        
        :Example:
    
        .. code-block:: python
           
           >>> pl = Polyline3D(Point3D(0,0,0), Point3D(1,0,0), Point3D(1,1,0))
           >>> print(pl.segments)
           Segments(Segment3D(Point3D(0,0,0), Point3D(1,0,0)), 
                    Segment3D(Point3D(1,0,0), Point3D(1,1,0))
        
        """
        n=len(self.points)
        return Segments(*[Segment3D(self.points[i],self.points[i+1]) for i in range(n-1)])
    
    
    # def union(self,polyline):
    #     """Returns the union of this polyline and another polyline
        
    #     :param polyline SimplePolyline: a polyline
    #         - for the union of a polyline and a segment, first convert the segment to a 1-item polyline
        
    #     :return result:
    #         - Polyline, the union of the polylines if they have 
    #             a same start point or end point
    #         - None, for polylines that don't have a union        
        
    #     Note: - this may return a polyline with two adjacent segments that are collinear
        
    #     """
        
        
    #     if self.points[-1]==polyline.points[0]:
    #         return Polyline3D(*self.points,*polyline.points[1:])
    #     elif self.points[-1]==polyline.points[-1]:
    #         return Polyline3D(*self.points,*polyline.reverse.points[1:])
    #     elif self.points[0]==polyline.points[-1]:
    #         return Polyline3D(*polyline.points,*self.points[1:])
    #     elif self.points[0]==polyline.points[0]:
    #         return Polyline3D(*polyline.reverse.points,*self.points[1:])
    #     else:
    #         return None
    
    
    