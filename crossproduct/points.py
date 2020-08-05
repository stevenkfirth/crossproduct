# -*- coding: utf-8 -*-

from collections.abc import Sequence
from .point import Point


class Points(Sequence):
    """A sequence of points.    
    
    :param points: A sequence of Point2D or Point3D instances. 
    :type points: Iterable
    
    :Example:
        
    .. code-block:: python
        
        >>> pts = Points(Point2D(0,0), Point2D(1,0))
        >>> print(pts)
        Points(Point2D(0,0), Point2D(1,0))
        
        >>> print(pts[1])
        Point2D(1,0)
    
    """
    
    def __init__(self,*points):
        ""
        self._points=list(points)
        
        
    def __eq__(self,points):
        """Tests if this points sequence and the supplied points sequence are equal.
        
        :param points: The points sequence to be tested.
        :type points: Points
        
        :return: True if the sequence items are equal, otherwise False.
        :rtype: bool
        
        :Example:
    
        .. code-block:: python
        
            >>> pts1 = Points(Point2D(0,0), Point2D(1,0))
            >>> pts2 = Points(Point2D(0,0), Point2D(1,0))
            >>> result = pts1 == pts2
            >>> print(result)
            True
            
        """
        if isinstance(points,Points) and self._points==points._points:
            return True
        else:
            return False
        
        
    def __getitem__(self,i):
        ""
        return self._points[i]
        
    
    def __len__(self):
        ""
        return len(self._points)
    
    
    def __repr__(self):
        ""
        return 'Points(%s)' % ', '.join([str(s) for s in self._points])
    
    
    def append(self,point,unique=False):
        """Appends supplied point to this points sequence.
        
        :param point: The point to be appended.
        :type point: Point2D or Point3D
        :param unique: If True, point is only appended if it does not already
            exist in the sequence; defaults to False.
        :type unique: bool
        
        :rtype: None
        
        :Example:
    
        .. code-block:: python
        
            >>> pts = Points(Point2D(0,0), Point2D(1,0))
            >>> pts.append(Point2D(2,0))
            >>> print(pts)
            Points(Point2D(0,0), Point2D(1,0), Point2D(2,0))
        
        """
        if isinstance(point,Point):
            if unique:
                if not point in self:
                    self._points.append(point)
            else:
                self._points.append(point)
                
        else:
            raise TypeError
    
    
    def project_2D(self,coordinate_index):
        """Projection of 3D points on a 2D plane
        
        :param coordinate_index: The index of the coordinate to ignore.
            Use coordinate_index=0 to ignore the x-coordinate, coordinate_index=1 
            for the y-coordinate and coordinate_index=2 for the z-coordinate.
        :type coordinate_index: int
        
        :return: Sequence of 2D points which have been projected from 3D points.
        :rtype: Points
        
        :Example:
    
        .. code-block:: python
        
            >>> pts = Points(Point3D(1,2,3), Point3D(4,5,6))
            >>> result = pts.project_2D(2)
            >>> print(result)
            Points(Point2D(1,2), Point2D(4,5))
               
        """
        points=[pt.project_2D(coordinate_index) for pt in self]
        return Points(*points)
    
    
    def project_3D(self,plane,coordinate_index):
        """Projection of 2D points on a 3D plane
        
        :param plane: The plane for the projection
        :type plane: Plane3D
        :param coordinate_index: The index of the coordinate which was ignored 
            to create the 2D projection. For example, coordinate_index=0
            means that the x-coordinate was ignored and this point
            was originally projected onto the yz plane.
        :type coordinate_index: int
        
        :return: Sequence of 3D points which have been projected from 2D points.
        :rtype: Points
               
        :Example:
    
        .. code-block:: python
        
            >>> pt = Points(Point2D(2,2))
            >>> pl = Plane3D(Point3D(0,0,1), Vector3D(0,0,1))
            >>> result = pts.project_3D(pl, 2)
            Points(Point3D(2,2,1))
        
        """
        points=[pt.project_3D(plane,coordinate_index) for pt in self]
        return Points(*points)
    
    
    def remove_points_in_segments(self,segments):
        """Removes any points that lie on any of the segments.
        
        :param segments: The segments to check.
        :type segments: Segments
        
        :return: New sequence with points removed if they exists in any part
            of the supplied segments.
        :rtype: Points
        
        :Example:
    
        .. code-block:: python
        
            >>> pts = Points(Point2D(0,0), Point2D(1,0))
            >>> segments = Segments(Segment2D(Point2D(0,0), Point2D(0,1)))
            >>> result = pts.remove_points_in_segments(segments)
            Points(Point2D(1,0))
        
        """
        points=[pt for pt in self if not segments.contains_point(pt)]
        return Points(*points)
        
    
    