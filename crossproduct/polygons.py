# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d

from collections.abc import Sequence
from .segments import Segments
from .points import Points
from .polylines import Polylines


class Polygons(Sequence):
    """A sequence of polygons.    
    
    :param polygons: A sequence of Polygon2D or Polygon3D instances. 
        
    :Example:
        
    .. code-block:: python
        
        >>> pgs = Polygons(Polygon2D(Point2D(0,0), Point2D(1,0), Point2D(1,1)))                       
        >>> print(pgs)
        Polygons(Polygon2D(Point2D(0,0), Point2D(1,0), Point2D(1,1)))
        
        >>> print(pgs[0])
        Polygon2D(Point2D(0,0), Point2D(1,0), Point2D(1,1))
    """
    
    def __init__(self,*polygons):
        ""
        self._polygons=list(polygons)
        
        
    def __eq__(self,obj):
        """Tests if this polygons sequence and the supplied polygons sequence are equal.
        
        :param polygons: The polygons sequence to be tested.
        :type polygons: Polygons
        
        :return: True if the polygons items are equal and in the same order;
            otherwise False.
        :rtype: bool
        
        :Example:
    
        .. code-block:: python
        
            >>> pgs1 = Polygons(Polygon2D(Point2D(0,0), Point2D(1,0), Point2D(1,1)))  
            >>> pgs2 = Polygons(Polygon2D(Point2D(0,0), Point2D(1,0), Point2D(1,1)))  
            >>> result = pgs1 == pgs2
            >>> print(result)
            True
            
        """
        if isinstance(obj,Polygons) and self._polygons==obj._polygons:
            return True
        else:
            return False
        
        
    def __getitem__(self,i):
        ""
        return self._polygons[i]
        
    
    def __len__(self):
        ""
        return len(self._polygons)
    
    
    def __repr__(self):
        ""
        return 'Polygons(%s)' % ', '.join([str(pg) for pg in self._polygons])
    
    
    @property
    def add_all(self):
        """Adds together the polygons in the sequence where possible
        
        :return: Returns a new Polygons sequence where the polygons have been
            added together where possible to form new polygons.        
        :rtype: Polygons
        
        """
        polygons=[pg for pg in self]
        i=0
        
        while True:
            try:
                pg=polygons[i]
            except IndexError:
                break
            try:
                new_pg,index=Polygons(*polygons[i+1:]).add_first(pg)
                #print(new_s,index)
                polygons[i]=new_pg
                polygons.pop(i+index+1)
            except ValueError:
                i+=1
        
        return Polygons(*polygons)
    
    
    def add_first(self,polygon):
        """Adds the first available polygon to the supplied polygon.
        
        This iterates through the polygons in the Polygons sequence. 
            When the first polygon which can be added to the supplied polygon is found,
            the result of this addition is returned along with its index.
        
        :raises ValueError: If no valid additions are found.
        
        :return: Returns a tuple with the addition result and the index of the polygon which was added.
        :rtype: tuple (Polygon,int)
        
        :Example:
    
        .. code-block:: python
        
            >>> pls = Polylines(Polyline2D(Point2D(0,0), Point2D(1,0)))
            >>> result = pls.add_first(Polyline2D(Point2D(1,0), Point2D(2,0)))
            >>> print(result)
            (Polyline2D(Point2D(0,0), Point2D(1,0), Point2D(2,0)),0)
        
        """
        for i,pg in enumerate(self):
            try:
                result=polygon+pg
                return result,i
            except ValueError:
                pass
        
        raise ValueError
    
    
    def append(self,polygon,unique=False):
        """Appends supplied polygon to this polygons sequence.
        
        :param polygon: The polygon to be appended.
        :type polygon: Polygon2D or Polygon3D
        :param unique: If True, polygon is only appended if it does not already
            exist in the sequence; defaults to False.
        :type unique: bool
        
        :rtype: None
        
        :Example:
    
        .. code-block:: python
        
            >>> pgs = Polygons(Polygon2D(Point2D(0,0), Point2D(1,0), Point2D(1,1)))
            >>> pgs.append(Polygons(Polygon2D(Point2D(0,0), Point2D(1,0), Point2D(1,1))))
            >>> print(pgs)
            Polylines(Polygons(Polygon2D(Point2D(0,0), Point2D(1,0), Point2D(1,1))),
                      Polygons(Polygon2D(Point2D(0,0), Point2D(1,0), Point2D(1,1))))
        
        """
        if polygon.classname =='Polygon':
            if unique:
                if not polygon in self:
                    self._polygons.append(polygon)
            else:
                self._polygons.append(polygon)
                
        else:
            raise TypeError
    
    
    def intersect_segment(self,segment):
        """Intersection of this Polygons sequence with the supplied segment.
        
        :param segment: A 2D or 3D segment.
        :type segment: Segment2D, Segment3D
        
        :return: A tuple of intersection points and intersection segments 
            (Points,Segments). 
        :rtype: tuple     
        
        """
        ipts=Points()
        isegments=Segments()
        
        for pg in self:
            pts,sgmts=pg.intersect_segment(segment)
            for pt in pts:
                ipts.append(pt,unique=True)
            for sgmt in sgmts:
                isegments.append(sgmt,unique=True)
        
        return ipts, isegments
    
    
    def plot(self,ax=None,normal=False,color='blue',**kwargs):
        """Plots the polygons on the supplied axes.
        
        :param ax: An Axes or Axes3D instance; optional.
        :type ax: matplotlib.axes.Axes, mpl_toolkits.mplot3d.axes3d.Axes3D
        :param normal: If True then a normal vector is plotted for a 3D polygon;
            default False.
        :type normal: bool
        :param color: Color keyword for the plot; default is 'blue'.
        :type color: str
        :param kwargs: Keyword arguments to be supplied to the matplotlib plot call.
                    
        """
        if not ax:
            if self[0].dimension=='2D':
                fig, ax = plt.subplots()
            else:
                fig = plt.figure()
                ax = fig.add_subplot(111, projection='3d')
        for pg in self:
            pg.plot(ax,
                    normal=normal,
                    color=color,
                    **kwargs)
    
    
    @property
    def polylines(self):
        """Returns a Polylines sequence of all the polylines of the polygons.
        
        :rtype: Polylines
        
        :Example:
    
        .. code-block:: python
        
            >>> pgs = Polygons(Polygon2D(Point2D(0,0), Point2D(1,0), Point2D(1,1)))
            >>> print(pgs.polylines)
            Polylines(Polyline3D(Point3D(0,0,1), Point3D(1,0,1), Point3D(1,1,1)))
        
        """
        polylines=Polylines()
        for pg in self:
            polylines.append(pg.polyline,unique=True)
        return polylines
    
    
    def project_3D(self,plane,coordinate_index):
        """Projection of sequence of 2D polygons on a 3D plane.
        
        :param plane: The plane for the projection
        :type plane: Plane3D
        :param coordinate_index: The index of the coordinate which was ignored 
            to create the 2D projection. For example, coordinate_index=0
            means that the x-coordinate was ignored and this point
            was originally projected onto the yz plane.
        :type coordinate_index: int
        
        :return: 3D polygons sequence which has been projected from the 2D polygons sequence.
        :rtype: Polygons
               
        :Example:
    
        .. code-block:: python
        
            >>> pgs = Polygons(Polygon2D(Point2D(0,0), Point2D(1,0), Point2D(1,1)))
            >>> pl = Plane3D(Point3D(0,0,1), Vector3D(0,0,1))
            >>> result = pgs.project_3D(pl, 2)
            >>> print(result)
            Polygons(Polygon3D(Point3D(0,0,1), Point3D(1,0,1), Point3D(1,1,1)))
        
        """
        polygons=[pg.project_3D(plane,coordinate_index) for pg in self]
        return Polygons(*polygons)
        
    
    
    
        
        
        
        
        
        
        
    