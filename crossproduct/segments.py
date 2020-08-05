# -*- coding: utf-8 -*-


from collections.abc import Sequence
from .points import Points
from .polylines import Polylines


class Segments(Sequence):
    """A sequence of segments.    
    
    :param segments: A sequence of Segment2D or Segment3D instances. 
    :type points: Iterable
    
    :Example:
        
    .. code-block:: python
        
        >>> sgmts = Segments(Segment2D(Point2D(0,0), Point2D(1,0)))                             
        >>> print(sgmts)
        Segments(Segment2D(Point2D(0,0), Point2D(1,0)))
        
        >>> print(sgmts[0])
        Segment2D(Point2D(0,0), Point2D(1,0))
    
    """
    
    def __init__(self,*segments):
        ""
    
        self._segments=list(segments)
        
        
# DONT USE AS A SEQUENCE ALREADY IMPLICITLY HAS A __CONTAINS__ METHOD
    # def __contains__(self,obj):
    #     """Tests if the segment sequence contains the object.
        
    #     :param obj: A point or segment. 
    #     :type obj: Point2D, Point3D, Segment2D, Segment3D
            
    #     :return: For point, True if the point lies on one of the segments; otherwise False. 
    #         For segment, True if the segment start and endpoints are on one of the the segments; otherwise False. 
    #     :rtype: bool
        
    #     :Example:
    
    #     .. code-block:: python
           
    #        # 2D example
    #        >>> s = Segment2D(Point2D(0,0), Point2D(1,0))
    #        >>> result = Point2D(2,0) in l
    #        >>> print(result)
    #        False
           
    #        # 3D example
    #        >>> s1 = Segment3D(Point2D(0,0,0), Point3D(1,0,0))
    #        >>> s2 = Segment3D(Point3D(0,0,0), Point3D(0.5,0,0))
    #        >>> result = s2 in s1
    #        >>> print(result)
    #        True        
        
    #     """
    #     if obj.classname in ['Point','Segment']:
            
    #         for s in self.segments:
    #             if obj in s:
    #                 return True
    #         return False
            
    #     else:
    #         return TypeError()
        
        
    def __eq__(self,segments):
        """Tests if this segments sequence and the supplied segments sequence are equal.
        
        :param segments: The segments sequence to be tested.
        :type segments: Segments
        
        :return: True if the sequence items are equal, otherwise False.
        :rtype: bool
        
        :Example:
    
        .. code-block:: python
        
            >>> sgmts1 = Segments(Segment2D((Point2D(0,0), Point2D(1,0)))
            >>> sgmts2 = Segments(Segment2D((Point2D(0,0), Point2D(1,0)))
            >>> result = sgmts1 == sgmts2
            >>> print(result)
            True
            
        """
        if isinstance(segments,Segments) and self._segments==segments._segments:
            return True
        else:
            return False
                
        
    def __getitem__(self,i):
        ""
        return self._segments[i]
        
    
    def __len__(self):
        ""
        return len(self._segments)
    
    
    def __repr__(self):
        ""
        return 'Segments(%s)' % ', '.join([str(s) for s in self._segments])
    
    
    def append(self,segment,unique=False):
        """Appends supplied segment to this segments sequence.
        
        :param segment: The segment to be appended.
        :type segment: Segment2D or Segment3D
        :param unique: If True, degment is only appended if it does not already
            exist in the sequence; defaults to False.
        :type unique: bool
        
        :rtype: None
        
        :Example:
    
        .. code-block:: python
        
            >>> sgmts = Segments(Segment2D(Point2D(0,0), Point2D(1,0)))
            >>> sgmts.append(Segment2D(Point2D(1,0), Point2D(2,0)))
            >>> print(sgmts)
            Segments(Segment2D(Point2D(0,0), Point2D(1,0)),
                     Segment2D(Point2D(1,0), Point2D(2,0)))
        
        """
        if segment.classname=='Segment':
            if unique:
                if not segment in self:
                    self._segments.append(segment)
            else:
                self._segments.append(segment)
                
        else:
            raise TypeError
    
    
    def contains_point(self,point):
        """Tests if the segment sequence contains the object.
        
        :param obj: A point or segment. 
        :type obj: Point2D, Point3D, Segment2D, Segment3D
            
        :return: For point, True if the point lies on one of the segments; otherwise False. 
            For segment, True if the segment start and endpoints are on one of the the segments; otherwise False. 
        :rtype: bool
        
        :Example:
    
        .. code-block:: python
           
           # 2D example
           >>> sgmts = Segments(Segment2D(Point2D(0,0), Point2D(1,0)))
           >>> result = sgmts.contains_point(Point2D(2,0))
           >>> print(result)
           False
           
        """
        for s in self.segments:
            if point in s:
                return True
        return False
    
    
    def difference_segments(self,segments):
        """Returns the difference between this segments sequence and the supplied segments sequence.
        
        :param segments: A segments sequence.
        :type segments: Segments
            
        :return: Any parts of this segments sequence which are not also part of the segments in the supplied sequence.
        :rtype: Segments
        
        :Example:
    
        .. code-block:: python
        
            >>> sgmts1 = Segments(Segment2D(Point2D(0,0), Point2D(1,0)))
            >>> sgmts2 = Segments(Segment2D(Point2D(0.5,0), Point2D(1,0)))
            >>> result = sgmts1.difference_segments(sgmts2)
            >>> print(result)
            Segments(Segment2D(Point2D(0,0), Point2D(0.5,0)))
        
        """
        diff_segments=Segments()
        for s in self:
            #print(s)
            #print(segments)
            result=s.difference_segments(segments)
            #print(result)
            if result:
                for s1 in result:
                    diff_segments.append(s1)
        if len(diff_segments)==0:
            return Segments() #None
        else:
            return diff_segments
    
    
    def intersect_halfline(self,halfline):
        """Returns the intersection of this segments sequence and a halfline.
        
        :param halfline: A halfline.
        :type halfline: Halfline2D, Halfline3D
        
        :return: A tuple of intersection points and intersection segments 
            (Points,Segments)
        :rtype: tuple
            
        """
        ipts=Points()
        isegments=Segments()
        for s in self:
            result=s.intersect_halfline(halfline)
            if result is None:
                continue
            elif result.classname=='Point':
                ipts.append(result,unique=True)
            elif result.classname=='Segment':
                isegments.append(result,unique=True)
            else:
                raise Exception
        
        # remove points which exist in the segments
        ipts=ipts.remove_points_in_segments(isegments)
        
        return ipts, isegments
    
    
    def intersect_line(self,line):
        """Returns the intersection of this segments sequence and a line.
        
        :param line: A line.
        :type line: Line2D, Line3D
        
        :return: A tuple of intersection points and intersection segments 
            (Points,Segments)
        :rtype: tuple
            
        """
        ipts=Points()
        isegments=Segments()
        for s in self:
            result=s.intersect_line(line)
            if result is None:
                continue
            elif result.classname=='Point':
                ipts.append(result,unique=True)
            elif result.classname=='Segment':
                isegments.append(result,unique=True)
            else:
                raise Exception
        
        # remove points which exist in the segments
        ipts=ipts.remove_points_in_segments(isegments)
        
        return ipts, isegments
    
    
    def intersect_segment(self,segment):
        """Returns the intersection of this segments sequence and a segment.
        
        :param segment: A segment.
        :type segment: Segment2D, Segment3D
        
        :return: A tuple of intersection points and intersection segments 
            (Points,Segments)
        :rtype: tuple
            
        """
        ipts=Points()
        isegments=Segments()
        for s in self:
            result=s.intersect_segment(segment)
            if result is None:
                continue
            elif result.classname=='Point':
                ipts.append(result,unique=True)
            elif result.classname=='Segment':
                isegments.append(result,unique=True)
            else:
                raise Exception
        
        # remove points which exist in the segments
        ipts=ipts.remove_points_in_segments(isegments)
        
        return ipts, isegments
        
    
    def intersect_segments(self,segments):
        """Returns the intersection of this segments sequence and another segments sequence.
        
        :param segments: A segments sequence.
        :type segments: Segments
        
        :return: A tuple of intersection points and intersection segments 
            (Points,Segments)
        :rtype: tuple
            
        """
        ipts=Points()
        isegments=Segments()
        for s in segments:
            result_ipts,result_isegments=self.intersect_segment(s)
            for pt in result_ipts:
                ipts.append(pt,unique=True)
            for s1 in result_isegments:
                isegments.append(s1,unique=True)
        
        # remove points which exist in the segments
        ipts=ipts.remove_points_in_segments(isegments)
        
        return ipts, isegments
    
    
    def project_2D(self,coordinate_index):
        """Projection of a sequence of 3D segments as a sequence of 2D segments.
        
        :param coordinate_index: The index of the coordinate to ignore.
            Use coordinate_index=0 to ignore the x-coordinate, coordinate_index=1 
            for the y-coordinate and coordinate_index=2 for the z-coordinate.
        :type coordinate_index: int
        
        :return: A 2D segment sequence based on the projection of the 3D segment sequece.
        :rtype: Segments
               
        :Example:
    
        .. code-block:: python
        
            >>> sgmts = Segments(Segment3D(Point3D(0,0,0), Point3D(1,2,3)))
            >>> result = sgmts.project_2D(0)
            >>> print(result)
            Segments(Segment2D(Point2D(0,0), Point2D(2,3)))
        
        """
        segments=[s.project_2D(coordinate_index) for s in self]
        return Segments(*segments)
    
    
    def project_3D(self,plane,coordinate_index):
        """Projection of sequence of 2D segment on a 3D plane.
        
        :param plane: The plane for the projection
        :type plane: Plane3D
        :param coordinate_index: The index of the coordinate which was ignored 
            to create the 2D projection. For example, coordinate_index=0
            means that the x-coordinate was ignored and this point
            was originally projected onto the yz plane.
        :type coordinate_index: int
        
        :return: 3D segment sequence which has been projected from the 2D segment sequence.
        :rtype: Segments
               
        :Example:
    
        .. code-block:: python
        
            >>> sgmts = Segments(Segment2D(Point2D(0,0), Point2D(1,0)))
            >>> pl = Plane3D(Point3D(0,0,1), Vector3D(0,0,1))
            >>> result = sgmts.project_3D(pl, 2)
            Segments(Segment3D(Point3D(0,0,1),Point3D(1,0,1)))
        
        """
        segments=[s.project_3D(plane,coordinate_index) for s in self]
        return Segments(*segments)
    
    
    # @property
    # def polyline(self):
    #     """Returns a polyline of the segments
        
    #     :return result:
    #     :rtype: Polyline or None
        
    #     """
        
    #     pl=self[0].polyline
    #     remaining_segments=Segments(*self[1:])
        
    #     while len(remaining_segments)>0:
    #         try:
    #             pl,remaining_segments=remaining_segments.union_polyline(pl)
    #         except TypeError:
    #             return None
            
    #     return pl
    
    
    def remove_segments_in_polygons(self,polygons):
        """Removes any segments that lie on any of the polygons' segments
        """
        segments=[s for s in self if not s in polygons.segments]
        return Segments(*segments)
    
    
    # @property
    # def union(self):    
    #     """Returns a Segments sequence 
        
    #     :return result: 
    #         - note multiple solutions are possible, only the first is returned
    #     :rtype Segments
        
    #     """
    #     segments=[s for s in self]
    #     n=len(segments)
    #     i=0
        
    #     while i<n-1:
    #         s=segments[i]
    #         j=i+1
    #         while j<n:
    #             s1=segments[j]
    #             u=s.union(s1)
    #             if s.is_collinear(s1) and not u is None:
    #                 segments[i]=s.__class__(u.points[0],u.points[-1]) # as u is a polyline
    #                 segments.pop(j)
    #                 break
    #             j+=1
    #         else:
    #             i+=1
    #         n=len(segments)
    #     return Segments(*segments)
    
    
    # def union_polyline(self,polyline):
    #     """Returns the first union of a segment in the sequence with the polyline
        
    #     :return result: (union_result (Polyline),
    #                      Segments sequence of remaining segments)
        
    #     """
    #     segments=[s for s in self]
    #     for i in range(len(segments)):
    #         u=polyline.union(segments[i].polyline)
    #         if u:
    #             segments.pop(i)
    #             return u,Segments(*segments)
    
    #     return None
    
    
    # def union_segment(self,segment):
    #     """Returns the first union of a segment in the sequence with the supplied segment
        
    #     :return result: (union_result (Polyline),
    #                      Segments sequence of remaining segments)
        
    #     """
    #     segments=[s for s in self]
    #     for i in range(len(segments)):
    #         u=segments[i].union(segment)
    #         if u:
    #             segments.pop(i)
    #             return u,Segments(*segments)
    
    #     return None
    
    
    
    # @property
    # def polylines(self):    
    #     """Returns the polylines that exist in the Segments sequence
        
    #     :return result: - 
    #         - each polyline can have one or more than one segments
    #     :rtype Polylines:
        
    #     """
        
    #     p=Polylines(*[s.polyline for s in self])
    #     return p.consolidate
    
        
   
        
        
        
        