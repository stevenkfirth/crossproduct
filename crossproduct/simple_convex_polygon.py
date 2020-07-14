# -*- coding: utf-8 -*-


from .segment import Segment2D, Segment3D
from .segments import Segments
from .simple_polygon import SimplePolygon2D, SimplePolygon3D
from .points import Points


class SimpleConvexPolygon():
    """A n-D convex polygon
    """
    
    classname='SimpleConvexPolygon'
    #superclassname='SimpleConvexPolygon'


class SimpleConvexPolygon2D(SimpleConvexPolygon,SimplePolygon2D):
    """A 2D convex polygon
    
    """
    
    dimension='2D'
    
    def __init__(self,*points):
        """
        
        param points: an array of points 
            - the first point is not repeated at the end of the array
        
        """
        
        SimplePolygon2D.__init__(self,*points)
        
        # converts the convex polygon to a counterclockwise orientation 
        #   this is done to enable the intersection algorithms to work
        if self.orientation<0:
            self.points=self.reverse.points
        
    
    def __repr__(self):
        """The string of this line for printing
        
        :return result:
        :rtype str:
            
        """
        return 'SimpleConvexPolygon2D(%s)' % ','.join([str(p) for p in self.points])
       
        
    @property
    def class_3D(self):
        return SimpleConvexPolygon3D
    
        
    def difference_simple_convex_polygon(self,simple_convex_polygon):
        """The difference between this 2D simple convex polygon and another
        
        :param simple_convex_polygon SimpleConvexPolygon: a simple convex polygon 
        
        :return result:
            - None
            - SimplePolygon
        
        """
        
        if self==simple_convex_polygon:
            return None

        result=self.intersect_simple_convex_polygon(simple_convex_polygon)
        
        if result is None or result.classname=='Point' or result.classname=='Segment':
            return self # returns the polygon -  no intersection

        elif isinstance(result,SimpleConvexPolygon):
            
            pl1=self.polyline.segments.difference_segments(result.polyline.segments).polyline # Segments
            
            #print(result.polyline.segments)
            #print(self.polyline.segments)
            #print('pl1',pl1)
            pl2=result.polyline.segments.difference_segments(self.polyline.segments).polyline
            pl3=pl1.union(pl2)
            return SimplePolygon2D(*pl3.points[:-1])
        
        # NOTE  THIS COULD RETURN MORE THAT ONE POLYGON
    
    
    def intersect_halfline(self,halfline):
        """Intersection of this convex polygon with a halfline
        
        :param halfline Halfline2D: a 2D halfline 
        
        :return intersection:
            - return value can be:
                - None -> no intersection (for a halfline which does not intersect the polygon)
                - Point2D -> a point (for a halfline which intersects the polygon at a single vertex)
                - Segment2D -> a segment 
                    - (for a halfline which intersects the polygon at 2 edges)
                    - (for a halfline which starts inside the polygon and intersects one edge)
        
        """
        result=self.intersect_line_t_values(halfline.line)
        #print(result)
        if result is None:
            return None 
        elif result[0]==result[1]:
            try:
                return halfline.calculate_point(result[0])
            except ValueError:
                return None
        else:
            try:
                P0=halfline.calculate_point(result[0])
            except ValueError:
                P0=halfline.calculate_point(0)
            try:
                P1=halfline.calculate_point(result[1])
            except ValueError:
                return None
            if P0==P1:
                return P0
            else:
                return Segment2D(P0,P1)
        
        
    def intersect_line(self,line):
        """Intersection of this convex polygon with a line
        
        :param line Line2D: a 2D line 
        
        :return intersection:
            - return value can be:
                - None -> no intersection (for a line which does not intersect the polygon)
                - Point2D -> a point (for a lien which intersects the polygon at a single vertex)
                - Segment2D -> a segment (for a line which intersects the polygon at 2 edges)
        
        """
        result=self.intersect_line_t_values(line)
        if result is None:
            return None
        elif result[0]==result[1]:
            return line.calculate_point(result[0])
        else:
            P0=line.calculate_point(result[0])
            P1=line.calculate_point(result[1])
            return Segment2D(P0,P1)
        
    
    def intersect_line_t_values(self,line):
        """Returns t values of the intersection of this convex polygon with a line
        
        :param line Line2D: a 2D line 
        
        :return t_values list: list of t values
            - None -> no intersection (for a line which does not intersect the polygon)
            - tuple with two items 
                - (for a line which intersects the polygon at a single vertex - items are the same point)
                - (for a line which intersects the polygon at 2 edges)
        
        
        """
        t_entering=[]
        t_leaving=[]
        for ps in self.polyline.segments:
            #print(ps)
            
            ev=ps.vL # edge vector
            n=ev.perp_vector*-1 #  normal to edge vector facing outwards
            try:
                t=(ps.P0-line.P0).dot(n) / line.vL.dot(n) # the t values of the line where the segment and line intersect
                
            except ZeroDivisionError: # the line and polygon segment are parallel
                if (line.P0-ps.P0).dot(n) > 0: # test if the line is outside the edge
                    #print('line is outside the edge')
                    return None # line is outside of the edge, there is no intersection with the polygon
                else:
                    continue # line is inside of the edge, ignore this segment and continue with others
            
            if line.vL.dot(n)<0:
                t_entering.append(t)
            else:
                t_leaving.append(t)
            
        t_entering_max=max(t_entering) # the line enters the polygon at the maximum t entering value
        
        t_leaving_min=min(t_leaving) # the line leaves the polygon at the minimum t leavign value
        
        if t_entering_max > t_leaving_min:
            
            return None
        
        else:
            
            return t_entering_max,t_leaving_min
        
                
    def intersect_segment(self,segment):
        """Intersection of this convex polygon with a segment
        
        :param segment Segment2D: a 2D segment 
        
        :return intersection:
            - return value can be:
                - None -> no intersection (for a segment which does not intersect the polygon)
                - Point2D -> a point (for a segment which intersects the polygon at a single vertex)
                - Segment2D -> a segment 
                    - (for a segment which intersects the polygon at 2 edges)
                    - (for a segment which starts or ends inside the polygon and intersects one edge)
        
        """
        result=self.intersect_line_t_values(segment.line)
        #print(result)
        if result is None:
            return None 
        elif result[0]==result[1]:
            try:
                return segment.calculate_point(result[0]) 
            except ValueError:
                return None 
        else:
            t0=result[0]
            t1=result[1]
            if t0<0 and t1<0:
                return None 
            elif t0>1 and t1>1:
                return None 
            else:
                try:
                    P0=segment.calculate_point(result[0])
                except ValueError:
                    P0=segment.calculate_point(0)
                try:
                    P1=segment.calculate_point(result[1])
                except ValueError:
                    P1=segment.calculate_point(1)   
                    
                if P0==P1:
                    return P0 
                else:
                    return Segment2D(P0,P1)    
    
    
    def intersect_segments(self,segments):
        """Intersection of this polygon with a Segments sequence
        
        :return result: (Points,Segments)
            - points which exist in segments are not returned
        
        """
        ipts=Points()
        isegments=Segments()
        for s in segments:
            result=self.intersect_segment(s)
            #print(result)
            if result is None:
                continue
            if result.classname=='Point':
                ipts.append(result,unique=True)
            elif result.classname=='Segment':
                isegments.append(result,unique=True)
            else:
                raise Exception
                
        ipts.remove_points_in_segments(isegments)
        return ipts,isegments
    
    
    def intersect_simple_convex_polygon(self,simple_convex_polygon):
        """Intersection of this 2D simple convex polygon with another 2D simple convex polygon
        
        :param simple_convex_polygon SimpleConvexPolygon: a simple convex polygon 
        
        :return intersection:
            - return value can be:
                - None -> no intersection (for a convex polygon whose segements 
                                           do not intersect the segments of this
                                           convex polygon)
                - Point2D -> a point (for a convex polygon whose segments intersect
                                      this convex polygon at a single vertex)
                - Segment2D -> a segment (for a convex polygon whose segments
                                          intersect this convex polygon at an edge segment)
                - SimpleConvexPolygon2D - > a simple convex polygon (for a convex
                                            polygon which overlaps this polygon)
                         
        """
        ipts1,isegments1=self.intersect_segments(simple_convex_polygon.polyline.segments)
        #print(ipts1,isegments1)
        
        if len(ipts1)==0 and len(isegments1)==0:
            return None # returns None - no intersection
        elif len(ipts1)==1 and len(isegments1)==0:
            return ipts1[0] # returns a Point2D - point intersection
        elif len(ipts1)>1:
            raise Exception
        elif len(ipts1)==0 and len(isegments1)==1:
            return isegments1[0] # returns a Segment2D - edge segment intersection
        else: # a simple complex polygon intersection
            ipts2,isegments2=simple_convex_polygon.intersect_segments(self.polyline.segments)
            #print(ipts2,isegments2)
            for s in isegments2:
                isegments1.append(s,unique=True)
            pl=isegments1.polyline
            #print(pl)
            pg=SimpleConvexPolygon2D(*pl.points[:-1])
            return pg
    
    
    def intersect_simple_polygon(self,simple_polygon):
        """
        """
        if isinstance(simple_polygon,SimpleConvexPolygon):
            return self.intersect_simple_convex_polygon(simple_polygon)
        else:
            return simple_polygon.intersect_simple_convex_polygon(self)
    
    
            
class SimpleConvexPolygon3D(SimpleConvexPolygon,SimplePolygon3D):
    """A 3D convex polygon
    """
    
        
    def __repr__(self):
        """The string of this line for printing
        
        :return result:
        :rtype str:
            
        """
        return 'SimpleConvexPolygon3D(%s)' % ','.join([str(p) for p in self.points])
    
    
    @property
    def class_2D(self):
        return SimpleConvexPolygon2D   
    
    
    def intersect_halfline(self,halfline):
        """Returns the intersection of this 3D polygon and a halfline
        
        :param line Halfline3D: a 3D halfline 
        
        :return result:
            - no intersection (None): 
                - for parallel, non-coplanar polygon plane and halfline
                - for skew polygon plane and halfline which do not intersect
            - a segment:
                - for a coplanar halfline which intersects the polygon at two points
            - a point: 
                - for a halfline skew to the polygon plane which intersects the polygon at a point
                - for a coplanar halfline which intersects the polygon one point
        
        """
        result=self.plane.intersect_halfline(halfline) # intersection of convex polygon plane with halfline
        
        if result is None:
            return None
        
        elif result.classname=='Point':
            if result in self:
                return result
            else:
                return None
            
        elif result.classname=='Halfline': # coplanar, look for intersections on 2D plane
            
            i,self2D=self.project_2D
            halfline2D=halfline.project_2D(i)
            
            result=self2D.intersect_halfline(halfline2D)
            
            if result is None: 
                return None
            else:
                return result.project_3D(self.plane,i)
            
            
    def intersect_line(self,line):
        """Returns the intersection of this polygon and a line
        
        :param line Line3D: a 3D line 
        
        :return result:
            - no intersection (None): 
                - for parallel, non-coplanar polygon plane and line
                - for skew polygon plane and line which do not intersect
            - a segment:
                - for a coplanar line which intersects the polygon at two points
            - a point: 
                - for a line skew to the polygon plane which intersects the polygon at a point
                - for a coplanar line which intersects the polygon at a vertex
        
        """
        result=self.plane.intersect_line(line) # intersection of convex polygon plane with line
        #print(result)
        
        if result is None:
            return None
        
        elif result.classname=='Point':
            if result in self:
                return result
            else:
                return None
            
        elif result.classname=='Line': # coplanar, look for intersections on 2D plane
            
            i,self2D=self.project_2D
            line2D=line.project_2D(i)
            
            ipts,isegments=self2D.intersect_line(line2D)
            
            if result is None: 
                return None
            else:
                return result.project_3D(self.plane,i)
            
            
    def intersect_plane(self,plane):
        """Returns the intersection of this 3D simple convex polygon and a plane
        
        :param plane Plane3D: a 3D plane 
        
        :return result:
            - no intersection (None): 
                - for parallel, non-coplanar 3D simple convex polygon and plane
                - for skew 3D simple convex polygon and plane which do not intersect
            - a polygon:
                - for coplanar 3D simple convex polygon and plane
            - a segment:
                - for 3D simple convex polygon which intersects the plane at two points
            - a point: 
                - for 3D simple convex polygon which intersects the plane at one point
        
        """
        if self.plane==plane:
            return self
        
        elif self.plane.is_parallel(plane):
            return None
        
        else:
        
            ipts,isegments=plane.intersect_segments(self.polyline.segments)
            
            if len(ipts)==0 and len(isegments)==0: # no intersections
                return None
            elif len(ipts)==1: # point intersection
                return ipts[0]
            elif len(ipts)==2: # segment intersection
                return Segment3D(ipts[0],ipts[1])
            elif len(isegments)==1: # segment intersection on a polygon edge
                return isegments[0]
            else:
                raise Exception
            
    
    def intersect_segment(self,segment):
        """Returns the intersection of this polygon and a segment
        
        :param line Segment3D: a 3D segment 
        
        :return result:
            - no intersection (None): 
                - for parallel, non-coplanar polygon plane and segment
                - for skew polygon plane and segment which do not intersect
            - a segment:
                - for a coplanar segment which intersects the polygon at two points
                - for a coplanar segment which is inside the polygon
            - a point: 
                - for a segment skew to the polygon plane which intersects the polygon at a point
                - for a coplanar segment which intersects the polygon one point
        
        """
        result=self.plane.intersect_segment(segment) # intersection of triangle plane with segment
        
        if result is None:
            return None
        
        elif result.classname=='Point':
            if result in self:
                return result
            else:
                return None
            
        elif result.classname=='Segment': # coplanar, look for intersections on 2D plane
            
            i,self2D=self.project_2D
            segment2D=segment.project_2D(i)
            
            ipts,isegments=self2D.intersect_segment(segment2D)
            
            if result is None: 
                return None
            else:
                return result.project_3D(self.plane,i)
            

    def intersect_simple_convex_polygon_coplanar(self,simple_convex_polygon):
        """Intersection of this polygon with another coplanar polygon
        
        """
        i,self_2D=self.project_2D
        i,scp_2D=simple_convex_polygon.project_2D
        
        result=self_2D.intersect_simple_convex_polygon(scp_2D)
    
        if result is None: 
            return None
        else:
            return result.project_3D(self.plane,i)
        
    
    def intersect_simple_convex_polygon_skew(self,simple_convex_polygon):
        """Intersection of this polygon with another skew polygon
        
        """
        result=self.intersect_plane(simple_convex_polygon.plane)
        
        if result is None:
            return None
        
        else:
        
            i,scp_2D=simple_convex_polygon.project_2D
            result_2D=result.project_2D(i)
            
            if result_2D.classname=='Point':
            
                if result_2D in scp_2D:
                    return result
                else:
                    return None
                
            elif result_2D.classname=='Segment':
                
                result2=scp_2D.intersect_segment(result_2D)
                
                if result2 is None:
                    return None
                else:
                    return result2.project_3D(simple_convex_polygon.plane,i)
                   
        
    def intersect_simple_convex_polygon(self,simple_convex_polygon):
        """Intersection of this simple convex polygon with another convex simple polygon
        
        :param simple_convex_polygon SimpleConvexPolygon: a simple convex polygon 
        
        :return intersection:
            - return value can be:
                - if the two polygons are on the same plane:
                    - None -> no intersection (for a convex polygon whose segements 
                                           do not intersect the segments of this
                                           convex polygon)
                    - Point3D -> a point (for a convex polygon whose segments intersect
                                      this convex polygon at a single vertex)
                    - Segment3D -> a segment (for a convex polygon whose segments
                                          intersect this convex polygon at an edge segment)
                    - SimpleConvexPolygon3D - > a simple convex polygon (for a convex
                                            polygon which overlaps this polygon)
                
                - if the two polygons are on skew planes
                    - None -> no intersection
                    - Point3D -> for two polygons which intersect at a single point
                    - Segment3D -> for two polygons that intersect along a segment
                         
        """
        if self.plane==simple_convex_polygon.plane:
            
            return self.intersect_simple_convex_polygon_coplanar(simple_convex_polygon)
            
        else: # polygons exist in different planes
            
            return self.intersect_simple_convex_polygon_skew(simple_convex_polygon)
                    
                    
                    
                 
            
    
    




        
    
    
    
    
    
    
    
    
    
    
    

            
    
    