# -*- coding: utf-8 -*-


from collections.abc import Sequence
from .points import Points
from .polylines import Polylines


class Segments(Sequence):
    """A sequence of segments    
    
    """
    
    def __init__(self,*segments):
        """
        """
    
        self.segments=list(segments)
        
        
    def __eq__(self,obj):
        """
        """
        if isinstance(obj,Segments) and self.segments==obj.segments:
            return True
        else:
            return False
        
        
        
    def __getitem__(self,i):
        """
        """
        return self.segments[i]
        
    
    def __len__(self):
        """
        """
        return len(self.segments)
    
    
    def __repr__(self):
        """The string of this segment for printing
        
        :return result:
        :rtype str:
            
        """
        return 'Segments(%s)' % ', '.join([str(s) for s in self.segments])
    
    
    def append(self,segment,unique=False):
        """
        """
        if segment.classname=='Segment':
            if unique:
                if not segment in self:
                    self.segments.append(segment)
            else:
                self.segments.append(segment)
                
        else:
            raise TypeError
    
    
    def difference_segment(self,segment):
        """Returns the difference between this segments sequence and self.
        
        

        """
        
        def rf(result,segments):
            if len(segments)==0:
                return result
            else:
                diff=result.difference_segment(segments[0])
                #print('diff',diff)
                if diff is None:
                    return None
                elif len(diff)==1:
                    if len(segments)>1:
                        result=rf(diff[0],segments[1:])
                    else:
                        result=diff[0],
                    return result
                elif len(diff)==2:
                    if len(segments)>1:
                        result=tuple(list(rf(diff[0],segments[1:]))+list(rf(diff[1],segments[1:])))
                    else:
                        result=diff[0],diff[1]
                    return result
                else:
                    raise Exception
                
        result=segment
        result=rf(result,self)
        return result
    
    
    def difference_segments(self,segments):
        """Returns the difference between self and segments
        
        :param segments Segments:
            
        :return result:
        :rtype Segments:
        
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
            return None
        else:
            return diff_segments
    
    
    def intersect_halfline(self,halfline):
        """Returns the intersection of this segments sequence and a halfline
        
        :param halfline Halfline: a halfline
        
        :return (ipts,isegments): (tuple of intersetion points, 
                                   tuple of intersection segments)
        :rtype tuple:
            
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
        ipts.remove_points_in_segments(isegments)
        
        return ipts, isegments
    
    
    def intersect_line(self,line):
        """Returns the intersection of this segments sequence and a line
        
        :param line Line: a line
        
        :return (ipts,isegments): (tuple of intersetion points, 
                                   tuple of intersection segments)
        :rtype tuple:
            
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
        ipts.remove_points_in_segments(isegments)
        
        return ipts, isegments
    
    
    def intersect_point(self,point):
        """Test if the point intersects with any of the segments
        
        :return result:
        :rtype bool:        
        
        """
        for s in self:
            if point in s:
                return True
        return False
    
    
    def intersect_segment(self,segment):
        """Returns the intersection of this segments sequence and a segment
        
        :param segment Segment: a segment
        
        :return (ipts,isegments): (tuple of intersetion points, 
                                   tuple of intersection segments)
        :rtype tuple:
            
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
        ipts.remove_points_in_segments(isegments)
        
        return ipts, isegments
        
    
    def intersect_segments(self,segments):
        """Returns the intersection of this segments sequence and another segments sequence
        
        :param segments Segments: a segments sequence
        
        :return (ipts,isegments): (tuple of intersetion points, 
                                   tuple of intersection segments)
        :rtype tuple:
            
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
        ipts.remove_points_in_segments(isegments)
        
        return ipts, isegments
    
    
    def project_2D(self,i):
        """Returns a projection of the segments on a 2D plane
        
        :param i int: the index of the coordinate which was ignored to create the 2D projection
        
        :return result:
               
        """
        segments=[s.project_2D(i) for s in self]
        return Segments(*segments)
    
    
    def project_3D(self,plane,i):
        """Returns a projection of the segments on a 3D plane
        
        :param plane Plane3D: the plane for the projection
        :param i int: the index of the coordinate which was ignored to create the 2D projection
        
        :return result:
               
        """
        segments=[s.project_3D(plane,i) for s in self]
        return Segments(*segments)
    
    
    @property
    def polyline(self):
        """Returns a polyline of the segments
        
        :return result:
        :rtype: Polyline or None
        
        """
#        # first union
#        s=self[0]
#        try:
#            pl,remaining_segments=Segments(*self[1:]).union_segment(s)
#        except TypeError:
#            return None
        
        pl=self[0].polyline
        remaining_segments=Segments(*self[1:])
        
        while len(remaining_segments)>0:
            try:
                pl,remaining_segments=remaining_segments.union_polyline(pl)
            except TypeError:
                return None
            
        return pl
    
    
    def remove_segments_in_polygons(self,polygons):
        """Removes any segments that lie on any of the polygons' segments
        """
        self.segments=[s for s in self if not s in polygons.segments]
    
    
    @property
    def union(self):    
        """Returns a Segments sequence 
        
        :return result: 
            - note multiple solutions are possible, only the first is returned
        :rtype Segments
        
        """
        segments=[s for s in self]
        n=len(segments)
        i=0
        
        while i<n-1:
            s=segments[i]
            j=i+1
            while j<n:
                s1=segments[j]
                u=s.union(s1)
                if s.is_collinear(s1) and not u is None:
                    segments[i]=s.__class__(u.points[0],u.points[-1]) # as u is a polyline
                    segments.pop(j)
                    break
                j+=1
            else:
                i+=1
            n=len(segments)
        return Segments(*segments)
    
    
    def union_polyline(self,polyline):
        """Returns the first union of a segment in the sequence with the polyline
        
        :return result: (union_result (Polyline),
                         Segments sequence of remaining segments)
        
        """
        segments=[s for s in self]
        for i in range(len(segments)):
            u=polyline.union(segments[i].polyline)
            if u:
                segments.pop(i)
                return u,Segments(*segments)
    
        return None
    
    
    def union_segment(self,segment):
        """Returns the first union of a segment in the sequence with the supplied segment
        
        :return result: (union_result (Polyline),
                         Segments sequence of remaining segments)
        
        """
        segments=[s for s in self]
        for i in range(len(segments)):
            u=segments[i].union(segment)
            if u:
                segments.pop(i)
                return u,Segments(*segments)
    
        return None
    
    
    
    @property
    def polylines(self):    
        """Returns the polylines that exist in the Segments sequence
        
        :return result: - 
            - each polyline can have one or more than one segments
        :rtype Polylines:
        
        """
        
        p=Polylines(*[s.polyline for s in self])
        return p.consolidate
    
        
        
        
        
        
        
        