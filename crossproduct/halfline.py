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
        """Tests if the halfline contains the object.
        
        :param obj: A point or segment.
        :type obj: Point2D, Point3D, Segment2D, Segment3D
            
        :return: For point, True if the point lies on the halfline; otherwise False. 
            For segment, True if the segment start point and end point are on the halfline; otherwise False
        :rtype: bool
        
        :Example:
    
        .. code-block:: python
           
           # 2D example
           >>> hl = Halfline2D(Point2D(0,0), Vector2D(1,0))
           >>> result = Point2D(2,0) in l
           >>> print(result)
           True
           
           # 3D example
           >>> hl = Halfline3D(Point3D(0,0,0), Vector3D(1,0,0))
           >>> hl = Halfline3D(Point3D(0,0,0), Vector3D(-1,0,0))
           >>> result = hl in l
           >>> print(result)
           False            
        
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
        """Tests if this halfline and the supplied halfline are equal.
        
        :param halfline: A halfline.
        :type halfline: Halfline2D, Halfline3D
        
        :return: True if the start points are the same and the vectors are codirectional;
            otherwise False.
        :rtype: bool
        
        :Example:
    
        .. code-block:: python
           
           # 2D example
           >>> hl = Halfline2D(Point2D(0,0), Vector2D(1,0))
           >>> result = hl == hl
           >>> print(result)
           True
           
           # 3D example
           >>> hl1 = Halfline3D(Point3D(0,0,0), Vector3D(1,0,0))
           >>> hl2 = Halfline3D(Point3D(0,0,0), Vector3D(-1,0,0))
           >>> result = hl1 == hl2
           >>> print(result)
           False
            
        """
        if isinstance(halfline,Halfline):
            return self.P0==halfline.P0 and self.vL.is_codirectional(halfline.vL)
        else:
            return False
        
        
    def calculate_point(self,t):
        """Returns a point on the halfline for a given t value.
        
        :param t: The t value.
        :type t: float
        
        :return: The point based on the t value.
        :rtype: Point2D, Point3D
        
        :Example:
        
        .. code-block:: python    
        
           # 2D example
           >>> hl = Halfline2D(Point2D(0,0), Vector2D(1,0))
           >>> result = hl.calcuate_point(3)
           >>> print(result)
           Point2D(3,0)
           
           # 3D example
           >>> hl = Halfline3D(Point3D(0,0,0), Vector3D(1,0,0))
           >>> result = hl.calcuate_point(3)
           >>> print(result)
           Point3D(3,0,0)
        
        """
        if t>=0:
            return self.P0 + (self.vL * t)
        else:
            raise ValueError('For a halfline, t must be greater than or equal to zero')
        
        
    def distance_to_point(self,point):
        """Returns the distance from this halfline to the supplied point.
        
        :param point: A point.
        :type point: Point2D, Point3D
        
        :return: The distance from the halfline to the point.
        :rtype: float
            
        :Example:
    
        .. code-block:: python
           
           # 2D example
           >>> hl = Halfline2D(Point2D(0,0), Vector2D(1,0))
           >>> result = hl.distance_to_point(Point2D(0,10))
           >>> print(result)
           10
           
           # 3D example
           >>> hl = Halfline3D(Point3D(0,0,0), Vector3D(1,0,0))
           >>> result = hl.distance_to_point(Point3D(10,0,0))
           >>> print(result)
           0
        
        """
        v=self.vL
        w=point-self.P0 
        c1=v.dot(w)
        if c1<=0: # i.e. t<0
            return w.length
        else:
            return self.line.distance_to_point(point)
        
        
    def intersect_line(self,line):
        """Returns the intersection of this halfline with the supplied line.
        
        :param line: A line.
        :type line: Line2D, Line3D
        
        :return: Returns a halfline (this halfline) if the halfline and line are collinear. 
            Returns a point if the halfline and line are skew and they intersect. 
            Returns None if the halfline and line are parallel. 
            Returns None if the halfline and line are skew but do not intersect. 
        :rtype: None, Point2D, Point3D, Halfline2D, Halfline3D        
            
        :Example:
    
        .. code-block:: python
           
           # 2D example
           >>> hl = Halfline2D(Point2D(0,0), Vector2D(1,0))
           >>> l = Line2D(Point2D(0,0), Vector2D(0,1))
           >>> result = hl.intersect_line(l)
           >>> print(result)
           Point2D(0,0)
           
           # 3D example
           >>> hl = Halfline3D(Point3D(0,0,0), Vector3D(1,0,0))
           >>> l = Line3D(Point3D(0,0,1), Vector3D(1,0,0))
           >>> result = hl.intersect_line(l)
           >>> print(result)
           None
            
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
        
        
    @property
    def P0(self):
        """The starting point of the halfline.
        
        :rtype: Point2D or Point3D
        
        """
        return self._P0
    
    
    @property
    def vL(self):
        """The vector of the halfline.
        
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
        ""
        return 'Halfline2D(%s, %s)' % (self.P0,self.vL)
             
            
    @property
    def dimension(self):
        """The dimension of the halfline.
        
        :return: '2D'
        :rtype: str
        
        :Example:
    
        .. code-block:: python
        
            >>> hl = Halfline2D(Point2D(0,0), Vector2D(1,0))
            >>> print(hl.dimension)
            '2D'     
        
        """
        return '2D'
    
     
    def intersect_halfline(self,halfline):
        """Returns the intersection of this halfline with the supplied halfline.
        
        :param halfline: A 2D halfline.
        :type halfline:  Halfline2D
        
        :return: Returns None for halflines that are parallel. 
            Returns None for skew halflines that don't intersect.
            Returns None for collinear but non-codirectional halflines that don't overlap.
            Returns a point for skew halflines that intersect. 
            Returns a point for collinear but non-codirectional halflines that have the same start point. 
            Returns a segment for collinear but non-codirectional halflines that overlap.
            Returns a halfline for halflines that are equal.
        :rtype: None, Point2D, Halfline2D, Segment2D
            
        :Example:
    
        .. code-block:: python
           
           >>> hl1 = Halfline2D(Point2D(0,0), Vector2D(1,0))
           >>> hl2 = Halfline2D(Point2D(0,0), Vector2D(0,1))
           >>> result = hl1.intersect_line(hl2)
           >>> print(result)
           Point2D(0,0)
        
        """
        if halfline in self.line: # codirectional or non-codirectional
            if self.vL.is_codirectional(halfline.vL): # codirectional
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
        """Returns the line which the halfline lies on.
        
        :return: A line with the same start point (P0) and vector (vL) as the halfline.
        :rtype: Line2D
        
        :Example:
    
        .. code-block:: python
           
           >>> hl= Halfline2D(Point2D(0,0), Vector2D(1,0))
           >>> result = hl.line
           >>> print(result)
           Line2D(Point2D(0,0), Vector2D(1,0))
        
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
        ""
        return 'Halfline3D(%s, %s)' % (self.P0,self.vL)
    
    
    @property
    def dimension(self):
        """The dimension of the halfline.
        
        :return: '3D'
        :rtype: str
        
        :Example:
    
        .. code-block:: python
        
            >>> hl = Halfine3D(Point3D(0,0,0), Vector3D(0,0,1))
            >>> print(hl.dimension)
            '3D'     
        
        """
        return '3D'
    
    
    def intersect_halfline(self,halfline):
        """Returns the intersection of this halfline with the supplied halfline.
        
        :param halfline: A 3D halfline.
        :type halfline:  Halfline3D
        
        :return: Returns None for halflines that are parallel. 
            Returns None for skew halflines that don't intersect.
            Returns None for collinear but non-codirectional halflines that don't overlap.
            Returns a point for skew halflines that intersect. 
            Returns a point for collinear but non-codirectional halflines that have the same start point. 
            Returns a segment for collinear but non-codirectional halflines that overlap.
            Returns a halfline for halflines that are equal.
        :rtype: None, Point3D, Halfline3D, Segment3D
            
        :Example:
    
        .. code-block:: python
           
           >>> hl1 = Halfline3D(Point2D(0,0,0), Vector2D(1,0,0))
           >>> hl2 = Halfline3D(Point2D(0,0,0), Vector2D(0,1,0))
           >>> result = hl1.intersect_line(hl2)
           >>> print(result)
           Point3D(0,0,0)
        
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
        """Returns the line which the halfline lies on.
        
        :return: A line with the same start point (P0) and vector (vL) as the halfline.
        :rtype: Line3D
        
        :Example:
    
        .. code-block:: python
           
           >>> hl= Halfline3D(Point3D(0,0,0), Vector3D(1,0,0))
           >>> result = hl.line
           >>> print(result)
           Line3D(Point3D(0,0,0), Vector3D(1,0,0))
        
        """
        return Line3D(self.P0,self.vL)
    
    
    def project_2D(self,coordinate_index):
        """Projection of the 3D halfline as a 2D halfline.
        
        :param coordinate_index: The index of the coordinate to ignore.
            Use coordinate_index=0 to ignore the x-coordinate, coordinate_index=1 
            for the y-coordinate and coordinate_index=2 for the z-coordinate.
        :type coordinate_index: int
        
        :return: A 2D halfline based on the projection of the 3D halfline.
        :rtype: Halfine2D
               
        :Example:
    
        .. code-block:: python
        
            >>> hl = Halfline3D(Point3D(0,0,0), Vector3D(1,2,3))
            >>> result = hl.project_2D(0)
            >>> print(result)
            Line2D(Point2D(0,0), Vector2D(2,3))   
        
        """
        
        if coordinate_index==0:
            return Halfline2D(Point2D(self.P0.y,self.P0.z),
                              Vector2D(self.vL.y,self.vL.z))
        elif coordinate_index==1:
            return Halfline2D(Point2D(self.P0.z,self.P0.x),
                              Vector2D(self.vL.z,self.vL.x))
        elif coordinate_index==2:
            return Halfline2D(Point2D(self.P0.x,self.P0.y),
                              Vector2D(self.vL.x,self.vL.y))
        else:
            raise Exception
                    
        
    
    