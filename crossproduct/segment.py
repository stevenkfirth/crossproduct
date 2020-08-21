# -*- coding: utf-8 -*-

from .point import Point, Point2D
from .points import Points
from .line import Line2D, Line3D
from .segments import Segments

SMALL_NUM=0.00000001


class Segment():
    "A n-D segment"
    
    classname='Segment'
    
    def __init__(self,P0,P1):
        ""        
        if P0==P1:
            raise ValueError('P0 and P1 cannot be equal for a segment')
        
        if isinstance(P0, Point):
            self._P0=P0
        else:
            raise TypeError
            
        if isinstance(P1, Point):
            self._P1=P1
        else:
            raise TypeError
    
    
    def __add__(self,segment):
        """Adds this segment to the supplied segment
        
        :param segment: A segment.
        :type segment: Segment2D, Segment3D
        
        :raises ValueError: If the segments are not collinear,
            do not share a start or end point,
            or if they overlap.            
        
        :return: A new segment which is the sum of the two segments.
        :rtype: Segment2D, Segment3D
        
        :Example:
    
        .. code-block:: python
           
           # 2D example
           >>> s1 = Segment2D(Point2D(0,0), Point2D(1,0))
           >>> s2 = Segment2D(Point2D(1,0), Point2D(2,0))
           >>> result = s1 + s2
           >>> print(result)
           Segment2D(Point2D(0,0), Point2D(2,0))
           
           # 3D example
           >>> s1 = Segment3D(Point2D(1,0,0), Point3D(0,0,0))
           >>> s2 = Segment3D(Point3D(0,0,0), Point3D(-1,0,0))
           >>> result = s1 + s2
           >>> print(result)
           Segment3D(Point3D(-1,0,0), Point3D(1,0,0))       
        
        """
        if not self.line==segment.line:
            
            raise ValueError('To add two segments, they must be collinear')
            
        s1=self.order
        s2=segment.order
        
        #print(s1)
        #print(s2)
        
        if not (s1.P1==s2.P0 or s1.P0==s2.P1):
            
            raise ValueError('To add two segments, they must have a shared start or end point and not overlap')
            
        line=self.line
        t_values=[line.calculate_t_from_point(self.P0),
                  line.calculate_t_from_point(self.P1),
                  line.calculate_t_from_point(segment.P0),
                  line.calculate_t_from_point(segment.P1)]
        return self.__class__(line.calculate_point(min(t_values)),
                              line.calculate_point(max(t_values)))
    
    
    def __contains__(self,obj):
        """Tests if the segment contains the object.
        
        :param obj: A point or segment. 
        :type obj: Point2D, Point3D, Segment2D, Segment3D
            
        :return: For point, True if the point lies on the segment; otherwise False. 
            For segment, True if the segment start and endpoints are on the segment; otherwise False. 
        :rtype: bool
        
        :Example:
    
        .. code-block:: python
           
           # 2D example
           >>> s = Segment2D(Point2D(0,0), Point2D(1,0))
           >>> result = Point2D(2,0) in l
           >>> print(result)
           False
           
           # 3D example
           >>> s1 = Segment3D(Point2D(0,0,0), Point3D(1,0,0))
           >>> s2 = Segment3D(Point3D(0,0,0), Point3D(0.5,0,0))
           >>> result = s2 in s1
           >>> print(result)
           True        
        
        """
        if isinstance(obj,Point):
            
            t=self.line.calculate_t_from_point(obj)
            try:
                pt=self.calculate_point(t)  
            except ValueError: # t<0<1
                return False
            return obj==pt 
        
        if isinstance(obj,Segment):
            
            return obj.P0 in self and obj.P1 in self
            
        else:
            return TypeError()


    def __eq__(self,segment):
        """Tests if this segment and the supplied segment are equal.
        
        :param segment: A segment.
        :type segment: Segment2D, Segment3D
        
        :return: True if the segments have the same start point and the same end point; 
            else True if the start point of one is the end point of the other, and vice versa;
            otherwise False.
        :rtype: bool
        
        :Example:
    
        .. code-block:: python
           
           # 2D example
           >>> s = Segment2D(Point2D(0,0), Point2D(1,0))
           >>> result = s == s
           >>> print(result)
           True
           
           # 3D example
           >>> s1 = Segment3D(Point3D(0,0,0), Point3D(1,0,0))
           >>> s2 = Segment3D(Point3D(0,0,0), Point3D(-1,0,0))
           >>> result = s1 == s2
           >>> print(result)
           False
            
        """
        if isinstance(segment,Segment):
            return ((self.P0==segment.P0 and self.P1==segment.P1) or
                    (self.P0==segment.P1 and self.P1==segment.P0))
        else:
            return False


    def calculate_point(self,t):
        """Returns a point on the segment for a given t value.
        
        :param t: The t value.
        :type t: float
        
        :return: A point on the segment based on the t value.
        :rtype: Point2D, Point3D
        
        :Example:
        
        .. code-block:: python    
        
           # 2D example
           >>> s = Segment2D(Point2D(0,0), Point2D(1,0))
           >>> result = s.calcuate_point(0.5)
           >>> print(result)
           Point2D(0.5,0)
           
           # 3D example
           >>> s = Segment3D(Point3D(0,0,0), Point3D(1,0,0))
           >>> result = s.calcuate_point(0)
           >>> print(result)
           Point3D(0,0,0)
                
        """
        if t>=0 and t<=1:
            return self.line.calculate_point(t)
        else:
            raise ValueError('For a segment, t must be equal to or between 0 and 1')
            
            
    def difference_segment(self,segment):
        """Returns the difference of two segments.
        
        :param segment: A segment.
        :type segment: Segment2D, Segment3D
            
        :return: A segments sequence of 0, 1 or 2 segments.
            Returns an empty segments sequence if the supplied segment is equal to or contains this segment.
            Returns a segments sequence with this segment if the supplied segment does not intersect this segment.
            Returns a segments sequence with a new segment if the supplied segment intersects this segment 
            including either one of the start point or end point.
            Returns a segment sequence with two new segments if the supplied segment intersects this segment
            and is contained within it.
        :rtype: Segments
        
        :Example:
        
        .. code-block:: python    
        
           # 2D example
           >>> s1 = Segment2D(Point2D(0,0), Point2D(1,0))
           >>> s2 = Segment2D(Point2D(0.5,0), Point2D(1,0))
           >>> result = s1.difference_segment(s2)
           >>> print(result)
           Segments(Segment2D(Point2D(0,0), Point2D(0.5,0)))
           
           # 3D example
           >>> s1 = Segment3D(Point3D(0,0,0), Point3D(1,0,0))
           >>> s2 = Segment3D(Point3D(-1,0,0), Point3D(2,0,0))
           >>> result = s1.difference_segment(s2)
           >>> print(result)
           Segments()               
        
        """
        if self in segment:
            return Segments()
        
        if self.line==segment.line:
            t0=self.line.calculate_t_from_point(segment.P0)
            t1=self.line.calculate_t_from_point(segment.P1)
            if t1<t0:
                t0,t1=t1,t0
            
            if t0>=1 or t1<=0:
                return Segments(self)
            elif t0>=0 and t1>=1:
                return Segments(self.__class__(self.calculate_point(0),
                                               self.calculate_point(t0)),)
            elif t0<=0 and t1<=1:
                return Segments(self.__class__(self.calculate_point(t1),
                                               self.calculate_point(1)),)
            else:
                return Segments(self.__class__(self.calculate_point(0),
                                               self.calculate_point(t0)),
                        self.__class__(self.calculate_point(t1),
                                       self.calculate_point(1)))
        else:
            return Segments(self)
        
        
    def difference_segments(self,segments):
        """Returns the difference between this segment and a segments sequence.
        
        :param segments: A segments sequence.
        :type segments: Segments
        
        :return: Any parts of this segment which are not also part of the segments in the sequence.
        :rtype: Segments
        
        :Example:
        
        .. code-block:: python    
        
           # 2D example
           >>> s = Segment2D(Point2D(0,0), Point2D(1,0))
           >>> sgmts = Segments(Segment2D(Point2D(0.2,0), Point2D(0.8,0))
           >>> result = s.difference_segments(sgmts)
           >>> print(result)
           Segments(Segment2D(Point2D(0,0), Point2D(0.2,0)),
                    Segment2D(Point2D(0.8,0),Point2D(1,0)))
           
           # 3D example
           >>> s = Segment3D(Point3D(0,0,0), Point3D(1,0,0))
           >>> sgmts = Segments(Segment3D(Point3D(-1,0,0), Point3D(2,0,0))
           >>> result = s.difference_segment(sgmts)
           >>> print(result)
           Segments()               
        
        """
        def rf(result,segments):
            if len(segments)==0:
                return result
            else:
                diff=result.difference_segment(segments[0])
                #print('diff',diff)
                if len(diff)==0:
                    return None
                elif len(diff)==1:
                    if len(segments)>1:
                        result=rf(diff[0],segments[1:])
                    else:
                        result=diff[0],
                    return result
                elif len(diff)==2:
                    if len(segments)>1:
                        result=tuple(list(rf(diff[0],segments[1:]))+list(rf(diff[1],segments[1:])))
                    else:
                        result=diff[0],diff[1]
                    return result
                else:
                    raise Exception
                
        result=self
        result=rf(result,segments)
        
        if result is None:
            return Segments()
        else:
            return Segments(*result)        
        
            
    def distance_to_point(self,point):
        """Returns the distance from the segment to the supplied point.
        
        :param point: A point.
        :type point: Point2D, Point3D
        
        :return: The distance between the segment and the point.
        :rtype: float
        
        :Example:
    
        .. code-block:: python
           
           # 2D example
           >>> s = Segment2D(Point2D(0,0), Point2D(1,0))
           >>> result = s.distance_to_point(Point2D(0,10))
           >>> print(result)
           10
           
           # 3D example
           >>> s = Segment3D(Point3D(0,0,0), Point3D(1,0,0))
           >>> result = s.distance_to_point(Point3D(10,0,0))
           >>> print(result)
           9
            
        """
        v=self.line.vL
        w=point-self.P0
        c1=v.dot(w)
        c2=v.dot(v)
        
        if c1<=0: # i.e. t<0
            return w.length
        elif c2<=c1: # i.e. T>0
            return (point-self.P1).length
        else:
            return self.line.distance_to_point(point)
    

    def intersect_line(self,line):
        """Returns the intersection of this segment with the supplied line.
        
        :param line: A line.
        :type line: Line2D, Line3D
        
        :return: Returns None for parallel non-collinear segment and line.
            Returns None for skew segment and line that don't intersect. 
            Returns point for skew segment and line that intersect.
            Returns segment (this segment) for a segment that lies on the line.
        :rtype: None, Point2D, Point3D, Segment2D, Segment3D            
            
        :Example:
    
        .. code-block:: python
           
           # 2D example
           >>> s = Segment2D(Point2D(0,0), Point2D(1,0))
           >>> l = Line2D(Point2D(0,0), Vector2D(0,1))
           >>> result = s.intersect_line(l)
           >>> print(result)
           Point2D(0,0)
           
           # 3D example
           >>> s = Segment3D(Point3D(0,0,0), Point3D(1,0,0))
           >>> l = Line3D(Point3D(0,0,1), Vector3D(1,0,0))
           >>> result = s.intersect_line(l)
           >>> print(result)
           None
            
        """
        if line==self.line: 
            return self
        elif self.line.is_parallel(line): # parallel but not collinear
            return None 
        else:
            p=self.line._intersect_line_skew(line)
            if p in self:
                return p
            else:
                return None


    @property
    def order(self):
        """Returns the segment with ordered points such that P0 is less than P1
        
        :return: If P0 < P1, returns the reverse of this segment;
            otherwise returns a copy of this segment.
        :rtype: Segment2D, Segment3D
            
        :Example:
    
        .. code-block:: python
           
           # 2D example
           >>> s = Segment2D(Point2D(1,0), Point2D(0,0))
           >>> result = s.order
           >>> print(result)
           Segment2D(Point2D(0,0), Point2D(1,0))
           
           # 3D example
           >>> s = Segment3D(Point3D(0,0,0), Point3D(1,0,0))
           >>> result = s.order
           >>> print(result)
           Segment3D(Point3D(0,0,0), Point3D(1,0,0))
            
        """
        if self.P0 < self.P1 :
            return self.__class__(self.P0,self.P1)
        else:
            return self.reverse
        
        
    @property
    def P0(self):
        """The start point of the segment.
        
        :rtype: Point2D, Point3D
        
        """
        return self._P0
    
    
    @property
    def P1(self):
        """The end point of the segment.
        
        :rtype: Point2D, Point3D
        
        """
        return self._P1
        
    
    @property
    def points(self):
        """Return the points P0 and P1 of the segment.
        
        :return: The segment points as (P0,P1).
        :rtype: Points
            
        :Example:
    
        .. code-block:: python
           
           # 2D example
           >>> s = Segment2D(Point2D(1,0), Point2D(0,0))
           >>> result = s.points
           >>> print(result)
           Points(Point2D(1,0), Point2D(0,0))
           
           # 3D example
           >>> s = Segment3D(Point3D(0,0,0), Point3D(1,0,0))
           >>> result = s.points
           >>> print(result)
           Points(Point3D(0,0,0), Point3D(1,0,0))
            
    
        """
        return Points(self.P0, self.P1)
    
    
    @property
    def reverse(self):
        """Returns the segment in reverse.
        
        :return: A segment where the start point is the end point of this segment, and vice versa.
        :rtype: Segment2D, Segment3D
        
        :Example:
    
        .. code-block:: python
           
           # 2D example
           >>> s = Segment2D(Point2D(1,0), Point2D(0,0))
           >>> result = s.reverse
           >>> print(result)
           Segment2D(Point2D(0,0), Point2D(1,0))
           
           # 3D example
           >>> s = Segment3D(Point3D(0,0,0), Point3D(1,0,0))
           >>> result = s.reverse
           >>> print(result)
           Segment3D(Point3D(1,0,0), Point3D(0,0,0))
            
        """
        return self.__class__(self.P1,self.P0)
    
    
    # def union(self,segment):
    #     """Returns the union of this segment and the supplied segment.
        
    #     :return:
    #         Returns a polyline for two segments if they have 
    #             a same start point or end point;
    #         otherwise returns None.      
    #     :rtype: None, Polyline
        
    #     """
    #     result=self.polyline.union(segment.polyline)
    #     if result is None:
    #         return None
    #     else:
    #         return result
        
        
        
#        if self.is_collinear(segment):
#            
#            if (self.P0 in segment
#                or self.P1 in segment): # if they overlap
#                
#                line=self.line
#                t_values=[line.calculate_t_from_point(self.P0),
#                          line.calculate_t_from_point(self.P1),
#                          line.calculate_t_from_point(segment.P0),
#                          line.calculate_t_from_point(segment.P1)]
#                return self.__class__(line.calculate_point(min(t_values)),
#                                      line.calculate_point(max(t_values)))
#                
#            else:
#                
#                return None
#            
#        else: # not collinear - look for a polyline union
#            
#            result=self.polyline.union(segment.polyline)
#            if result is None:
#                return None
#            else:
#                return result
            
    
    

class Segment2D(Segment):
    """A two dimensional segment, situated on an x, y plane.
    
    Equation of the halfline is P(t) = P0 + vL*t where:
        
        - P(t) is a point on the halfline
        - P0 is the start point of the halfline
        - vL is the halfline vector
        - t is any real, positive number between 0 and 1
        
    """
       
    def __repr__(self):
        ""
        return 'Segment2D(%s, %s)' % (self.P0,self.P1)


    @property
    def dimension(self):
        """The dimension of the segment.
        
        :return: '2D'
        :rtype: str
        
        :Example:
    
        .. code-block:: python
        
            >>> s = Segment2D(Point2D(0,0), Point2D(1,0))
            >>> print(s.dimension)
            '2D'     
        
        """
        return '2D'
    

    def intersect_halfline(self,halfline):
        """Returns the interesection of this segment and a halfline.
        
        :param halfline: A 2D halfline.
        :type halfline: HalfLine2D
                
        :return: Returns None for parallel non-collinear segment and halfline.
            Returns None for skew segment and halfline that don't intersect. 
            Returns None for collinear segment and halfline that don't intersect.
            Returns point for skew segment and halfline that intersect.
            Returns point for collinear segment and halfline that intersect at the start or end point.
            Returns segment for collinear segment and halfline that intersect.
        :rtype: None, Point2D, Segment2D         
            
        :Example:
    
        .. code-block:: python
           
           >>> s = Segment2D(Point2D(0,0), Point2D(1,0))
           >>> hl = Halfine2D(Point2D(0,0), Vector2D(0,1))
           >>> result = s.intersect_halfline(hl)
           >>> print(result)
           Point2D(0,0)
        
        """
        if halfline in self.line: 
            if self.P0 in halfline and self.P1 in halfline:
                return self
            elif self.P0==halfline.P0:
                return self.P0
            elif self.P1==halfline.P0:
                return self.P1
            elif self.P0 in halfline:
                return Segment2D(self.P0,halfline.P0,)
            elif self.P1 in halfline:
                return Segment2D(halfline.P0,self.P1)
            else: 
                return None
        elif self.line.is_parallel(halfline): # parallel but not collinear
            return None 
        else:
            p=self.line.intersect_line_skew(halfline.line)
            #print(p)
            if p in self and p in halfline:
                return p
            else:
                return None
                
            
    def intersect_segment(self,segment):
        """Returns the interesection of this segment and another segment.
        
        :param segment: A 2D segment.
        :type segment: Segment2D
        
        :return: Returns None for parallel non-collinear segments.
            Returns None for skew segments that don't intersect. 
            Returns None for collinear segments that don't intersect.
            Returns point for skew segments that intersect.
            Returns point for collinear segments that intersect at a start or end point.
            Returns segment for collinear segments that intersect.
        :rtype: None, Point2D, Segment2D         
            
        :Example:
    
        .. code-block:: python
           
           >>> s1 = Segment2D(Point2D(0,0), Point2D(1,0))
           >>> s2 = Segment2D(Point2D(0,0), Point2D(0,1))
           >>> result = s1.intersect_segment(s2)
           >>> print(result)
           Point2D(0,0)
            
        """
        if segment in self.line:
            
            try:
                t0=self.line.calculate_t_from_x(segment.P0.x)
            except ValueError:
                t0=self.line.calculate_t_from_y(segment.P0.y)
                
            try:
                t1=self.line.calculate_t_from_x(segment.P1.x)
            except ValueError:
                t1=self.line.calculate_t_from_y(segment.P1.y)
            
            #t1=self.calculate_t_from_point(segment.P1)
            
            if t0 > t1: # must have t0 smaller than t1, swap if not
                t0, t1 = t1, t0 
            
            if (t0 > 1 or t1 < 0): # intersecting segment does not overlap
                return None
            
            if t0<0: t0=0 # clip to min 0
            if t1>1: t1=1 # clip to max 1
            
            if t0==t1: # point overlap
                return self.calculate_point(t0)
            
            # they overlap in a valid subsegment
            return Segment2D(self.calculate_point(t0),self.calculate_point(t1))
        
        elif self.line.is_parallel(segment.line): # parallel but not collinear
            return None 
        
        else:
            p=self.line._intersect_line_skew(segment.line)
            if p in self and p in segment:
                return p
            else:
                return None
    
    
    @property
    def line(self):
        """Returns the line which the segment lies on.
        
        :return: A line with the same start point (P0) and vector (P1-P0) as the segment.
        :rtype: Line2D
        
        :Example:
    
        .. code-block:: python
           
           >>> s = Segment2D(Point2D(0,0), Point2D(1,0))
           >>> result = s.line
           >>> print(result)
           Line2D(Point2D(0,0), Vector2D(1,0))
        
        """
        return Line2D(self.P0,self.P1-self.P0)
    
    
    def plot(self,ax,**kwargs):
        """Plots the segment on the supplied axes.
        
        :param ax: An Axes instance.
        :type ax:  matplotlib.axes.Axes 
        :param kwargs: keyword arguments to be supplied to the Axes.plot call
                            
        """
        x=[p.x for p in self.points]
        y=[p.y for p in self.points]
        ax.plot(x,y,**kwargs)
    
    
    # @property
    # def polyline(self):
    #     """Returns a simple polyline of the segment
        
    #     :return polyline:
    #     :rtype SimplePolyline2D:        
        
    #     """
    #     from .simple_polyline import SimplePolyline2D
    #     return SimplePolyline2D(self.P0,self.P1)
        
    
    def project_3D(self,plane,coordinate_index):
        """Projection of 2D segment on a 3D plane.
        
        :param plane: The plane for the projection
        :type plane: Plane3D
        :param coordinate_index: The index of the coordinate which was ignored 
            to create the 2D projection. For example, coordinate_index=0
            means that the x-coordinate was ignored and this point
            was originally projected onto the yz plane.
        :type coordinate_index: int
        
        :return: 3D segment which has been projected from the 2D segment.
        :rtype: Segment3D
               
        :Example:
    
        .. code-block:: python
        
            >>> s = Segment2D(Point2D(0,0), Point2D(1,0))
            >>> pl = Plane3D(Point3D(0,0,1), Vector3D(0,0,1))
            >>> result = s.project_3D(pl, 2)
            Segment3D(Point3D(0,0,1),Point3D(1,0,1))
        
        """
        P0=self.P0.project_3D(plane,coordinate_index)
        P1=self.P1.project_3D(plane,coordinate_index)
        return Segment3D(P0,P1)
    
    
    
class Segment3D(Segment):
    """A three dimensional segment, situated on an x, y, z plane.
    
    Equation of the halfline is P(t) = P0 + vL*t where:
        
        - P(t) is a point on the halfline
        - P0 is the start point of the halfline
        - vL is the halfline vector
        - t is any real, positive number between 0 and 1
        
    """
    
    def __repr__(self):
        ""
        return 'Segment3D(%s, %s)' % (self.P0,self.P1)
    
    
    @property
    def dimension(self):
        """The dimension of the segment.
        
        :return: '3D'
        :rtype: str
        
        :Example:
    
        .. code-block:: python
        
            >>> s = Segment3D(Point3D(0,0,0), Point3D(0,0,1))
            >>> print(s.dimension)
            '3D'     
        
        """
        return '3D'
    
        
    def distance_to_segment(self,segment):
        """Returns the distance from this segment to the supplied segment
        
        :param segment: A 3D segment.
        :type segment: Segment3D
        
        :return: The distance between the two segments.
        :rtype: float
        
        :Example:
    
        .. code-block:: python
        
            >>> s1 = Segment3D(Point3D(0,0,0), Point3D(0,0,1))
            >>> s2 = Segment3D(Point3D(0,0,2), Point3D(0,0,3))
            >>> result= s1.distance_to_segment(s2)
            >>> print(result)
            1     
        
        """
        u=self.line.vL
        v=segment.line.vL
        w=self.P0-segment.P0
        a=u.dot(u)
        b=u.dot(v)
        c=v.dot(v)
        d=u.dot(w)
        e=v.dot(w)
        D=a*c - b*b
        sc,sN,sD = D,D,D      # sc = sN / sD, default sD = D >= 0
        tc,tN,tD = D,D,D       # tc = tN / tD, default tD = D >= 0
        
        if D< SMALL_NUM: # the lines are almost parallel
            
            sN=0 # force using point P0 on segment S1
            sD=1 # to prevent possible division by 0.0 later
            tN=e
            tD=c
            
        else: # get the closest points on the infinite lines
            
            sN=b*e-c*d
            tN=a*e-b*d
            
            if sN<0: # sc < 0 => the s=0 edge is visible
                
                sN=0
                tN=e
                tD=c
                
            elif sN>sD: # sc > 1  => the s=1 edge is visible
                
                sN=sD
                tN=e+b
                tD=c
                
        if tN<0: # tc < 0 => the t=0 edge is visible
            
            tN=0
            # recompute sc for this edge
            if -d<0:
                sN=0
            elif -d>a:
                sN-sD
            else:
                sN=-d
                sD=a
                
        elif tN>tD: # tc > 1  => the t=1 edge is visible
            
            tN=tD
            # recompute sc for this edge
            if -d+b<0:
                sN=0
            elif -d+b>a:
                sN=sD
            else:
                sN=-d+b
                sD=a
                
        # finally do the division to get sc and tc
        sc=0 if abs(sN)<SMALL_NUM else sN / sD
        tc=0 if abs(tN)<SMALL_NUM else tN / tD
        
        # get the difference of the two closest points
        dP = w + u*sc - v*tc  # =  S1(sc) - S2(tc)
            
        return dP.length
    
    
    def intersect_halfline(self,halfline):
        """Returns the interesection of this segment and a halfline
        
        :param halfline: A 3D halfline.
        :type halfline: HalfLine3D
                
        :return: Returns None for parallel non-collinear segment and halfline.
            Returns None for skew segment and halfline that don't intersect. 
            Returns None for collinear segment and halfline that don't intersect.
            Returns point for skew segment and halfline that intersect.
            Returns point for collinear segment and halfline that intersect at the start or end point.
            Returns segment for collinear segment and halfline that intersect.
        :rtype: None, Point3D, Segment3D            
            
        :Example:
    
        .. code-block:: python
           
           >>> s = Segment3D(Point3D(0,0,0), Point3D(1,0,0))
           >>> hl = Halfline3D(Point3D(0,0,1), Vector3D(1,0,0))
           >>> result = s.intersect_halfline(hl)
           >>> print(result)
           None
        
        """
        if halfline in self.line: 
            if self.P0 in halfline and self.P1 in halfline:
                return self
            elif self.P0==halfline.P0:
                return self.P0
            elif self.P1==halfline.P0:
                return self.P1
            elif self.P0 in halfline:
                return Segment2D(self.P0,halfline.P0,)
            elif self.P1 in halfline:
                return Segment2D(halfline.P0,self.P1)
            else: 
                return None
        elif self.line.is_parallel(halfline): # parallel but not collinear
            return None 
        else:
            p=self.line._intersect_line_skew(halfline.line)
            #print(p)
            if p in self and p in halfline:
                return p
            else:
                return None
             
            
    def intersect_segment(self,segment):
        """Returns the interesection of this segment and another segment.
        
        :param segment: A 3D segment.
        :type segment: Segment3D
        
        :return: Returns None for parallel non-collinear segments.
            Returns None for skew segments that don't intersect. 
            Returns None for collinear segments that don't intersect.
            Returns point for skew segments that intersect.
            Returns point for collinear segments that intersect at a start or end point.
            Returns segment for collinear segments that intersect.
        :rtype: None, Point2D, Segment2D         
            
        :Example:
    
        .. code-block:: python
           
           >>> s1 = Segment3D(Point3D(0,0,0), Point3D(1,0,0))
           >>> s2 = Segment3D(Point3D(0,0,0), Point3D(0,1,0))
           >>> result = s1.intersect_segment(s2)
           >>> print(result)
           Point3D(0,0,0)
            
        """
        if segment in self.line:
            
            try:
                t0=self.calculate_t_from_x(segment.P0.x)
            except ValueError:
                try:
                    t0=self.calculate_t_from_y(segment.P0.y)
                except ValueError:
                    t0=self.calculate_t_from_z(segment.P0.z)
                    
            try:
                t1=self.calculate_t_from_x(segment.P1.x)
            except ValueError:
                try:
                    t1=self.calculate_t_from_y(segment.P1.y)
                except ValueError:
                    t1=self.calculate_t_from_z(segment.P1.z)
                    
            if t0 > t1: # must have t0 smaller than t1, swap if not
                t0, t1 = t1, t0 
            
            if (t0 > 1 or t1 < 0): # intersecting segment does not overlap
                return None
            
            if t0<0: t0=0 # clip to min 0
            if t1>1: t1=1 # clip to max 1
            
            if t0==t1: # point overlap
                return self.calculate_point(t0)
            
            # they overlap in a valid subsegment
            return Segment3D(self.calculate_point(t0),self.calculate_point(t1))
        
        elif self.line.is_parallel(segment.line): # parallel but not collinear
            return None 
        
        else:
            p=self.line._intersect_line_skew(segment.line)
            if p in self and p in segment:
                return p
            else:
                return None
        
    
    @property
    def line(self):
        """Returns the line which the segment lies on.
        
        :return: A line with the same start point (P0) and vector (P1-P0) as the halfline.
        :rtype: Line3D
        
        :Example:
    
        .. code-block:: python
           
           >>> s = Segment3D(Point3D(0,0,0), Point3D(1,0,0))
           >>> result = s.line
           >>> print(result)
           Line3D(Point3D(0,0,0), Vector3D(1,0,0))
        
        """
        return Line3D(self.P0,self.P1-self.P0)
    
    
    def plot(self,ax,**kwargs):
        """Plots the segment on the supplied axes
        
        :param ax: An Axes3D instance.
        :type ax: mpl_toolkits.mplot3d.axes3d.Axes3D
        :param kwargs: keyword arguments to be supplied to the Axes3D.plot call
                    
        """
        x=[p.x for p in self.points]
        y=[p.y for p in self.points]
        z=[p.z for p in self.points]
        ax.plot(x,y,z,**kwargs)
    
    
    # @property
    # def polyline(self):
    #     """Returns a simple polyline of the segment
        
    #     :return polyline:
    #     :rtype SimplePolyline3D:        
        
    #     """
    #     from .simple_polyline import SimplePolyline3D
    #     return SimplePolyline3D(self.P0,self.P1)
    
    
    def project_2D(self,coordinate_index):
        """Projection of the 3D segment as a 2D segment.
        
        :param coordinate_index: The index of the coordinate to ignore.
            Use coordinate_index=0 to ignore the x-coordinate, coordinate_index=1 
            for the y-coordinate and coordinate_index=2 for the z-coordinate.
        :type coordinate_index: int
        
        :return: A 2D segment based on the projection of the 3D segment.
        :rtype: Segment2D
               
        :Example:
    
        .. code-block:: python
        
            >>> s = Segment3D(Point3D(0,0,0), Point3D(1,2,3))
            >>> result = s.project_2D(0)
            >>> print(result)
            Segment2D(Point2D(0,0), Point2D(2,3))   
        
        """
        
        if coordinate_index==0:
            return Segment2D(Point2D(self.P0.y,self.P0.z),
                              Point2D(self.P1.y,self.P1.z))
        elif coordinate_index==1:
            return Segment2D(Point2D(self.P0.z,self.P0.x),
                             Point2D(self.P1.z,self.P1.x))
        elif coordinate_index==2:
            return Segment2D(Point2D(self.P0.x,self.P0.y),
                             Point2D(self.P1.x,self.P1.y))
        else:
            raise Exception
                    
        
    
  