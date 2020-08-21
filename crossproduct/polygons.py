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
        ""
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
        
    
    
    # @property
    # def adjacent_polygons(self):
    #     """Returns a list of Polygon sequences containing polygons that are adjacent to each other
        
        
    #     """
        
        
        
    
    
    # @property
    # def union_adjacent(self):
    #     """Returns the adjacent unions of the simple polygons
        
    #     :rtype: Polygons
    #     """
    #     if len(self)==0:
    #         return self        
        
    #     result=Polygons()
    #     pg=self[0]
    #     remaining_polygons=Polygons(*self[1:])
    #     while True:
    #         #print('---')
    #         #print('i',i)
    #         #print('pg',pg)
    #         #print('remaining_polygons',remaining_polygons)
    #         #print('result',result)
    #         try:
    #             pg,remaining_polygons=remaining_polygons.union_adjacent_simple_polygon(pg)
                
    #         except TypeError:
    #             result.append(pg)
    #             try:
    #                 pg=remaining_polygons[0]
    #             except IndexError:
    #                 break
    #             remaining_polygons=Polygons(*remaining_polygons[1:])
    #     return result
    
    
    # def union_adjacent_simple_polygon(self,polygon):
    #     """Returns the first adjacent union of a polygon in the sequence with the polyline
        
    #     :return result: (union_result (Polygon),
    #                      Polygons sequence of remaining polygons)
        
    #     """
    #     pgs=[pg for pg in self]
    #     for i in range(len(pgs)):
    #         u=polygon.union_adjacent_simple_polygon(pgs[i])
    #         if u:
    #             pgs.pop(i)
    #             return u,Polygons(*pgs)
    
    #     return None
        
        
        
        
        
        
        
        
        
        
        
    