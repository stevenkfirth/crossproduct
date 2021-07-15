# -*- coding: utf-8 -*-

import collections.abc
import itertools
import math

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import shapely.geometry
import triangle as tr
import numpy as np

ABS_TOL = 1e-7 # default value for math.isclose


class _BaseGeometricObject():
    """A base class for all geometric objects.
    
    """
    
    def __eq__(self,obj):
        """Test for equality between objects.
        
        :param obj: A geometric object.
        
        :returns: True if the two objects are of the same class and have the 
            same coordinates;
            otherwise False.
        :rtype: bool
        
        .. rubric:: Code Examples
    
        .. code-block:: python
        
            >>> from crossproduct import Point
            >>> print(Point(1,2) == Point(1,2))
            True
            
            >>> from crossproduct import Point, Points
            >>> print(Points(Point(1,2)) == Points(Point(1,2)))
            True
        
        """
        if isinstance(obj,self.__class__):
            return self.coordinates==obj.coordinates
        else:
            return False
        
        
    def __hash__(self):
        """
        """
        return self.coordinates


class _BaseShapelyObject():
    """A base class for geometric objects that can be represented with shapely objects.
    
    
    
    
    """
    
            
    def _shapely_to_objs(self,shapely_obj):
        ""
        if shapely_obj.is_empty:
            return []
        elif isinstance(shapely_obj,shapely.geometry.Point):
            return [self._shapely_point_to_point(shapely_obj)]
        elif isinstance(shapely_obj,shapely.geometry.LineString):
            return [self._shapely_linestring_to_polyloop(shapely_obj)]
        elif isinstance(shapely_obj,shapely.geometry.Polygon):
            return [self._shapely_polygon_to_polygon(shapely_obj)]
        elif isinstance(shapely_obj,shapely.geometry.MultiPoint):
            return [self._shapely_point_to_point(x) for x in shapely_obj]
        elif isinstance(shapely_obj,shapely.geometry.MultiLineString):
            return [self._shapely_linestring_to_polyloop(x) for x in shapely_obj]
        elif isinstance(shapely_obj,shapely.geometry.MultiPolygon):
            return [self._shapely_polygon_to_polygon(x) for x in shapely_obj]
        elif isinstance(shapely_obj,shapely.geometry.GeometryCollection):
            return [self._shapely_to_objs(x)[0] for x in shapely_obj]
        else:
            raise Exception  # type not captured
        
        
    def _shapely_linestring_to_polyloop(self,shapely_obj):
        ""
        return Polyline(*(Point(*x) for x in shapely_obj.coords))
    
    
    def _shapely_point_to_point(self,shapely_obj):
        ""
        return Point(*shapely_obj.coords[0])
        
    
    def _shapely_polygon_to_polygon(self,shapely_obj):
        ""
        holes=[]  # to do
        for x in shapely_obj.interiors:
            hole_pg=Polygon(*(Point(*y) for y in x.coords[:-1]))
            holes.append(hole_pg)
        return Polygon(*(Point(*x) for x in shapely_obj.exterior.coords[:-1]),
                       holes=holes)
    
    
    def _shapely_to_pts_pls_pgns(self,shapely_obj):
        ""
        result=self._shapely_to_objs(shapely_obj)
            
        pts=[]
        pls=[]
        pgs=[]
        
        for obj in result:
            if isinstance(obj,Point):
                pts.append(obj)
            elif isinstance(obj,Polyline):
                pls.append(obj)
            elif isinstance(obj,Polygon):
                pgs.append(obj)
            else:
                raise Exception  # type not captured
                
        return Points(*pts),Polylines(*pls),Polygons(*pgs)
    
    
    @property
    def centroid(self):
        """
        """
        if self.nD==2:
            return self._shapely_point_to_point(self._shapely.centroid)
        elif self.nD==3:
            raise Exception  # shapely doesn't work for 3d
        else:
            raise ValueError
        
    
    def difference(self,obj):
        """The geometric difference between self and obj.
        
        :param obj: A geometric object.
        
        :returns: A tuple of the difference objects.
        :rtype: tuple
        
        .. rubric:: Code Examples
        
        .. code-block:: python
        
            >>> from crossproduct import Point, Polygon
            >>> pt=Point(0.5,0.5)
            >>> pg=Polygon(Point(0,0),Point(1,0),Point(1,1),Point(0,1))
            >>> result=pt.difference(pg)
            >>> print(result)
            ()
            
            >>> from crossproduct import Point, Points, Polygon
            >>> pts=Points(Point(0.5,0.5))
            >>> pg=Polygon(Point(0,0),Point(1,0),Point(1,1),Point(0,1))
            >>> result=pts.difference(pg)
            >>> print(result)
            ()
        
        """
        
        if self.nD==2:
            
            a=self._shapely
            b=obj._shapely
            result=a.difference(b)
            #print(result)
            return tuple(self._shapely_to_objs(result))
            
        elif self.nD==3:
            
            raise Exception  # shapely doesn't work for 3d
            
        else:
            
            raise ValueError
    
            
    def intersection(self,obj):
        """The geometric intersection between self and obj.
        
        :param obj: A geometric object.
        
        :returns: A tuple of the difference objects.
        :rtype: tuple
        
        .. rubric:: Code Examples
        
        .. code-block:: python
        
            >>> from crossproduct import Point, Polygon
            >>> pt=Point(0.5,0.5)
            >>> pg=Polygon(Point(0,0),Point(1,0),Point(1,1),Point(0,1))
            >>> result=pt.intersection(pg)
            >>> print(result)
            (Point(0.5,0.5),)
            
            >>> from crossproduct import Point, Points, Polygon
            >>> pts=Points(Point(0.5,0.5))
            >>> pg=Polygon(Point(0,0),Point(1,0),Point(1,1),Point(0,1))
            >>> result=pts.intersection(pg)
            >>> print(result)
            (Point(0.5,0.5),)
        
        """
        if self.nD==2:
            
            a=self._shapely
            b=obj._shapely
            result=a.intersection(b)
            return tuple(self._shapely_to_objs(result))
                
        elif self.nD==3:
            
            raise Exception  # shapely doesn't work for 3d
            
        else:
            
            raise ValueError
        
        

class _BaseSequence(collections.abc.Sequence):
    """A base class for geometric objects that are represented as a mmutable sequence.
    
    """
    
    
    def __getitem__(self,index):
        ""
        return self._items[index]
    
   
    def __init__(self,*items):
        ""
        
        self._items=tuple(items)
        

    def __len__(self):
        ""
        return len(self._items)
    
    
    def __repr__(self):
        ""
        return '%s(%s)' % (self.__class__.__name__,
                           ','.join([str(c) for c in self]))
    
    
    @property
    def coordinates(self):
        """Returns a tuple representation of the object.
        
        :returns: The coordinates as a tuple. 
        :rtype: tuple
        
        .. rubric:: Code Examples
        
        .. code-block:: python
        
            >>> from crossproduct import Point, Points
            >>> pts = Points(Point(1,1),Point(2,2))
            >>> result = pts.coordinates()
            >>> print(result)
            ((1.0,1.0),(2.0,2.0))
        
        """
        return tuple(x.coordinates for x in self)
    
    
    @property
    def nD(self):
        """The number of dimensions of the object.
        
        :returns: 2 or 3
        :rtype: int
        
        .. rubric:: Code Examples
    
        .. code-block:: python
        
            >>> from crossproduct import Point, Points
            >>> pts = Points(Point(1,1))
            >>> print(pts.nD)
            2
            
        """
        return self[0].nD
    
    
    def project_2D(self,coordinate_index):
        """Projects the object on a 2D plane.
        
        
        """
        return self.__class__(*(x.project_2D(coordinate_index) for x in self))
    
    
    def project_3D(self,plane,coordinate_index):
        """Projects the object on a 2D plane.
        
        
        """
        return self.__class__(*(x.project_3D(plane,coordinate_index) 
                                for x in self))
        
 

class Point(_BaseGeometricObject,_BaseSequence,_BaseShapelyObject):
    """A point, as described by xy or xyz coordinates.
    
    In *crossproduct* a `Point` object is a immutable sequence. 
    Iterating over a `Point` will provide its coordinates.
    Indexing a `Point` will return the coordinate for that index (0=x, 1=y, 2=z).
    
    :param coordinates: Argument list of two (xy) or three (xyz) coordinates. 
        Coordinates should be of type int, float or similar numeric. These values
        are converted to floats.
    
    .. rubric:: Code Example
    
    .. code-block:: python
       
       >>> from crossproduct import Point
       >>> pt = Point(1,2)
       >>> print(pt)
       Point(1.0,2.0)
       >>> print(list(pt))      # prints a list of the coordinates
       [1.0,2.0]
       >>> print(pt[1])         # prints the y coordinate
       2.0
    
    
    """
    
    def __add__(self,vector):
        """The addition of this point and a vector.
        
        :param vector: The vector to be added to the point.
        :type vector: Vector
        
        :rtype: Point
        
        .. rubric:: Code Example
    
        .. code-block:: python
        
            >>> from crossproduct import Point
            >>> p = Point(1,2)
            >>> result = p + Vector(1,1)
            >>> print(result)
            Point(2.0,3.0)
        
        """
        zipped=itertools.zip_longest(self,vector) # missing values filled with None
        try:
            coordinates=[a+b for a,b in zipped]
        except TypeError: # occurs if, say, a or b is None
            raise ValueError('Point and vector to add must be of the same length.')
        return Point(*coordinates)
    
    
    def __init__(self,*coordinates):
        ""
        self._items=tuple(coordinates)
        
        
    def __sub__(self,point_or_vector):
        """Subtraction of supplied object from this point.
        
        :param point_or_vector: Either a point or a vector.
        :type point_or_vector: Point or Vector
        
        :return: If a point is supplied, then a vector is returned (i.e. v=P1-P0). 
            If a vector is supplied, then a point is returned (i.e. P1=P0-v).
        :rtype: Point or Vector
        
        .. rubric:: Code Example
    
        .. code-block:: python
        
            >>> from crossproduct import Point
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
        
    
    @property
    def _shapely(self):
        """An equivalent shapely object(s) of self.
        
        :raises ValueError: If point is not 2D.
        
        :rtype: shapely.geometry.Point
        
        """
        if self.nD==2:
            return shapely.geometry.Point(self.coordinates)
        else:
            raise ValueError  # only 2d for shapely objects
    
    
    @property       
    def coordinates(self):
        """Returns a tuple representation of the point.
        
        :returns: The coordinates as a tuple. 
            For a point, this can also be achieved by creating a 
            tuple of the point itself (i.e. :code:`tuple(pt)`).
        :rtype: tuple
        
        .. rubric:: Code Example
        
        .. code-block:: python
        
            >>> from crossproduct import Point
            >>> pt = Point(2,2)
            >>> result = pt.coordinates()
            >>> print(result)
            (2.0,2.0)
        
        """
        return self._items
    
    
    def equals(self,point):
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
        
            >>> from crossproduct import Point
            >>> result = Point(1,2).equals(Point(2,2))
            >>> print(result)
            False
            
        """
        zipped=itertools.zip_longest(self,point) # missing values filled with None
        try:
            result=[math.isclose(a, b, abs_tol=ABS_TOL) for a,b in zipped]
        except TypeError: # occurs if, say, a or b is None
            raise ValueError('Points to compare must be of the same length.')
        return all(result)


    @property
    def nD(self):
        """The number of dimensions of the point.
        
        :returns: 2 or 3
        :rtype: int
        
        .. rubric:: Code Example
    
        .. code-block:: python
        
            >>> from crossproduct import Point
            >>> pt = Point(1,1)
            >>> print(pt.nD)
            2
            
        """
        return len(self)
    
    
    def project_2D(self,coordinate_index):
        """Projection of a 3D point as a 2D point.
        
        :param coordinate_index: The index of the coordinate to ignore.
            Use coordinate_index=0 to ignore the x-coordinate, coordinate_index=1 
            for the y-coordinate and coordinate_index=2 for the z-coordinate.
        :type coordinate_index: int
        
        :raises ValueError: If coordinate_index is not between 0 and 2.
        
        :return: A 2D point based on the projection of the 3D point.
        :rtype: Point
               
        .. rubric:: Code Example
    
        .. code-block:: python
        
            >>> from crossproduct import Point
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
        """Projection of a 2D point on a 3D plane.
        
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
        
            >>> from crossproduct import Point, Plane
            >>> pt = Point(2,2)
            >>> pl = Plane(Point(0,0,1), Vector(0,0,1))
            >>> result = pt.project_3D(pl, 2)
            >>> print(result)
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
        
        :rtype: float
        
        .. rubric:: Code Example
    
        .. code-block:: python
        
            >>> from crossproduct import Point
            >>> pt = Point(0,1,2)
            >>> print(pt.x)
            0.0
            
        """
        return self[0]
    
    
    @property
    def y(self):
        """The y coordinate of the point.
        
        :rtype: float
        
        .. rubric:: Code Example
    
        .. code-block:: python
        
            >>> from crossproduct import Point
            >>> pt = Point(0,1,2)
            >>> print(pt.y)
            1.0
            
        """
        return self[1]
    
    
    @property
    def z(self):
        """The z coordinate of the point.
        
        :raises IndexError: If point is a 2D point.
        
        :rtype: float
        
        .. rubric:: Code Example
    
        .. code-block:: python
        
            >>> from crossproduct import Point
            >>> pt = Point(0,1,2)
            >>> print(pt.z)
            2.0
        
        """
        return self[2]
    



class Points(_BaseGeometricObject,_BaseSequence,_BaseShapelyObject):
    """A collection of points.    
    
    In *crossproduct* a `Points` object is a immutable sequence. 
    Iterating over a `Points` will provide its Point objects.
    
    :param points: An argument list of Point instances. 
    
    .. rubric:: Code Example
        
    .. code-block:: python
        
        >>> from crossproduct import Point, Points
        >>> pts = Points(Point(0,0), Point(1,0))
        >>> print(pts)
        Points(Point(0.0,0.0), Point(1.0,0.0))
        >>> print(pts[1])
        Point(1.0,0.0)
    
    """
    
    def __init__(self,*points):
        ""
        self._items=tuple(points)
    
    
    @property
    def _shapely(self):
        ""
        if len(self)==0 or self.nD==2:
            x=[pt._shapely for pt in self]
            return shapely.geometry.MultiPoint(x)
        else:
            raise Exception  # only 2d for shapely objects
    
    
    @property
    def centroid(self):
        """The centroid of the points.
        
        :rtype: Point
        
        """
        if self.nD==2:
            return self._shapely_point_to_point(self._shapely.centroid)
        elif self.nD==3:
            return Point(*(sum(c)/len(c) for c in zip(*self.coordinates)))
        else:
            raise ValueError
            
            

class Vector(_BaseGeometricObject,_BaseSequence):
    """A vector, as described by xy or xyz coordinates.
    
    In *crossproduct* a Vector object is a immutable sequence. 
    Iterating over a Vector will provide its coordinates.
    Indexing a vector will return the coordinate for that index (0=x, 1=y, 2=z).
    
    :param coordinates: Argument list of two (xy) or three (xyz) coordinates. 
        Coordinates should be of type int, float or similar numeric. These values
        are converted to floats.
    
    .. rubric:: Code Example
    
    .. code-block:: python
       
       >>> from crossproduct import Vector
       >>> v = Vector(1,2)
       >>> print(v)
       Vector(1.0,2.0)
    
    """

    def __add__(self,vector):
        """Addition of this vector and a supplied vector.
        
        :param vector: A vector.
        :type vector: Vector
        
        :rtype: Vector
        
        .. rubric:: Code Example
    
        .. code-block:: python
           
           >>> from crossproduct import Vector
           >>> v = Vector(1,2)
           >>> result = v + Vector(1,1)
           >>> print(result)
           Vector(2.0,3.0)
            
        """
        zipped=itertools.zip_longest(self,vector) # missing values filled with None
        try:
            coordinates=[a+b for a,b in zipped]
        except TypeError: # occurs if, say, a or b is None
            raise ValueError('Vectors to add must be of the same length.')
        return Vector(*coordinates)
    

    def __init__(self,*coordinates):
        ""
        self._items=tuple(coordinates)


    def __mul__(self,scalar):
        """Multiplication of this vector and a supplied scalar value.
        
        :param scalar: A numerical scalar value.
        :type scalar: float
        
        :rtype: Vector
        
        .. rubric:: Code Example
        
        .. code-block:: python
           
           >>> from crossproduct import Vector
           >>> v = Vector(1,2)
           >>> result = v1 * 2
           >>> print(result)
           Vector(2.0,4.0)
        
        """
        return Vector(*(c*scalar for c in self))            
    
    
    def __sub__(self,vector):
        """Subtraction of this vector and a supplied vector.
        
        :param vector: A vector.
        :type vector: Vector
        
        :rtype: Vector
        
        .. rubric:: Code Example
    
        .. code-block:: python
           
           >>> from crossproduct import Vector
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


    def angle(self,vector):
        """Returns the angle between this vector and the supplied vector.
        
        :param vector: A 2D or 3D vector.
        :type vector: Vector
        
        :return: The angle in radians.
        :rtype: float
        
        .. rubric:: Code Example
    
        .. code-block:: python
           
           >>> from crossproduct import Vector
           >>> v1=Vector(0,1)
           >>> v2=Vector(1,1)
           >>> result=v1.angle(v2)
           >>> print(result)            # a 45 degree angle
           0.7853981633974484
        
        """
        return math.acos(self.dot(vector)/self.length/vector.length)
    
    
    @property
    def coordinates(self):
        """Returns a tuple representation of the vector.
        
        :returns: The coordinates as a tuple. 
            For a vector, this can also be achieved by creating a 
            tuple of the vector itself (i.e. :code:`tuple(v)`).
        :rtype: tuple
        
        .. code-block:: python
        
            >>> from crossproduct import Vector
            >>> v = Vector(2,2)
            >>> result = v.coordinates
            >>> print(result)
            (2.0,2.0)
        
        """
        return self._items
    

    def cross_product(self,vector):
        """Returns the 3D cross product of this vector and the supplied vector.
        
        :param vector: A 3D vector.
        :type vector: Vector
        
        :raises ValueError: If the vector is not a 3D vector.
        
        :return: The 3D cross product of the two vectors. 
            This returns a new vector which is perpendicular to 
            this vector (self) and the supplied vector. 
            The returned vector has direction according to the right hand rule. 
            If this vector (self) and the supplied vector are collinear,
            then the returned vector is (0,0,0)
        
        :rtype: Vector
        
        .. rubric:: Code Example
        
        .. code-block:: python
           
           >>> from crossproduct import Vector
           >>> v1 = Vector(1,0,0)
           >>> v2 = Vector(0,1,0)
           >>> result = v1.cross_product(v2)
           >>> print(result)
           Vector(0,0,1)
        
        """
        if self.nD==3:
            (v1,v2,v3),(w1,w2,w3)=list(self),list(vector)
            return Vector(v2*w3-v3*w2,
                          v3*w1-v1*w3,
                          v1*w2-v2*w1)
        else:
            raise ValueError('"cross_product" method can only be used for a 3D vector.')
            

    def dot(self,vector):
        """Return the dot product of this vector and the supplied vector.
        
        :param vector: A vector.
        :type vector: Vector
        
        :returns: The dot product of the two vectors: 
            returns 0 if self and vector are perpendicular; 
            returns >0 if the angle between self and vector is an acute angle (i.e. <90deg); 
            returns <0 if the angle between self and vector is an obtuse angle (i.e. >90deg).
        :rtype: float
        
        .. rubric:: Code Example
        
        .. code-block:: python
           
           >>> from crossproduct import Vector
           >>> v1 = Vector(1,0)
           >>> v2 = Vector(0,1)               
           >>> result = v1.dot(v2)
           >>> print(result)
           0
        
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
           >>> from crossproduct import Vector
           >>> v = Vector(1,2)
           >>> result = v.index_largest_absolute_coordinate
           >>> print(result)
           1
           
           # 3D example
           >>> from crossproduct import Vector
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
           >>> from crossproduct import Vector
           >>> v1 = Vector(1,2)
           >>> v2 = Vector(2,4)
           >>> result = v1.is_codirectional(v2)
           >>> print(result)
           True
           
           # 3D example
           >>> from crossproduct import Vector
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
           
           >>> from crossproduct import Vector
           >>> v1 = Vector(1,0)
           >>> v2 = Vector(2,0)               
           >>> result = v1.is_collinear(v2)
           >>> print(result)
           True     
           
           >>> from crossproduct import Vector
           >>> v1 = Vector(1,0,0)
           >>> v2 = Vector(2,0,0)               
           >>> result = v1.is_collinear(v2)
           >>> print(result)
           True        
        
        """
        if self.nD==2:
            return math.isclose(self.perp_product(vector), 0, abs_tol=ABS_TOL)
        elif self.nD==3:
            return math.isclose(self.cross_product(vector).length, 0, abs_tol=ABS_TOL)
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
           >>> from crossproduct import Vector
           >>> v1 = Vector(1,2)
           >>> v2 = Vector(-2,-4)
           >>> result = v1.is_opposite(v2)
           >>> print(result)
           True
           
           # 3D example
           >>> from crossproduct import Vector
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
           >>> from crossproduct import Vector
           >>> v1 = Vector(1,0)
           >>> v2 = Vector(0,1)
           >>> result = v1.is_perpendicular(v2)
           >>> print(result)
           True
           
           # 3D example
           >>> from crossproduct import Vector
           >>> v1 = Vector(1,0,0)
           >>> v2 = Vector(0,1,0)
           >>> result = v1.is_perpendicular(v2)
           >>> print(result)
           True
        
        """
        return math.isclose(self.dot(vector), 0, abs_tol=ABS_TOL)
        
    
    @property
    def length(self):
        """Returns the length of the vector.
        
        :rtype: float
        
        .. rubric:: Code Example
    
        .. code-block:: python
           
           >>> from crossproduct import Vector
           >>> v = Vector(1,0)
           >>> result = v.length
           >>> print(result)
           1
        
        """
        return sum(c**2 for c in self)**0.5
    
    
    @property
    def nD(self):
        """The number of dimensions of the vector.
        
        :returns: 2 or 3
        :rtype: int
        
        .. rubric:: Code Example
    
        .. code-block:: python
        
            >>> from crossproduct import Vector
            >>> v = Vector(1,1)
            >>> print(v.nD)
            2
            
        """
        return len(self)
    
    
    @property
    def normalise(self):
        """Returns the normalised vector of this vector.
        
        :returns: A codirectional vector of length 1.
        :rtype: Vector
        
        :Example:
    
        .. code-block:: python
           
           >>> from crossproduct import Vector
           >>> v = Vector(3,0)
           >>> result = v.normalise
           >>> print(result)
           Vector(1,0)
        
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
           >>> from crossproduct import Vector
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
            
        .. rubric:: Code Example
    
        .. code-block:: python
           
           >>> from crossproduct import Vector
           >>> v1 = Vector(1,0)
           >>> v2 = Vector(1,0)               
           >>> result = v1.perp_product(v2)
           >>> print(result)
           0
        
        """
        if self.nD==2:
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
           
           >>> from crossproduct import Vector
           >>> v = Vector(1,0)
           >>> result = v.perp_vector
           >>> print(result)
           Vector(0,1)
        
        """
        if self.nD==2:
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
           
           >>> from crossproduct import Vector
           >>> v1 = Vector(1,0,0)
           >>> v2 = Vector(0,1,0)
           >>> v3 = Vector(0,0,1)
           >>> result = v1.triple_product(v2,v3)
           >>> print(result)
           1
        
        """
        return self.dot(vector1.cross_product(vector2))


    @property
    def x(self):
        """The x coordinate of the vector.
        
        :rtype: float
        
        .. rubric:: Code Example
    
        .. code-block:: python
        
            >>> from crossproduct import Vector
            >>> v = Vector(0,1,2)
            >>> print(v.x)
            0.0
        
        """
        return self[0]
    
    
    @property
    def y(self):
        """The y coordinate of the vector.
        
        :rtype: float
        
        .. rubric:: Code Example
    
        .. code-block:: python
        
            >>> from crossproduct import Vector
            >>> v = Vector(0,1,2)
            >>> print(v.y)
            1.0
        
        """
        return self[1]
    
    
    @property
    def z(self):
        """The z coordinate of the vector.
        
        :raises IndexError: If vector is a 2D vector.
        
        :rtype: float
        
        .. rubric:: Code Example
    
        .. code-block:: python
        
            >>> from crossproduct import Vector
            >>> v = Vector(0,1,2)
            >>> print(v.z)
            2.0
        
        """
        return self[2]
    

class Line(_BaseGeometricObject):
    """A 2D or 3D line, as described by a point and a vector.
    
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
       
       # 2D example
       >>> from crossproduct import Point, Vector, Line
       >>> l = Line(Point(0,0), Vector(1,0))
       >>> print(l)
       Line(Point(0,0), Vector(1,0))
       
       # 3D example
       >>> from crossproduct import Point, Vector, Line
       >>> l = Line(Point(0,0,0), Vector(1,0,0))
       >>> print(l)
       Line(Point(0,0,0), Vector(1,0,0))
    
    """
    
    def __init__(self,P0,vL):
        ""
        if math.isclose(vL.length, 0, abs_tol=ABS_TOL):
            raise ValueError('length of vL must be greater than zero')
        self._P0=P0
        self._vL=vL
    
    
    def __repr__(self):
        ""
        return 'Line(%s, %s)' % (self.P0,self.vL)
    
    
    def calculate_point(self,t):
        """Returns a point on the line for a given t value. 
        
        :param t: The t value of the equation of the line.
        :type t: float
        
        :return: A point on the line calcualted using the t value. 
        :rtype: Point
        
        .. rubric:: Code Example
        
        .. code-block:: python    
        
           # 2D example
           >>> from crossproduct import Point, Vector, Line
           >>> l = Line(Point(0,0), Vector(1,0))
           >>> result = l.calcuate_point(3)
           >>> print(result)
           Point(3,0)
           
           # 3D example
           >>> from crossproduct import Point, Vector, Line
           >>> l = Line(Point(0,0,0), Vector(1,0,0))
           >>> result = l.calcuate_point(-3)
           >>> print(result)
           Point(-3,0,0)
        
        """
        return self.P0 + (self.vL * t)


    def calculate_t_from_coordinates(self,*coordinates):
        """Returns t for a given set of coordinates.
        
        First attempts to calculate t from the x coordinate. 
        If this fails then next attempts to calculate t from the y coordinate.
        If this fails then attempts to calculate t from the z coordinate.
        
        :param coordinates: Argument list of xy or xyz coordinate values (floats).
        
        :return: The calculated t value.
        :rtype: float
        
        :Example:
        
        .. code-block:: python
           
           # 2D example
           >>> from crossproduct import Point, Vector, Line
           >>> l = Line(Point(0,0), Vector(1,0))
           >>> result = l.calculate_t_from_point(Point(3,0))
           >>> print(result)
           3
        
           # 3D example
           >>> from crossproduct import Point, Vector, Line
           >>> l = Line(Point(0,0,0), Vector(1,0,0))
           >>> result = l.calculate_t_from_point(Point(3,0,0))
           >>> print(result)
           3
            
        """
        for P0,vL,point in zip(self.P0,self.vL,coordinates): # loop through x, y, z components
            if not math.isclose(vL, 0, abs_tol=ABS_TOL):
                return (point-P0) / vL
        raise Exception()
    
    
    def contains(self,obj):
        """Tests if the line contains the object.
        
        :param obj: A point, halfline or segment.
        :type obj: Point, Halfline, Segment
        
        :raises TypeError: If supplied object is not supported by this method.
            
        :return:  For point, True if the point lies on the line; otherwise False. 
            For halfline, True if the halfline startpoint is on the line and 
            the halfline vector is collinear to the line vector; otherwise False. 
            For segment, True if the segment start and endpoints are on the line; otherwise False. 
        :rtype: bool
        
        .. rubric:: Code Example
    
        .. code-block:: python
           
           # 2D example
           >>> from crossproduct import Point, Vector, Line
           >>> l = Line(Point(0,0), Vector(1,0))
           >>> result = Point(2,0) in l
           >>> print(result)
           True
           
           # 3D example
           >>> from crossproduct import Point, Vector, Line
           >>> l = Line(Point(0,0,0), Vector(1,0,0))
           >>> hl = Halfline(Point(0,0,0), Vector(-1,0,0))
           >>> result = hl in l
           >>> print(result)
           True
            
        """
        if isinstance(obj,Point):
            t=self.calculate_t_from_coordinates(*obj)
            pt=self.calculate_point(t)           
            return obj.equals(pt)
                    
        # elif isinstance(obj,Halfline):
        #     return self.contains(obj.P0) and obj.vL.is_collinear(self.vL)
        
        # elif isinstance(obj,Segment):
        #     return self.contains(obj.P0) and self.contains(obj.P1)
        
        else:
            raise TypeError
        
    
    
    @property
    def coordinates(self):
        """Returns a tuple representation of the line.
        
        :returns: The starting point of the line and the line vector as tuples. 
        :rtype: tuple
        
        .. code-block:: python
        
            >>> from crossproduct import Point, Vector, Line
            >>> l = Line(Point(0,0,0), Vector(1,0,0))
            >>> result = l.coordinates
            >>> print(result)
            ((0.0,0.0,0.0), (1.0,0.0,0.0))
        
        """
        return (self.P0.coordinates,self.vL.coordinates)
    
    
    def equals(self,line):
        """Tests if this line and the supplied line are equal.
        
        :param line: A line.
        :type line: Line
        
        :raises TypeError: If a Line instance is not supplied.
        
        :return: True if the start point of supplied line lies on line (self),
            and the vL of supplied line is collinear to the vL of line (self); 
            otherwise False.
        :rtype: bool
            
        .. rubric:: Code Example
    
        .. code-block:: python
           
           # 2D example
           >>> from crossproduct import Point, Vector, Line
           >>> l = Line(Point(0,0), Vector(1,0))
           >>> result = l == l
           >>> print(result)
           True
           
           # 3D example
           >>> from crossproduct import Point, Vector, Line
           >>> l1 = Line(Point(0,0,0), Vector(1,0,0))
           >>> l2 = Line(Point(0,0,0), Vector(-1,0,0))
           >>> result = l1 == l2
           >>> print(result)
           True
           
        """
        if isinstance(line,Line):
            return self.contains(line.P0) and self.vL.is_collinear(line.vL)
        else:
            raise TypeError('Line.__eq__ should be used with a Line instance')
    
    
    @property
    def nD(self):
        """The number of dimensions of the line.
        
        :returns: 2 or 3
        :rtype: int
        
        .. rubric:: Code Example
    
        .. code-block:: python
        
            >>> from crossproduct import Point, Vector, Line
            >>> l = Line(Point(0,0,0), Vector(1,0,0))
            >>> print(l.nD)
            3
            
        """
        return self.P0.nD
    
    
    @property
    def P0(self):
        """The starting point of the line.
        
        :rtype: Point
        
        """
        return self._P0
    
    
    @property
    def plane(self):
        """A plane which the line lies on.
        
        
        """
        if not self.vL.is_collinear(Vector(1,0,0)):
            N=self.vL.cross_product(Vector(1,0,0))
        elif not self.vL.is_collinear(Vector(0,1,0)):
            N=self.vL.cross_product(Vector(0,1,0))
        else:
            N=self.vL.cross_product(Vector(0,0,1))
            
        return Plane(self.P0,N)
        
    
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
        
            >>> from crossproduct import Point, Vector, Line
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
            
    

class Polyline(_BaseGeometricObject,_BaseSequence,_BaseShapelyObject):
    """A 2D or 3D polyline.
    
    A polyline is a series of joined segments which are defined as a series of points.
    
    In *crossproduct* a Polyline object is a immutable sequence. 
    Iterating over a Polyline will provide its Point instances.
    
    :param points: Argument list of Point instances.
    
    .. rubric:: Code Example
    
    .. code-block:: python
       
       >>> from crossproduct import Point, Polyline
       >>> pl = Polyline(Point(0,0), Point(1,0), Point(1,1))
       >>> print(pl)
       Polyline(Point(0.0,0.0), Point(1.0,0.0), Point(1.0,1.0))
       
    """
    
    @property
    def _shapely(self):
        ""
        if self.nD==2:
            return shapely.geometry.LineString(self.coordinates)
        else:
            raise Exception  # only 2d for shapely polygons


    def contains(self,obj):
        ""
        if isinstance(obj,Point):
            
            for pl in self.polylines:
                line=pl.lines[0]
                t=line.calculate_t_from_coordinates(*obj)
                pt=line.calculate_point(t)  
                return obj.equals(pt)
            
        else:
            
            raise Exception
        
        


    def _intersection_point_3D(self,point):
        ""
        if self.contains(point):
            return (point,)
        else:
            return tuple()
        
        
    def _intersection_polyline_3D(self,polyline):
        ""
        result=[]
        for pl1 in self.polylines:
            l1=pl1.lines[0]
            plane=l1.plane
            for pl2 in polyline.polylines:
                l2=pl2.lines[0]
                if l1.equals(l2):
                    i=plane.N.index_largest_absolute_coordinate
                    pl1_2D=pl1.project_2D(i)
                    pl2_2D=pl2.project_2D(i)
                    x=pl1_2D.intersection(pl2_2D)
                    result.extend([y.project_3D(plane,i) for y in x])
                    
        return tuple(result)
                


    def intersection(self,obj):
        """The geometric intersection between self and obj.
        
        :param obj: A geometric object.
        
        :returns: A tuple of the difference objects.
        :rtype: tuple
        
        .. rubric:: Code Examples
        
        .. code-block:: python
        
            >>> from crossproduct import Point, Polygon
        
        """
        if self.nD==2:
            if isinstance(obj,_BaseShapelyObject):
                return _BaseShapelyObject.intersection(self,obj)
            else:
                raise Exception('%s' % obj.__class__)  # not implemented yet
        
        elif self.nD==3:
            
            if isinstance(obj,Point):
                return self._intersection_point_3D(obj)
            elif isinstance(obj,Polyline):
                return self._intersection_polyline_3D(obj)
            else:
                raise Exception('%s' % obj.__class__)  # not implemented yet
            
            
    @property
    def lines(self):
        """Returns the lines for the polyline segments.
        
        :return: A set of lines with the same start point (P0) and vector (P1-P0) as the segment.
        :rtype: tuple
        
        .. rubric:: Code Example
    
        .. code-block:: python
          
        """
        pls=self.polylines
        return tuple(Line(pl[0],pl[1]-pl[0]) for pl in pls)


    

    @property
    def polylines(self):
        """Returns a Polylines of the individual line segments
        """
        n=len(self)
        return Polylines(*[Polyline(self[i],self[i+1]) for i in range(n-1)])


    @property
    def reverse(self):
        """Return a polyline with the points reversed.
        
        :rtype: Polyline
        
        .. rubric:: Code Example
    
        .. code-block:: python
        
           >>> from crossproduct import Point,Polyline
           >>> pl = Polyline(Point(0,0), Point(1,0), Point(1,1))
           >>> result = pl.reverse
           >>> print(result)
           Polyline(Point(1.0,1.0),Point(1.0,0.0),Point(0.0,0.0))
        
        """
        return Polyline(*self[::-1])



class Polylines(_BaseGeometricObject,_BaseSequence,_BaseShapelyObject):
    """A sequence of polylines.    
    
    In *crossproduct* a Polylines object is a mutable sequence. 
    Iterating over a Polylines object will provide its Polyline instances.
    Index, append, insert and delete actions are available.
    
    :param polylines: An argument list of Polyline instances. 
    
    """
    
    def __init__(self,*polylines):
        ""
        self._items=tuple(polylines)
    
    @property
    def _shapely(self):
        ""
        if len(self)==0 or self.nD==2:
            x=[pl._shapely for pl in self]
            return shapely.geometry.MultiLineString(x)
        else:
            raise Exception  # only 2d for shapely objects


class Plane(_BaseGeometricObject):
    """A three dimensional plane, situated on an x, y, z plane.
    
    Equation of plane: N . (P - P0) = 0 where:
        
        - N is a normal 3D vector to the plane
        - P is any point on the plane
        - P0 is the start point of the plane
    
    :param P0: A 3D point on the plane.
    :type P0: Point
    :param N: A 3D vector which is normal to the plane.
    :type N: Vector
    
    .. rubric:: Code Example
    
    .. code-block:: python
       
       >>> from crossproduct import Point, Vector, Plane
       >>> pn = Plane(Point(0,0,0), Vector(0,0,1))
       >>> print(pn)
       Plane(Point(0.0,0.0,0.0), Vector(0.0,0.0,1.0))

    """    
    
    def __init__(self,P0,N):
        ""
        self._P0=P0
        self._N=N

        
    def __repr__(self):
        ""
        return 'Plane(%s, %s)' % (self.P0,self.N)
    
    
    def contains(self,obj):
        """Tests if the plane contains the object.
        
        :param obj: A 3D geometric object.
        :type obj: Point, Line, Halfline, Segment
            
        :raises TypeError: If obj is of a type that cannot be contained in a plane.
        
        :rtype: bool
        
        .. rubric:: Code Example
    
        .. code-block:: python
           
           >>> from crossproduct import Point, Vector, Plane
           >>> pn = Plane(Point(0,0,0), Vector(0,0,1))
           >>> result = pn.contains(Point(1,1,0))
           >>> print(result)
           True
           
        
        """
        if isinstance(obj,Point):
            return self.N.is_perpendicular(obj-self.P0)
        elif isinstance(obj,Line):
            return self.contains(obj.P0) and self.N.is_perpendicular(obj.vL)
        #elif isinstance(obj,Halfline) or isinstance(obj,Segment):            
        #    return self.contains(obj.P0) and self.N.is_perpendicular(obj.line.vL)
        else:
            raise TypeError
    
    def coordinates(self):
        """Returns a tuple representation of the plane.
        
        :returns: The point and vector of the plane as tuples. 
        :rtype: tuple
        
        .. rubric:: Code Example
    
        .. code-block:: python
           
           >>> from crossproduct import Point, Vector, Plane
           >>> pn = Plane(Point(0,0,0), Vector(0,0,1))
           >>> result = pl.coordinates()
           >>> print(result)
           ((0.0,0.0,0.0), (0.0,0.0,1.0))
        
        """
        return tuple(self.P0), tuple(self.N)
         
    
    def _intersect_line(self,line):
        """Returns the intersection of this plane and a line.
        
        :param line: A 3D line. 
        :type line: Line
        
        :return: Returns None for parallel, non-collinear plane and line.
            Returns a line for a line on the plane.
            Returns a point for a skew line which intersects the plane.
        :rtype: None, Point, Line     
        
        .. rubric:: Code Example
    
        .. code-block:: python
           
           >>> from crossproduct import Point, Vector, Line, Plane
           >>> pn = Plane(Point(0,0,0), Vector(0,0,1))
           >>> result = pn.intersect_line(Line(Point(5,5,0),Vector(1,1,1)))
           >>> print(result)
           Point(5.0,5.0,0.0)
        
        """
        if self.contains(line): # plane and line are collinear
            return (line,)
        elif self.N.is_perpendicular(line.vL): # plane and line are parallel 
            return tuple()
        else:
            return self._intersect_line_skew(line)
    
    
    def _intersect_line_skew(self,skew_line):
        """Returns the intersection of this plane and a skew line.
        
        :param skew_line: A 3D line which is skew to the plane.
        :type skew_line: Line
        
        :return: The intersection point.
        :rtype: Point
        
        """
        n=self.N
        u=skew_line.vL
        w=skew_line.P0-self.P0
        t=-n.dot(w) / n.dot(u)
        return (skew_line.calculate_point(t),)
       
    
    def _intersection_plane(self,plane):
        """Returns the intersection of this plane and another plane.
        
        :param plane: A 3D plane.
        :type plane: Plane
        
        :return: Returns None for parallel, non-coplanar planes.
            Returns a plane for two coplanar planes.
            Returns a line for non-parallel planes.
        :rtype: tuple   
        
        .. rubric:: Code Example
    
        .. code-block:: python
           
           >>> from crossproduct import Point, Vector, Plane
           >>> pn = Plane(Point(0,0,0), Vector(0,0,1))
           >>> result = pn.intersect_plane(Plane(Point(0,0,0), Vector(1,0,0)))
           >>> print(result)
           Line(Point(0.0,0.0,0.0), Vector(0.0,1.0,0.0))
    
        """
        if plane.equals(self):
            return (self,)
        elif plane.N.is_collinear(self.N):
            return tuple()
        else:
            n1=self.N
            d1=-n1.dot(self.P0-Point(0,0,0))
            n2=plane.N
            d2=-n2.dot(plane.P0-Point(0,0,0))
            n3=n1.cross_product(n2)
            P0=Point(0,0,0) + ((n1*d2-n2*d1).cross_product(n3) * (1 / (n3.length**2)))
            u=n3
            return (Line(P0,u),)
    
    
    def equals(self,plane):
        """Tests if this plane and the supplied plane occupy the same geometric space.
        
        :param plane: A 3D plane.
        :type plane: Plane
        
        :return: True if the normal vectors are collinear and 
            a point can exist on both planes;
            otherwise False.
        :rtype: bool
        
        .. rubric:: Code Example
    
        .. code-block:: python
           
           >>> from crossproduct import Point, Vector, Plane
           >>> pn1 = Plane(Point(0,0,0), Vector(0,0,1))
           >>> pn2 = Plane(Point(1,1,0), Vector(0,0,-1))
           >>> result = pn1.equals(pn2)
           >>> print(result)
           True
            
        """
        if isinstance(plane,Plane):
            return self.N.is_collinear(plane.N) and self.contains(plane.P0)
        else:
            return False
    
    
    def intersection(self,obj):
        """
        """
        if isinstance(obj,Plane):
            return self._intersection_plane(obj)
        elif isinstance(obj,Line):
            return self._intersect_line(obj)
        else:
            raise Exception  # not implemented yet
    

    @property
    def N(self):
        """The vector normal to the plane.
        
        :rtype: Vector
        
        .. rubric:: Code Example
    
        .. code-block:: python
           
           >>> from crossproduct import Point, Vector, Plane
           >>> pn = Plane(Point(0,0,0), Vector(0,0,1))
           >>> print(pn.N)
           Vector(0.0,0.0,1.0)
        
        """
        return self._N
    

    @property
    def nD(self):
        """The number of dimensions of the plane.
        
        :returns: 2 or 3
        :rtype: int
        
        .. rubric:: Code Example
    
        .. code-block:: python
           
           >>> from crossproduct import Point, Vector, Plane
           >>> pn = Plane(Point(0,0,0), Vector(0,0,1))
           >>> print(pn.nD)
           3
        
        """
        return self.P0.nD


    @property
    def P0(self):
        """The start point of the plane.
        
        :rtype: Point
        
        .. rubric:: Code Example
    
        .. code-block:: python
           
           >>> from crossproduct import Point, Vector, Plane
           >>> pn = Plane(Point(0,0,0), Vector(0,0,1))
           >>> print(pn.P0)
           Point(0.0,0.0,0.0)
        
        """
        return self._P0


    def point_xy(self,x,y):
        """Returns a 3D point on the plane given as x and y coordinates.
        
        :param x: An x-coordinate.
        :type x: float
        :param y: A y-coordinate.
        :type y: float
        
        :raises ValueError: If there are no points on the plane with the xy values.
        
        :rtype: Point
        
        .. rubric:: Code Example
    
        .. code-block:: python
           
           >>> from crossproduct import Point, Vector, Plane
           >>> pn = Plane(Point(0,0,0), Vector(1,1,1))
           >>> result = pn.point_xy(1,1)
           >>> print(result)
           Point(1.0,1.0,-2.0)
        
        """
        try:
            z=self.P0.z-(self.N.x*(x-self.P0.x)+self.N.y*(y-self.P0.y))/self.N.z
        except ZeroDivisionError:
            raise ValueError('xy points (%s,%s) must exist on the plane.' % (x,y))
        return Point(x,y,z)
    
    
    def point_yz(self,y,z):
        """Returns a 3D point on the plane given as y and z coordinates.
        
        :param y: A y-coordinate.
        :type y: float
        :param z: A z-coordinate.
        :type z: float
        
        :raises ValueError: If there are no points on the plane with the yz values.
        
        :rtype: Point
        
        .. code-block:: python
           
           >>> from crossproduct import Point, Vector, Plane
           >>> pn = Plane(Point(0,0,0), Vector(1,1,1))
           >>> result = pn.point_yz(1,1)
           >>> print(result)
           Point(-2.0,1.0,1.0)
        
        """
        try:
            x=self.P0.x-(self.N.y*(y-self.P0.y)+self.N.z*(z-self.P0.z))/self.N.x
        except ZeroDivisionError:
            raise ValueError('yz points (%s,%s) must exist on the plane.' % (y,z))
        return Point(x,y,z)
    
    
    def point_zx(self,z,x):
        """Returns a 3D point on the plane given as z and x coordinates.
        
        :param z: A z-coordinate.
        :type z: float
        :param x: An x-coordinate.
        :type x: float
        
        :raises ValueError: If there are no points on the plane with the zx values.
        
        :rtype: Point
        
        .. rubric:: Code Example
    
        .. code-block:: python
           
           >>> from crossproduct import Point, Vector, Plane
           >>> pn = Plane(Point(0,0,0), Vector(1,1,1))
           >>> result = pn.point_zx(1,1)
           >>> print(result)
           Point(1.0,-2.0,1.0)
        
        """
        try:
            y=self.P0.y-(self.N.z*(z-self.P0.z)+self.N.x*(x-self.P0.x))/self.N.y
        except ZeroDivisionError:
            raise ValueError('zx points (%s,%s) must exist on the plane.' % (z,x))
        return Point(x,y,z)
    

    def signed_distance_to_point(self,point):
        """Returns the signed distance to the supplied point.
        
        :param point: A 3D point.
        :type point:  Point
        
        :return: The signed distance between the plane and the point.
            The return value is positive for one side of the plane 
            (the side in the direction of the normal) and is negative for
            the other side.
        :rtype: float
        
        .. rubric:: Code Example
    
        .. code-block:: python
           
           >>> from crossproduct import Point, Vector, Line, Plane
           >>> pn = Plane(Point(0,0,0), Vector(0,0,1))
           >>> result = pn.signed_distance_to_point(Point(1,1,-1))
           >>> print(result)
           -1.0
           
        """
        return self.N.dot(point-self.P0) / self.N.length


    

class Polygon(_BaseGeometricObject,_BaseShapelyObject):
    """A polygon, situated on an xy or xyz plane. 
    
    This polygon cannot be self-intersecting, and can be concave or convex.
    
    :param points: Argument list of the Point instances of the vertices 
        of the polygon, in order. The first point is not repeated at the end. 
    :param holes: A sequence of polygons representing holes in the polygon.
    
    .. rubric:: Code Example

    .. code-block:: python
       
       >>> pg = Polygon(Point(0,0), Point(1,0), Point(1,1))
       >>> print(pg)
       Polygon(Point(0,0), Point(1,0), Point(1,1))
    
    """

    def __eq__(self,polygon):
        """Tests if this polygon and the supplied polygon are equal.
        
        :param polygon: A polygon.
        :type polygon: Polygon
        
        :return: True if the two polygons have the same points in the same order, 
            both for the exterior and any holes
            otherwise False.
        :rtype: bool
        
        .. rubric:: Code Example

        .. code-block:: python
           
            # 2D example
            >>> pg1 = Polygon(Point(0,0), Point(1,0), Point(1,1))
            >>> pg2 = Polygon(Point(0,0), Point(1,0), Point(1,1))
            >>> print(pl1 == pl2)
            True
            
        """
        if isinstance(polygon,Polygon):
            
            if self.exterior.coordinates==polygon.exterior.coordinates:
                
                if self.holes.coordinates==polygon.holes.coordinates:
                    return True
                else:
                    return False
                
            else:
                return False
            
        else:
            return False
        

    def __init__(self,*points,holes=None):
        ""
        
        self._points=Points(*points)
        if holes is None:
            self._holes=Polygons()
        else:
            self._holes=Polygons(*holes)
        
        
    def __repr__(self):
        ""
        return '%s(%s%s)' % (self.__class__.__name__,
                                     ','.join([str(c) for c in self.points]),
                                     ', holes=%s' % self.holes if len(self.holes)>0 else ''
                                     )
        
    
    @property
    def _shapely(self):
        """
        
        :rtype: shapely.geometry.MultiPolygon
        
        """
        if self.nD==2:
            x=[shapely.geometry.Polygon(pg.coordinates[0]) for pg in self.polygons]
            return shapely.geometry.MultiPolygon(x)
        else:
            raise Exception  # only 2d for shapely polygons


    @property
    def area(self):
        """The area of the polygon.
        
        :rtype: float
        
        """
        if self.nD==2:
            return float(self._shapely.area)
        elif self.nD==3:
            plane=self.plane
            i=plane.N.index_largest_absolute_coordinate
            self_2D=self.project_2D(i)
            if i==0:
                return self_2D.signed_area*(plane.N.length/(N.x))
            elif i==1:
                return self_2D.signed_area*(plane.N.length/(N.y))
            elif i==2:
                return self_2D.signed_area*(plane.N.length/(N.z))
            else:
                raise Exception
        else:
            raise ValueError


    @property
    def centroid(self):
        """The centroid of the polygon.
        
        :rtype: Point
        
        """
        if self.nD==2:
            return self._shapely_point_to_point(self._shapely.centroid)
        elif self.nD==3:
            plane=self.plane
            i=plane.N.index_largest_absolute_coordinate
            self_2D=self.project_2D(i)
            return self_2D.centroid.project_3D(plane,i)
        else:
            raise ValueError
        

    @property
    def coordinates(self):
        """Returns a tuple representation of the polygon.
        
        :returns: The exterior and holes coordinates as a tuple. 
            
        :rtype: tuple
        
        .. code-block:: python
        
            >>> from crossproduct import Point, Polygon
            >>> pg=Polygon(Point(0,0),Point(1,0),Point(1,1),Point(0,1))
            >>> result = pg.coordinates()
            >>> print(result)
            (((0, 0), (1, 0), (1, 1), (0, 1)), ())
        
        """
        return (tuple(pt.coordinates for pt in self.points),
                tuple(tuple(pt.coordinates for pt in hole.points) 
                      for hole in self.holes))


    def _difference_polygon_3D(self,polygon):
        ""
        a=self.plane.intersection(polygon.plane) # returns () or (Line,) or (Plane,)
        #print(a)
        
        if len(a)==0: # polygon planes do not intersect
            return tuple([self])
        
        elif isinstance(a[0],Line): # the intersection of the two polygon planes as a line
            return tuple([self])

        elif isinstance(a[0],Plane): # polygons lie on the same plane
            
            plane=self.plane
            i=plane.N.index_largest_absolute_coordinate
            self_2D=self.project_2D(i)
            polygon_2D=polygon.project_2D(i)
            result=self_2D.difference(polygon_2D)
            return tuple(x.project_3D(plane,i) for x in result)
           
        
    def _difference_polygons_3D(self,polygons):
        ""
        result=set()
        for pg in polygons:
            x=self.difference(pg)
            result.update(x)
        return tuple(result)
        

    def difference(self,obj):
        """The geometric difference between self and obj.
        
        :param obj: A geometric object.
        
        :returns: A tuple of the difference objects.
        :rtype: tuple
        
        """
        # to do ... 3D difference
        if self.nD==2:
            if isinstance(obj,_BaseShapelyObject):
                return _BaseShapelyObject.difference(self,obj)
            else:
                raise Exception('%s' % obj.__class__)
        
        elif self.nD==3:
            
            if isinstance(obj,Point):
                return tuple([self])
            elif isinstance(obj,Points):
                return tuple([self])
            elif isinstance(obj,Polyline):
                return tuple([self])
            elif isinstance(obj,Polylines):
                return tuple([self])
            elif isinstance(obj,Polygon):
                return self._difference_polygon_3D(obj)
            elif isinstance(obj,Polygons):
                return self._difference_polygons_3D(obj)
            else:
                raise Exception  # not implemented yet
            
        else:
            raise ValueError
        
    
    @property
    def exterior(self):
        ""
        return Polygon(*self.points)
    

    @property
    def holes(self):
        ""
        return self._holes
    
    
    def _intersection_line_2D(self,line):
        ""
        minx, miny, maxx, maxy = self.exterior._shapely.bounds
        t0=line.calculate_t_from_coordinates(minx,miny)
        t1=line.calculate_t_from_coordinates(maxx,maxy)
        pt0=line.calculate_point(t0)
        pt1=line.calculate_point(t1)
        pl=Polyline(pt0,pt1)
        return self.intersection(pl)
    
    
    def _intersection_line_3D(self,line):
        ""
        a=self.plane.intersection(line) # returns () or (Point,) or (Line,)
        #print(a)
        if len(a)==0: # polygon planes do not intersect
            return tuple()
        
        elif isinstance(a[0],Point):
            return self.intersection(a[0])
        
        elif isinstance(a[0],Line):  # line is on the same plane as polygon
            
            i=self.plane.N.index_largest_absolute_coordinate
            self_2D=self.project_2D(i)
            line_2D=line.project_2D(i)
            result=self_2D.intersection(line_2D)
            return tuple(x.project_3D(self.plane,i) for x in result)
        
        else:
            raise Exception
        
    
    def _intersection_polygon_3D(self,polygon):
        ""
        a=self.plane.intersection(polygon.plane) # returns () or (Line,) or (Plane,)
        #print(a)
        if len(a)==0: # polygon planes do not intersect
            return tuple()
        
        elif isinstance(a[0],Plane): # polygons lie on the same plane
            
            i=self.plane.N.index_largest_absolute_coordinate
            self_2D=self.project_2D(i)
            polygon_2D=polygon.project_2D(i)
            result=self_2D.intersection(polygon_2D)
            return tuple(x.project_3D(self.plane,i) for x in result)
            
        elif isinstance(a[0],Line): # the intersection of the two polygon planes as a line
            
            line=a[0]
            x=self.intersection(line)
            y=polygon.intersection(line)
            
            result=[]
            for x1 in x:
                for y1 in y:
                    result.extend(x1.intersection(y1))
            
            return tuple(result)
            
        
    def _intersection_polygons_3D(self,polygons):
        ""
        result=set()
        for pg in polygons:
            x=self.intersection(pg)
            result.update(x)
        return tuple(result)
        
    
    def intersection(self,obj):
        """The geometric intersection between self and obj.
        
        :param obj: A geometric object.
        
        :returns: A tuple of the difference objects.
        :rtype: tuple
        
        .. rubric:: Code Examples
        
        .. code-block:: python
        
            >>> from crossproduct import Point, Polygon
        
        """
        if self.nD==2:
            if isinstance(obj,_BaseShapelyObject):
                return _BaseShapelyObject.intersection(self,obj)
            elif isinstance(obj,Line):
                return self._intersection_line_2D(obj)
            else:
                raise Exception('%s' % obj.__class__)
        
        elif self.nD==3:
            
            if isinstance(obj,Line):
                return self._intersection_line_3D(obj)
            elif isinstance(obj,Polygon):
                return self._intersection_polygon_3D(obj)
            elif isinstance(obj,Polygons):
                return self._intersection_polygons_3D(obj)
            else:
                raise Exception  # not implemented yet
            
        else:
            raise ValueError
            
            
    @property
    def nD(self):
        """The number of dimensions of the polygon.
        
        :returns: 2 or 3
        :rtype: int
        
        .. rubric:: Code Examples
    
        .. code-block:: python
        
            >>> from crossproduct import Point, Points
            >>> pts = Points(Point(1,1))
            >>> print(pts.nD)
            2
            
        """
        return self.points[0].nD
            
    
    def next_index(self,i):
        """Returns the next point index in the polygon.
        
        :param i: A point index.
        :type i: int
        
        :return: Returns the index of the next point in the polygon. 
            If i is the index of the last point, then the index of 
            the first point (i.e. 0) is returned.
        :rtype: int
        
        :Example:
    
        .. code-block:: python
           
            >>> pg = Polygon2D(Point2D(0,0), Point2D(1,0), Point2D(1,1))
            >>> result = pg.next_index(0)
            >>> print(result)
            1
        
        """
        n=len(self.points)
        if i==n-1:
            return 0
        else:
            return i+1
    
    
    
            
    @property
    def plane(self):
        """Returns the plane of the 3D polygon
        
        :return plane: a 3D plane which contains all the polygon points
        :rtype: Plane3D
        
        """
        if self.nD==3:
            P0,P1,P2=self.points[:3]
            N=(P1-P0).cross_product(P2-P1)
            return Plane(P0,N)
        else:
            raise ValueError
            
    
    @property
    def points(self):
        """Returns the exterior points.
        """
        return self._points
            
            
    @property
    def polylines(self):
        """Returns polylines of the polygon exterior and the polygon holes.
        
        :return: A polyline of the polygon points which starts and ends at 
            the first polygon point.
            tuple (exterior polyline, hole polylines)
        :rtype: tuple     
        
        :Example:
    
        .. code-block:: python
           
            
        """
        return (Polyline(*(list(self.points) + [self.points[0]])), 
                Polylines(*(Polyline(*(list(hole.points) + [hole.points[0]])) 
                            for hole in self.holes))
                )


    @property
    def polygons(self):
        """An equivalent polygons collection representing the polygon and its holes.
        
        Each polygon does not have any holes.
        
        :rtype: Polygons
        """
        
        if self.nD==2:
        
            if len(self.holes)==0:
                return Polygons(self)
            else:
                return self.triangles
                
        elif self.nD==3:
            
            plane=self.plane
            i=plane.N.index_largest_absolute_coordinate
            self_2D=self.project_2D(i)
            result=self_2D.polygons
            return Polygons(*(x.project_3D(plane,i) for x in result))
            
        else:
            
            raise ValueError
            
            
    def _project_2D_exterior(self,coordinate_index):
        ""
        return Polygon(*(x.project_2D(coordinate_index) 
                         for x in self.points))
            
            
    def project_2D(self,coordinate_index):
        """Projects the object on a 2D plane.
        
        """
        return Polygon(*self._project_2D_exterior(coordinate_index).points,
                       holes=[hole._project_2D_exterior(coordinate_index)
                              for hole in self.holes])
    
    
    def _project_3D_exterior(self,plane,coordinate_index):
        ""
        return Polygon(*(x.project_3D(plane,coordinate_index) 
                         for x in self.points))
    
    
    def project_3D(self,plane,coordinate_index):
        """Projects the object on a 3D plane.
        
        """
        return Polygon(*self._project_3D_exterior(plane,coordinate_index).points,
                       holes=[hole._project_3D_exterior(plane,coordinate_index)
                              for hole in self.holes])
            
    
    @property
    def reverse(self):
        """Returns a polygon with the exterior points reversed.
        
        :return: A new polygon with the points in reverse order.
        :rtype: Polygon
        
        .. rubric:: Code Example
    
        .. code-block:: python
           
            # 2D example
            >>> pg = Polygon(Point(0,0), Point(1,0), Point(1,1))
            >>> print(pg.reverse)
            Polygon(Point(1,1), Point(1,0), Point(0,0))
        
            # 3D example
            >>> pg = Polygon(Point(0,0,0), Point(1,0,0), Point(1,1,0))
            >>> print(pg.reverse)
            Polygon(Point(1,1,0), Point(1,0,0), Point(0,0,0))
        
        """
        points=[self.points[i] 
                for i in range(len(self.points)-1,-1,-1)]
        return self.__class__(*points, holes=self.holes)
            
    
    @property
    def triangles(self):
        """Returns a Polygons sequence of triangles which when combined have 
            the same shape as the polygon.
            
        Triangles have no holes.
        
        2d only
        
        :rtype: Polygons
        
        
        """
        if self.nD==2:
            
            if len(self.holes)==0:
                
                vertices=self.coordinates[0]
                segments=np.array([(x,x+1) for x in range(len(self.points))])
                segments[-1][1]=0
                A=dict(vertices=vertices,
                       segments=segments)
                B=tr.triangulate(A,'p')
                tris=[]
                if 'triangles' in B:
                    for x in B['triangles']:
                        tri=Polygon(*(Point(*vertices[y]) for y in x))
                        tris.append(tri)
                return Polygons(*tris)
            
            else:
                
                # exterior vertices and segments
                vertices=list(self.coordinates[0])
                segments=[[x,x+1] for x in range(len(self.points))]
                segments[-1][1]=0
                holes=[]
                # holes vertices and segments
                for hole in self.holes:
                    vertices.extend(hole.coordinates[0])
                    n=len(segments)
                    segments.extend(np.array([(x,x+1) for x in range(n,n+len(self.points))]))
                    segments[-1][1]=n
                    holes.append(hole.exterior.triangles[0].centroid.coordinates)
                # get triangles
                A=dict(vertices=vertices,
                       segments=segments,
                       holes=holes)
                B=tr.triangulate(A,'p')
                tris=[]
                if 'triangles' in B:
                    for x in B['triangles']:
                        tri=Polygon(*(Point(*vertices[y]) for y in x))
                        tris.append(tri)
                return Polygons(*tris)  #  each polygon is a triangle with no holes
            
        elif self.nD==3:
            
            plane=self.plane
            i=plane.N.index_largest_absolute_coordinate
            self_2D=self.project_2D(i)
            result=self_2D.triangles
            return Polygons(*(x.project_3D(plane,i) for x in result))
           
        else:
            
            raise ValueError
            
    

class Polygons(_BaseGeometricObject,_BaseSequence,_BaseShapelyObject):
    """A sequence of polygons.    
    
    :param polygons: A sequence of Polygon instances. 
        
    .. rubric:: Code Example
    
    .. code-block:: python
        
        >>> pgs = Polygons(Polygon(Point(0,0), Point(1,0), Point(1,1)))                       
        >>> print(pgs)
        Polygons(Polygon(Point(0,0), Point(1,0), Point(1,1)))
        
        >>> print(pgs[0])
        Polygon(Point(0,0), Point(1,0), Point(1,1))
    """
    
    def __init__(self,*polygons):
        ""
        self._items=tuple(polygons)
    
    @property
    def _shapely(self):
        ""
        if len(self)==0 or self.nD==2:
            x=[shapely.geometry.Polygon(pg1.coordinates[0]) 
               for pg in self
               for pg1 in pg.polygons]
            return shapely.geometry.MultiPolygon(x)
        else:
            raise Exception  # only 2d for shapely polygons


class Tetrahedron(_BaseGeometricObject,_BaseSequence):
    """A tetrahedron, situated on the xyz plane. 
    
    :param polygons: A sequence of polygons for the outer faces.
        All polygons should not have any holes. 
        All polygons must have outward facing normals.
    :type polygons: Polygons or other sequence.
    
    """
    
    def __init__(self,*polygons):
        ""
        self._items=Polygons(*polygons)
        
        
    @property
    def polygons(self):
        ""
        return self._items
        
        
def tetrahedron_from_points(P0,P1,P2,P3):
    """Forms a tetrahedron from the specified points.
    
    :returns: A tetrahedron 
    :rtype: Tetrahedron
    
    """
    pts=Points(P0,P1,P2,P3)
    pgs=Polygons(*(Polygon(*x) for x in itertools.combinations(pts,3)))
    centroid=pts.centroid
    
    # makes sure all polygon plane normals are outward facing
    result=[]
    for pg in pgs:
        plane=pg.plane
        if plane.signed_distance_to_point(centroid)>0:
            result.append(pg.reverse)
        else:
            result.append(pg)
        
    return Tetrahedron(*result)
    

def tetrahedrons_from_extruded_triangle(triangle, extrud_vector):
    """
    Returns the internal tetrahedrons for an extruded triangle.
    
    """
    
    th0=tetrahedron_from_points(*triangle.points,
                                triangle.points[0]+extrud_vector)
    th1=tetrahedron_from_points(triangle.points[1],
                                triangle.points[2],
                                triangle.points[0]+extrud_vector,
                                triangle.points[1]+extrud_vector)
    th2=tetrahedron_from_points(triangle.points[0]+extrud_vector,
                                triangle.points[1]+extrud_vector,
                                triangle.points[2]+extrud_vector,
                                triangle.points[2])
    return [th0,th1,th2]
    
    
    
    
    
    
class ExtrudedPolyhedron(_BaseGeometricObject,_BaseSequence):
    """
    """
    
    def __init__(self,base_polygon,extrud_vector):
        ""
        self._base_polygon=base_polygon
        self._extrud_vector=extrud_vector
        self._items=None
        self._tetrahedrons=None
        
        # _items
        if base_polygon.plane.N.dot(extrud_vector)>0:  # if angle is less than 90
            base_polygon=base_polygon.reverse
        top_polygon=Polygon(*(pt+extrud_vector for pt in base_polygon.reverse.points))
        side_polygons=[]
        for i in range(len(base_polygon.points)):
            pg=Polygon(base_polygon.points[i]+extrud_vector,
                       base_polygon.points[base_polygon.next_index(i)]+extrud_vector,
                       base_polygon.points[base_polygon.next_index(i)],
                       base_polygon.points[i])
            side_polygons.append(pg)
        self._items=Polygons(base_polygon, top_polygon, *side_polygons)
        
        # _tetrahedrons
        result=[]
        for triangle in base_polygon.triangles:
            result.extend(tetrahedrons_from_extruded_triangle(triangle, extrud_vector))
        self._tetrahedrons=result
        
        
    @property
    def base_polygon(self):
        ""
        return self._base_polygon
    
    
    def extrud_vector(self):
        ""
        return self._extrud_vector
        
        
    @property
    def polygons(self):
        ""
        return self._items
    
    
    @property
    def tetrahedrons(self):
        ""
        return self._tetrahedrons

    
    
    
    
    