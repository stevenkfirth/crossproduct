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



class _BaseShapelyObject():
    ""
    
    def __eq__(self,obj):
        ""
    
        if isinstance(obj,self.__class__):
                
            if len(self)==0 or self.nD==2:
                
                a=self._shapely
                b=obj._shapely
                                        
                return a.equals(b)  # might not work if very small differences exist?
                
            elif self.nD==3:
                
                raise Exception  # to do
            
            else:
                print(self)
                print(self.nD)
            
                raise ValueError
            
        else:
            raise TypeError
           
            
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
        
    
    
        
        
    
    def difference(self,obj):
        ""
        
        if self.nD==2:
            
            a=self._shapely
            b=obj._shapely
            result=a.difference(b)
            #print(result)
            return self._shapely_to_pts_pls_pgns(result)[2]
            
        elif self.nD==3:
            
            raise Exception  # shapely doesn't work for 3d
            
        else:
            
            raise ValueError
    
            
    def intersection(self,obj):
        ""
        if self.nD==2:
            
            a=self._shapely
            b=obj._shapely
            result=a.intersection(b)
            return self._shapely_to_pts_pls_pgns(result)
                
        elif self.nD==3:
            
            raise Exception  # shapely doesn't work for 3d
            
        else:
            
            raise ValueError
        
        

class _BaseSequence(collections.abc.Sequence):
    ""
    
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
        ""
        return tuple(x.coordinates for x in self)
    
    
    @property
    def nD(self):
        ""
        return self[0].nD
        
 

class Point(_BaseSequence,_BaseShapelyObject):
    """A point, as described by xy or xyz coordinates.
    
    In *crossproduct* a `Point` object is a immutable sequence. 
    Iterating over a `Point` will provide its coordinates.
    Indexing a `Point` will return the coordinate for that index (0=x, 1=y, 2=z).
    
    :param coordinates: Argument list of two (xy) or three (xyz) coordinates. 
        Coordinates should be of type int, float or similar numeric. These values
        are converted to floats.
    
    :raises ValueError: If less then 2 or more than 3 arguments are supplied.
    
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
    
    def __init__(self,*coordinates):
        ""
        
        self._items=tuple(coordinates)
        
    
    @property
    def _shapely(self):
        ""
        if self.nD==2:
            return shapely.geometry.Point(self.coordinates)
        else:
            raise Exception  # only 2d for shapely objects
    
    
    @property       
    def coordinates(self):
        ""
        return self._items


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


class Points(_BaseSequence,_BaseShapelyObject):
    """A sequence of points.    
    
    In *crossproduct* a Points object is a mutable sequence. 
    Iterating over a Points object will provide its Point instances.
    Index, append, insert and delete actions are available.
    
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
    
    @property
    def _shapely(self):
        ""
        if len(self)==0 or self.nD==2:
            x=[pt._shapely for pt in self]
            return shapely.geometry.MultiPoint(x)
        else:
            raise Exception  # only 2d for shapely objects
    


class Polyline(_BaseSequence,_BaseShapelyObject):
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


    @property
    def polylines(self):
        """Returns a Polylines of the individual line segments
        """
        n=len(self)
        return Polylines(*[Polyline(self[i],self[i+1]) for i in range(n-1)])



class Polylines(_BaseSequence,_BaseShapelyObject):
    """A sequence of polylines.    
    
    In *crossproduct* a Polylines object is a mutable sequence. 
    Iterating over a Polylines object will provide its Polyline instances.
    Index, append, insert and delete actions are available.
    
    :param polylines: An argument list of Polyline instances. 
    
    """
    
    @property
    def _shapely(self):
        ""
        if len(self)==0 or self.nD==2:
            x=[pl._shapely for pl in self]
            return shapely.geometry.MultiLineString(x)
        else:
            raise Exception  # only 2d for shapely objects
    
    

class Polygon(_BaseSequence,_BaseShapelyObject):
    """A polygon, situated on an xy or xyz plane. 
    
    In crossproduct a Polygon object is a immutable sequence. 
    Iterating over a Polygon will provide its Point instances.
    
    This polygon might be self-intersecting, and could be concave or convex.
    
    No two adjacent polygon edges should lie on the same line.
    
    :param points: Argument list of the Point instances of the vertices 
        of the polygon, in order. The first point is not repeated at the end. 
    :param holes: A sequence of polygons representing holes in the polygon.
    
    
    .. rubric:: Code Example

    .. code-block:: python
       
       >>> pg = Polygon(Point(0,0), Point(1,0), Point(1,1))
       >>> print(pg)
       Polygon(Point(0,0), Point(1,0), Point(1,1))
    
    """

    # def __eq__(self,polygon):
    #     """Tests if this polygon and the supplied polygon are equal.
        
    #     :param polygon: A polygon.
    #     :type polygon: Polygon
        
    #     :return: True if the two polygons have the same points and 
    #         the points are in the same order (from any start point), 
    #         either forward or reversed;       
    #         otherwise False.
    #     :rtype: bool
        
    #     .. rubric:: Code Example

    #     .. code-block:: python
           
    #         # 2D example
    #         >>> pg1 = Polygon(Point(0,0), Point(1,0), Point(1,1))
    #         >>> pg2 = Polygon(Point(0,0), Point(1,1), Point(1,0))
    #         >>> result = pl1 == pl2
    #         >>> print(result)
    #         True
            
    #     """
    #     if isinstance(polygon,Polygon):
            
    #         if self.nD==2:
                
    #             a=self._shapely
    #             b=polygon._shapely
                                        
    #             return a.equals(b)  # might not work if very small differences exist?
                
    #         elif self.nD==3:
                
    #             pass  # to do
            
    #         else:
                
    #             raise ValueError
            
    #     else:
    #         raise TypeError
        

   
    def __init__(self,*points,holes=None):
        ""
        
        self._items=Points(*points)
        if holes is None:
            self._holes=Polygons()
        else:
            self._holes=Polygons(*holes)
        # self._known_convex=known_convex
        # self._known_simple=known_simple
        # self._triangles=None
        # self._ccw=None
        
        
    def __repr__(self):
        ""
        return '%s(%s%s)' % (self.__class__.__name__,
                                     ','.join([str(c) for c in self]),
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
        ""
        return self._shapely.area



    @property
    def centroid(self):
        ""
        if self.nD==2:
            if len(self.holes)==0:
                return self._shapely_point_to_point(self._shapely[0].centroid)
            else:
                raise Exception  # to do
        elif self.nD==3:
            
            raise Exception  # to do
            
        else:
            
            raise ValueError
        



    @property
    def exterior(self):
        ""
        return Polygon(*self)
    
    
    
        
        
    

    @property
    def holes(self):
        ""
        return self._holes



    @property
    def polyline(self):
        """Returns a polyline of the polygon points.
        
        :return: A polyline of the polygon points which starts and ends at 
            the first polygon point.
        :rtype: Polyline     
        
        :Example:
    
        .. code-block:: python
           
            
        """
        return Polyline(*(list(self) + [self[0]]))
    


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
            
            raise Exception  # to do
            
        else:
            
            raise ValueError
            
            
            
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
                segments=np.array([(x,x+1) for x in range(len(self))])
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
                vertices=list(self.coordinates)
                segments=[[x,x+1] for x in range(len(self))]
                segments[-1][1]=0
                holes=[]
                # holes vertices and segments
                for hole in self.holes:
                    vertices.extend(hole.coordinates)
                    n=len(segments)
                    segments.extend(np.array([(x,x+1) for x in range(n,n+len(self))]))
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
            
            raise Exception  # to do
            
        else:
            
            raise ValueError
            
        
    


    
    

class Polygons(_BaseSequence,_BaseShapelyObject):
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

    