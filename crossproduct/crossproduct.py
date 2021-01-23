# -*- coding: utf-8 -*-

import collections.abc
import itertools
import math

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
            result=[math.isclose(a, b, abs_tol=ABS_TOL) for a,b in zipped]
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
                if math.isclose(a, b, abs_tol=ABS_TOL): continue
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
    


class Points(collections.abc.MutableSequence):
    """A sequence of points.    
    
    In crossproduct a Points object is a mutable sequence. 
    Iterating over a Points object will provide its Point instances.
    Index, append, insert and delete actions are available.
    
    :param points: An argument list of Point instances. 
    
    .. rubric:: Code Example
        
    .. code-block:: python
        
        >>> pts = Points(Point(0,0), Point(1,0))
        >>> print(pts)
        Points(Point(0.0,0.0), Point(1.0,0.0))
        
        >>> print(pts[1])
        Point(1.0,0.0)
    
    """
    
    def __delitem__(self,index):
        ""
        del self._points[index]
        
    
    def __getitem__(self,index):
        ""
        return self._points[index]
    
    
    def __init__(self,*points):
        ""
        self._points=list(points)
    
    
    def __len__(self):
        ""
        return len(self._points)
    
    
    def __repr__(self):
        ""
        return 'Points(%s)' % ', '.join([str(pt) for pt in self])
    
    
    def __setitem__(self,index,value):
        ""
        self._points[index]=value
    
    
    def insert(self,index,value):
        ""
        return self._points.insert(index,value)
    
    

class Vector(collections.abc.Sequence):
    """A vector, as described by xy or xyz coordinates.
    
    In crossproduct a Vector object is a immutable sequence. 
    Iterating over a Vector will provide its coordinates.
    Indexing a vector will return the coordinate for that index (0=x, 1=y, 2=z)
    
    :param coordinates: Argument list of two (xy) or three (xyz) coordinates. 
        Coordinates should be of type int, float or similar numeric. These values
        are converted to floats.
    
    :raises ValueError: If less then 2 or more than 3 arguments are supplied.
    
    .. rubric:: Code Example
    
    .. code-block:: python
       
       >>> v = Vector(1,2)
       >>> print(v)
       Vector(1.0,2.0)
    
    .. seealso:: `<https://geomalgorithms.com/points_and_vectors.html#Basic-Definitions>`_
    
    """

    def __add__(self,vector):
        """Addition of this vector and a supplied vector.
        
        :param vector: A vector.
        :type vector: Vector
        
        :rtype: Vector
        
        .. rubric:: Code Example
    
        .. code-block:: python
           
           >>> v = Vector(1,2)
           >>> result = v + Vector(1,1)
           >>> print(result)
           Vector(2.0,3.0)
            
        .. seealso:: `<https://geomalgorithms.com/points_and_vectors.html#Vector-Addition>`_
            
        """
        zipped=itertools.zip_longest(self,vector) # missing values filled with None
        try:
            coordinates=[a+b for a,b in zipped]
        except TypeError: # occurs if, say, a or b is None
            raise ValueError('Vectors to add must be of the same length.')
        return Vector(*coordinates)
    


    def __eq__(self,vector):
        """Tests if this vector and the supplied vector have the same coordinates.
        
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
        zipped=itertools.zip_longest(self,vector) # missing values filled with None
        try:
            result=[math.isclose(a, b, abs_tol=ABS_TOL) for a,b in zipped]
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
            raise ValueError('Vector coordinates must have a length of 2 or 3')


    def __len__(self):
        ""
        return len(self._coordinates)
    
    
    def __mul__(self,scalar):
        """Multiplication of this vector and a supplied scalar value.
        
        :param scalar: A numerical scalar value.
        :type scalar: float
        
        :rtype: Vector
        
        .. rubric:: Code Example
        
        .. code-block:: python
           
           >>> v = Vector(1,2)
           >>> result = v1 * 2
           >>> print(result)
           Vector(2.0,4.0)
        
        .. seealso:: `<https://geomalgorithms.com/points_and_vectors.html#Scalar-Multiplication>`_
        
        """
        return Vector(*(c*scalar for c in self))            
    
    
    
    def __repr__(self):
        ""
        return 'Vector(%s)' % ','.join([str(c) for c in self.coordinates])


    def __sub__(self,vector):
        """Subtraction of this vector and a supplied vector.
        
        :param vector: A vector.
        :type vector: Vector
        
        :rtype: Vector
        
        .. rubric:: Code Example
    
        .. code-block:: python
           
           >>> v = Vector(1,2)
           >>> result = v - Vector(1,1)
           >>> print(result)
           Vector(0,1)
        
        """
        zipped=itertools.zip_longest(self,vector) # missing values filled with None
        try:
            coordinates=[a-b for a,b in zipped]
        except TypeError: # occurs if, say, a or b is None
            raise ValueError(r'Vectors to subtract must be of the same length.')
        return Vector(*coordinates)
        

    def cross_product(self,vector):
        """Returns the 3D cross product of this vector and the supplied vector.
        
        :param vector: A 3D vector.
        :type vector: Vector
        
        :return: The 3D cross product of the two vectors. 
            This returns a new vector which is perpendicular to 
            this vector (self) and the supplied vector. 
            The returned vector has direction according to the right hand rule. 
            If this vector (self) and the supplied vector are collinear,
            then the returned vector is (0,0,0)
        
        :rtype: Vector
        
        .. rubric:: Code Example
        
        .. code-block:: python
           
           >>> v1 = Vector3D(1,0,0)
           >>> v2 = Vector3D(0,1,0)
           >>> result = v1.cross_product(v2)
           >>> print(result)
           Vector3D(0,0,1)
        
        .. seealso:: `<https://geomalgorithms.com/vector_products.html#3D-Cross-Product>`_
        
        """
        (v1,v2,v3),(w1,w2,w3)=list(self),list(vector)
        return Vector(v2*w3-v3*w2,
                      v3*w1-v1*w3,
                      v1*w2-v2*w1)


    def dot(self,vector):
        """Return the dot product of this vector and the supplied vector.
        
        :param vector: A vector.
        :type vector: Vector
        
        :returns: The dot product of the two vectors: 
            returns 0 if self and vector are perpendicular; 
            returns >0 if the angle between self and vector is an acute angle (i.e. <90deg); 
            returns <0 if the angle between seld and vector is an obtuse angle (i.e. >90deg).
        :rtype: float
        
        .. rubric:: Code Example
        
        .. code-block:: python
           
           >>> v1 = Vector(1,0)
           >>> v2 = Vector(0,1)               
           >>> result = v1.dot(v2)
           >>> print(result)
           0
           
           >>> v1 = Vector(1,0,0)
           >>> v2 = Vector(0,1,0)
           >>> result = v1.dot(v2)
           >>> print(result)
           0
        
        .. seealso:: `<https://geomalgorithms.com/vector_products.html#Dot-Product>`_
        
        """
        zipped=itertools.zip_longest(self,vector) # missing values filled with None
        try:
            return sum(a*b for a,b in zipped)
        except TypeError: # occurs if, say, a or b is None
            raise ValueError(r'Vectors to subtract must be of the same length.')
        

    @property
    def index_largest_absolute_coordinate(self):
        """Returns the index of the largest absolute coordinate of the vector.
        
        :return: 1 if the x-coordinate has the largest absolute value, 
            2 if the y-coordinate has the largest absolute value, or
            (for 3D vectors) 3 if the z-coordinate has the largest
            absolute value.
        :rtype: int
        
        .. rubric:: Code Example
    
        .. code-block:: python
           
           # 2D example
           >>> v = Vector(1,2)
           >>> result = v.index_largest_absolute_coordinate
           >>> print(result)
           1
           
           # 3D example
           >>> v = Vector(1,2,3)
           >>> result = v.index_largest_absolute_coordinate
           >>> print(result)
           2
            
        """
        absolute_coords=[abs(c) for c in self]
        return absolute_coords.index(max(absolute_coords)) 
    
    
    def is_codirectional(self,vector):
        """Tests if this vector and the supplied vector are codirectional.
        
        :param vector: A vector.
        :type vector: Vector
        
        :return: True if the vectors point in the exact same direction; 
            otherwise False.
        :rtype: bool
        
        .. rubric:: Code Example
            
        .. code-block:: python
           
           # 2D example
           >>> v1 = Vector(1,2)
           >>> v2 = Vector(2,4)
           >>> result = v1.is_codirectional(v2)
           >>> print(result)
           True
           
           # 3D example
           >>> v1 = Vector(1,1,1)
           >>> v2 = Vector(1,0,0)
           >>> result = v1.is_codirectional(v2)
           >>> print(result)
           False
            
        """
        return self.is_collinear(vector) and self.dot(vector)>0
        

    def is_collinear(self,vector):
        """Tests if this vector and the supplied vector are collinear.
        
        :param vector: A vector.
        :type vector: Vector
        
        :raise ValueError: If the vector is not 2D or 3D.
        
        :return: True if the vectors lie on the same line; 
            otherwise False.
        :rtype: bool
        
        .. rubric:: Code Example
        
        .. code-block:: python
           
           >>> v1 = Vector(1,0)
           >>> v2 = Vector(2,0)               
           >>> result = v1.is_collinear(v2)
           >>> print(result)
           True     
           
           >>> v1 = Vector3D(1,0,0)
           >>> v2 = Vector3D(2,0,0)               
           >>> result = v1.is_collinear(v2)
           >>> print(result)
           True        
        
        
        """
        if len(self)==2:
            return math.isclose(self.perp_product(vector), 0, abs_tol=ABS_TOL)
            #return abs(self.perp_product(vector)) < SMALL_NUM 
        if len(self)==3:
            return math.isclose(self.cross_product(vector).length, 0, abs_tol=ABS_TOL)
            #return self.cross_product(vector).length < SMALL_NUM 
        else:
            raise ValueError('"is_collinear" method requires a 2D or 3D vector.')
              
            
    def is_opposite(self,vector):
        """Test if this vector and the supplied vector are opposites.
        
        :param vector: A vector.
        :type vector: Vector
        
        :return: True if the vectors point in exact opposite directions; 
            otherwise False.
        :rtype: bool
        
        .. rubric:: Code Example
            
        .. code-block:: python
           
           # 2D example
           >>> v1 = Vector(1,2)
           >>> v2 = Vector(-2,-4)
           >>> result = v1.is_opposite(v2)
           >>> print(result)
           True
           
           # 3D example
           >>> v1 = Vector(1,2,3)
           >>> v2 = Vector(-1,-2,-3)
           >>> result = v1.is_opposite(v2)
           >>> print(result)
           True
        
        """
        return self.is_collinear(vector) and self.dot(vector)<0
            
    
    def is_perpendicular(self,vector):
        """Test if this vector and the supplied vector are perpendicular.
        
        :param vector: A vector.
        :type vector: Vector
        
        :return: True if the vectors are perpendicular; 
            otherwise False.
        :rtype: bool
        
        .. rubric:: Code Example
                
        .. code-block:: python
           
           # 2D example
           >>> v1 = Vector(1,0)
           >>> v2 = Vector(0,1)
           >>> result = v1.is_perpendicular(v2)
           >>> print(result)
           True
           
           # 3D example
           >>> v1 = Vector(1,0,0)
           >>> v2 = Vector(0,1,0)
           >>> result = v1.is_perpendicular(v2)
           >>> print(result)
           True
        
        """
        return math.isclose(self.dot(vector), 0, abs_tol=ABS_TOL)
        #return abs(self.dot(vector))<SMALL_NUM
        
    
    @property
    def length(self):
        """Returns the length of the vector.
        
        :rtype: float
        
        .. rubric:: Code Example
    
        .. code-block:: python
           
           >>> v = Vector(1,0)
           >>> result = v.length
           >>> print(result)
           1
        
        .. seealso:: `<https://geomalgorithms.com/points_and_vectors.html#Vector-Length>`_
        
        """
        return sum(c**2 for c in self)**0.5
        #(self.x**2+self.y**2)**0.5
    
    
    @property
    def normalise(self):
        """Returns the normalised vector of this vector.
        
        :returns: A codirectional vector of length 1.
        :rtype: Vector
        
        :Example:
    
        .. code-block:: python
           
           >>> v = Vector(3,0)
           >>> result = v.normalise
           >>> print(result)
           Vector(1,0)
        
        .. seealso:: `<https://geomalgorithms.com/points_and_vectors.html#Vector-Length>`_
        
        """
        l=self.length
        return Vector(*(c/l for c in self))
    
    
    @property
    def opposite(self):
        """Returns the opposite vector of this vector
        
        :return: A collinear vector which points in the opposite direction.
        :rtype: Vector
        
        .. rubric:: Code Example
            
        .. code-block:: python
           
           # 2D example
           >>> v = Vector(1,2)
           >>> result = v.opposite
           >>> print(result)
           Vector(-1,-2)
           
           # 3D example
           >>> v = Vector(1,2,3)
           >>> result = v.opposite
           >>> print(result)
           Vector(-1,-2,-3)
        
        """
        return self*-1

    
    def perp_product(self,vector):
        """Returns the perp product of this vector and the supplied vector.
        
        :param vector: A 2D vector.
        :type vector: Vector

        :raises ValueError: If this vector is not a 2D vector.
       
        :return: The perp product of the two vectors. 
            The perp product is the dot product of 
            the perp_vector of this vector and the supplied vector. 
            If supplied vector is collinear with self, returns 0. 
            If supplied vector is on the left of self, returns >0 (i.e. counterclockwise). 
            If supplied vector is on the right of self, returns <0 (i.e. clockwise).
        :rtype: float
            
        .. code-block:: python
    
        .. code-block:: python
           
           >>> v1 = Vector(1,0)
           >>> v2 = Vector(1,0)               
           >>> result = v1.perp_product(v2)
           >>> print(result)
           0
        
        .. seealso:: `<https://geomalgorithms.com/vector_products.html#2D-Perp-Product>`_
        
        """
        if len(self)==2:
            return self.perp_vector.dot(vector)
        else:
            raise ValueError('"perp_product" method only applicable for a 2D vector.')


    @property
    def perp_vector(self):
        """Returns the perp vector of this 2D vector.
        
        :raises ValueError: If this vector is not a 2D vector.
        
        :return: The perp vector, i.e. the normal vector on the left 
            (counterclockwise) side of self.
        :rtype: Vector
        
        .. rubric:: Code Example
    
        .. code-block:: python
           
           >>> v = Vector(1,0)
           >>> result = v.perp_vector
           >>> print(result)
           Vector(0,1)
        
        .. seealso:: `<https://geomalgorithms.com/vector_products.html#2D-Perp-Operator>`_
        
        """
        if len(self)==2:
            return Vector(-self.y,self.x)
        else:
            raise ValueError('"perp_vector" method only applicable for a 2D vector.')


    def triple_product(self,vector1,vector2):
        """Returns the triple product of this vector and 2 supplied vectors.
        
        :param vector1: A 3D vector.
        :type vector1: Vector
        :param vector2: A 3D vector.
        :type vector2: Vector
        
        :return: The triple product of the three vectors. 
            The result is equal to the volume of the parallelepiped (3D equivalent of a parallelogram). 
            The result is equal to six times the volume of the tetrahedron (3D shape with 4 vertices). 
            
        :rtype: float
        
        .. rubric:: Code Example
    
        .. code-block:: python
           
           >>> v1 = Vector(1,0,0)
           >>> v2 = Vector(0,1,0)
           >>> v3 = Vector(0,0,1)
           >>> result = v1.triple_product(v2,v3)
           >>> print(result)
           1
        
        .. seealso:: `<https://geomalgorithms.com/vector_products.html#3D-Triple-Product>`_        
        
        """
        return self.dot(vector1.cross_product(vector2))


    @property
    def x(self):
        """The x coordinate of the vector.
        
        :rtype: int, float
        
        """
        return self[0]
    
    
    @property
    def y(self):
        """The y coordinate of the vector.
        
        :rtype: int, float
        
        """
        return self[1]
    
    
    @property
    def z(self):
        """The z coordinate of the vector.
        
        :raises IndexError: If vector is a 2D vector.
        
        :rtype: int, float
        
        """
        return self[2]
    
    
    
class Line():
    """A line, as described by a Point and a Vector
    
    Equation of the line is P(t) = P0 + vL*t where:
    
        - P(t) is a point on the line; 
        - P0 is the start point of the line; 
        - vL is the line vector; 
        - t is any real number.
    
    :param P0: The start point of the line.
    :type P0: Point
    :param vL: The line vector.
    :type vL: Vector
    
    :raises ValueError: If the length of vL is zero.
    
    .. rubric:: Code Example
    
    .. code-block:: python
       
       >>> l = Line(Point(0,0), Vector(1,0))
       >>> print(l)
       Line(Point(0,0), Vector(1,0))
       
       >>> l = Line(Point(0,0,0), Vector(1,0,0))
       >>> print(l)
       Line(Point(0,0,0), Vector(1,0,0))
    
    
    .. seealso:: `<https://geomalgorithms.com/a02-_lines.html>`_
    
    
    """
    
    def __eq__(self,line):
        """Tests if this line and the supplied line are equal.
        
        :param line: A line.
        :type line: Line
        
        :return: True if the start point of supplied line lies on line (self),
            and the vL of supplied line is collinear to the vL of line (self); 
            otherwise False.
            Also returns False if supplied line is not a Line object.
        :rtype: bool
            
        .. rubric:: Code Example
    
        .. code-block:: python
           
           # 2D example
           >>> l = Line(Point(0,0), Vector(1,0))
           >>> result = l == l
           >>> print(result)
           True
           
           # 3D example
           >>> l1 = Line(Point(0,0,0), Vector(1,0,0))
           >>> l2 = Line(Point(0,0,0), Vector(-1,0,0))
           >>> result = l1 == l2
           >>> print(result)
           True
           
        """
        if isinstance(line,Line):
            return self.contains(line.P0) and self.vL.is_collinear(line.vL)
        else:
            return False


    def __repr__(self):
        ""
        return 'Line(%s, %s)' % (self.P0,self.vL)

    
    def __init__(self,P0,vL):
        ""
        if math.isclose(vL.length, 0, abs_tol=ABS_TOL):
            raise ValueError('length of vL must be greater than zero')
                
        self._P0=P0
        self._vL=vL
    
    
    def _intersect_line_skew(self,skew_line):
        """Returns the point of intersection of this line and the supplied skew line
        """
        #2D
        if len(self.P0)==2:
            return self._intersect_line_skew_2D(skew_line)
        #3D
        elif len(self.P0)==3:
            return self._intersect_line_skew_3D(skew_line)
        else:
            raise Exception # must be either 2D or 3D

    
    def _intersect_line_skew_2D(self,skew_line):
        """Returns the point of intersection of this line and the supplied skew line
        """
        u=self.vL
        v=skew_line.vL
        w=self.P0-skew_line.P0 
        t=-v.perp_product(w) / v.perp_product(u)
        return self.calculate_point(t)
        

    def _intersect_line_skew_3D(self,skew_line):
        """Returns the point of intersection of this line and the supplied (skew) line
        
        - return value can be:
            - None -> no intersection (for skew lines which do not intersect in 3D space)
            - Point3D -> a point (for skew lines which intersect)
        
        """
        if not self.is_parallel(skew_line):
        
            # find the coordinate to ignore for the projection
            cp=self.vL.cross_product(skew_line.vL)
            absolute_coords=[abs(x) for x in cp] 
            i=absolute_coords.index(max(absolute_coords)) % 3 # the coordinate to ignore for projection
                    
            #print('i',i)
            
            # project 3D lines to 2D
            self2D=self.project_2D(i)
            skew_line2D=skew_line.project_2D(i)
            
            #print('self2D', self2D)
            #print('skew_line2D',skew_line2D)
            
            # find intersection point for 2D lines
            ipt=self2D._intersect_line_skew_2D(skew_line2D)
            
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
    
    
    def calculate_point(self,t):
        """Returns a point on the line for a given t value. 
        
        :param t: The t value of the equation of the line.
        :type t: float
        
        :return: A point on the line calcualted using the t value. 
        :rtype: Point
        
        .. rubric:: Code Example
        
        .. code-block:: python    
        
           # 2D example
           >>> l = Line(Point(0,0), Vector(1,0))
           >>> result = l.calcuate_point(3)
           >>> print(result)
           Point(3,0)
           
           # 3D example
           >>> l = Line(Point(0,0,0), Vector(1,0,0))
           >>> result = l.calcuate_point(-3)
           >>> print(result)
           Point(-3,0,0)
        
        """
        return self.P0 + (self.vL * t)


    def calculate_t_from_point(self,point):
        """Returns t for a given point.
        
        :param point: A point on the line.
        :type point: Point
        
        :return: The calculated t value.
        :rtype: float
        
        :Example:
        
        .. code-block:: python
           
           >>> l = Line(Point(0,0), Vector(1,0))
           >>> result = l.calculate_t_from_point(Point(3,0))
           >>> print(result)
           3
        
           >>> l = Line(Point(0,0,0), Vector(1,0,0))
           >>> result = l.calculate_t_from_point(Point(3,0,0))
           >>> print(result)
           3
            
        """
        for P0,vL,point in zip(self.P0,self.vL,point): # loop through x, y, z components
            if not math.isclose(vL, 0, abs_tol=ABS_TOL):
                return (point-P0) / vL
        raise Exception()
                
    
    def contains(self,obj):
        """Tests if the line contains the object.
        
        :param obj: A point, halfline or segment.
        :type obj: Point, Halfline, Segment
            
        :return:  For point, True if the point lies on the line; otherwise False. 
            For halfline, True if the halfline startpoint is on the line and 
            the halfline vector is collinear to the line vector; otherwise False. 
            For segment, True if the segment start and endpoints are on the line; otherwise False. 
        :rtype: bool
        
        .. rubric:: Code Example
    
        .. code-block:: python
           
           # 2D example
           >>> l = Line(Point(0,0), Vector(1,0))
           >>> result = Point(2,0) in l
           >>> print(result)
           True
           
           # 3D example
           >>> l = Line(Point(0,0,0), Vector(1,0,0))
           >>> hl = Halfline(Point(0,0,0), Vector(-1,0,0))
           >>> result = hl in l
           >>> print(result)
           True
            
        """
        if isinstance(obj,Point):
            t=self.calculate_t_from_point(obj)
            pt=self.calculate_point(t)           
            return obj==pt 
                    
        elif isinstance(obj,Halfline):
            return self.contains(obj.P0) and obj.vL.is_collinear(self.vL)
        
        elif isinstance(obj,Segment):
            return self.contains(obj.P0) and self.contains(obj.P1)
        
        else:
            raise TypeError
        
        
    def distance_to_line(self,line):
        """Returns the distance from this line to the supplied line.
        
        :param line: A line.
        :type line: Line
        
        :return: The distance between the two lines.
        :rtype: float
        
        .. rubric:: Code Example
    
        .. code-block:: python
           
           >>> l1 = Line(Point(0,0), Vector(1,0))
           >>> l2 = Line(Point(0,1), Vector(1,0))
           >>> result = l1.distance_to_line(l2)
           >>> print(result)
           1
        
        .. seealso:: `<https://geomalgorithms.com/a07-_distance.html>`_
        
        """
        #2D
        if len(self.P0)==2:
        
            if self.is_parallel(line):
                return self.distance_to_point(line.P0)
            else:
                return 0 # as these are skew infinite 2D lines

        #3D
        elif len(self.P0)==3: 

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
    
        else:
            raise Exception # must be 2D or 3D


    
    def distance_to_point(self,point):
        """Returns the distance from this line to the supplied point.
        
        :param point: A point.
        :type point: Point2D or Point3D
                    
        :return: The distance from the line to the point. 
        :rtype: float
        
        .. rubric:: Code Example
        
        .. code-block:: python
           
           # 2D example
           >>> l = Line(Point(0,0), Vector(1,0))
           >>> result = l.distance_to_point(Point(0,10))
           >>> print(result)
           10
           
           # 3D example
           >>> l = Line(Point(0,0,0), Vector(1,0,0))
           >>> result = l.distance_to_point(Point(10,0,0))
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
        :type line: Line
        
        :return: Returns a line (this line) if lines are collinear. 
            Returns None (i.e. no intersection) if lines are parallel. 
            For 2D, returns a point if lines are skew.  
            For 3D, returns either None or a point if lines are skew. 
        :rtype: None, Point, Line 
        
        .. rubric:: Code Example
        
        .. code-block:: python
           
           # 2D example
           >>> l1 = Line(Point(0,0), Vector(1,0))
           >>> l2 = Line(Point(0,0), Vector(0,1))
           >>> result = l.intersect_line(l2)
           >>> print(result)
           Point(0,0)
           
           # 3D example
           >>> l1 = Line(Point(0,0,0), Vector(1,0,0))
           >>> l2 = Line(Point(0,0,1), Vector(1,0,0))
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
        :type obj: Line
        
        :return: Returns True if the lines are parallel (this includes the
            case of collinear lines); 
            otherwise False. 
        :rtype: bool
            
        .. rubric:: Code Example
    
        .. code-block:: python
           
           # 2D example
           >>> l1 = Line(Point(0,0), Vector(1,0))
           >>> l2 = Line(Point(0,0), Vector(0,1))
           >>> result = l.is_parallel(l2)
           >>> print(result)
           False
           
           # 3D example
           >>> l1 = Line(Point3D(0,0,0), Vector(1,0,0))
           >>> l2 = Line(Point3D(0,0,1), Vector(2,0,0))
           >>> result = l1.is_parallel(l2)
           >>> print(result)
           True
            
        """
        return self.vL.is_collinear(line.vL)

    
    @property
    def P0(self):
        """The starting point of the line.
        
        :rtype: Point
        
        """
        return self._P0
    
    
    def project_2D(self,coordinate_index):
        """Projection of the 3D line as a 2D line.
        
        :param coordinate_index: The index of the coordinate to ignore.
            Use coordinate_index=0 to ignore the x-coordinate, coordinate_index=1 
            for the y-coordinate and coordinate_index=2 for the z-coordinate.
        :type coordinate_index: int
        
        :return: A 2D line based on the projection of the 3D line.
        :rtype: Line
               
        .. rubric:: Code Example
    
        .. code-block:: python
        
            >>> l = Line(Point(0,0,0), Vector(1,2,3))
            >>> result = l.project_2D(0)
            >>> print(result)
            Line(Point(0,0), Vector(2,3))   
        
        """
        
        if coordinate_index==0:
            return Line(Point(self.P0.y,self.P0.z),
                        Vector(self.vL.y,self.vL.z))
        elif coordinate_index==1:
            return Line(Point(self.P0.z,self.P0.x),
                        Vector(self.vL.z,self.vL.x))
        elif coordinate_index==2:
            return Line(Point(self.P0.x,self.P0.y),
                        Vector(self.vL.x,self.vL.y))
        else:
            raise ValueError
                    
            
    @property
    def vL(self):
        """The vector of the line.
        
        :rtype: Vector
        
        """
        return self._vL



class Halfline():
    """A halfline, as described by a Point and a Vector
    
    Equation of the halfline is P(t) = P0 + vL*t where:
        
        - P(t) is a point on the halfline
        - P0 is the start point of the halfline
        - vL is the halfline vector
        - t is any real, positive number
    
    :param P0: The start point of the halfline.
    :type P0: Point
    :param vL: The halfline vector.
    :type vL: Vector
    
    :raises ValueError: If the length of vL is zero.
    
    .. rubric:: Code Example
    
    .. code-block:: python
       
       >>> hl = Halfline(Point(0,0), Vector(1,0))
       >>> print(hl)
       Halfline(Point(0,0), Vector(1,0))
       
       >>> hl = Halfline(Point(0,0,0), Vector(1,0,0))
       >>> print(hl)
       Halfline(Point(0,0,0), Vector(1,0,0))
    
    .. seealso:: `<https://geomalgorithms.com/a02-_lines.html>`_
    
    """
    
    def __eq__(self,halfline):
        """Tests if this halfline and the supplied halfline are equal.
        
        :param halfline: A halfline.
        :type halfline: Halfline
        
        :return: True if the start points are the same and the vectors are codirectional;
            otherwise False.
            Also returns False is supplied halfline is not a Halfline object.
        :rtype: bool
        
        .. rubric:: Code Example
    
        .. code-block:: python
           
           # 2D example
           >>> hl = Halfline(Point(0,0), Vector(1,0))
           >>> result = hl == hl
           >>> print(result)
           True
           
           # 3D example
           >>> hl1 = Halfline(Point(0,0,0), Vector(1,0,0))
           >>> hl2 = Halfline(Point(0,0,0), Vector(-1,0,0))
           >>> result = hl1 == hl2
           >>> print(result)
           False
            
        """
        if isinstance(halfline,Halfline):
            return self.P0==halfline.P0 and self.vL.is_codirectional(halfline.vL)
        else:
            return False
        
    
    def __init__(self,P0,vL):
        ""
        if math.isclose(vL.length, 0, abs_tol=ABS_TOL):
            raise ValueError('length of vL must be greater than zero')
                
        self._P0=P0
        self._vL=vL


    def __repr__(self):
        ""
        return 'Halfine(%s, %s)' % (self.P0,self.vL)


    def calculate_point(self,t):
        """Returns a point on the halfline for a given t value.
        
        :param t: The t value.
        :type t: float
        
        :raises ValueError: If t is less than zero.
        
        :return: The point based on the t value.
        :rtype: Point
        
        .. rubric:: Code Example
        
        .. code-block:: python    
        
           # 2D example
           >>> hl = Halfline(Point(0,0), Vector(1,0))
           >>> result = hl.calcuate_point(3)
           >>> print(result)
           Point(3,0)
           
           # 3D example
           >>> hl = Halfline(Point(0,0,0), Vector(1,0,0))
           >>> result = hl.calcuate_point(3)
           >>> print(result)
           Point(3,0,0)
        
        """
        if math.isclose(t, 0, abs_tol=ABS_TOL) or t>0:
            return self.P0 + (self.vL * t)
        else:
            raise ValueError('For a halfline, t must be greater than or equal to zero')
        

    def contains(self,obj):
        """Tests if the halfline contains the object.
        
        :param obj: A point or segment.
        :type obj: Point, Segment
            
        :return: For point, True if the point lies on the halfline; otherwise False. 
            For segment, True if the segment start point and end point are on the halfline; otherwise False
        :rtype: bool
        
        .. rubric:: Code Example
        
        .. code-block:: python
           
           # 2D example
           >>> hl = Halfline(Point(0,0), Vector(1,0))
           >>> result = Point(2,0) in l
           >>> print(result)
           True
           
           # 3D example
           >>> hl = Halfline(Point(0,0,0), Vector(1,0,0))
           >>> hl = Halfline(Point(0,0,0), Vector(-1,0,0))
           >>> result = hl in l
           >>> print(result)
           False            
        
        """
        if isinstance(obj,Point):
            
            t=self.line.calculate_t_from_point(obj)
            try:
                pt=self.calculate_point(t)  
            except ValueError: # t<0
                return False
            return obj==pt 
        
        elif isinstance(obj,Segment):
            return self.contains(obj.P0) and self.contains(obj.P1)
            
        else:
            return TypeError()


    def distance_to_point(self,point):
        """Returns the distance from this halfline to the supplied point.
        
        :param point: A point.
        :type point: Point
        
        :return: The distance from the halfline to the point.
        :rtype: float
            
        .. rubric:: Code Example
        
        .. code-block:: python
           
           # 2D example
           >>> hl = Halfline(Point(0,0), Vector(1,0))
           >>> result = hl.distance_to_point(Point(0,10))
           >>> print(result)
           10
           
           # 3D example
           >>> hl = Halfline(Point(0,0,0), Vector(1,0,0))
           >>> result = hl.distance_to_point(Point(10,0,0))
           >>> print(result)
           0
        
        .. seealso:: `<https://geomalgorithms.com/a02-_lines.html>`_
        
        """
        v=self.vL
        w=point-self.P0 
        c1=v.dot(w)
        if c1<=0: # i.e. t<0
            return w.length
        else:
            return self.line.distance_to_point(point)


    def intersect_halfline(self,halfline):
        """Returns the intersection of this halfline with the supplied halfline.
        
        :param halfline: A halfline.
        :type halfline:  Halfline
        
        :return: Returns None for halflines that are parallel. 
            Returns None for skew halflines that don't intersect.
            Returns None for collinear but non-codirectional halflines that don't overlap.
            Returns a point for skew halflines that intersect. 
            Returns a point for collinear but non-codirectional halflines that have the same start point. 
            Returns a segment for collinear but non-codirectional halflines that overlap.
            Returns a halfline for halflines that are equal.
        :rtype: None, Point, Halfline, Segment
            
        .. rubric:: Code Example
        
        .. code-block:: python
           
           >>> hl1 = Halfline(Point(0,0), Vector(1,0))
           >>> hl2 = Halfline(Point(0,0), Vector(0,1))
           >>> result = hl1.intersect_line(hl2)
           >>> print(result)
           Point(0,0)
        
           >>> hl1 = Halfline(Point(0,0,0), Vector(1,0,0))
           >>> hl2 = Halfline(Point(0,0,0), Vector(0,1,0))
           >>> result = hl1.intersect_line(hl2)
           >>> print(result)
           Point(0,0,0)
        
        """
        if self.line.contains(halfline): # codirectional or non-codirectional
            if self.vL.is_codirectional(halfline.vL): # codirectional
                if halfline.contains(self.P0): # returns the halfline which is 'inside' the other
                    return self
                else:
                    return halfline
            else: # non-codirectional
                if halfline.contains(self.P0): #  the halflines intersect
                    if self.P0==halfline.P0:
                        return self.P0
                    else:
                        return Segment(self.P0,halfline.P0)
                else: # the halflines don't intersect
                    return None
        elif self.line.is_parallel(halfline.line): # parallel but not collinear
            return None # should this be a 'no intersection' class??
        else:
            p=self.line._intersect_line_skew(halfline.line)
            if self.contains(p) and halfline.contains(p):
                return p
            else:
                return None
        

    def intersect_line(self,line):
        """Returns the intersection of this halfline with the supplied line.
        
        :param line: A line.
        :type line: Line2D, Line3D
        
        :return: Returns a halfline (this halfline) if the halfline and line are collinear. 
            Returns a point if the halfline and line are skew and they intersect. 
            Returns None if the halfline and line are parallel. 
            Returns None if the halfline and line are skew but do not intersect. 
        :rtype: None, Point2D, Point3D, Halfline2D, Halfline3D        
            
        .. rubric:: Code Example
        
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
        
        .. seealso:: `<https://geomalgorithms.com/a05-_intersect-1.html>`_
        
        """
        if self.line==line:
            return self
        elif self.line.is_parallel(line):
            return None # should this be a 'no intersection' class??
        else:
            p=self.line._intersect_line_skew(line)
            #print(p)
            if self.contains(p):
                return p
            else:
                return None


    @property
    def line(self):
        """Returns the line which the halfline lies on.
        
        :return: A line with the same start point (P0) and vector (vL) as the halfline.
        :rtype: Line
        
        .. rubric:: Code Example
        
        .. code-block:: python
           
           >>> hl= Halfline(Point(0,0), Vector(1,0))
           >>> result = hl.line
           >>> print(result)
           Line(Point(0,0), Vector(1,0))
           
           >>> hl= Halfline(Point(0,0,0), Vector(1,0,0))
           >>> result = hl.line
           >>> print(result)
           Line(Point(0,0,0), Vector(1,0,0))
        
        
        """
        return Line(self.P0,self.vL)
    

    @property
    def P0(self):
        """The starting point of the halfline.
        
        :rtype: Point
        
        """
        return self._P0
    
    
    def project_2D(self,coordinate_index):
        """Projection of the 3D halfline as a 2D halfline.
        
        :param coordinate_index: The index of the coordinate to ignore.
            Use coordinate_index=0 to ignore the x-coordinate, coordinate_index=1 
            for the y-coordinate and coordinate_index=2 for the z-coordinate.
        :type coordinate_index: int
        
        :return: A 2D halfline based on the projection of the 3D halfline.
        :rtype: Halfine
               
        .. rubric:: Code Example
        
        .. code-block:: python
        
            >>> hl = Halfline(Point(0,0,0), Vector(1,2,3))
            >>> result = hl.project_2D(0)
            >>> print(result)
            Line(Point(0,0), Vector(2,3))   
        
        """
        
        if coordinate_index==0:
            return Halfline(Point(self.P0.y,self.P0.z),
                            Vector(self.vL.y,self.vL.z))
        elif coordinate_index==1:
            return Halfline(Point(self.P0.z,self.P0.x),
                            Vector(self.vL.z,self.vL.x))
        elif coordinate_index==2:
            return Halfline(Point(self.P0.x,self.P0.y),
                            Vector(self.vL.x,self.vL.y))
        else:
            raise Exception
                    
    
    @property
    def vL(self):
        """The vector of the halfline.
        
        :rtype: Vector
        
        """
        return self._vL
    


class Segment():
    """A 2D or 3D segment.
    
    Equation of the segment is P(t) = P0 + vL*t where:
        
        - P(t) is a point on the segment
        - P0 is the start point of the segment
        - vL is the segment vector
        - t is any real, positive number between 0 and 1
    
    :param P0: The start point of the segment.
    :type P0: Point
    :param P1: The end point of the segment.
    :type P1: Point
    
    :raises ValueError: If P0 and P1 are the same point.
    
    .. rubric:: Code Example
    
    .. code-block:: python
       
       >>> s = Segment(Point(0,0), Point(1,0))
       >>> print(s)
       Segment(Point(0,0), Point(1,0))
       
       >>> s = Segment(Point(0,0,0), Point(1,0,0))
       >>> print(s)
       Segment(Point(0,0,0), Point(1,0,0))
    
    """
    
    def __add__(self,segment):
        """Adds this segment to the supplied segment.
        
        :param segment: A segment.
        :type segment: Segment
        
        :raises ValueError: If the segments are not collinear,
            do not share a start or end point,
            or if they overlap.            
        
        :return: A new segment which is the sum of the two segments.
        :rtype: Segment
        
        .. rubric:: Code Example
    
        .. code-block:: python
           
           # 2D example
           >>> s1 = Segment(Point(0,0), Point(1,0))
           >>> s2 = Segment(Point(1,0), Point(2,0))
           >>> result = s1 + s2
           >>> print(result)
           Segment(Point(0,0), Point(2,0))
           
           # 3D example
           >>> s1 = Segment(Point(1,0,0), Point(0,0,0))
           >>> s2 = Segment(Point(0,0,0), Point(-1,0,0))
           >>> result = s1 + s2
           >>> print(result)
           Segment(Point(-1,0,0), Point(1,0,0))       
        
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
    
    
    def __eq__(self,segment):
        """Tests if this segment and the supplied segment are equal.
        
        :param segment: A segment.
        :type segment: Segment
        
        :return: True if the segments have the same start point and the same end point; 
            else True if the start point of one is the end point of the other, and vice versa;
            otherwise False.
        :rtype: bool
        
        .. rubric:: Code Example
    
        .. code-block:: python
           
           # 2D example
           >>> s = Segment(Point(0,0), Point(1,0))
           >>> result = s == s
           >>> print(result)
           True
           
           # 3D example
           >>> s1 = Segment(Point(0,0,0), Point(1,0,0))
           >>> s2 = Segment(Point(0,0,0), Point(-1,0,0))
           >>> result = s1 == s2
           >>> print(result)
           False
            
        """
        if isinstance(segment,Segment):
            return ((self.P0==segment.P0 and self.P1==segment.P1) or
                    (self.P0==segment.P1 and self.P1==segment.P0))
        else:
            return False


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


    def __repr__(self):
        ""
        return 'Segment(%s, %s)' % (self.P0,self.P1)


    def calculate_point(self,t):
        """Returns a point on the segment for a given t value.
        
        :param t: The t value.
        :type t: float
        
        :return: A point on the segment based on the t value.
        :rtype: Point
        
        .. rubric:: Code Example
        
        .. code-block:: python    
        
           # 2D example
           >>> s = Segment(Point(0,0), Point(1,0))
           >>> result = s.calcuate_point(0.5)
           >>> print(result)
           Point(0.5,0)
           
           # 3D example
           >>> s = Segment(Point(0,0,0), Point(1,0,0))
           >>> result = s.calcuate_point(0)
           >>> print(result)
           Point(0,0,0)
                
        """
        if t>=0-SMALL_NUM and t<=1+SMALL_NUM: ## MADE A CHANGE HERE
            return self.line.calculate_point(t)
        else:
            raise ValueError('For a segment, t must be equal to or between 0 and 1')


    def contains(self,obj):
        """Tests if the segment contains the object.
        
        :param obj: A point or segment. 
        :type obj: Point, Segment
            
        :return: For point, True if the point lies on the segment; otherwise False. 
            For segment, True if the segment start and endpoints are on the segment; otherwise False. 
        :rtype: bool
        
        .. rubric:: Code Example
    
        .. code-block:: python
           
           # 2D example
           >>> s = Segment(Point(0,0), Point(1,0))
           >>> result = Point(2,0) in l
           >>> print(result)
           False
           
           # 3D example
           >>> s1 = Segment(Point(0,0,0), Point(1,0,0))
           >>> s2 = Segment(Point(0,0,0), Point(0.5,0,0))
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


    def difference_segment(self,segment):
        """Returns the difference of two segments.
        
        :param segment: A segment.
        :type segment: Segment
            
        :return: A segments sequence of 0, 1 or 2 segments.
            Returns an empty segments sequence if the supplied segment is equal to or contains this segment.
            Returns a segments sequence with this segment if the supplied segment does not intersect this segment.
            Returns a segments sequence with a new segment if the supplied segment intersects this segment 
            including either one of the start point or end point.
            Returns a segment sequence with two new segments if the supplied segment intersects this segment
            and is contained within it.
        :rtype: Segments
        
        .. rubric:: Code Example
        
        .. code-block:: python    
        
           # 2D example
           >>> s1 = Segment(Point(0,0), Point(1,0))
           >>> s2 = Segment(Point(0.5,0), Point(1,0))
           >>> result = s1.difference_segment(s2)
           >>> print(result)
           Segments(Segment(Point(0,0), Point(0.5,0)))
           
           # 3D example
           >>> s1 = Segment(Point(0,0,0), Point(1,0,0))
           >>> s2 = Segment(Point(-1,0,0), Point(2,0,0))
           >>> result = s1.difference_segment(s2)
           >>> print(result)
           Segments()               
        
        """
        if self in segment:
            return Segments()
        
        if self.line==segment.line:
            t0=self.line.calculate_t_from_point(segment.P0)
            t1=self.line.calculate_t_from_point(segment.P1)
            #print(self)
            #print(segment)
            #print(t0,t1)
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
        
        .. rubric:: Code Example
        
        .. code-block:: python    
        
           # 2D example
           >>> s = Segment(Point(0,0), Point(1,0))
           >>> sgmts = Segments(Segment(Point(0.2,0), Point(0.8,0))
           >>> result = s.difference_segments(sgmts)
           >>> print(result)
           Segments(Segment(Point(0,0), Point(0.2,0)),
                    Segment(Point(0.8,0),Point(1,0)))
           
           # 3D example
           >>> s = Segment(Point(0,0,0), Point(1,0,0))
           >>> sgmts = Segments(Segment(Point(-1,0,0), Point(2,0,0))
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
        :type point: Point
        
        :return: The distance between the segment and the point.
        :rtype: float
        
        .. rubric:: Code Example
    
        .. code-block:: python
           
           # 2D example
           >>> s = Segment(Point(0,0), Point(1,0))
           >>> result = s.distance_to_point(Point(0,10))
           >>> print(result)
           10
           
           # 3D example
           >>> s = Segment(Point(0,0,0), Point(1,0,0))
           >>> result = s.distance_to_point(Point(10,0,0))
           >>> print(result)
           9
            
        .. seealso:: `<https://geomalgorithms.com/a02-_lines.html>`_
            
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
    
    
    def intersect_halfline(self,halfline):
        """Returns the interesection of this segment and a halfline.
        
        :param halfline: A halfline.
        :type halfline: HalfLine
                
        :return: Returns None for parallel non-collinear segment and halfline.
            Returns None for skew segment and halfline that don't intersect. 
            Returns None for collinear segment and halfline that don't intersect.
            Returns point for skew segment and halfline that intersect.
            Returns point for collinear segment and halfline that intersect at the start or end point.
            Returns segment for collinear segment and halfline that intersect.
        :rtype: None, Point, Segment         
            
        .. rubric:: Code Example
    
        .. code-block:: python
           
           >>> s = Segment(Point(0,0), Point(1,0))
           >>> hl = Halfine(Point(0,0), Vector(0,1))
           >>> result = s.intersect_halfline(hl)
           >>> print(result)
           Point(0,0)
        
           >>> s = Segment(Point(0,0,0), Point(1,0,0))
           >>> hl = Halfline(Point(0,0,1), Vector(1,0,0))
           >>> result = s.intersect_halfline(hl)
           >>> print(result)
           None
        
        .. seealso:: `<https://geomalgorithms.com/a05-_intersect-1.html>`_
        
        """
        #2D
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
                
        #3D
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
        
    

    def intersect_line(self,line):
        """Returns the intersection of this segment with the supplied line.
        
        :param line: A line.
        :type line: Line
        
        :return: Returns None for parallel non-collinear segment and line.
            Returns None for skew segment and line that don't intersect. 
            Returns point for skew segment and line that intersect.
            Returns segment (this segment) for a segment that lies on the line.
        :rtype: None, Point, Segment            
            
        .. rubric:: Code Example
    
        .. code-block:: python
           
           # 2D example
           >>> s = Segment(Point(0,0), Point(1,0))
           >>> l = Line(Point(0,0), Vector(0,1))
           >>> result = s.intersect_line(l)
           >>> print(result)
           Point(0,0)
           
           # 3D example
           >>> s = Segment(Point(0,0,0), Point(1,0,0))
           >>> l = Line(Point(0,0,1), Vector(1,0,0))
           >>> result = s.intersect_line(l)
           >>> print(result)
           None
        
        .. seealso:: `<https://geomalgorithms.com/a05-_intersect-1.html>`_
        
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


    def intersect_segment(self,segment):
        """Returns the interesection of this segment and another segment.
        
        :param segment: A segment.
        :type segment: Segment
        
        :return: Returns None for parallel non-collinear segments.
            Returns None for skew segments that don't intersect. 
            Returns None for collinear segments that don't intersect.
            Returns point for skew segments that intersect.
            Returns point for collinear segments that intersect at a start or end point.
            Returns segment for collinear segments that intersect.
        :rtype: None, Point, Segment        
            
        .. rubric:: Code Example
    
        .. code-block:: python
           
           >>> s1 = Segment(Point(0,0), Point(1,0))
           >>> s2 = Segment(Point(0,0), Point(0,1))
           >>> result = s1.intersect_segment(s2)
           >>> print(result)
           Point(0,0)
           
           >>> s1 = Segment(Point(0,0,0), Point(1,0,0))
           >>> s2 = Segment(Point(0,0,0), Point(0,1,0))
           >>> result = s1.intersect_segment(s2)
           >>> print(result)
           Point(0,0,0)
        
        .. seealso:: `<https://geomalgorithms.com/a05-_intersect-1.html>`_
        
        """
        #2D
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
    
        #3D
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
        
        :return: A line with the same start point (P0) and vector (P1-P0) as the segment.
        :rtype: Line
        
        .. rubric:: Code Example
    
        .. code-block:: python
           
           >>> s = Segment(Point(0,0), Point(1,0))
           >>> result = s.line
           >>> print(result)
           Line(Point(0,0), Vector(1,0))
           
           >>> s = Segment(Point(0,0,0), Point(1,0,0))
           >>> result = s.line
           >>> print(result)
           Line(Point(0,0,0), Vector(1,0,0))
        
        
        """
        return Line2D(self.P0,self.P1-self.P0)
        return Line3D(self.P0,self.P1-self.P0)

    @property
    def order(self):
        """Returns the segment with ordered points such that P0 is less than P1.
        
        :return: If P0 < P1, returns the reverse of this segment;
            otherwise returns a copy of this segment.
        :rtype: Segment
            
        .. rubric:: Code Example
    
        .. code-block:: python
           
           # 2D example
           >>> s = Segment(Point(1,0), Point(0,0))
           >>> result = s.order
           >>> print(result)
           Segment(Point(0,0), Point(1,0))
           
           # 3D example
           >>> s = Segment(Point(0,0,0), Point(1,0,0))
           >>> result = s.order
           >>> print(result)
           Segment(Point(0,0,0), Point(1,0,0))
            
        """
        if self.P0 < self.P1 :
            return self.__class__(self.P0,self.P1)
        else:
            return self.reverse
        

    @property
    def P0(self):
        """The start point of the segment.
        
        :rtype: Point
        
        """
        return self._P0
    
    
    @property
    def P1(self):
        """The end point of the segment.
        
        :rtype: Point
        
        """
        return self._P1
        
    
    def plot2D(self,ax,**kwargs):
        """Plots the segment on the supplied axes.
        
        :param ax: An Axes instance.
        :type ax:  matplotlib.axes.Axes 
        :param kwargs: keyword arguments to be supplied to the Axes.plot call
                            
        """
        x=[p.x for p in self.points]
        y=[p.y for p in self.points]
        ax.plot(x,y,**kwargs)


    def plot3D(self,ax,**kwargs):
        """Plots the segment on the supplied axes
        
        :param ax: An Axes3D instance.
        :type ax: mpl_toolkits.mplot3d.axes3d.Axes3D
        :param kwargs: keyword arguments to be supplied to the Axes3D.plot call
                    
        """
        x=[p.x for p in self.points]
        y=[p.y for p in self.points]
        z=[p.z for p in self.points]
        ax.plot(x,y,z,**kwargs)


    def project_2D(self,coordinate_index):
        """Projection of the 3D segment as a 2D segment.
        
        :param coordinate_index: The index of the coordinate to ignore.
            Use coordinate_index=0 to ignore the x-coordinate, coordinate_index=1 
            for the y-coordinate and coordinate_index=2 for the z-coordinate.
        :type coordinate_index: int
        
        :return: A 2D segment based on the projection of the 3D segment.
        :rtype: Segment
               
        .. rubric:: Code Example
    
        .. code-block:: python
        
            >>> s = Segment(Point(0,0,0), Point(1,2,3))
            >>> result = s.project_2D(0)
            >>> print(result)
            Segment(Point(0,0), Point(2,3))   
        
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
                    
  
    def project_3D(self,plane,coordinate_index):
        """Projection of 2D segment on a 3D plane.
        
        :param plane: The plane for the projection
        :type plane: Plane
        :param coordinate_index: The index of the coordinate which was ignored 
            to create the 2D projection. For example, coordinate_index=0
            means that the x-coordinate was ignored and this point
            was originally projected onto the yz plane.
        :type coordinate_index: int
        
        :return: 3D segment which has been projected from the 2D segment.
        :rtype: Segment
               
        .. rubric:: Code Example
    
        .. code-block:: python
        
            >>> s = Segment(Point(0,0), Point(1,0))
            >>> pl = Plane(Point(0,0,1), Vector(0,0,1))
            >>> result = s.project_3D(pl, 2)
            Segment(Point(0,0,1),Point(1,0,1))
        
        """
        P0=self.P0.project_3D(plane,coordinate_index)
        P1=self.P1.project_3D(plane,coordinate_index)
        return Segment3D(P0,P1)
    

    # IS SEGMENTS AN ITERABLE SEQUENCE - IF SO THEN THIS IS 'list(self)'
    @property
    def points(self):
        """Return the points P0 and P1 of the segment.
        
        :return: The segment points as (P0,P1).
        :rtype: Points
            
        .. rubric:: Code Example
    
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
        :rtype: Segment
        
        .. rubric:: Code Example
    
        .. code-block:: python
           
           # 2D example
           >>> s = Segment(Point(1,0), Point(0,0))
           >>> result = s.reverse
           >>> print(result)
           Segment(Point(0,0), Point(1,0))
           
           # 3D example
           >>> s = Segment(Point(0,0,0), Point(1,0,0))
           >>> result = s.reverse
           >>> print(result)
           Segment(Point(1,0,0), Point(0,0,0))
            
        """
        return self.__class__(self.P1,self.P0)
    


class Plane():
    """A three dimensional plane, situated on an x, y, z plane.
    
    Equation of plane: N . (P - P0) = 0 where:
        
        - N is a normal 3D vector to the plane
        - P is any point on the plane
        - P0 is the start point of the plane
    
    :param P0: A 3D point on the plane.
    :type P0: Point3D
    :param N: A 3D vector which is normal to the plane.
    :type N: Vector3D 
    
    :Example:
    
    .. code-block:: python
       
       >>> pn = Plane3D(Point3D(0,0,0), Vector3D(0,0,1))
       >>> print(pn)
       Plane3D(Point3D(0,0,0), Vector3D(0,0,1))

    .. seealso: `<https://geomalgorithms.com/a04-_planes.html>`_

    """    
    
    
    def __init__(self,P0,N):
        ""
        self._P0=P0
        self._N=N


    @property
    def P0(self):
        """The start point of the plane.
        
        :rtype: Point2D
        
        """
        return self._P0


    def point_xy(self,x,y):
        """Returns a point on the plane given a x and y coordinates.
        
        :param x: An x-coordinate.
        :type x: float
        :param y: A y-coordinate.
        :type y: float
        
        :rtype: Point3D
        
        """
        z=self._P0.z-(self._N.x*(x-self._P0.x)+self._N.y*(y-self._P0.y))/self._N.z
        return Point(x,y,z)
    
    
    def point_zx(self,z,x):
        """Returns a point on the plane given a x and y coordinates.
        
        :param z: A z-coordinate.
        :type z: float
        :param x: An x-coordinate.
        :type x: float
        
        :rtype: Point3D
        
        """
        y=self._P0.y-(self._N.z*(z-self._P0.z)+self._N.x*(x-self._P0.x))/self._N.y
        return Point(x,y,z)
    
    
    def point_yz(self,y,z):
        """Returns a point on the plane given a x and y coordinates.
        
        :param y: A y-coordinate.
        :type y: float
        :param z: A z-coordinate.
        :type z: float
        
        :rtype: Point3D
        
        """
        x=self._P0.x-(self._N.y*(y-self._P0.y)+self._N.z*(z-self._P0.z))/self._N.x
        return Point(x,y,z)
    


    @property
    def N(self):
        """The vector normal to the plane.
        
        :rtype: Vector3D
        
        """
        return self._N
