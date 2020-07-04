# -*- coding: utf-8 -*-

from .point import Point, Point2D
from .line import Line, Line2D, Line3D

SMALL_NUM=0.00000001


class Segment():
    "A n-D segment"
    
    
    def __init__(self,P0,P1):
        """
        :param P0 Point: the start point of the segment
        :param p1 Point: the end point of the segment
        
        """
        
        if P0==P1:
            raise ValueError('P0 and P1 cannot be equal for a segment')
        
        if isinstance(P0, Point):
            self.P0=P0
        else:
            raise TypeError
            
        if isinstance(P1, Point):
            self.P1=P1
        else:
            raise TypeError
    
    
    def __contains__(self,obj):
        """Tests if the segment contains the object
        
        :param obj: a geometric object 
            - Point, Segement
            
        :return result:
            - for point, True if the point lies on the halfline
            - for segment, True if the segment start and endpoints are on the halfline
        :rtype bool:
        
        """
        if isinstance(obj,Point):
            
            t=self.calculate_t_from_point(obj)
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
        """Tests if this segment and the supplied segment are equal
        
        :param line HalfLine: a halfline
        
        :return result: 
            - True if 
                - they have the same start point and end point, or
                - the start point of one is the end point of the other, and vice versa
            - otherwise False
        :rtype bool:
            
        """
        if isinstance(segment,Segment):
            return ((self.P0==segment.P0 and self.P1==segment.P1) or
                    (self.P0==segment.P1 and self.P1==segment.P0))
        else:
            return False


    def calculate_point(self,t):
        """Returns a point on the segment for a given t value
        
        :param t int/float: the t value
        
        :return point:
        :rtype Point2D
        
        """
        if t>=0 and t<=1:
            return self.P0 + (self.vL * t)
        else:
            raise ValueError('For a segment, t must be equal to or between 0 and 1')
            
            
    def distance_point(self,point):
        """Returns the distance to the supplied object
        
        :param point: a point
        
        :return distance: the distance from the point to the object
        :rtype float:
            
        """
        v=self.vL
        w=point-self.P0
        c1=v.dot(w)
        c2=v.dot(v)
        
        if c1<=0: # i.e. t<0
            return w.length
        elif c2<=c1: # i.e. T>0
            return (point-self.P1).length
        else:
            return self.line.distance_point(point)
    

    def intersect_line(self,line):
        """Returns the intersection of this segment with the supplied line
        
        :param line Line: a line 
        
        :return result:
            - return value can be:
                - Segment -> a segment (for a segment that lies on the line) 
                - Point -> a point (for a skew segment and line that intersect)
                - None -> no intersection (for parallel non-collinear segment and line, 
                    or skew segment and line that don't intersect)
            
        """
        if line==self.line: 
            return self
        elif self.line.is_parallel(line): # parallel but not collinear
            return None 
        else:
            p=self.line.intersect_line_skew(line)
            if p in self:
                return p
            else:
                return None


    def is_collinear(self,linelike_obj):
        """Tests if this segment and the supplied line-like object are collinear
        
        :param linelike_obj: a Line, HalfLine or Segment
        
        :return result: the result of the test
            - returns True if the linkline_obj is collinear to thie segment
            - otherwise False
        :rtype bool:
            
        """
        return self.line.is_collinear(linelike_obj)
        
    
    @property
    def order(self):
        """Returns the segment with ordered points such that P0 is less than P1
        
        :return segment:
            
        """
        if self.P0 < self.P1 :
            
            return self
        
        else:
            
            return self.reverse
        
        

    @property
    def points(self):
        """Return the points P0 and P1 of the segment
        
        :return points: (P0,P1)
        :rtype tuple:
            
        """
        return self.P0, self.P1
    
    @property
    def reverse(self):
        """Returns the segment in reverse
        
        :return segment:
        
        """
        return self.__class__(self.P1,self.P0)
    
    
    def union(self,segment):
        """Returns the union of two segments
        
        :return result:
            - DEPRECIATED -- Segment2D, the union of the two collinear segments if 
                they have a same start or end point
            - Polyline2D, the union of two non-collinear segments if they have 
                a same start point or end point
            - None, for segments that don't have a union        
        
        """
        result=self.polyline.union(segment.polyline)
        if result is None:
            return None
        else:
            return result
        
        
        
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
            
    
    @property
    def vL(self):
        """Return the vector from P0 to P1
        
        :return vector:
        :rtype Vector2D:
            
        """
        return self.P1-self.P0
    


class Segment2D(Segment,Line2D):
    """A 2D segment
    
    Equation of the halfline is P(t) = P0 + vL*t
        where:
            - P(t) is a point on the halfline
            - P0 is the start point of the halfline
            - vL is the halfline vector
            - t is any real, positive number between 0 and 1
        
    """
       
    def __repr__(self):
        """The string of this segment for printing
        
        :return result:
        :rtype str:
            
        """
        return 'Segment2D(%s, %s)' % (self.P0,self.P1)


    def intersect_halfline(self,halfline):
        """Returns the interesection of this segment and a halfline
        
        :param halfline HalfLine2D: a 2D halfline
        
        :return result:
            - no intersection (None), for:
                - parallel segment and halfline which are not collinear
                - skew segment and halfline which don't intersect
                - collinear segment and halfline which don't intersect
            - a segment, for:
                - collinear segment and halfline which intersect
            - a point, for:
                - collinear segment and halfline which intersect at the start or end point
                - skew segment and halfline which intersect
            
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
        """Returns the interesection of this segment and another segment
        
        :param segment Segment2D: a 2D segment
        
        :return result:
            - no intersection (None), for:
                - parallel segment and segment which are not collinear
                - skew segment and segment which don't intersect
                - collinear segment and segment which don't intersect
            - a segment, for:
                - collinear segment and segment which intersect
            - a point, for:
                - collinear segment and line which intersect at the start or end point
                - skew segment and segment which intersect
            
        """
        if segment in self.line:
            
            try:
                t0=self.calculate_t_from_x(segment.P0.x)
            except ValueError:
                t0=self.calculate_t_from_y(segment.P0.y)
                
            try:
                t1=self.calculate_t_from_x(segment.P1.x)
            except ValueError:
                t1=self.calculate_t_from_y(segment.P1.y)
            
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
        
        elif self.line.is_parallel(segment): # parallel but not collinear
            return None 
        
        else:
            p=self.line.intersect_line_skew(segment.line)
            if p in self and p in segment:
                return p
            else:
                return None
    
    
    @property
    def line(self):
        """Return the line which the halfline lies on
        
        :return line:
        :rtype Line2D:
        """
        return Line2D(self.P0,self.vL)
    
    
    def plot(self,ax,**kwargs):
        """Plots the segment on the supplied axes
        
        :param ax matplotlib.axes.Axes: an Axes instance
        :param **kwargs: keyword arguments to be supplied to the Axes.plot call
                    
        
        """
        x=[p.x for p in self.points]
        y=[p.y for p in self.points]
        ax.plot(x,y,**kwargs)
    
    
    @property
    def polyline(self):
        """Returns a simple polyline of the segment
        
        :return polyline:
        :rtype SimplePolyline2D:        
        
        """
        from .simple_polyline import SimplePolyline2D
        return SimplePolyline2D(self.P0,self.P1)
        
    
    
class Segment3D(Segment,Line3D):
    """A 3D segment
    
    Equation of the halfline is P(t) = P0 + vL*t
        where:
            - P(t) is a point on the halfline
            - P0 is the start point of the halfline
            - vL is the halfline vector
            - t is any real, positive number between 0 and 1
        
    """
    
    def __repr__(self):
        """The string of this segment for printing
        
        :return result:
        :rtype str:
            
        """
        return 'Segment3D(%s, %s)' % (self.P0,self.P1)
    
    
    def distance_halfline(self,halfline):
        "this would be based on Segment.distance_segment"
        raise NotImplementedError
    
    
    def distance_line(self,line):
        "this would be based on Segment.distance_segment"
        raise NotImplementedError
    
    
    def distance_segment(self,segment):
        """Returns the distance to the supplied segment
        
        :param segment Segment: a segment
        
        :return distance: the distance from the segment to the supplied segment
        :rtype float:
            
        """
        u=self.vL
        v=segment.vL
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
        
        :param halfline HalfLine3D: a 3D halfline
        
        :return result:
            - no intersection (None), for:
                - parallel segment and halfline which are not collinear
                - skew segment and halfline which don't intersect
                - collinear segment and halfline which don't intersect
            - a segment, for:
                - collinear segment and halfline which intersect
            - a point, for:
                - collinear segment and halfline which intersect at the start or end point
                - skew segment and halfline which intersect
            
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
        """Returns the interesection of this segment and another segment
        
        :param segment Segment3D: a 3D segment
        
        :return result:
            - no intersection (None), for:
                - parallel segment and segment which are not collinear
                - skew segment and segment which don't intersect
                - collinear segment and segment which don't intersect
            - a segment, for:
                - collinear segment and segment which intersect
            - a point, for:
                - collinear segment and line which intersect at the start or end point
                - skew segment and segment which intersect
            
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
        
        elif self.line.is_parallel(segment): # parallel but not collinear
            return None 
        
        else:
            p=self.line.intersect_line_skew(segment.line)
            if p in self and p in segment:
                return p
            else:
                return None
        
    
    @property
    def line(self):
        """Return the line which the halfline lies on
        
        :return line:
        :rtype Line3D:
        """
        return Line3D(self.P0,self.vL)
    
    
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
    def polyline(self):
        """Returns a simple polyline of the segment
        
        :return polyline:
        :rtype SimplePolyline3D:        
        
        """
        from .simple_polyline import SimplePolyline3D
        return SimplePolyline3D(self.P0,self.P1)
    
    
    def project_2D(self,i):
        """Projects the 3D segment to a 2D segment
        
        :param i int: the coordinte index to ignore
            - index is the index of the coordinate which is ignored in the projection
                - 0 for x
                - 1 for y
                - 2 for z
                
        :return segment: 
        :rtype Segment2D:
            
        """
        
        if i==0:
            return Segment2D(Point2D(self.P0.y,self.P0.z),
                              Point2D(self.P1.y,self.P1.z))
        elif i==1:
            return Segment2D(Point2D(self.P0.z,self.P0.x),
                             Point2D(self.P1.z,self.P1.x))
        elif i==2:
            return Segment2D(Point2D(self.P0.x,self.P0.y),
                             Point2D(self.P1.x,self.P1.y))
        else:
            raise Exception
                    
        
    
  