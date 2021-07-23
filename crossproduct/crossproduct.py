# -*- coding: utf-8 -*-

# general
import collections.abc
import itertools
import math

# for plotting
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# for external geometric calculations
import shapely.geometry
import shapely.ops
import triangle as tr

# for rendering
import vpython


ABS_TOL = 1e-7 # default value for math.isclose


class SequenceObject(collections.abc.Sequence):
    """
    """
    def __getitem__(self,index):
        ""
        if isinstance(index, slice):
            indices = range(*index.indices(len(self._items)))
            return self.__class__(*[self._items[i] for i in indices])
        else:
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
                           ', '.join([str(c) for c in self]))
    

class GeometricEntity():
    """
    
    Includes all
    
    """
    
    def __eq__(self,obj):
        """Test for equality between objects.
        
        :param obj: A geometric object.
        
        :returns: True if the two objects are of the same class and have the 
            same coordinates;
            otherwise False.
        :rtype: bool
        
        """
        if isinstance(obj,self.__class__):
            return self.coordinates==obj.coordinates
        else:
            return False
        
    

class GeometricObject(GeometricEntity):
    """
    
    All except for Vector
    
    """
    @property
    def coordinates(self):
        """Returns a tuple representation of the object.
        
        :returns: The coordinates as a tuple. 
        :rtype: tuple
    
        """
        return tuple(x.coordinates for x in self)
    
    
    def difference(self,obj):
        """The geometric difference between self and obj.
        
        :param obj: A geometric object.
        
        :returns: The difference objects.
        :rtype: GeometryObjects
        
        """
        
        if self.nD==2:
            
            a=self._shapely
            b=obj._shapely
            result=a.difference(b)
            #print(result)
            return GeometryObjects(*self._shapely_to_objs(result))
            
        elif self.nD==3:
            
            raise Exception  # shapely doesn't work for 3d
            
        else:
            
            raise ValueError
    
            
    def intersection(self,obj):
        """The geometric intersection between self and obj.
        
        :param obj: A geometric object.
        
        :returns: The intersection objects.
        :rtype: GeometryObjects
        
        """
        if self.nD==2:
            
            a=self._shapely
            b=obj._shapely
            result=a.intersection(b)
            return GeometryObjects(*self._shapely_to_objs(result))
                
        elif self.nD==3:
            
            raise Exception  # shapely doesn't work for 3d
            
        else:
            
            raise ValueError
            
            
    def intersects(self,obj):
        """Returns True if self and obj intersect in any way
        
        :param obj: A geometric object.
        
        :rtype: bool
        
        """
        if self.nD==2:
            
            a=self._shapely
            b=obj._shapely
            return a.intersects(b)
                
        elif self.nD==3:
            
            raise Exception  # shapely doesn't work for 3d
            
        else:
            
            raise ValueError
            
            
    def split(self,obj):
        """The geometric split between self and obj.
        
        :param obj: A geometric object.
        
        :returns: The split objects.
        :rtype: GeometryObjects
        
        """
        if self.nD==2:
            
            a=self._shapely
            b=obj._shapely
            result=shapely.ops.split(a,b)
            return GeometryObjects(*self._shapely_to_objs(result))
                
        elif self.nD==3:
            
            raise Exception  # shapely doesn't work for 3d
            
        else:
            
            raise ValueError
    
    
    @property
    def nD(self):
        """The number of dimensions of the object.
        
        :returns: 2 or 3
        :rtype: int
        
        """
        return self[0].nD
    
    
    
class FiniteGeometricObject(GeometricObject, SequenceObject):
    """
    
    Point, Points, Polyline, Polylines, Polygon, Polygons,
    Tetrahedron, ExtrudedPolyhedron
    
    """
    
    
    
    @property
    def _vpython_vector(self):
        ""
        return [x._vpython_vector for x in self]

    
    
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
    def bounds(self):
        """
        """
        if self.nD==2:
            return self._shapely.bounds
        elif self.nD==3:
            result=[]
            a=list(zip(*self.points.coordinates))
            result.extend([min(b) for b in a])
            result.extend([max(b) for b in a])
            return tuple(result)
        else:
            raise ValueError
            
    
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
        
    
    def project_2D(self,coordinate_index):
        """Projects the object on a 2D plane.
        
        
        """
        return self.__class__(*(x.project_2D(coordinate_index) for x in self))
    
    
    def project_3D(self,plane,coordinate_index):
        """Projects the object on a 2D plane.
        
        
        """
        return self.__class__(*(x.project_3D(plane,coordinate_index) 
                                for x in self))
        

    
class InfiniteGeometricObject(GeometricObject):
    """
    
    Line, Plane
    
    """

    
class GeometryObjects(GeometricObject, SequenceObject):
    """
    
    A collection of geometric objects (i.e. all but vectors)
    
    """
    

 

class Point(FiniteGeometricObject):
    """A point, as described by xy or xyz coordinates.
    
    In *crossproduct* a `Point` object is a immutable sequence. 
    Iterating over a `Point` will provide its coordinates.
    Indexing a `Point` will return the coordinate for that index (0=x, 1=y, 2=z).
    
    :param coordinates: Argument list of two (xy) or three (xyz) coordinates. 
        Coordinates should be of type int, float or similar numeric. These values
        are converted to floats.

    """
    
    def __add__(self,vector):
        """The addition of this point and a vector.
        
        :param vector: The vector to be added to the point.
        :type vector: Vector
        
        :rtype: Point
        
        """
        zipped=itertools.zip_longest(self,vector) # missing values filled with None
        try:
            coordinates=[a+b for a,b in zipped]
        except TypeError: # occurs if, say, a or b is None
            raise ValueError('Point and vector to add must be of the same length.')
        return Point(*coordinates)
    
    
    def __init__(self,*coordinates):
        ""
        self._items=tuple(map(float,coordinates))
        
        
    def __sub__(self,point_or_vector):
        """Subtraction of supplied object from this point.
        
        :param point_or_vector: Either a point or a vector.
        :type point_or_vector: Point or Vector
        
        :return: If a point is supplied, then a vector is returned (i.e. v=P1-P0). 
            If a vector is supplied, then a point is returned (i.e. P1=P0-v).
        :rtype: Point or Vector
        
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
    def centroid(self):
        """The centroid of the point (i.e. self).
        
        :rtype: Point
        
        """
        return self
    
    
    @property       
    def coordinates(self):
        """Returns a tuple representation of the point.
        
        :returns: The coordinates as a tuple. 
            For a point, this can also be achieved by creating a 
            tuple of the point itself (i.e. :code:`tuple(pt)`).
        :rtype: tuple
        
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
            
        """
        return len(self)
    
    
    def plot(self, ax=None, **kwargs):
        """Plots the point on the supplied axes.
        
        :param ax: An 2D or 3D Axes instance.
        :type ax:  matplotlib.axes._subplots.AxesSubplot, matplotlib.axes._subplots.Axes3DSubplot
        :param kwargs: keyword arguments to be passed to the Axes.plot call.
                   
        :returns: The matplotlib axes.
        :rtype: matplotlib.axes._subplots.AxesSubplot or 
        matplotlib.axes._subplots.Axes3DSubplot
    
        """
        if ax is None:
            fig,ax=get_matplotlib_fig_ax(self.nD)
        
        if not 'marker' in kwargs:
            kwargs['marker']='o'
        
        x=[[c] for c in self]
        ax.plot(*x, **kwargs)
        return ax
    
    
    def project_2D(self,coordinate_index):
        """Projection of a 3D point as a 2D point.
        
        :param coordinate_index: The index of the coordinate to ignore.
            Use coordinate_index=0 to ignore the x-coordinate, coordinate_index=1 
            for the y-coordinate and coordinate_index=2 for the z-coordinate.
        :type coordinate_index: int
        
        :raises ValueError: If coordinate_index is not between 0 and 2.
        
        :return: A 2D point based on the projection of the 3D point.
        :rtype: Point
               
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
    def _vpython_vector(self):
        ""
        return vpython.vector(*self.coordinates)


    def render(self,
           scene=None,
           radius=5,
           color=vpython.color.red,
           ):
        """Renders the object using vpython.
        
        :param scene: A vpython canvas.
        :type scene: vpython.vpython.canvas
        :param radius: The radius f the point.
        :type radius: float
        :param color: The color of the point.
        :type color: vpython.cyvector.vector

        :returns: The scene
        :rtype: vpython.vpython.canvas
        
        """
        
        if scene is None:
            scene=get_render_scene()
        
        vpython.points(pos=[self._vpython_vector],
                       color=color,
                       radius=radius)
        
        return scene




    @property
    def x(self):
        """The x coordinate of the point.
        
        :rtype: float
        
        """
        return self[0]
    
    
    @property
    def y(self):
        """The y coordinate of the point.
        
        :rtype: float
        
        """
        return self[1]
    
    
    @property
    def z(self):
        """The z coordinate of the point.
        
        :raises IndexError: If point is a 2D point.
        
        :rtype: float
        
        """
        return self[2]
    



class Points(FiniteGeometricObject):
    """A collection of points.    
    
    In *crossproduct* a `Points` object is a immutable sequence. 
    Iterating over a `Points` will provide its Point objects.
    
    :param points: An argument list of Point instances. 
    
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
    
            

            
    def plot(self, ax=None, **kwargs):
        """Plots the points on the supplied axes.
        
        :param ax: An 2D or 3D Axes instance.
        :type ax:  matplotlib.axes._subplots.AxesSubplot, matplotlib.axes._subplots.Axes3DSubplot
        :param kwargs: keyword arguments to be passed to the Axes.plot call.
                   
        :returns: The matplotlib axes.
        :rtype: matplotlib.axes._subplots.AxesSubplot or 
        matplotlib.axes._subplots.Axes3DSubplot
    
        """
        if ax is None:
            fig,ax=get_matplotlib_fig_ax(self.nD)
        
        if not 'marker' in kwargs:
            kwargs['marker']='o'
        
        ax.scatter(*zip(*self.coordinates), **kwargs)
        return ax
    
    
    def render(self,
           scene=None,
           radius=5,
           color=vpython.color.red,
           ):
        ""
        
        if scene is None:
            scene=get_render_scene()
        
        vpython.points(pos=self._vpython_vector,
                       color=color,
                       radius=radius)
    
        return scene
            

class Vector(GeometricEntity, SequenceObject):
    """A vector, as described by xy or xyz coordinates.
    
    In *crossproduct* a Vector object is a immutable sequence. 
    Iterating over a Vector will provide its coordinates.
    Indexing a vector will return the coordinate for that index (0=x, 1=y, 2=z).
    
    :param coordinates: Argument list of two (xy) or three (xyz) coordinates. 
        Coordinates should be of type int, float or similar numeric. These values
        are converted to floats.
    
    """

    def __add__(self,vector):
        """Addition of this vector and a supplied vector.
        
        :param vector: A vector.
        :type vector: Vector
        
        :rtype: Vector
        
        """
        zipped=itertools.zip_longest(self,vector) # missing values filled with None
        try:
            coordinates=[a+b for a,b in zipped]
        except TypeError: # occurs if, say, a or b is None
            raise ValueError('Vectors to add must be of the same length.')
        return Vector(*coordinates)
    

    def __init__(self,*coordinates):
        ""
        self._items=tuple(map(float,coordinates))


    def __mul__(self,scalar):
        """Multiplication of this vector and a supplied scalar value.
        
        :param scalar: A numerical scalar value.
        :type scalar: float
        
        :rtype: Vector
        
        """
        return Vector(*(c*scalar for c in self))            
    
    
    def __sub__(self,vector):
        """Subtraction of this vector and a supplied vector.
        
        :param vector: A vector.
        :type vector: Vector
        
        :rtype: Vector
        
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
        
        """
        return math.acos(self.dot(vector)/self.length/vector.length)
    
    
    @property
    def _vpython_vector(self):
        ""
        return vpython.vector(*self.coordinates)

    
    @property
    def coordinates(self):
        """Returns a tuple representation of the vector.
        
        :returns: The coordinates as a tuple. 
            For a vector, this can also be achieved by creating a 
            tuple of the vector itself (i.e. :code:`tuple(v)`).
        :rtype: tuple
        
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
        
        """
        return self.is_collinear(vector) and self.dot(vector)<0
            
    
    def is_perpendicular(self,vector):
        """Test if this vector and the supplied vector are perpendicular.
        
        :param vector: A vector.
        :type vector: Vector
        
        :return: True if the vectors are perpendicular; 
            otherwise False.
        :rtype: bool
        
        """
        return math.isclose(self.dot(vector), 0, abs_tol=ABS_TOL)
        
    
    @property
    def length(self):
        """Returns the length of the vector.
        
        :rtype: float
        
        """
        return sum(c**2 for c in self)**0.5
    
    
    @property
    def nD(self):
        """The number of dimensions of the vector.
        
        :returns: 2 or 3
        :rtype: int
        
        """
        return len(self)
    
    
    @property
    def normalise(self):
        """Returns the normalised vector of this vector.
        
        :returns: A codirectional vector of length 1.
        :rtype: Vector
        
        """
        l=self.length
        return Vector(*(c/l for c in self))
    
    
    @property
    def opposite(self):
        """Returns the opposite vector of this vector
        
        :return: A collinear vector which points in the opposite direction.
        :rtype: Vector
        
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
        
        """
        if self.nD==2:
            return Vector(-self.y,self.x)
        else:
            raise ValueError('"perp_vector" method only applicable for a 2D vector.')


    def render(self,
           scene=None,
           color=vpython.color.blue,
           **kwargs
           ):
        ""
        
        if scene is None:
            scene=get_render_scene()
        
        vpython.arrow(pos=Point(0,0,0)._vpython_vector,
                      axis=self._vpython_vector,
                      color=color,
                      **kwargs
                      )
        
        return scene
    


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
        
        """
        return self.dot(vector1.cross_product(vector2))


    @property
    def x(self):
        """The x coordinate of the vector.
        
        :rtype: float
        
        """
        return self[0]
    
    
    @property
    def y(self):
        """The y coordinate of the vector.
        
        :rtype: float
        
        """
        return self[1]
    
    
    @property
    def z(self):
        """The z coordinate of the vector.
        
        :raises IndexError: If vector is a 2D vector.
        
        :rtype: float
        
        """
        return self[2]
    

class Line(InfiniteGeometricObject):
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
    
    
    def _intersection_line_skew(self,skew_line):
        """Returns the point of intersection of this line and the supplied skew line
        """
        #2D
        if self.nD==2:
            return self._intersection_line_skew_2D(skew_line)
        #3D
        elif self.nD==3:
            return self._intersection_line_skew_3D(skew_line)
        else:
            raise Exception # must be either 2D or 3D

    
    def _intersection_line_skew_2D(self,skew_line):
        """Returns the point of intersection of this line and the supplied skew line
        """
        u=self.vL
        v=skew_line.vL
        w=self.P0-skew_line.P0 
        t=-v.perp_product(w) / v.perp_product(u)
        return GeometryObjects(self.calculate_point(t))
        

    def _intersection_line_skew_3D(self,skew_line):
        """Returns the point of intersection of this line and the supplied (skew) line
        
        - return value can be:
            - None -> no intersection (for skew lines which do not intersect in 3D space)
            - Point -> a point (for skew lines which intersect)
        
        """
        if not self.is_parallel(skew_line):
        
            # find the coordinate to ignore for the projection
            cp=self.vL.cross_product(skew_line.vL)
            absolute_coords=[abs(x) for x in cp] 
            i=absolute_coords.index(max(absolute_coords)) % 3 # the coordinate to ignore for projection
                    
            # project 3D lines to 2D
            self2D=self.project_2D(i)
            skew_line2D=skew_line.project_2D(i)
            
            # find intersection point for 2D lines
            ipt=self2D._intersection_line_skew_2D(skew_line2D)[0]
            
            # find t values for the intersection point on each 2D line
            t1=self2D.calculate_t_from_coordinates(*ipt)
            t2=skew_line2D.calculate_t_from_coordinates(*ipt)
            
            # calculate the 3D intersection points from the t values
            ipt1=self.calculate_point(t1)
            ipt2=skew_line.calculate_point(t2)
            
            if ipt1==ipt2: # test the two 3D intersection points are the same
                return GeometryObjects(ipt1)
            else:
                return GeometryObjects()
        
        else:
            raise ValueError('%s and %s are not skew lines' % (self,skew_line))
    
    
    
    def _intersection_line(self,line):
        """Returns the intersection of this line with the supplied line. 
        
        """
        if self==line: # test for collinear lines
            return GeometryObjects(self)
        elif self.is_parallel(line): # test for parallel lines
            return GeometryObjects()
        else: # a skew line
            return self._intersection_line_skew(line)
        
        
    def intersection(self,obj):
        """The intersection of this line with obj
        
        :rtype: GeometryObjects
        
        """
        if isinstance(obj,Line):
            return self._intersection_line(obj)
        
        
    
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
    
    
    def intersects(self,obj):
        """Tests if the line intersects with the object.
        
        :param obj: A point, halfline or segment.
        :type obj: Point, Halfline, Segment
        
        :raises TypeError: If supplied object is not supported by this method.
            
        :return:  For point, True if the point lies on the line; otherwise False. 
            For halfline, True if the halfline startpoint is on the line and 
            the halfline vector is collinear to the line vector; otherwise False. 
            For segment, True if the segment start and endpoints are on the line; otherwise False. 
        :rtype: bool
            
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
            return self.intersects(line.P0) and self.vL.is_collinear(line.vL)
        else:
            raise TypeError('Line.__eq__ should be used with a Line instance')
    
    
    def is_parallel(self,line):
        """Tests if this line and the supplied line are parallel. 
        
        :param obj: A line.
        :type obj: Line
        
        :return: Returns True if the lines are parallel (this includes the
            case of collinear lines); 
            otherwise False. 
        :rtype: bool
            
        """
        return self.vL.is_collinear(line.vL)
    
    
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
            
    

class Polyline(FiniteGeometricObject):
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


    def intersects(self,obj):
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
        if self.intersects(point):
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
                

    def equals(self,polyline):
        """Tests if this polyline and the supplied polyline are equal.
        
        :param polyline: A polyline.
        :type polyline: Polyline
        
        :return: True if the polylines have the same points in the same order, 
            either as supplied or in reverse;
            otherwise False.
        :rtype: bool
        
        """
        
        if isinstance(polyline,Polyline):
            
            if self.points==polyline.points or self.points==polyline.reverse.points:
                return True
            else:
                return False
            
        else:
            return False


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
            if hasattr(obj,'_shapely'):
                return GeometricObject.intersection(self,obj)
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


    def plot(self, ax=None, **kwargs):
        """Plots the polyline on the supplied axes.
        
        :param ax: An 2D or 3D Axes instance.
        :type ax:  matplotlib.axes._subplots.AxesSubplot, matplotlib.axes._subplots.Axes3DSubplot
        :param kwargs: keyword arguments to be passed to the Axes.plot call.
                   
        :returns: The matplotlib axes.
        :rtype: matplotlib.axes._subplots.AxesSubplot or 
        matplotlib.axes._subplots.Axes3DSubplot
    
        """
        if ax is None:
            fig,ax=get_matplotlib_fig_ax(self.nD)
        
        ax.plot(*zip(*self.coordinates), **kwargs)
        return ax
    
    
    @property
    def points(self):
        """Returns the polyline points.
        """
        return self._items
    

    @property
    def polylines(self):
        """Returns a Polylines of the individual line segments
        """
        n=len(self)
        return Polylines(*[Polyline(self[i],self[i+1]) for i in range(n-1)])


    def render(self,
           scene=None,
           color=vpython.color.blue,
           **kwargs
           ):
        ""
        
        if scene is None:
            scene=get_render_scene()
        
        vpython.curve(pos=self._vpython_vector,
                      color=color,
                      **kwargs
                      )
        
        return scene
    


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



class Polylines(FiniteGeometricObject):
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


    def plot(self, ax=None, **kwargs):
        """Plots the polylines on the supplied axes.
        
        :param ax: An 2D or 3D Axes instance.
        :type ax:  matplotlib.axes._subplots.AxesSubplot, matplotlib.axes._subplots.Axes3DSubplot
        :param kwargs: keyword arguments to be passed to the Axes.plot call.
                   
        :returns: The matplotlib axes.
        :rtype: matplotlib.axes._subplots.AxesSubplot or 
        matplotlib.axes._subplots.Axes3DSubplot
    
        """
        if ax is None:
            fig,ax=get_matplotlib_fig_ax(self.nD)
        
        for pl in self:
            ax=pl.plot(ax,**kwargs)
        return ax
    
    

    @property
    def points(self):
        ""
        result=[]
        for pl in self:
            result.extend(pl)
        return Points(*result)


    def render(self,
           scene=None,
           color=vpython.color.blue,
           **kwargs
           ):
        ""
        
        if scene is None:
            scene=get_render_scene()
        
        for pl in self:
            pl.render(scene=scene,
                      color=color,
                      **kwargs)
        
        return scene
    



class Plane(InfiniteGeometricObject):
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
         
    
    def _intersection_line(self,line):
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
            return GeometryObjects(line)
        elif self.N.is_perpendicular(line.vL): # plane and line are parallel 
            return GeometryObjects()
        else:
            return self._intersect_line_skew(line)
    
    
    def _intersection_line_skew(self,skew_line):
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
        return GeometryObjects(skew_line.calculate_point(t))
       
    
    def _intersection_plane(self,plane):
        """Returns the intersection of this plane and another plane.
        
        :param plane: A 3D plane.
        :type plane: Plane
        
        :return: Returns None for parallel, non-coplanar planes.
            Returns a plane for two coplanar planes.
            Returns a line for non-parallel planes.
        :rtype: GeometryObjects  
        
        .. rubric:: Code Example
    
        .. code-block:: python
           
           >>> from crossproduct import Point, Vector, Plane
           >>> pn = Plane(Point(0,0,0), Vector(0,0,1))
           >>> result = pn.intersect_plane(Plane(Point(0,0,0), Vector(1,0,0)))
           >>> print(result)
           Line(Point(0.0,0.0,0.0), Vector(0.0,1.0,0.0))
    
        """
        if plane.equals(self):
            return GeometryObjects(self)
        elif plane.N.is_collinear(self.N):
            return GeometryObjects()
        else:
            n1=self.N
            d1=-n1.dot(self.P0-Point(0,0,0))
            n2=plane.N
            d2=-n2.dot(plane.P0-Point(0,0,0))
            n3=n1.cross_product(n2)
            P0=Point(0,0,0) + ((n1*d2-n2*d1).cross_product(n3) * (1 / (n3.length**2)))
            u=n3
            return GeometryObjects(Line(P0,u))
    
    @property
    def axes(self):
        """Returns 'x' and 'y' axes for a plane.
        
        Used when using 2D coordinates within a 3D polygon.
        
        :returns: vx, vy - two vectors
        :rtype: tuple
        
        """
        
        # x-vector
        x=self.intersection(Plane(Point(0,0,0),Vector(0,0,-1)))
        #print('---',x)
        if len(x)>0 and isinstance(x[0],Line):
            vx=x[0].vL.normalise
        else:
            vx=self.N.cross_product(Vector(0,-1,0)).normalise
        #print('vx',vx)
        
        # y-vector
        vy=vx.cross_product(self.N).normalise.opposite
        #print('vy',vy)
        
        return vx, vy
    
    
    def point_on_axes(self,point,vx,vy):
        """Returns x and y coordinates of a 3D point on a 3D plane.
        
        Relative to the plane start point (P0) and the plane 'x and y' axes.
        
        :param plane: A plane.
        :param point: A 3D point on the plane
        
        vx, vy from 'axes' method
        
        :rtype: Point
        
        """
    
        if not self.intersects(point):
            raise ValueError
    
        #vx, vy = plane_axes(plane)
        
        #print('point',point)
        a=Line(self.P0,vx)
        #print('a',a)
        b=Line(point,vy.opposite)
        #print('b',b)
        x=a.intersection(b)[0]
        #print('x',x)
        t_a=a.calculate_t_from_coordinates(*x)
        t_b=b.calculate_t_from_coordinates(*x)
        #print(t_a,t_b)
        return Point(t_a,t_b)
    
    
    def polygon_on_axes(self,polygon,vx,vy):
        """Returns a 2D polygon of a 3D polygon on the plane axes.
        
        Relative to the plane start point (P0) and the plane 'x and y' axes.
        
        :param polygon: A polygon.
        
        :rtype: Polygon
        
        """
        if polygon.nD==2:
            raise ValueError
        elif polygon.nD==3:
            pts=[]
            for pt in polygon:
                pts.append(self.point_on_axes(pt,vx,vy))
            return Polygon(*pts)
        else:
            raise Exception
    
    
    
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
    
    
    def intersects(self,obj):
        """
        """
        
        if isinstance(obj,Point):
            return self.N.is_perpendicular(obj-self.P0)
            
        else:
            raise Exception
    
    
    def intersection(self,obj):
        """
        """
        if isinstance(obj,Plane):
            return self._intersection_plane(obj)
        elif isinstance(obj,Line):
            return self._intersection_line(obj)
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


    

class Polygon(FiniteGeometricObject):
    """A polygon, situated on an xy or xyz plane. 
    
    In *crossproduct* a Polygon object is a immutable sequence. 
    Iterating over a Polygon will provide its exterior Point instances.
    
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
        
        self._items=Points(*points)
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
            x=[shapely.geometry.Polygon(pg.coordinates) for pg in self.polygons]
            return shapely.geometry.MultiPolygon(x)
        else:
            raise Exception  # only 2d for shapely polygons


    @property
    def area(self):
        """The area of the polygon.
        
        :rtype: float
        
        """
        if self.nD==2:
            return abs(float(self._shapely.area))
        elif self.nD==3:
            plane=self.plane
            N=plane.N
            i=plane.N.index_largest_absolute_coordinate
            self_2D=self.project_2D(i)
            if i==0:
                return abs(self_2D.area*(N.length/(N.x)))
            elif i==1:
                return abs(self_2D.area*(N.length/(N.y)))
            elif i==2:
                return abs(self_2D.area*(N.length/(N.z)))
            else:
                raise Exception
        else:
            raise ValueError


    @property
    def azimuth(self):
        """The azimuth angle of the polygon from the y axis.
        
        :type polygon: crossproduct.SimplePolygon
        
        :returns: The azimuth angle in degrees where 0 degrees is the direction 
            of the y axis and a positive angle is clockwise.
            If the surface is horizontal, then returns None.
        :rtype: float, None
            
        """
        if self.nD==2:
            raise ValueError  # not possible for 2D
        elif self.nD==3:
            N=self.plane.N
            v=Vector(N.x,N.y)
            if v.length==0:
                return None
            y_axis=Vector(0,1)
            angle=math.degrees(v.angle(y_axis))
            if v.perp_product(y_axis)>=0: # if y_axis is on the left of v
                return angle
            else: # y_axis is on the right of v
                return angle * -1
        else:
            raise Exception


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
        """Returns a tuple representation of the polygon exterior.
        
        :returns: The exterior and holes coordinates as a tuple. 
            
        :rtype: tuple
        
        .. code-block:: python
        
            >>> from crossproduct import Point, Polygon
            >>> pg=Polygon(Point(0,0),Point(1,0),Point(1,1),Point(0,1))
            >>> result = pg.coordinates()
            >>> print(result)
            (((0, 0), (1, 0), (1, 1), (0, 1)), ())
        
        """
        return tuple(pt.coordinates for pt in self.points)


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
        if len(polygons)==0:
            return GeometryObjects(self)
        else:
            raise Exception ## to do
            result=[]
            for pg in self.polygons:
                for pg1 in polygons:
                    x=self.difference(pg)
                    print(x)
                    result.update(x)  # does this work?
            return GeometryObjects(result)
        

    def difference(self,obj):
        """The geometric difference between self and obj.
        
        :param obj: A geometric object.
        
        :returns: A tuple of the difference objects.
        :rtype: tuple
        
        """
        if self.nD==2:
            if hasattr(obj,'_shapely'):
                return GeometricObject.difference(self,obj)
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
            if hasattr(obj,'_shapely'):
                return GeometricObject.intersection(self,obj)
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
            
            
    def intersects(self,obj):
        """Returns True if self intersects in any way with obj
        
        
        
        
        """
        if self.nD==2:
            if hasattr(obj,'_shapely'):
                return GeometricObject.intersects(self,obj)
            else:
                raise Exception('%s' % obj.__class__)
        
        elif self.nD==3:
            plane=self.plane
            i=plane.N.index_largest_absolute_coordinate
            self_2D=self.project_2D(i)
            obj_2D=self.project_2D(i)
            return self_2D.intersects(obj_2D)
            
            
        else:
            raise ValueError
            
            
    @property
    def leftmost_lowest_vertex(self):
        """Returns the index of the leftmost lowest point of the polygon.
        
        :rtype: int
        
        :Example:
    
        .. code-block:: python
           
           
        """
        if self.nD==2:
        
            min_i=0
            for i in range(1,len(self)):
                if self[i].y>self[min_i].y:
                    continue
                if (self[i].y==self[min_i].y) and (self[i].x > self[min_i].x):
                    continue
                min_i=i
            return min_i
    
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
            for i in range(0,len(self)+1-3):
                P0,P1,P2=self.points[i:i+3]
                N=(P1-P0).cross_product(P2-P1)
                if N.length>ABS_TOL:
                    return Plane(P0,N)
        else:
            raise ValueError
        raise ValueError('3D polygon has no plane')
            
            
    def plot(self, ax=None, set_lims=False, **kwargs):
        """Plots the polygon on the supplied axes.
        
        :param ax: An 2D or 3D Axes instance.
        :type ax:  matplotlib.axes._subplots.AxesSubplot, matplotlib.axes._subplots.Axes3DSubplot
        :param kwargs: keyword arguments to be passed to the Axes.plot call.
                   
        :returns: The matplotlib axes.
        :rtype: matplotlib.axes._subplots.AxesSubplot or 
        matplotlib.axes._subplots.Axes3DSubplot
    
        """
        if ax is None:
            fig,ax=get_matplotlib_fig_ax(self.nD)
            
        kwargs['color']=kwargs.get('color','tab:blue')
        kwargs['linewidth']=kwargs.get('linewidth',0)
        
        if self.nD==2:
            for tri in self.polygons:
                ax.fill(*zip(*tri.coordinates), **kwargs)
        elif self.nD==3:
            verts=[tri.coordinates for tri in self.polygons]
            pc=Poly3DCollection(verts,**kwargs)
            ax.add_collection3d(pc)
                
        if set_lims:
            if self.nD==2:
                minx,miny,maxx,maxy=self.bounds        
                ax.set_xlim(minx,maxx)
                ax.set_ylim(miny,maxy)
            elif self.nD==3:
                minx,miny,minz,maxx,maxy,maxz=self.bounds        
                ax.set_xlim(minx,maxx)
                ax.set_ylim(miny,maxy)
                ax.set_zlim(minz,maxz)
            
        return ax
    
    
    
    @property
    def points(self):
        """Returns the exterior points.
        """
        return self._items
            
    @property
    def polyline(self):
        """returns a polyline of the polygon exterior
        """
        return Polyline(*(list(self.points) + [self.points[0]]))
    
            
    # @property
    # def polylines(self):
    #     """Returns polylines of the polygon exterior and the polygon holes.
        
    #     :return: A polyline of the polygon points which starts and ends at 
    #         the first polygon point.
    #         tuple (exterior polyline, hole polylines)
    #     :rtype: Polylines     
        
    #     :Example:
    
    #     .. code-block:: python
           
            
    #     """
    #     return Polylines(Polyline(*(list(self.points) + [self.points[0]])), 
    #             (*(Polyline(*(list(hole.points) + [hole.points[0]])) 
    #                         for hole in self.holes))
    #             )

        
        
    #     return (Polyline(*(list(self.points) + [self.points[0]])), 
    #             Polylines(*(Polyline(*(list(hole.points) + [hole.points[0]])) 
    #                         for hole in self.holes))
    #             )


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
                #print(self)
                #print(self.holes)
                
                pgs=[self]  # polygons to be split by hole lines
                for hole in self.holes:
                    l=hole.polyline.lines[0]
                    #print(l)
                    x=[]
                    for pg in pgs:
                        x.extend(pg.exterior.split(l))
                    pgs=x
                #print(pgs)
                
                result=[]
                for pg in pgs:
                    result.extend(pg.difference(self.holes))
                return Polygons(*result)
                
                #return Polygons(*self.exterior.difference(self.holes))
                #return self.triangles  # or self.difference(self.holes) ??
                
        elif self.nD==3:
            
            if len(self.holes)==0:
                return Polygons(self)
            else:
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
    


    def render(self,
           scene=None,
           color=vpython.color.blue,
           **kwargs
           ):
        ""
        
        if scene is None:
            scene=get_render_scene()
        
        for tri in self.triangles:
            vs=[]
            for pt in tri.points:
                v=vpython.vertex(pos=pt._vpython_vector, 
                                 color=color,
                                 **kwargs)
                vs.append(v)
            
            vpython.triangle(vs=vs)
        
        
        return scene
    
        
    
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
           
    
    
    def _split_line_3D(self,line):
        ""
        a=self.plane.intersection(line) # returns () or (Point,) or (Line,)
        #print(a)
        if len(a)==0: # line does not intersect polygon plane
            return self
        
        elif isinstance(a[0],Point): # line is skew to polygon plane
            return self
        
        elif isinstance(a[0],Line):  # line is on the same plane as polygon
            
            i=self.plane.N.index_largest_absolute_coordinate
            self_2D=self.project_2D(i)
            line_2D=line.project_2D(i)
            result=self_2D.split(line_2D)
            return GeometryObjects(*(x.project_3D(self.plane,i) for x in result))
        
        else:
            raise Exception
    
    
    
    def split(self,obj):
        """
        
        
        """
        if self.nD==2:
            if hasattr(obj,'_shapely'):
                return GeometricObject.split(self,obj)
            elif isinstance(obj,Line):
                minx,miny,maxx,maxy=self.bounds
                t0=obj.calculate_t_from_coordinates(minx,miny)
                t1=obj.calculate_t_from_coordinates(maxx,maxy)
                P0=obj.calculate_point(t0)
                P1=obj.calculate_point(t1)
                return self.split(Polyline(P0,P1))
            else:
                raise Exception('%s' % obj.__class__)
        
        elif self.nD==3:
            
            if isinstance(obj,Line):
                return self._split_line_3D(obj)
            else:
                raise Exception  # not implemented yet
            
        else:
            raise ValueError
    
    
    @property
    def tilt(self):
        """The tilt angle of the polygon from the horizontal.
        
        :returns: The tilt angle in degrees where vertically up is 0 degrees and 
            face down is 180 degrees.
        :rtype: float
            
        """
        return math.degrees(self.plane.N.angle(Vector(0,0,1)))
    
    
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
                
                vertices=self.coordinates
                segments=[[x,x+1] for x in range(len(self.points))]
                segments[-1][1]=0
                A=dict(vertices=vertices,
                       segments=segments)
                B=tr.triangulate(A,'p')
                tris=[]
                if 'triangles' in B:
                    for x in B['triangles']:
                        tri=Polygon(*(Point(*B['vertices'][y]) for y in x))
                        tris.append(tri)
                return Polygons(*tris)
            
            else:
                
                pgs=self.polygons
                result=[]
                for pg in pgs:
                    result.extend(pg.triangles)
                return Polygons(*result)
                
                # exterior vertices and segments
                vertices=list(self.coordinates)
                segments=[[x,x+1] for x in range(len(self.points))]
                segments[-1][1]=0
                holes=[]
                # holes vertices and segments
                for hole in self.holes:
                    vertices.extend(hole.coordinates)
                    n=len(segments)
                    segments.extend([[x,x+1] for x in range(n,n+len(self.points))])
                    segments[-1][1]=n
                    holes.append(hole.exterior.triangles[0].centroid.coordinates)
                # get triangles
                A=dict(vertices=vertices,
                       segments=segments,
                       holes=holes)
                #print(A)
                B=tr.triangulate(A,'p')
                #print(B['triangles'])
                #print(len(vertices))
                #print(B)
                #print(len(B['vertices']))
                tris=[]
                if 'triangles' in B:
                    for x in B['triangles']:
                        tri=Polygon(*(Point(*B['vertices'][y]) for y in x))
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
            
            
            
    def relative_2D_polygon(self,inner_polygon3D):
        """
        
        Used in to_python to find the 2D polygon input for an opening
        
        
        :returns: A 2D polygon
        
        """
        if self.nD==2:
            raise ValueError
        elif self.nD==3:
            vx, vy = self.plane.axes
            self_2D=self.plane.polygon_on_axes(self,vx,vy)
            start_point_2D=self_2D[self_2D.leftmost_lowest_vertex]
            
            pts=[]
            for pt in inner_polygon3D:
                a=self.plane.point_on_axes(pt,vx,vy)
                #print(a)
                b=Point(*(a-start_point_2D))
                #print(b)
                pts.append(b)
            return Polygon(*pts)
        
        else:
            raise Exception
            
            
    def relative_3D_polygon(self,inner_polygon2D):
        """Given a 2D polygon within a 'relative polygon' returns the 3D polygon.
        
        Relative to the lowest le:ftmost vertex (2D) and the plane 'x and y' axes.
        
        :param polygon2D: A 2D polygon that sits within a 3D polygon.
        :param polygon3D: The 3D polygon.
        
        :returns: A 3D polygon
        :rtype: Polygon
        
        """
        if self.nD==2:
            raise ValueError
        elif self.nD==3:
            vx, vy = self.plane.axes
            self_2D=self.plane.polygon_on_axes(self,vx,vy)
            start_point_3D=self[self_2D.leftmost_lowest_vertex]
            
            pg=Polygon(*(start_point_3D+vx*pt.x+vy*pt.y 
                         for pt in inner_polygon2D))
            if not pg.plane.N.is_codirectional(self.plane.N):
                pg=pg.reverse
            return pg 
        else:
            raise Exception
    

class Polygons(FiniteGeometricObject):
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
            x=[shapely.geometry.Polygon(pg1.coordinates) 
               for pg in self
               for pg1 in pg.polygons]
            return shapely.geometry.MultiPolygon(x)
        else:
            raise Exception  # only 2d for shapely polygons


    def render(self,
           scene=None,
           color=vpython.color.blue,
           **kwargs
           ):
        ""
        
        if scene is None:
            scene=get_render_scene()
        
        for pg in self:
            pg.render(scene=scene,
                      color=color,
                      **kwargs)
        
        return scene
    
    
    def plot(self, ax=None, set_lims=False, **kwargs):
        """Plots the polygons on the supplied axes.
        
        :param ax: An 2D or 3D Axes instance.
        :type ax:  matplotlib.axes._subplots.AxesSubplot, matplotlib.axes._subplots.Axes3DSubplot
        :param kwargs: keyword arguments to be passed to the Axes.plot call.
                   
        :returns: The matplotlib axes.
        :rtype: matplotlib.axes._subplots.AxesSubplot or 
        matplotlib.axes._subplots.Axes3DSubplot
    
        """
        for pg in self:
            ax=pg.plot(ax,**kwargs)
            
        if set_lims:
            if self.nD==2:
                minx,miny,maxx,maxy=self.bounds        
                ax.set_xlim(minx,maxx)
                ax.set_ylim(miny,maxy)
            elif self.nD==3:
                minx,miny,minz,maxx,maxy,maxz=self.bounds        
                ax.set_xlim(minx,maxx)
                ax.set_ylim(miny,maxy)
                ax.set_zlim(minz,maxz)
            
        return ax
            
        #return Polygon.plot(self,ax,**kwargs)
            
    
    @property
    def points(self):
        """All polygon exterior points
        """
        result=[]
        for pg in self:
            result.extend(pg.points)
        return Points(*result)   
    
    
    @property
    def polyline(self):
        ""
        result=[]
        for pg in self:
            result.append(pg.polyline)
        return Polylines(*result)   
    
    
    @property
    def polylines(self):
        ""
        result=[]
        for pg in self:
            result.extend(pg.polylines)
        return Polylines(*result)   
    
    
    @property
    def polygons(self):
        ""
        result=[]
        for pg in self:
            result.extend(pg.polygons)
        return Polygons(*result)   


    # def split(self,obj):
    #     ""
    #     result=[]
    #     for pg in self:
    #         result.extend(pg.split(obj))
    #     return Polygons(*result) 
    

    @property
    def triangles(self):
        ""
        result=[]
        for pg in self:
            result.extend(pg.triangles)
        return Polygons(*result)   
         

class Polyhedron(FiniteGeometricObject):
    """A tetrahedron, situated on the xyz plane. 
    
    :param polygons: A sequence of polygons for the outer faces.
        All polygons should not have any holes. 
        All polygons must have outward facing normals.
    :type polygons: Polygons or other sequence.
    :param tetrahedrons: A list of equivalent tetrahedrons with the
        same combined shape as the polygons
    :type tetrahedrons: Polyhedrons
    
    """
    
    def __init__(self,*polygons,tetrahedrons=None):
        ""
        self._items=Polygons(*polygons)
        
        
        if not tetrahedrons is None:
            self._tetrahedrons=tetrahedrons
        elif len(polygons)==4:
            self._tetrahedrons=Polyhedrons(self)
        else:
            self._tetrahedrons=None
            
            
    @property
    def base_polygon_and_extrud_vector(self):
        """Creates a floor polygon and extrud vector by decomposing a polyhedron.
        
        :param polyhedron: A 3D polyhedron with all faces with outward pointing normals
        :type polyhedron: crossproduct.Polyhedron
        
        :raises ValueError: 
            - If polyhedron does not have six polygon faces.    
        
        :returns: A tuple of:
            - floor_polygon (crossproduct.Polygon): 
                A 3D polygon which acts as the base of the polygon.
            - extrud_vector (crossproduct.Vector): 
                A 3D vector in a direction behind the plane of the floor_polygon.
        :rtype: tuple
        
        """
    
        # loop through polygons
        for pg in self:
            #print(pg)
            
            # find a parallel polygon (i.e. the opposite face) - if nto then continue
            for pg1 in self:
                if pg==pg1:
                    continue  # continue on this loop
                elif pg.plane.N.is_collinear(pg1.plane.N):
                    opposite_pg=pg1
                    break  # continue on main loop
            else:
                continue  # continue with main loop if no opposite polygon is found
            #print(opposite_pg)
            
            # find single polylines not on the two facing polygons
            pls=[pl for pl in self.polylines 
                      if not any(pl.equals(pl1) 
                                 for pl1 in pg.polyline.polylines)
                      and not any(pl.equals(pl1) 
                                  for pl1 in opposite_pg.polyline.polylines)]
            
            # are all the polylines collinear and of the same length? - if not the continue
            v0=pls[0][1]-pls[0][0]
            for pl in pls[1:]:
                v=pl.lines[0].vL
                if not v.is_collinear(v0) or not v.length==v0.length:
                    continue  # continue on main loop
            
            floor_polygon=pg
            extrud_vector=v0
            
            # is extrud vector pointing the opposite direction to the polygon normal
            #   - if not then the extrud vector is reversed
            if floor_polygon.plane.N.dot(extrud_vector)>0:  # if angle is less than 90
                extrud_vector=extrud_vector.opposite
            
            return floor_polygon, extrud_vector
            
        raise ValueError('Polyhedron cannot be decomposed')
            
            
            
            
    @property
    def points(self):
        "Unique points"
        result=[]
        for pg in self:
            for pt in pg:
                if not any(x.equals(pt) for x in result):
                    result.append(pt)
        return Points(*result)
    
    
    @property
    def polylines(self):
        "Unique polylines (length=1)"
        result=[]
        for pg in self:
            for pl in pg.polyline.polylines:
                if not any(x.equals(pl) for x in result):
                    result.append(pl)
        return Polylines(*result)
            
            
    @property
    def polygons(self):
        ""
        return self._items
    
    
    @property
    def tetrahedrons(self):
        ""
        return self._tetrahedrons
    
    
    @property
    def _volume_tetrahedron(self):
        ""
        P0,P1,P2,P3=self.points
        v0,v1,v2=P1-P0,P2-P0,P3-P0
        return abs((v0.dot(v1.cross_product(v2)))/6.0)
    
    
    @property
    def volume(self):
        ""
        return sum(th._volume_tetrahedron for th in self.tetrahedrons)
    
    
    
class Polyhedrons(FiniteGeometricObject):
    """
    """
    
    
    
        
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
        
    return Polyhedron(*result)
    

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
    return Polyhedrons(th0,th1,th2)
    
    
def polyhedron_from_base_polygon_and_extrud_vector(base_polygon,
                                                   extrud_vector):
    """
    """
    # polygons
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
    polygons=Polygons(base_polygon, top_polygon, *side_polygons)
    
    # tetrahedrons
    result=[]
    for triangle in base_polygon.triangles:
        result.extend(tetrahedrons_from_extruded_triangle(triangle, extrud_vector))
    tetrahedrons=Polyhedrons(*result)
    
    return Polyhedron(*polygons,tetrahedrons=tetrahedrons)
        
    
    
    
def get_render_scene():
    ""
    scene=vpython.canvas()
    scene.background=vpython.color.gray(0.95)
    scene.height=200
    scene.width=300
    scene.forward=vpython.vector(0,1,-1)
    scene.up=vpython.vector(0,0,1)

    return scene


def get_matplotlib_fig_ax(nD):
    """
    """
    if nD==2:
        fig, ax = plt.subplots()
        
    elif nD==3:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.set_zlabel('z-coordinate')
    else:
        raise Exception
        
    ax.set_xlabel('x-coordinate')
    ax.set_ylabel('y-coordinate')
    return fig,ax
    
    
    
    