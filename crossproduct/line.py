# -*- coding: utf-8 -*-


from .point import Point2D
from .vector import Vector2D


SMALL_NUM=0.00000001


class Line():
    "A n-D line"
    
    classname='Line'
    
    def __init__(self,P0,vL,validate=False):
        ""
        if validate:
            if vL.length<SMALL_NUM:
                raise ValueError('length of vL must be greater than zero')
                
        self._P0=P0
        self._vL=vL
    
    
    def __contains__(self,obj):
        """Tests if the line contains the object
        
        :param obj: A point, halfline or segment.
        :type obj: Point2D, Point3D, Halfline2D, Halfline3D, Segment2D or Segment3D
            
        :return:  For point, True if the point lies on the line; otherwise False. 
            For halfline, True if the halfline startpoint is on the line and 
            the halfline vector is collinear to the line vector; otherwise False. 
            For segment, True if the segment start and endpoints are on the line; otherwise False. 
        :rtype: bool
        
        :Example:
    
        .. code-block:: python
           
           # 2D example
           >>> l = Line2D(Point2D(0,0), Vector2D(1,0))
           >>> result = Point2D(2,0) in l
           >>> print(result)
           True
           
           # 3D example
           >>> l = Line3D(Point3D(0,0,0), Vector3D(1,0,0))
           >>> hl = Halfline3D(Point3D(0,0,0), Vector3D(-1,0,0))
           >>> result = hl in l
           >>> print(result)
           True
            
        """
        if obj.classname=='Point':
            t=self.calculate_t_from_point(obj)
            pt=self.calculate_point(t)           
            return obj==pt 
                    
        elif obj.classname=='Halfline':
            return obj.P0 in self and obj.vL.is_collinear(self.vL)
        
        elif obj.classname=='Segment':
            return obj.P0 in self and obj.P1 in self
        
        else:
            raise TypeError
        
        
    def __eq__(self,line):
        """Tests if this line and the supplied line are equal.
        
        :param line: A line.
        :type line: Line2D or Line3D
        
        :return: True if the start point of supplied line lies on line (self),
            and the vL of supplied line is collinear to the vL of line (self); 
            otherwise False.
        :rtype: bool
            
        :Example:
    
        .. code-block:: python
           
           # 2D example
           >>> l = Line2D(Point2D(0,0), Vector2D(1,0))
           >>> result = l == l
           >>> print(result)
           True
           
           # 3D example
           >>> l1 = Line3D(Point3D(0,0,0), Vector3D(1,0,0))
           >>> l2 = Line3D(Point3D(0,0,0), Vector3D(-1,0,0))
           >>> result = l1 == l2
           >>> print(result)
           True
           
        """
        if isinstance(line,Line):
            return line.P0 in self and line.vL.is_collinear(self.vL)
        else:
            return False
        
        
    def calculate_point(self,t):
        """Returns a point on the line for a given t value. 
        
        :param t: The t value of the equation of the line.
        :type t: float
        
        :return: A point on the line calcualted using the t value. 
        :rtype: Point2D or Point3D
        
        :Example:
        
        .. code-block:: python    
        
           # 2D example
           >>> l = Line2D(Point2D(0,0), Vector2D(1,0))
           >>> result = l.calcuate_point(3)
           >>> print(result)
           Point2D(3,0)
           
           # 3D example
           >>> l = Line3D(Point3D(0,0,0), Vector3D(1,0,0))
           >>> result = l.calcuate_point(-3)
           >>> print(result)
           Point3D(-3,0,0)
        
        """
        return self.P0 + (self.vL * t)
    
    
    def calculate_t_from_x(self,x):
        """Returns t for a given x coordinate. 
        
        :param x: A x coordinate.
        :type x: float
        
        :return: The calculated t value.
        :rtype: float
        
        :Example:
        
        .. code-block:: python
           
           # 2D example
           >>> l = Line2D(Point2D(0,0), Vector2D(1,0))
           >>> result = l.calculate_t_from_x(3)
           >>> print(result)
           3
           
           # 3D example
           >>> l = Line3D(Point3D(0,0,0), Vector3D(1,0,0))
           >>> result = l.calculate_t_from_x(3)
           >>> print(result)
           3
        
        """
        try:
            return (x-self.P0.x) / (self.vL.x)
        except ZeroDivisionError:
            raise ValueError('%s has a vector with an x component of 0' % self)
    
    
    def calculate_t_from_y(self,y):
        """Returns t for a given y coordinate. 
        
        :param y: A y coordinate.
        :type y: float
        
        :return: The calculated t value.
        :rtype: float
        
        :Example:
        
        .. code-block:: python
           
           # 2D example
           >>> l = Line2D(Point2D(0,0), Vector2D(0,1))
           >>> result = l.calculate_t_from_y(3)
           >>> print(result)
           3
           
           # 3D example
           >>> l = Line3D(Point3D(0,0,0), Vector3D(0,1,0))
           >>> result = l.calculate_t_from_y(3)
           >>> print(result)
           3
           
        """
        try:
            return (y-self.P0.y) / (self.vL.y)
        except ZeroDivisionError:
            raise ValueError('%s has a vector with an y component of 0' % self)
    
    
    
    def distance_to_point(self,point):
        """Returns the distance from this line to the supplied point.
        
        :param point: A point.
        :type point: Point2D or Point3D
                    
        :return: The distance from the line to the point. 
        :rtype: float
        
        :Example:
    
        .. code-block:: python
           
           # 2D example
           >>> l = Line2D(Point2D(0,0), Vector2D(1,0))
           >>> result = l.distance_to_point(Point2D(0,10))
           >>> print(result)
           10
           
           # 3D example
           >>> l = Line3D(Point3D(0,0,0), Vector3D(1,0,0))
           >>> result = l.distance_to_point(Point3D(10,0,0))
           >>> print(result)
           0
            
        .. seealso:: `<https://geomalgorithms.com/a02-_lines.html>`_
            
        """
        w=point-self.P0
        b=w.dot(self.vL) / self.vL.dot(self.vL)
        ptB=self.P0+self.vL*b
        return (ptB-point).length
        
    
    def intersect_line(self,line):
        """Returns the intersection of this line with the supplied line. 
        
        :param line: A line.
        :type line: Line2D or Line3D
        
        :return: Returns a line (this line) if lines are collinear. 
            Returns None (i.e. no intersection) if lines are parallel. 
            For 2D, returns a point if lines are skew.  
            For 3D, returns either None or a point if lines are skew. 
        :rtype: None, Point2D, Point3D, Line2D, Line3D. 
        
        :Example:
    
        .. code-block:: python
           
           # 2D example
           >>> l1 = Line2D(Point2D(0,0), Vector2D(1,0))
           >>> l2 = Line2D(Point2D(0,0), Vector2D(0,1))
           >>> result = l.intersect_line(l2)
           >>> print(result)
           Point2D(0,0)
           
           # 3D example
           >>> l1 = Line3D(Point3D(0,0,0), Vector3D(1,0,0))
           >>> l2 = Line3D(Point3D(0,0,1), Vector3D(1,0,0))
           >>> result = l1.intersect_line(l2)
           >>> print(result)
           None
        
        .. seealso:: `<https://geomalgorithms.com/a05-_intersect-1.html>`_
        
        """
        if self==line: # test for collinear lines
            return self
        elif self.is_parallel(line): # test for parallel lines
            return None 
        else: # a skew line
            return self._intersect_line_skew(line)
    
    
    def is_parallel(self,line):
        """Tests if this line and the supplied line are parallel. 
        
        :param obj: A line.
        :type obj: Line2D, Line3D
        
        :return: Returns True if the lines are parallel; 
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
        return self.vL.is_collinear(line.vL)
    
    
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



class Line2D(Line):
    """A two dimensional line, situated on an x, y plane.
    
    Equation of the line is P(t) = P0 + vL*t where:
    
        - P(t) is a point on the line; 
        - P0 is the start point of the line; 
        - vL is the line vector; 
        - t is any real number.
    
    :param P0: The start point of the line.
    :type P0: Point2D
    :param vL: The line vector.
    :type vL: Vector2D
    
    :Example:
    
    .. code-block:: python
       
       >>> l = Line2D(Point2D(0,0), Vector2D(1,0))
       >>> print(l)
       Line2D(Point2D(0,0), Vector2D(1,0))
    
    .. seealso:: `<https://geomalgorithms.com/a02-_lines.html>`_
    
    """
    
    def __repr__(self):
        ""
        return 'Line2D(%s, %s)' % (self.P0,self.vL)
    
    
    def calculate_t_from_point(self,point):
        """Returns t for a given point.
        
        :param point: A point on the line.
        :type point: Point2D
        
        :return: The calculated t value.
        :rtype: float
        
        :Example:
        
        .. code-block:: python
           
           >>> l = Line2D(Point2D(0,0), Vector2D(1,0))
           >>> result = l.calculate_t_from_point(Point2D(3,0))
           >>> print(result)
           3
            
        """
        try:
            return self.calculate_t_from_x(point.x)
        except ValueError:
            return self.calculate_t_from_y(point.y)
        
    
    @property
    def dimension(self):
        """The dimension of the line.
        
        :return: '2D'
        :rtype: str
        
        :Example:
    
        .. code-block:: python
        
            >>> l = Line2D(Point2D(0,0), Vector2D(1,0))
            >>> print(l.dimension)
            '2D'     
        
        """
        
        return '2D'
    
    
    def distance_to_line(self,line):
        """Returns the distance from this line to the supplied line.
        
        :param line: A line.
        :type line: Line2D
        
        :return: The distance between the two lines.
        :rtype: float
        
        :Example:
        
        .. code-block:: python
           
           >>> l1 = Line2D(Point2D(0,0), Vector2D(1,0))
           >>> l2 = Line2D(Point2D(0,1), Vector2D(1,0))
           >>> result = l1.distance_to_line(l2)
           >>> print(result)
           1
        
        .. seealso:: `<https://geomalgorithms.com/a07-_distance.html>`_
        
        """
        if self.is_parallel(line):
            return self.distance_to_point(line.P0)
        else:
            return 0 # as these are skew infinite 2D lines
                    
        
    def _intersect_line_skew(self,skew_line):
        """Returns the point of intersection of this line and the supplied skew line
        """
        u=self.vL
        v=skew_line.vL
        w=self.P0-skew_line.P0 
        t=-v.perp_product(w) / v.perp_product(u)
        return self.calculate_point(t)
        
        
        
        
class Line3D(Line):
    """A three dimensional line, situated on an x, y, z plane.
    
    Equation of the line is P(t) = P0 + vL*t where:
    
        - P(t) is a point on the line; 
        - P0 is the start point of the line; 
        - vL is the line vector; 
        - t is any real number.
    
    :param P0: The start point of the line.
    :type P0: Point3D
    :param vL: The line vector.
    :type vL: Vector3D
    
    :Example:
    
    .. code-block:: python
       
       >>> l = Line3D(Point3D(0,0,0), Vector3D(1,0,0))
       >>> print(l)
       Line3D(Point3D(0,0,0), Vector3D(1,0,0))
    
    .. seealso:: `<https://geomalgorithms.com/a02-_lines.html>`_
    
    """     
    
    def __repr__(self):
        ""
        return 'Line3D(%s, %s)' % (self.P0,self.vL)
        
        
    def calculate_t_from_point(self,point):
        """Returns t for a given point.
        
        :param point: A point on the line.
        :type point: Point3D
        
        :return: The calculated t value.
        :rtype: float
        
        :Example:
        
        .. code-block:: python
           
           >>> l = Line3D(Point3D(0,0), Vector3D(1,0))
           >>> result = l.calculate_t_from_point(Point3D(3,0))
           >>> print(result)
           3
            
        """
        try:
            return self.calculate_t_from_x(point.x)
        except ValueError:
            try:
                return self.calculate_t_from_y(point.y)
            except ValueError:
                return self.calculate_t_from_z(point.z)
                
            
    def calculate_t_from_z(self,z):
        """Returns t for a given z coordinate. 
        
        :param z: A z coordinate.
        :type z: float
        
        :return: The calculated t value.
        :rtype: float
        
        :Example:
        
        .. code-block:: python
           
           >>> l = Line3D(Point3D(0,0,0), Vector3D(0,0,1))
           >>> result = l.calculate_t_from_z(3)
           >>> print(result)
           3
        
        """
        try:
            return (z-self.P0.z) / (self.vL.z)
        except ZeroDivisionError:
            raise ValueError('%s has a vector with an z component of 0' % self)
    
    
    @property
    def dimension(self):
        """The dimension of the line.
        
        :return: '3D'
        :rtype: str
        
        :Example:
    
        .. code-block:: python
        
            >>> l = Line3D(Point3D(0,0,0), Vector3D(0,0,1))
            >>> print(l.dimension)
            '3D'     
        
        """
        
        return '3D'
    
    
    def distance_to_line(self,line):
        """Returns the distance from this line to the supplied line.
        
        :param line: A line.
        :type line: Line3D
        
        :return: The distance between the two lines.
        :rtype: float
        
        :Example:
        
        .. code-block:: python
           
           >>> l1 = Line3D(Point3D(0,0,0), Vector3D(1,0,0))
           >>> l2 = Line3D(Point3D(0,1,0), Vector3D(0,0,1))
           >>> result = l1.distance_to_line(l2)
           >>> print(result)
           1
        
        .. seealso:: `<https://geomalgorithms.com/a07-_distance.html>`_
        
        """
        if self.is_parallel(line):
                
            return self.distance_to_point(line.P0)
        
        else:
            
            w0=self.P0-line.P0
            u=self.vL
            v=line.vL
            a=u.dot(u)
            b=u.dot(v)
            c=v.dot(v)
            d=u.dot(w0)
            e=v.dot(w0)
            
            sc=(b*e-c*d) / (a*c-b**2)
            tc=(a*e-b*d) / (a*c-b**2)
            
            Pc=self.calculate_point(sc)
            Qc=line.calculate_point(tc)
            
            return (Pc-Qc).length

        
    def _intersect_line_skew(self,skew_line):
        """Returns the point of intersection of this line and the supplied (skew) line
        
        - return value can be:
            - None -> no intersection (for skew lines which do not intersect in 3D space)
            - Point3D -> a point (for skew lines which intersect)
        
        """
        if not self.is_parallel(skew_line):
        
            # find the coordinate to ignore for the projection
            cp=self.vL.cross_product(skew_line.vL)
            absolute_coords=[abs(x) for x in cp.coordinates] 
            i=absolute_coords.index(max(absolute_coords)) % 3 # the coordinate to ignore for projection
                    
            #print('i',i)
            
            # project 3D lines to 2D
            self2D=self.project_2D(i)
            skew_line2D=skew_line.project_2D(i)
            
            #print('self2D', self2D)
            #print('skew_line2D',skew_line2D)
            
            # find intersection point for 2D lines
            ipt=self2D._intersect_line_skew(skew_line2D)
            
            # find t values for the intersection point on each 2D line
            t1=self2D.calculate_t_from_point(ipt)
            t2=skew_line2D.calculate_t_from_point(ipt)
            
            # calculate the 3D intersection points from the t values
            ipt1=self.calculate_point(t1)
            ipt2=skew_line.calculate_point(t2)
            
            #print(ipt1,ipt2)
            
            if ipt1==ipt2: # test the two 3D intersection points are the same
                return ipt1
            else:
                return None
        
        else:
            raise ValueError('%s and %s are not skew lines' % (self,skew_line))
        
        
    def project_2D(self,coordinate_index):
        """Projection of the 3D line as a 2D line.
        
        :param coordinate_index: The index of the coordinate to ignore.
            Use coordinate_index=0 to ignore the x-coordinate, coordinate_index=1 
            for the y-coordinate and coordinate_index=2 for the z-coordinate.
        :type coordinate_index: int
        
        :return: A 2D line based on the projection of the 3D line.
        :rtype: Line2D
               
        :Example:
    
        .. code-block:: python
        
            >>> l = Line3D(Point3D(0,0,0), Vector3D(1,2,3))
            >>> result = l.project_2D(0)
            >>> print(result)
            Line2D(Point2D(0,0), Vector2D(2,3))   
        
        """
        
        if coordinate_index==0:
            return Line2D(Point2D(self.P0.y,self.P0.z),
                          Vector2D(self.vL.y,self.vL.z))
        elif coordinate_index==1:
            return Line2D(Point2D(self.P0.z,self.P0.x),
                          Vector2D(self.vL.z,self.vL.x))
        elif coordinate_index==2:
            return Line2D(Point2D(self.P0.x,self.P0.y),
                          Vector2D(self.vL.x,self.vL.y))
        else:
            raise ValueError
                    
        


