# -*- coding: utf-8 -*-

import collections.abc
import itertools
import math


ABS_TOL = 1e-7 # default value for math.isclose


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
    
    

class Vector2D(Vector):
    """A two dimensional vector, situated on an x, y plane.
    
    :param x: The x coordinate of the vector.
    :type x: float
    :param y: The y coordinate of the vector.
    :type y: float
    
    :Example:
    
    .. code-block:: python
       
       >>> v = Vector2D(1,2)
       >>> print(v)
       Vector2D(1,2)
    
    .. seealso:: `<https://geomalgorithms.com/points_and_vectors.html#Basic-Definitions>`_
    
    """

    def __init__(self,x,y):
        ""
        self._x=x
        self._y=y        
    
    
    def __add__(self,vector):
        """Addition of this vector and a supplied vector.
        
        :param vector: A 2D vector.
        :type vector: Vector2D
        
        :rtype: Vector2D
        
        :Example:
    
        .. code-block:: python
           
           >>> v = Vector2D(1,2)
           >>> result = v + Vector2D(1,1)
           >>> print(result)
           Vector2D(2,3)
            
        .. seealso:: `<https://geomalgorithms.com/points_and_vectors.html#Vector-Addition>`_
            
        """
        return Vector2D(self.x+vector.x,
                        self.y+vector.y)
            
    
    def __eq__(self,vector):
        """Tests if this vector and the supplied vector are equal.
        
        :param vector: A 2D vector.
        :type vector: Vector2D
        
        :return: True if the vector coordinates are the same; otherwise false
        :rtype: bool
            
        :Example:
    
        .. code-block:: python
           
           >>> v1 = Vector2D(1,2)
           >>> v2 = Vector2D(2,2)               
           >>> result = v1 == v2
           >>> print(result)
           False
            
        """
        return (abs(self.x-vector.x)<SMALL_NUM and 
                abs(self.y-vector.y)<SMALL_NUM)
    
    
    def __repr__(self):
        ""
        return 'Vector2D(%s)' % ','.join([str(c) for c in self.coordinates])
    
    
    def __mul__(self,scalar):
        """Multiplication of this vector and a supplied scalar value.
        
        :param scalar: a numerical scalar value
        :type scalar: float
        
        :rtype: Vector2D
        
        :Example:
    
        .. code-block:: python
           
           >>> v = Vector2D(1,2)
           >>> result = v1 * 2
           >>> print(result)
           Vector2D(2,4)
        
        .. seealso:: `<https://geomalgorithms.com/points_and_vectors.html#Scalar-Multiplication>`_
        
        """
        return Vector2D(self.x*scalar,
                        self.y*scalar)
            
    
    def __sub__(self,vector):
        """Subtraction of this vector and a supplied vector.
        
        :param vector: A 2D vector.
        :type vector: Vector2D
        
        :rtype: Vector2D
        
        :Example:
    
        .. code-block:: python
           
           >>> v = Vector2D(1,2)
           >>> result = v - Vector2D(1,1)
           >>> print(result)
           Vector2D(0,1)
        
        """
        return Vector2D(self.x-vector.x,
                            self.y-vector.y)
    
    
    @property
    def coordinates(self):
        """Returns the coordinates of the vector.
        
        :return: The x and y coordinates as tuple (x,y)
        :rtype: tuple
        
        :Example:
    
        .. code-block:: python
           
           >>> v = Vector2D(1,2)
           >>> result = v.coordinates
           >>> print(result)
           (1,2)
        
        """
        return self.x, self.y
    
    
    @property
    def dimension(self):
        """The dimension of the vector.
        
        :return: '2D'
        :rtype: str
        
        :Example:
    
        .. code-block:: python
        
            >>> v = Vector2D(2,1)
            >>> print(v.dimension)
            '2D'     
        
        """
        
        return '2D'
    
    
    def dot(self,vector):
        """Return the dot product of this vector and the supplied vector.
        
        :param vector: A 2D vector.
        :type vector: Vector2D
        
        :return: The dot product of the two vectors: 
            returns 0 if self and vector are perpendicular; 
            returns >0 if the angle between self and vector is an acute angle (i.e. <90deg); 
            returns <0 if the angle between seld and vector is an obtuse angle (i.e. >90deg).
        :rtype: float
        
        :Example:
    
        .. code-block:: python
           
           >>> v1 = Vector2D(1,0)
           >>> v2 = Vector2D(0,1)               
           >>> result = v1.dot(v2)
           >>> print(result)
           0
        
        .. seealso:: `<https://geomalgorithms.com/vector_products.html#Dot-Product>`_
        
        """
        return self.x*vector.x+self.y*vector.y
            

    def is_collinear(self,vector):
        """Tests if this vector and the supplied vector are collinear.
        
        :param vector: A 2D vector.
        :type vector: Vector2D
        
        :return: True if the vectors lie on the same line; 
            otherwise False.
        :rtype: bool
        
        :Example:
    
        .. code-block:: python
           
           >>> v1 = Vector2D(1,0)
           >>> v2 = Vector2D(2,0)               
           >>> result = v1.is_collinear(v2)
           >>> print(result)
           True        
        
        """
        return abs(self.perp_product(vector)) < SMALL_NUM 
        
    
    @property
    def length(self):
        """Returns the length of the vector.
        
        :rtype: float
        
        :Example:
    
        .. code-block:: python
           
           >>> v = Vector2D(1,0)
           >>> result = v.length
           >>> print(result)
           1
        
        .. seealso:: `<https://geomalgorithms.com/points_and_vectors.html#Vector-Length>`_
        
        """
        return (self.x**2+self.y**2)**0.5
    
    
    @property
    def normalise(self):
        """Returns the normalised vector of this vector.
        
        :return: A codirectional vector of length 1.:
        :rtype: Vector 2D
        
        :Example:
    
        .. code-block:: python
           
           >>> v = Vector2D(3,0)
           >>> result = v.normalise
           >>> print(result)
           Vector2D(1,0)
        
        .. seealso:: `<https://geomalgorithms.com/points_and_vectors.html#Vector-Length>`_
        
        """
        l=self.length
        return Vector2D(self.x/l,
                        self.y/l)
    
    
    def perp_product(self,vector):
        """Returns the perp product of this vector and the supplied vector.
        
        :param vector: A 2D vector.
        :type vector: Vector2D
        
        :return: The perp product of the two vectors. 
            The perp product is the dot product of 
            the perp_vector of this vector and the supplied vector. 
            If supplied vector is collinear with self, returns 0. 
            If supplied vector is on the left of self, returns >0 (i.e. counterclockwise). 
            If supplied vector is on the right of self, returns <0 (i.e. clockwise).
        :rtype: float
            
        :Example:
    
        .. code-block:: python
           
           >>> v1 = Vector2D(1,0)
           >>> v2 = Vector2D(1,0)               
           >>> result = v1.perp_product(v2)
           >>> print(result)
           0
        
        .. seealso:: `<https://geomalgorithms.com/vector_products.html#2D-Perp-Product>`_
        
        """
        return self.perp_vector.dot(vector)
                
    
    @property
    def perp_vector(self):
        """Returns the perp vector of this vector.
        
        :return: The perp vector, i.e. the normal vector on the left 
            (counterclockwise) side of self.
        :rtype: Vector2D
        
        :Example:
    
        .. code-block:: python
           
           >>> v = Vector2D(1,0)
           >>> result = v.perp_vector
           >>> print(result)
           Vector2D(0,1)
        
        .. seealso:: `<https://geomalgorithms.com/vector_products.html#2D-Perp-Operator>`_
        
        """
        return Vector2D(-self.y,self.x)


    @property
    def x(self):
        """The x coordinate of the vector.
        
        :rtype: float
        
        """
        return self._x
    
    @property
    def y(self):
        """The y coordinate of the vector.
        
        :rtype: float
        
        """
        return self._y



class Vector3D(Vector):
    """A three dimensional vector, situated on an x, y, z plane.
    
    :param x: The x coordinate of the vector.
    :type x: float
    :param y: The y coordinate of the vector.
    :type y: float
    :param z: The y coordinate of the vector.
    :type z: float
    
    :Example:
    
    .. code-block:: python
       
       >>> v = Vector3D(1,2,3)
       >>> print(v)
       Vector3D(1,2,3)
    
    .. seealso:: `<https://geomalgorithms.com/points_and_vectors.html#Basic-Definitions>`_
    
    """

    def __init__(self,x=0,y=0,z=0):
        ""
        self._x=x
        self._y=y
        self._z=z
        
    
    def __add__(self,vector):
        """Addition of this vector and a supplied vector.
        
        :param vector: A 3D vector.
        :type vector: Vector3D
        
        :rtype: Vector3D
        
        :Example:
    
        .. code-block:: python
           
           >>> v = Vector3D(1,2,3)
           >>> result = v + Vector3D(1,1,1)
           >>> print(result)
           Vector3D(2,3,4)
            
        """
        return Vector3D(self.x+vector.x,
                        self.y+vector.y,
                        self.z+vector.z)
                    
    
    def __eq__(self,vector):
        """Tests if this vector and the supplied vector are equal.
        
        :param vector: A 3D vector.
        :type vector: Vector3D
        
        :return: True if the vector coordinates are the same; otherwise false
        :rtype: bool
            
        :Example:
    
        .. code-block:: python
           
           >>> v1 = Vector3D(1,2,3)
           >>> v2 = Vector3D(2,2,3)               
           >>> result = v1 == v2
           >>> print(result)
           False
            
        """
        if isinstance(vector,Vector3D):
            return (abs(self.x-vector.x)<SMALL_NUM 
                    and abs(self.y-vector.y)<SMALL_NUM
                    and abs(self.z-vector.z)<SMALL_NUM)
        else:
            return False
            
        
    def __repr__(self):
        ""
        return 'Vector3D(%s)' % ','.join([str(c) for c in self.coordinates])


    def __mul__(self,scalar):
        """Multiplication of this vector and a supplied scalar value.
        
        :param scalar: a numerical scalar value
        :type scalar: float
        
        :rtype: Vector3D
        
        :Example:
    
        .. code-block:: python
           
           >>> v = Vector3D(1,2,3)
           >>> result = v1 * 2
           >>> print(result)
           Vector2D(2,4,6)
        
        .. seealso:: `<https://geomalgorithms.com/points_and_vectors.html#Scalar-Multiplication>`_
        
        """
        if isinstance(scalar,int) or isinstance(scalar,float):
            return Vector3D(self.x*scalar,
                            self.y*scalar,
                            self.z*scalar)
        else:
            raise TypeError
    
    
    def __sub__(self,vector):
        """Subtraction of this vector and a supplied vector.
        
        :param vector: A 3D vector.
        :type vector: Vector3D
        
        :rtype: Vector3D
        
        :Example:
    
        .. code-block:: python
           
           >>> v = Vector3D(1,2,3)
           >>> result = v - Vector3D(1,1,1)
           >>> print(result)
           Vector3D(0,1,2)
        
        """
        return Vector3D(self.x-vector.x,
                        self.y-vector.y,
                        self.z-vector.z)
        


    def cross_product(self,vector):
        """Returns the 3D cross product of this vector and the supplied vector.
        
        :param vector: A 3D vector.
        :type vector: Vector3D
        
        :return: The 3D cross product of the two vectors. 
            This returns a new vector which is perpendicular to 
            this vector (self) and the supplied vector. 
            The returned vector has direction according to the right hand rule. 
            If this vector (self) and the supplied vector are collinear,
            then the returned vector is (0,0,0)
        
        :rtype: Vector3D
        
        :Example:
    
        .. code-block:: python
           
           >>> v1 = Vector3D(1,0,0)
           >>> v2 = Vector3D(0,1,0)
           >>> result = v1.cross_product(v2)
           >>> print(result)
           Vector3D(0,0,1)
        
        .. seealso:: `<https://geomalgorithms.com/vector_products.html#3D-Cross-Product>`_
        
        """
        (v1,v2,v3),(w1,w2,w3)=self.coordinates,vector.coordinates
        return Vector3D(v2*w3-v3*w2,
                        v3*w1-v1*w3,
                        v1*w2-v2*w1)


    @property
    def coordinates(self):
        """Returns the coordinates of the vector.
        
        :return: The x and y coordinates as tuple (x,y,z)
        :rtype: tuple
        
        :Example:
    
        .. code-block:: python
           
           >>> v = Vector3D(1,2,3)
           >>> result = v.coordinates
           >>> print(result)
           (1,2,3)
        
        """
        return self.x, self.y, self.z
    
    
    @property
    def dimension(self):
        """The dimension of the vector.
        
        :return: '3D'
        :rtype: str
        
        :Example:
    
        .. code-block:: python
        
            >>> v = Vector3D(1,2,3)
            >>> print(v.dimension)
            '3D'     
        
        """
        
        return '3D'
    
    
    def dot(self,vector):
        """Return the dot product of this vector and the supplied vector.
        
        :param vector: A 3D vector.
        :type vector: Vector3D
        
        :return: The dot product of the two vectors: 
            returns 0 if self and vector are perpendicular; 
            returns >0 if the angle between self and vector is an acute angle (i.e. <90deg); 
            returns <0 if the angle between seld and vector is an obtuse angle (i.e. >90deg).
        :rtype: float
        
        :Example:
    
        .. code-block:: python
           
           >>> v1 = Vector3D(1,0,0)
           >>> v2 = Vector3D(0,1,0)
           >>> result = v1.dot(v2)
           >>> print(result)
           0
        
        .. seealso:: `<https://geomalgorithms.com/vector_products.html#Dot-Product>`_
        
        """
        return self.x*vector.x + self.y*vector.y + self.z*vector.z
        

    def is_collinear(self,vector):
        """Tests if this vector and the supplied vector are collinear.
        
        :param vector: A 3D vector.
        :type vector: Vector3D
        
        :return: True if the vectors lie on the same line; 
            otherwise False.
        :rtype: bool
        
        :Example:
    
        .. code-block:: python
           
           >>> v1 = Vector3D(1,0,0)
           >>> v2 = Vector3D(2,0,0)               
           >>> result = v1.is_collinear(v2)
           >>> print(result)
           True        
        
        """
        return self.cross_product(vector).length < SMALL_NUM 
            
    
    @property
    def length(self):
        """Returns the length of the vector.
        
        :rtype: float
        
        :Example:
    
        .. code-block:: python
           
           >>> v = Vector3D(1,0,0)
           >>> result = v.length
           >>> print(result)
           1
        
        .. seealso:: `<https://geomalgorithms.com/points_and_vectors.html#Vector-Length>`_
        
        """
        return (self.x**2 + self.y**2 + self.z**2)**0.5
    
    
    @property
    def normalise(self):
        """Returns the normalised vector of this vector.
        
        :return: A codirectional vector of length 1.
        :rtype: Vector3D
        
        :Example:
    
        .. code-block:: python
           
           >>> v = Vector3D(3,0,0)
           >>> result = v.normalise
           >>> print(result)
           Vector3D(1,0)
        
        .. seealso:: `<https://geomalgorithms.com/points_and_vectors.html#Vector-Length>`_
        
        """
        l=self.length
        return Vector3D(self.x/l,
                        self.y/l,
                        self.z/l)
    
          
    def triple_product(self,vector1,vector2):
        """Returns the triple product of this vector and 2 supplied vectors.
        
        :param vector1: A 3D vector.
        :type vector1: Vector3D
        :param vector2: A 3D vector.
        :type vector2: Vector3D
        
        :return: The triple product of the three vectors. 
            The result is equal to the volume of the parallelepiped (3D equivalent of a parallelogram). 
            The result is equal to six times the volume of the tetrahedron (3D shape with 4 vertices). 
            
        :rtype: float
        
        :Example:
    
        .. code-block:: python
           
           >>> v1 = Vector3D(1,0,0)
           >>> v2 = Vector3D(0,1,0)
           >>> v3 = Vector3D(0,0,1)
           >>> result = v1.triple_product(v2,v3)
           >>> print(result)
           1
        
        .. seealso:: `<https://geomalgorithms.com/vector_products.html#3D-Triple-Product>`_        
        
        """
        return self.dot(vector1.cross_product(vector2))
            
        
    @property
    def x(self):
        """The x coordinate of the vector.
        
        :rtype: float
        
        """
        return self._x
    
    
    @property
    def y(self):
        """The y coordinate of the vector.
        
        :rtype: float
        
        """
        return self._y
    
    
    @property
    def z(self):
        """The z coordinate of the vector.
        
        :rtype: float
        
        """
        return self._z    
        
        
        
        
    
    
    