# -*- coding: utf-8 -*-

from collections.abc import Sequence
from .segments import Segments


class Polylines(Sequence):
    """A sequence of polylines.    
    
    :param polylines: A sequence of Polyline2D or Polyline3D instances. 
        
    :Example:
        
    .. code-block:: python
        
        >>> pls = Polylines(Polyline2D(Point2D(0,0), Point2D(1,0)))                       
        >>> print(pls)
        Polylines(Polyline2D(Point2D(0,0), Point2D(1,0)))
        
        >>> print(pls[0])
        Polyline2D(Point2D(0,0), Point2D(1,0))
    """
    
    def __init__(self,*polylines):
        ""
        self._polylines=list(polylines)
        
        
    def __eq__(self,polylines):
        """Tests if this polylines sequence and the supplied polylines sequence are equal.
        
        :param polylines: The polylines sequence to be tested.
        :type polylines: Polylines
        
        :return: True if the polylines items are equal, otherwise False.
        :rtype: bool
        
        :Example:
    
        .. code-block:: python
        
            >>> pls1 = Polylines(Polyline2D(Point2D(0,0), Point2D(1,0)))  
            >>> pls2 = Polylines(Polyline2D(Point2D(0,0), Point2D(1,0)))  
            >>> result = pls1 == pls2
            >>> print(result)
            True
            
        """
        if isinstance(polylines,Polylines) and self._polylines==polylines._polylines:
            return True
        else:
            return False
        
        
    def __getitem__(self,i):
        ""
        return self._polylines[i]
        
    
    def __len__(self):
        ""
        return len(self._polylines)
    
    
    def __repr__(self):
        ""
        return 'Polylines(%s)' % ', '.join([str(s) for s in self._polylines])
    
    
    @property
    def add_all(self):
        """Adds together the polylines in the sequence where possible
        
        :return: Returns a new Polylines sequence where the polylines have been
            added together where possible to form new polylines.        
        :rtype: Polylines
        
        """
        polylines=[pl for pl in self]
        i=0
        
        while True:
            try:
                pl=polylines[i]
            except IndexError:
                break
            try:
                new_pl,index=Polylines(*polylines[i+1:]).add_first(pl)
                #print(new_s,index)
                polylines[i]=new_pl
                polylines.pop(i+index+1)
            except ValueError:
                i+=1
        
        return Polylines(*polylines)
        
    
    def add_first(self,polyline):
        """Adds the first available polyline to the supplied polyline.
        
        This iterates through the polylines in the Polylines sequence. 
            When the first polyline which can be added to the supplied polyline is found,
            the result of this addition is returned along with its index.
        
        :raises ValueError: If no valid additions are found.
        
        :return: Returns a tuple with the addition result and the index of the polyline which was added.
        :rtype: tuple (Polyline,int)
        
        :Example:
    
        .. code-block:: python
        
            >>> pls = Polylines(Polyline2D(Point2D(0,0), Point2D(1,0)))
            >>> result = pls.add_first(Polyline2D(Point2D(1,0), Point2D(2,0)))
            >>> print(result)
            (Polyline2D(Point2D(0,0), Point2D(1,0), Point2D(2,0)),0)
        
        """
        for i,pl in enumerate(self):
            try:
                result=polyline+pl
                return result,i
            except ValueError:
                pass
        
        raise ValueError
        
    
    
    def append(self,polyline,unique=False):
        """Appends supplied polyline to this polylines sequence.
        
        :param polyline: The polyline to be appended.
        :type polyline: Polyline2D or Polyline3D
        :param unique: If True, polyline is only appended if it does not already
            exist in the sequence; defaults to False.
        :type unique: bool
        
        :rtype: None
        
        :Example:
    
        .. code-block:: python
        
            >>> pls = Polylines(Polyline2D(Point2D(0,0), Point2D(1,0)))
            >>> pls.append(Polyline2D(Point2D(1,0), Point2D(2,0)))
            >>> print(pls)
            Polylines(Polyline2D(Point2D(0,0), Point2D(1,0)),
                      Polyline2D(Point2D(1,0), Point2D(2,0)))
        
        """
        if polyline.classname=='Polyline':
            if unique:
                if not polyline in self:
                    self._polylines.append(polyline)
            else:
                self._polylines.append(polyline)
                
        else:
            raise TypeError
    
    
    @property
    def segments(self):
        """Returns a Segments sequence of all the segments of the polygons.
        
        :rtype: Segments
        
        :Example:
    
        .. code-block:: python
        
            >>> pls = Polylines(Polyline2D(Point2D(0,0), Point2D(1,0)))
            >>> print(pls.segments)
            Segments(Segment2D(Point2D(0,0), Point2D(1,0)))
        
        """
        segments=Segments()
        for pl in self:
            for s in pl.segments:
                segments.append(s,unique=True)
        return segments
    
    
    
    # @property
    # def consolidate(self):    
    #     """Returns a Polylines sequence with the same segments but a minimum number of polylines
        
    #     :return result: 
    #         - each polyline can have one or more segments
    #         - note there may be multiple solutions, only the first solution is returned
        
    #     :rtype Polylines
        
    #     """
    #     polylines=[pl for pl in self]
    #     n=len(polylines)
    #     i=0
        
    #     while i<n-1:
            
    #         pl=polylines[i]
    #         j=i+1
            
    #         while j<n:
                
    #             u=pl.union(polylines[j])
                
    #             if not u is None:
    #                 polylines[i]=u
    #                 polylines.pop(j)
    #                 break
                
    #             j+=1

    #         else:
    #             i+=1
                    
    #         n=len(polylines)
           
    #     return Polylines(*polylines)
        
    
    
        
        
        
        
        
        
        
        
        