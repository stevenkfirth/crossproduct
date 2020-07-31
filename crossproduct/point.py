# -*- coding: utf-8 -*-

from .vector import Vector2D, Vector3D

SMALL_NUM=0.00000001


class Point():
    " A n-D point"

    classname='Point'
    
    def distance_to_point(self,point):
        """Returns the distance to the supplied point.
        
        :param point: The point to calculate the distance to.
        :type point: Point2D or Point3D
        
        :return: The distance between the two points.
        :rtype: float
        
        :Example:
    
        .. code-block:: python
           
           # 2D example
           >>> p1 = Point2D(1,2)
           >>> p1 = Point2D(2,2)
           >>> result = p1.distance_to_point(p2)
           >>> print(result)
           1
           
           # 3D example
           >>> p1 = Point3D(1,2,3)
           >>> p1 = Point3D(2,2,3)
           >>> result = p1.distance_to_point(p2)
           >>> print(result)
           1
            
        """
        return (point-self).length
    


class Point2D(Point):
    """A two dimensional point, situated on an x, y plane.
    
    :param x: The x coordinate of the point.
    :type x: float
    :param y: The y coordinate of the point.
    :type y: float
    
    :Example:
    
    .. code-block:: python
       
       >>> p = Point2D(1,2)
       >>> print(p)
       Point2D(1,2)
    
    """
    
    def __init__(self,x,y):
        ""
        self._x=x
        self._y=y
            
        
    def __add__(self,vector):
        """The addition of this point and a vector.
        
        :param vector: The vector to be added to the point.
        :type vector: Vector2D
        
        :rtype: Point2D
        
        :Example:
    
        .. code-block:: python
        
            >>> p = Point2D(1,2)
            >>> result = p + Vector2D(1,1)
            >>> print(result)
            Point2D(2,3)
        
        """
        return Point2D(self.x+vector.x,
                       self.y+vector.y)
        
        
        
    def __eq__(self,point):
        """Tests if this point and the supplied point are equal.
        
        :param point: The point to be tested.
        :type point: Point2D
        
        :return: True if the point coordinates are the same, otherwise False.
        :rtype: bool
        
        :Example:
    
        .. code-block:: python
        
            >>> result = Point2D(1,2) == Point2D(2,2)
            >>> print(result)
            False
            
        """
        if isinstance(point,Point2D):
            return (abs(self.x-point.x)<SMALL_NUM and 
                    abs(self.y-point.y)<SMALL_NUM)
        else:
            return False
    
    
    def __lt__(self,point):
        """Tests if the coordinates of this point are lower than the supplied point.
        
        :param point: The point to be tested.
        :type point: Point2D
        
        :return: True if the x coordinate of this point is lower than the 
            supplied point, otherwise False. If both x coordinates are equal, then 
            True if the y coordinate of this point is lower than the 
            supplied point, otherwise False. 
        :rtype: bool
        
        :Example:
    
        .. code-block:: python
        
            >>> result = Point2D(1,2) < Point2D(2,2)
            >>> print(result)
            True
        
        """
        if self.x < point.x:
            return True
        else:
            if self.x == point.x and self.y < point.y:
                return True
            else:
                return False
        
        
        
    
    def __repr__(self):
        ""
        return 'Point2D(%s)' % ','.join([str(c) for c in self.coordinates])
    
    
    def __sub__(self,point_or_vector):
        """Subtraction of supplied object from this point.
        
        :param point_or_vector: Either a 2D point or a 2D vector
        :type point_or_vector: Point2D or Vector2D
        
        :return: If a point is supplied, then a vector is returned (i.e. v=P1-P0). 
            If a vector is supplied, then a point is returned (i.e. P1=P0-v).
        :rtype: Point2D or Vector2D
        
        :Example:
    
        .. code-block:: python
        
            >>> result = Point2D(2,2) - Point2D(1,2)
            >>> print(result)
            Vector2D(1,0)
        
        """
        obj=point_or_vector
        if isinstance(obj,Point2D):
            return Vector2D(self.x-obj.x,
                            self.y-obj.y)
        elif isinstance(obj,Vector2D):
            return Point2D(self.x-obj.x,
                           self.y-obj.y)
        else:
            raise TypeError
    
    
    @property
    def coordinates(self):
        """The coordinates of the point
        
        :return: The x and y coordinates as a tuple (x,y)
        :rtype: tuple
        
        :Example:
    
        .. code-block:: python
        
            >>> p = Point2D(2,1)
            >>> print(p.coordinates)
            (2,1)            
        
        """
        return self.x, self.y
    
    
    @property
    def dimension(self):
        """The dimension of the point.
        
        :return: '2D'
        :rtype: str
        
        :Example:
    
        .. code-block:: python
        
            >>> p = Point2D(2,1)
            >>> print(p.dimension)
            '2D'     
        
        """
        
        return '2D'
    
    
    def project_3D(self,plane,coordinate_index):
        """Projection of the point on a 3D plane
        
        :param plane: The plane for the projection
        :type plane: Plane3D
        :param coordinate_index: The index of the coordinate which was ignored 
            to create the 2D projection. For example, coordinate_index=0
            means that the x-coordinate was ignored and this point
            was originally projected onto the yz plane.
        :type coordinate_index: int
        
        :return: The 3D point as projected onto the plane.
        :rtype: Point3D
               
        :Example:
    
        .. code-block:: python
        
            >>> pt = Point2D(2,2)
            >>> pl = Plane3D(Point3D(0,0,1), Vector3D(0,0,1))
            >>> result = pt.project_3D(pl, 2)
            Point3D(2,2,1)   
        
        """
        
        if coordinate_index==0:
            point=plane.point_yz(self.x,self.y)
        elif coordinate_index==1:
            point=plane.point_zx(self.x,self.y)
        elif coordinate_index==2:
            point=plane.point_xy(self.x,self.y)
        else:
            raise ValueError
            
        return point
    
    
    @property
    def x(self):
        """The x coordinate of the point.
        
        :rtype: float
        
        """
        return self._x
    
    
    @property
    def y(self):
        """The y coordinate of the point.
        
        :rtype: float
        
        """
        return self._y
    

class Point3D(Point):
    """A three dimensional point, situated on an x, y, z plane.
    
    :param x: The x coordinate of the point.
    :type x: float
    :param y: The y coordinate of the point.
    :type y: float
    :param z: The z coordinate of the point.
    :type z: float
    
    :Example:
    
    .. code-block:: python
       
       >>> p = Point3D(1,2,3)
       >>> print(p)
       Point3D(1,2,3)
    
    """
    
    def __init__(self,x,y,z):
        ""
        self._x=x
        self._y=y
        self._z=z
    
    
    def __add__(self,vector):
        """The addition of this point and a vector.
        
        :param vector: The vector to be added to the point.
        :type vector: Vector3D
        
        :rtype: Point3D
        
        :Example:
    
        .. code-block:: python
        
            >>> p = Point3D(1,2,3)
            >>> result = p + Vector3D(1,1,1)
            >>> print(result)
            Point3D(2,3,4)
        
        """
        return Point3D(self.x+vector.x,
                       self.y+vector.y,
                       self.z+vector.z)
                    
    
    def __eq__(self,point):
        """Tests if this point and the supplied point are equal.
        
        :param point: The point to be tested.
        :type point: Point3D
        
        :return: True if the point coordinates are the same, otherwise False.
        :rtype: bool
        
        :Example:
    
        .. code-block:: python
        
            >>> result = Point3D(1,2,3) == Point3D(2,2,2)
            >>> print(result)
            False
            
        """
        if isinstance(point,Point3D):
            return (abs(self.x-point.x)<SMALL_NUM 
                    and abs(self.y-point.y)<SMALL_NUM
                    and abs(self.z-point.z)<SMALL_NUM
                    )
        else:
            return False
            
        
    def __lt__(self,point):
        """Tests if the coordinates of this point are lower than the supplied point.
        
        :param point: The point to be tested.
        :type point: Point3D
        
        :return: True if the x coordinate of this point is lower than the 
            supplied point, otherwise False. If both x coordinates are equal, then 
            True if the y coordinate of this point is lower than the 
            supplied point, otherwise False. If both x and y coordinates are equal, then 
            True if the z coordinate of this point is lower than the 
            supplied point, otherwise False. 
            
        :rtype: bool
        
        :Example:
    
        .. code-block:: python
        
            >>> result = Point3D(1,2,3) < Point3D(2,2,2)
            >>> print(result)
            True
        
        """
        if self.x < point.x:
            return True
        else:
            if self.x == point.x and self.y < point.y:
                return True
            else:
                if self.y == point.y and self.z < point.z:
                    return True
                else:
                    return False
        
    
    def __repr__(self):
        """The string of this point for printing
        
        :return result:
        :rtype str:
            
        """
        return 'Point3D(%s)' % ','.join([str(c) for c in self.coordinates])
    
    
    def __sub__(self,point_or_vector):
        """Subtraction of supplied object from this point.
        
        :param point_or_vector: Either a 3D point or a 3D vector
        :type point_or_vector: Point3D or Vector3D
        
        :return: If a point is supplied, then a vector is returned (i.e. v=P1-P0). 
            If a vector is supplied, then a point is returned (i.e. P1=P0-v).
        :rtype: Point3D or Vector3D
        
        :Example:
    
        .. code-block:: python
        
            >>> result = Point3D(2,2,2) - Point3D(1,2,3)
            >>> print(result)
            Vector3D(1,0,-1)
        
        """
        obj=point_or_vector
        if isinstance(obj,Point3D):
            return Vector3D(self.x-obj.x,
                            self.y-obj.y,
                            self.z-obj.z)
        elif isinstance(obj,Vector3D):
            return Point3D(self.x-obj.x,
                           self.y-obj.y,
                           self.z-obj.z)
        else:
            raise TypeError
            
    
    @property
    def coordinates(self):
        """The coordinates of the point
        
        :return: The x, y and z coordinates as a tuple (x,y,z).
        :rtype: tuple
        
        :Example:
    
        .. code-block:: python
        
            >>> p = Point3D(2,1,3)
            >>> print(p.coordinates)
            (2,1,3)            
        
        """
        return self.x, self.y, self.z
    
    
    @property
    def dimension(self):
        """The dimension of the point.
        
        :return: '3D'
        :rtype: str
        
        :Example:
    
        .. code-block:: python
        
            >>> p = Point3D(1,2,3)
            >>> print(p.dimension)
            '3D'     
        
        """
        
        return '3D'
    
    
    def project_2D(self,coordinate_index):
        """Projection of the 3D point as a 2D point.
        
        :param coordinate_index: The index of the coordinate to ignore.
            Use coordinate_index=0 to ignore the x-coordinate, coordinate_index=1 
            for the y-coordinate and coordinate_index=2 for the z-coordinate.
        :type coordinate_index: int
        
        :return: A 2D point based on the projection of the 3D point.
        :rtype: Point2D
               
        :Example:
    
        .. code-block:: python
        
            >>> pt = Point3D(1,2,3)
            >>> result = pt.project_2D(1)
            >>> print(result)
            Point2D(1,3)   
        
        """
        
        if coordinate_index==0:
            return Point2D(self.y,self.z)
        elif coordinate_index==1:
            return Point2D(self.z,self.x)
        elif coordinate_index==2:
            return Point2D(self.x,self.y)
        else:
            raise ValueError
                    
        
    @property
    def x(self):
        """The x coordinate of the point.
        
        :rtype: float
        
        """
        return self._x
    
    
    @property
    def y(self):
        """The y coordinate of the point.
        
        :rtype: float
        
        """
        return self._y
    
    
    @property
    def z(self):
        """The z coordinate of the point.
        
        :rtype: float
        
        """
        return self._z
    
    
    