# -*- coding: utf-8 -*-

import collections.abc
import itertools
import math

from .vector import Vector

ABS_TOL = 1e-7 # default value for math.isclose



class Point(collections.abc.Sequence):
    """A point, as described by xy or xyz coordinates.
    
    In crossproduct a Point object is a immutable sequence. 
    Iterating over a Point will provide its coordinates.
    Indexing a Point will return the coordinate for that index (0=x, 1=y, 2=z)
    
    :param coordinates: Argument list of two (xy) or three (xyz) coordinates. 
        Coordinates should be of type int, float or similar numeric. These values
        are converted to floats.
    
    :raises ValueError: If less then 2 or more than 3 arguments are supplied.
    
    .. rubric:: Code Example
    
    .. code-block:: python
       
       >>> pt = Point(1,2)
       >>> print(pt)
       Point(1.0,2.0)
       >>> print(list(pt))      # print a list of the coordinates
       [1.0,2.0]
       >>> print(pt[1])      # print the y coordinate
       2.0
    
    .. seealso:: `<https://geomalgorithms.com/points_and_vectors.html#Basic-Definitions>`_
    
    """
    
    def __add__(self,vector):
        """The addition of this point and a vector.
        
        :param vector: The vector to be added to the point.
        :type vector: Vector
        
        :rtype: Point
        
        .. rubric:: Code Example
    
        .. code-block:: python
        
            >>> p = Point(1,2)
            >>> result = p + Vector(1,1)
            >>> print(result)
            Point(2.0,3.0)
        
        .. seealso:: `<https://geomalgorithms.com/points_and_vectors.html#Vector-Addition>`_
        
        """
        zipped=itertools.zip_longest(self,vector) # missing values filled with None
        try:
            coordinates=[a+b for a,b in zipped]
        except TypeError: # occurs if, say, a or b is None
            raise ValueError('Point and vector to add must be of the same length.')
        return Point(*coordinates)
    
    
    def __eq__(self,point):
        """Tests if this point and the supplied point have the same coordinates.
        
        A tolerance value is used so coordinates with very small difference 
        are considered equal.
        
        :param point: The point to be tested.
        :type point: Point
        
        :raises ValueError: If points are not of the same length.
        
        :return: True if the point coordinates are the same, otherwise False.
        :rtype: bool
        
        .. rubric:: Code Example
    
        .. code-block:: python
        
            >>> result = Point(1,2) == Point(2,2)
            >>> print(result)
            False
            
        """
        zipped=itertools.zip_longest(self,point) # missing values filled with None
        try:
            result=[self._coordinates_equal(a,b) for a,b in zipped]
        except TypeError: # occurs if, say, a or b is None
            raise ValueError('Points to compare must be of the same length.')
        return all(result)
    
    
    def __getitem__(self,index):
        ""
        return self._coordinates[index]
    
    
    def __init__(self,*coordinates):
        ""
        if len(coordinates)==2 or len(coordinates)==3:
            self._coordinates=tuple(float(c) for c in coordinates)
        else:
            raise ValueError('Point coordinates must have a length of 2 or 3')


    def __len__(self):
        ""
        return len(self._coordinates)


    def __lt__(self,point):
        """Tests if the coordinates of this point are lower than the supplied point.
        
        A tolerance value is used so coordinates with very small difference 
        are considered equal.
        
        :param point: The point to be tested.
        :type point: Point
        
        :raises ValueError: If points are not of the same length.
        
        :return: True if the x coordinate of this point is lower than the 
            supplied point, otherwise False. If both x coordinates are equal, then 
            True if the y coordinate of this point is lower than the 
            supplied point, otherwise False. For 3D points -> if both x and y coordinates 
            are equal, then 
            True if the z coordinate of this point is lower than the 
            supplied point, otherwise False. 
        :rtype: bool
        
        .. rubric:: Code Example
    
        .. code-block:: python
        
            >>> result = Point(1,2) < Point(2,2)
            >>> print(result)
            True
        
        """
        zipped=itertools.zip_longest(self,point) # missing values filled with None
        try:
            for a,b in zipped:
                if self._coordinates_equal(a, b): continue
                return a<b
        except TypeError: # occurs if, say, a or b is None
            raise ValueError('Points to compare must be of the same length.')
    
    
    def __repr__(self):
        ""
        return 'Point(%s)' % ','.join([str(c) for c in self])
    
        
    def __sub__(self,point_or_vector):
        """Subtraction of supplied object from this point.
        
        :param point_or_vector: Either a point or a vector.
        :type point_or_vector: Point or Vector
        
        :return: If a point is supplied, then a vector is returned (i.e. v=P1-P0). 
            If a vector is supplied, then a point is returned (i.e. P1=P0-v).
        :rtype: Point2D or Vector2D
        
        .. rubric:: Code Example
    
        .. code-block:: python
        
            >>> result = Point(2,2) - Point(1,2)
            >>> print(result)
            Vector(1.0,0.0)
        
        """
        zipped=itertools.zip_longest(self,point_or_vector) # missing values filled with None
        try:
            coordinates=[a-b for a,b in zipped]
        except TypeError: # occurs if, say, a or b is None
            raise ValueError(r'Point and point/vector to subtract must be of the same length.')
        if isinstance(point_or_vector,Point):
            return Vector(*coordinates)
        else:
            return Point(*coordinates)
            
    
    def _coordinates_equal(self,a,b):
        """Return True if a and b are equal within the tolerance value.
        """
        return math.isclose(a, b, abs_tol=ABS_TOL)
        
    
    
    def distance_to_point(self,point):
        """Returns the distance to the supplied point.
        
        :param point: The point to calculate the distance to.
        :type point: Point
        
        :return: The distance between the two points.
        :rtype: float
        
        .. rubric:: Code Example
    
        .. code-block:: python
           
           >>> p1 = Point(1,2)
           >>> p1 = Point(2,2)
           >>> result = p1.distance_to_point(p2)
           >>> print(result)
           1
            
        """
        return (point-self).length
    
    
    def project_2D(self,coordinate_index):
        """Projection of a 3D point as a 2D point.
        
        :param coordinate_index: The index of the coordinate to ignore.
            Use coordinate_index=0 to ignore the x-coordinate, coordinate_index=1 
            for the y-coordinate and coordinate_index=2 for the z-coordinate.
        :type coordinate_index: int
        
        :raises ValueError: If coordinate_index is not between 0 and 2.
        
        :return: A 2D point based on the projection of the 3D point.
        :rtype: Point2D
               
        .. rubric:: Code Example
    
        .. code-block:: python
        
            >>> pt = Point(1,2,3)
            >>> result = pt.project_2D(1)
            >>> print(result)
            Point(1.0,3.0)   
        
        """
        
        if coordinate_index==0:
            return Point(self.y,self.z)
        elif coordinate_index==1:
            return Point(self.z,self.x)
        elif coordinate_index==2:
            return Point(self.x,self.y)
        else:
            raise ValueError('coordinate_index must be between 0 and 2')
    
    
    def project_3D(self,plane,coordinate_index):
        """Projection of the point on a 3D plane.
        
        :param plane: The plane for the projection
        :type plane: Plane
        :param coordinate_index: The index of the coordinate which was ignored 
            to create the 2D projection. For example, coordinate_index=0
            means that the x-coordinate was ignored and this point
            was originally projected onto the yz plane.
        :type coordinate_index: int
        
        :raises ValueError: If coordinate_index is not between 0 and 2.
        
        :return: The 3D point as projected onto the plane.
        :rtype: Point
               
        .. rubric:: Code Example
    
        .. code-block:: python
        
            >>> pt = Point(2,2)
            >>> pl = Plane3D(Point(0,0,1), Vector(0,0,1))
            >>> result = pt.project_3D(pl, 2)
            Point(2.0,2.0,1.0)   
        
        """
        
        if coordinate_index==0:
            point=plane.point_yz(self.x,self.y)
        elif coordinate_index==1:
            point=plane.point_zx(self.x,self.y)
        elif coordinate_index==2:
            point=plane.point_xy(self.x,self.y)
        else:
            raise ValueError('coordinate_index must be between 0 and 2')
            
        return point
    
    
    @property
    def x(self):
        """The x coordinate of the point.
        
        :rtype: int, float
        
        """
        return self[0]
    
    
    @property
    def y(self):
        """The y coordinate of the point.
        
        :rtype: int, float
        
        """
        return self[1]
    
    
    @property
    def z(self):
        """The z coordinate of the point.
        
        :raises IndexError: If point is a 2D point.
        
        :rtype: int, float
        
        """
        return self[2]
    
    
    
    
    
    


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
    
    .. seealso:: `<https://geomalgorithms.com/points_and_vectors.html#Basic-Definitions>`_
    
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
        
        .. seealso:: `<https://geomalgorithms.com/points_and_vectors.html#Vector-Addition>`_
        
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
        return 'Point2D(%s)' % ','.join([str(round(c,4)) for c in self.coordinates])
    
    
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
        """The coordinates of the point.
        
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
        """Projection of the point on a 3D plane.
        
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
    
    .. seealso:: `<https://geomalgorithms.com/points_and_vectors.html#Basic-Definitions>`_
    
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
        
        .. seealso:: `<https://geomalgorithms.com/points_and_vectors.html#Vector-Addition>`_
        
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
        """The string of this point for printing.
        
        :return result:
        :rtype str:
            
        """
        return 'Point3D(%s)' % ','.join([str(c) for c in self.coordinates])
        #return 'Point3D(%s)' % ','.join([str(round(c,4)) for c in self.coordinates])
    
    
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
        """The coordinates of the point.
        
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
    
    
    