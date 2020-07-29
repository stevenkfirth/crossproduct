# -*- coding: utf-8 -*-

from .line import Line2D, Line3D
from .point import Point2D
from .segment import Segment2D, Segment3D
from .vector import Vector2D


SMALL_NUM=0.00000001


class Halfline():
    "A n-D halfline"
    
    classname='Halfline'
           
    def __init__(self,P0,vL,validate=False):
        ""
        if validate:
            if vL.length<SMALL_NUM:
                raise ValueError('length of vL must be greater than zero')
                
        self._P0=P0
        self._vL=vL
        
    
    def __contains__(self,obj):
        """Tests if the halfline contains the object
        
        :param obj: a geometric object 
        :type obj: Point2D, Point3D, Segment2D, Segment3D
            
        :return:
            - for point, True if the point lies on the halfline
            - for segment, True if the segment start and endpoints are on the halfline
        :rtype: bool
        
        """
        if obj.classname=='Point':
            
            t=self.line.calculate_t_from_point(obj)
            try:
                pt=self.calculate_point(t)  
            except ValueError: # t<0
                return False
            return obj==pt 
        
        elif obj.classname=='Segment':
            if obj.P0 in self and obj.P1 in self:
                return True
            else:
                return False
            
        else:
            return TypeError()
        
        
    def __eq__(self,halfline):
        """Tests if this halfline and the supplied halfline are equal
        
        :param halfline: a halfline
        :type halfline: Halfline2D, Halfline3D
        
        :return: 
            - True if 
                - the start points are the same
                - the vectors are codirectional
            - otherwise False
        :rtype: bool
            
        """
        if isinstance(halfline,Halfline):
            return self.P0==halfline.P0 and self.vL.is_codirectional(halfline.vL)
        else:
            return False
        
        
    def calculate_point(self,t):
        """Returns a point on the halfline for a given t value
        
        :param t: the t value
        :type t: float
        
        :return: point
        :rtype: Point
        
        """
        if t>=0:
            return self.P0 + (self.vL * t)
        else:
            raise ValueError('For a halfline, t must be greater than or equal to zero')
        
        
    def distance_to_point(self,point):
        """Returns the distance to the supplied point
        
        :param point: a point
        :type point: Point2D, Point3D
        
        :return: the distance from the point to the point
        :rtype: float
            
        """
        v=self.vL
        w=point-self.P0 
        c1=v.dot(w)
        if c1<=0: # i.e. t<0
            return w.length
        else:
            return self.line.distance_to_point(point)
        
        
    def intersect_line(self,line):
        """Returns the intersection of this halfline with the supplied line
        
        :param line: a  line 
        :type line: Line2D, Line3D
        
        :return:
            - return value can be:
                - Halfline -> a halfline (for a halfline that lies on the line) 
                - Point -> a point (for skew halfline and line that intersect)
                - None -> no intersection (for parallel line and halfline, 
                    or skew halfline and line that don't intersect)
        
        """
        if self.line==line:
            return self
        elif self.line.is_parallel(line):
            return None # should this be a 'no intersection' class??
        else:
            p=self.line._intersect_line_skew(line)
            #print(p)
            if p in self:
                return p
            else:
                return None
        
        
    def is_collinear(self,linelike_obj):
        """Tests if this halfline and the supplied line-like object are collinear
        
        :param linelike_obj: a Line, Halfline or Segment
        :type linelike_obj: Line2D, Line3D, Halfline2D, Halfline3D, Segment2D, Segment3D
        
        :return result: the result of the test
            - returns True if the linkline_obj is collinear to this halfline
            - otherwise False
        :rtype bool:
            
        """
        return self.line.is_collinear(linelike_obj)
    
        
    def is_codirectional(self,halfline):
        """Tests if this halfline and the supplied halfline are collinear
        
        :param halfline: a halfline
        :type halfline: Halfline2D, Halfline3D
        
        :return: 
            - returns True if the halflines are codirectional
            - otherwise False
        :rtype: bool
            
        """
        if isinstance(halfline,Halfline):
            return self.vL.is_codirectional(halfline.vL)
        else:
            return TypeError
            
        
    def is_parallel(self,linelike_obj):
        """Tests if this halfline and the supplied object are parallel. 
        
        :param obj: A line, halfline or segment.
        :type obj: Line2D, Line3D, Halfline2D, Halfline3D, Segment2D or Segment3D
        
        :return: Returns True if the obj vector is collinear with the line vector; 
            otherwise False. 
        :rtype: bool
            
        :Example:
    
        .. code-block:: python
           
           # 2D example
           >>> l1 = Line2D(Point2D(0,0), Vector2D(1,0))
           >>> l2 = Line2D(Point2D(0,0), Vector2D(0,1))
           >>> result = l.is_parallel(l2)
           >>> print(result)
           False
           
           # 3D example
           >>> l1 = Line3D(Point3D(0,0,0), Vector3D(1,0,0))
           >>> l2 = Line3D(Point3D(0,0,1), Vector3D(2,0,0))
           >>> result = l1.is_parallel(l2)
           >>> print(result)
           True
            
        """
        return self.vL.is_collinear(linelike_obj.vL)
        
        
    @property
    def P0(self):
        """The starting point of the line.
        
        :rtype: Point2D or Point3D
        
        """
        return self._P0
    
    
    @property
    def vL(self):
        """The vector of the line.
        
        :rtype: Vector2D or Vector3D
        
        """
        return self._vL
        

class Halfline2D(Halfline):
    """A two dimensional halfline, situated on an x, y plane.
    
    Equation of the halfline is P(t) = P0 + vL*t where:
        
        - P(t) is a point on the halfline
        - P0 is the start point of the halfline
        - vL is the halfline vector
        - t is any real, positive number
        
    """        
    
    def __repr__(self):
        """The string of this halfline for printing
        
        :rtype: str
            
        """
        return 'Halfline2D(%s, %s)' % (self.P0,self.vL)
             
            
    @property
    def dimension(self):
        """The dimension of the halfline.
        
        :return: '2D'
        :rtype: str
        
        :Example:
    
        .. code-block:: python
        
            >>> l = Line2D(Point2D(0,0), Vector2D(1,0))
            >>> print(l.dimensions)
            '2D'     
        
        """
        
        return '2D'
    
     
    def intersect_halfline(self,halfline):
        """Returns the intersection of this halfline with the supplied halfline
        
        :param halfline: a 2D halfline 
        :type halfline:  Halfline2D
        
        :return:
            - return value can be:
                - Halfline2D -> a halfline (for equal halflines) 
                - Point2D -> a point (for skew halflines that intersect, 
                    or collinear but non-codirectional halflines that start at the same point)
                - Segment2D -> a segment (for collinear but non-codirectional 
                    halflines that intersect but start at different points)
                - None -> no intersection (for parallel halfline, 
                    skew halflines that don't intersect,
                    or for collinear but non-codirectional halflines that don't intersect)
            
        """
        if halfline in self.line: # codirectional or non-codirectional
            if self.is_codirectional(halfline): # codirectional
                if self.P0 in halfline: # returns the halfline which is 'inside' the other
                    return self
                else:
                    return halfline
            else: # non-codirectional
                if self.P0 in halfline: #  the halflines intersect
                    if self.P0==halfline.P0:
                        return self.P0
                    else:
                        return Segment2D(self.P0,halfline.P0)
                else: # the halflines don't intersect
                    return None
        elif self.line.is_parallel(halfline.line): # parallel but not collinear
            return None # should this be a 'no intersection' class??
        else:
            p=self.line._intersect_line_skew(halfline.line)
            if p in self and p in halfline:
                return p
            else:
                return None
        
        
    @property
    def line(self):
        """Return the line which the halfline lies on
        
        :rtype: Line2D
        """
        return Line2D(self.P0,self.vL)
    
    
    
class Halfline3D(Halfline):
    """A three dimensional line, situated on an x, y, z plane.
    
    Equation of the halfline is P(t) = P0 + vL*t where:
        
        - P(t) is a point on the halfline
        - P0 is the start point of the halfline
        - vL is the halfline vector
        - t is any real, positive number
        
    """
    
    def __repr__(self):
        """The string of this halfline for printing
        """
        return 'Halfline3D(%s, %s)' % (self.P0,self.vL)
    
    
    @property
    def dimension(self):
        """The dimension of the halfline.
        
        :return: '3D'
        :rtype: str
        
        :Example:
    
        .. code-block:: python
        
            >>> l = Line3D(Point3D(0,0,0), Vector3D(0,0,1))
            >>> print(l.dimensions)
            '3D'     
        
        """
        
        return '3D'
    
    
    def intersect_halfline(self,halfline):
        """Returns the intersection of this halfline with the supplied halfline
        
        :param halfline: a 3D halfline 
        :type halfline: Halfline3D
        
        :return:
            - return value can be:
                - Halfline3D -> a halfline (for equal halflines) 
                - Point3D -> a point (for skew halflines that intersect, 
                    or collinear but non-codirectional halflines that start at the same point)
                - Segment3D -> a segment (for collinear but non-codirectional 
                    halflines that intersect but start at different points)
                - None -> no intersection (for parallel halfline, 
                    skew halflines that don't intersect,
                    or for collinear but non-codirectional halflines that don't intersect)
            
        """
        if halfline in self.line: # codirectional or non-codirectional
            if self.is_codirectional(halfline): # codirectional
                if self.P0 in halfline: # returns the halfline which is 'inside' the other
                    return self
                else:
                    return halfline
            else: # non-codirectional
                if self.P0 in halfline: #  the halflines intersect
                    if self.P0==halfline.P0:
                        return self.P0
                    else:
                        return Segment3D(self.P0,halfline.P0)
                else: # the halflines don't intersect
                    return None
        elif self.line.is_parallel(halfline.line): # parallel but not collinear
            return None # should this be a 'no intersection' class??
        else:
            p=self.line.intersect_line_skew(halfline.line)
            if p in self and p in halfline:
                return p
            else:
                return None
    
        
    @property
    def line(self):
        """Return the line which the halfline lies on
        
        :rtype: Line3D
        """
        return Line3D(self.P0,self.vL)
    
    
    def project_2D(self,i):
        """Projects the 3D halfline to a 2D halfline
        
        :param i: the coordinte index to ignore
            - index is the index of the coordinate which is ignored in the projection
                - 0 for x
                - 1 for y
                - 2 for z
        :type i: int
                
        :return: halfline:
        :rtype: Halfline2D
            
        """
        
        if i==0:
            return Halfline2D(Point2D(self.P0.y,self.P0.z),
                              Vector2D(self.vL.y,self.vL.z))
        elif i==1:
            return Halfline2D(Point2D(self.P0.z,self.P0.x),
                              Vector2D(self.vL.z,self.vL.x))
        elif i==2:
            return Halfline2D(Point2D(self.P0.x,self.P0.y),
                              Vector2D(self.vL.x,self.vL.y))
        else:
            raise Exception
                    
        
    
    