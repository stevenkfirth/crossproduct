# -*- coding: utf-8 -*-


from collections.abc import Sequence
from .points import Points
#from .polylines import Polylines


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
        
    
    def __eq__(self,segments):
        """Tests if this segments sequence and the supplied segments sequence are equal.
        
        :param segments: The segments sequence to be tested.
        :type segments: Segments
        
        :return: True if the sequence items are equal, otherwise False.
        :rtype: bool
        
        :Example:
    
        .. code-block:: python
        
            >>> sgmts1 = Segments(Segment2D(Point2D(0,0), Point2D(1,0)))
            >>> sgmts2 = Segments(Segment2D(Point2D(0,0), Point2D(1,0)))
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
    
    
    @property
    def add_all(self):
        """Adds together the segments in the sequence where possible
        
        :return: Returns a new Segments sequence where the segments have been
            added together where possible to form new segments.        
        :rtype: Segments
        
        """
        segments=[s for s in self]
        i=0
        
        while True:
            try:
                s=segments[i]
            except IndexError:
                break
            try:
                new_s,index=Segments(*segments[i+1:]).add_first(s)
                #print(new_s,index)
                segments[i]=new_s
                segments.pop(i+index+1)
            except ValueError:
                i+=1
        
        return Segments(*segments)
        
    
    def add_first(self,segment):
        """Adds the first available segment to the supplied segment.
        
        This iterates through the segments in the Segments sequence. 
            When the first segment which can be added to the supplied segment is found,
            the result of this addition is returned along with its index.
        
        :raises ValueError: If no valid additions are found.
        
        :return: Returns a tuple with the addition result and the index of the segment which was added.
        :rtype: tuple (Segment,int)
        
        :Example:
    
        .. code-block:: python
        
            >>> sgmts = Segments(Segment2D(Point2D(0,0), Point2D(1,0)))
            >>> result = sgmts.add_first(Segment2D(Point2D(1,0), Point2D(2,0)))
            >>> print(result)
            (Segment2D(Point2D(0,0), Point2D(2,0)),0)
        
        """
        for i,s in enumerate(self):
            try:
                result=segment+s
                return result,i
            except ValueError:
                pass
        
        raise ValueError
    
    
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
        for s in self._segments:
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
    
    
    def remove_segments_in_polygons(self,polygons):
        """Removes any segments that lie on any of the polygons' segments
        """
        segments=[s for s in self if not s in polygons.polylines.segments]
        return Segments(*segments)
    
    

        