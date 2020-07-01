# -*- coding: utf-8 -*-

from .halfline import Halfline2D, Halfline3D
from .line import Line2D, Line3D
from .segment import Segment, Segment2D, Segment3D
from .simple_polygon import SimplePolygon2D, SimplePolygon3D
from .simple_polyline import SimplePolyline,SimplePolyline2D, SimplePolyline3D
from .point import Point,Point2D, Point3D
from .plane import Plane3D
from .vector import Vector2D


class SimpleConvexPolygon():
    """A n-D convex polygon
    """

class SimpleConvexPolygon2D(SimplePolygon2D):
    """A 2D convex polygon
    
    """
    
    def __init__(self,*points):
        """
        
        param points: an array of points 
            - the first point is not repeated at the end of the array
        
        """
        
         # converting to a polyline checks for point types and adjacent segment collinearity
        pl=SimplePolyline(*points,points[0])
        
        self.points=tuple(pl.points[:-1])
    
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
        if len(result)==0:
            return None
        elif len(result)==1:
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
        if len(result)==0:
            return None
        elif len(result)==1:
            return line.calculate_point(result[0])
        else:
            P0=line.calculate_point(result[0])
            P1=line.calculate_point(result[1])
            return Segment2D(P0,P1)
        
    
    def intersect_line_t_values(self,line):
        """Returns t values of the intersection of this convex polygon with a line
        
        :param line Line2D: a 2D line 
        
        :return t_values list: list of t values
            - empty set -> no intersection (for a line which does not intersect the polygon)
            - set with single item -> (for a line which intersects the polygon at a single vertex)
            - set with two items -> (for a line which intersects the polygon at 2 edges)
        
        
        """
        t_entering=[]
        t_leaving=[]
        for ps in self.polyline.segments:
            ev=ps.vL # edge vector
            n=ev.perp_vector*-1 #  normal to edge vector facing outwards
            try:
                t=(ps.P0-line.P0).dot(n) / line.vL.dot(n) # the t values of the line where the segment and line intersect
                
            except ZeroDivisionError: # the line and polygon segment are parallel
                if (line.P0-ps.P0).dot(n) > 0: # test if the line is outside the edge
                    return [] # line is outside of the edge, there is no intersection with the polygon
                else:
                    continue # line is inside of the edge, ignore this segment and continue with others
            
            if line.vL.dot(n)<0:
                t_entering.append(t)
            else:
                t_leaving.append(t)
            
        t_entering_max=max(t_entering) # the line enters the polygon at the maximum t entering value
        
        t_leaving_min=min(t_leaving) # the line leaves the polygon at the minimum t leavign value
        
        if t_entering_max > t_leaving_min:
            
            return []
        
        if t_entering_max==t_leaving_min:
            
            return [t_entering_max]
        
        else:
            
            return [t_entering_max,t_leaving_min]
        
        
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
        if len(result)==0:
            return None
        elif len(result)==1:
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
    
    
    def intersect_convex_polygon(self,convex_polygon):
        """Intersection of this convex polygon with another convex polygon
        
        :param convex_polygon SimpleConvexPolygon2D: a 2D convex polygon 
        
        :return intersection:
            - return value can be:
                - None -> no intersection (for a convex polygon whose segements 
                                           do not intersect the segments of this
                                           convex polygon)
                - Point2D -> a point (for a convex polygon whose segments intersect
                                      this convex polygon at a single vertex)
                - SimplePolyline2D -> a polyline (for a convex polygon whose segments
                                              intesect this convex polygon) 
                         
        """
        ipoint=None
        isegments=[]
        for ps in convex_polygon.polyline.segments:
            #print('ps',ps)
            result=self.intersect_segment(ps)
            #print('result',result)
            if isinstance(result,Point2D):
                ipoint=result
            elif isinstance(result,Segment2D):
                isegments.append(result)
                
        if len(isegments)>0:
            
            # order segments
            segments=[isegments[0]]
            for i in range(1,len(isegments)):
                s=isegments[i]
                if s.P0==segments[-1].P1:
                    segments+=[s]
                else:
                    segments=[s]+segments
                    
            # convert segments to polyline
            points=[s.P0 for s in segments]
            points+=[segments[-1].P1]
            return SimplePolyline2D(*points)
        
        elif not ipoint is None:
            return ipoint
        else:
            return None
        
        
    def union_convex_polygon(self,convex_polygon):
        """Returns the union of this convex polygon with another convex polygon
        
        :param convex_polygon SimpleConvexPolygon2D: a 2D convex polygon 
        
        :return union_result:
            - return value can be:
                - None -> no intersection (for a convex polygon whose segments 
                                           do not intersect the segments of this
                                           convex polygon)
                - Point2D -> a point (for a convex polygon whose segments intersect
                                      this convex polygon at a single vertex)
                - SimplePolyline2D -> a polyline (for convex polygons tha intersect on 
                                            one or more edges)
                - SimpleConvexPolygon2d -> a convex polygon (for convex polygons that intersect and overlap)
                            
        """
        if self==convex_polygon:
            
            return self
        
        else:
        
            result=self.intersect_convex_polygon(convex_polygon)
            
            if result is None:
                return None
            
            elif isinstance(result,Point):
                return result
            
            else: # result contains a polyline
                
                result2=convex_polygon.intersect_convex_polygon(self) # this will also return a polyline
                
                if result2==result: # edge intersection
                    return result
                
                else: # overlap intersection
                    
                    points=result.points[:-1]+result2.points[:-1]
                    return SimpleConvexPolygon2D(*points)
        
        
        
class SimpleConvexPolygon3D(SimplePolygon3D):
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
        """Returns the intersection of this polygon and a halfline
        
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
        
        elif isinstance(result,Point3D):
            if result in self:
                return result
            else:
                return None
            
        elif isinstance(result,Halfline3D): # coplanar, look for intersections on 2D plane
            
            i,self2D=self.project_2D
            halfline2D=halfline.project_2D(i)
            
            result=self2D.intersect_halfline(halfline2D)
            
            if result is None:    
                return None
            
            elif isinstance(result,Point):
                
                t=halfline2D.calculate_t_from_point(result)
                return halfline.calculate_point(t)
            
            elif isinstance(result,Segment):
                
                t0=halfline2D.calculate_t_from_point(result.P0)
                t1=halfline2D.calculate_t_from_point(result.P1)
                P0=halfline.calculate_point(t0)
                P1=halfline.calculate_point(t1)
                return Segment3D(P0,P1)
                
            raise Exception
    
        else:
            raise Exception
    
    
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
        
        if result is None:
            return None
        
        elif isinstance(result,Point3D):
            if result in self:
                return result
            else:
                return None
            
        elif isinstance(result,Line3D): # coplanar, look for intersections on 2D plane
            
            i,self2D=self.project_2D
            line2D=line.project_2D(i)
            
            result=self2D.intersect_line(line2D)
            
            if result is None:    
                return None
            
            elif isinstance(result,Point):
                
                t=line2D.calculate_t_from_point(result)
                return line.calculate_point(t)
            
            elif isinstance(result,Segment):
                
                t0=line2D.calculate_t_from_point(result.P0)
                t1=line2D.calculate_t_from_point(result.P1)
                P0=line.calculate_point(t0)
                P1=line.calculate_point(t1)
                return Segment3D(P0,P1)
                
            raise Exception
    
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
        
        elif isinstance(result,Point3D):
            if result in self:
                return result
            else:
                return None
            
        elif isinstance(result,Segment3D): # coplanar, look for intersections on 2D plane
            
            i,self2D=self.project_2D
            segment2D=segment.project_2D(i)
            
            result=self2D.intersect_segment(segment2D)
            
            if result is None:    
                return None
            
            elif isinstance(result,Point):
                
                t=segment2D.calculate_t_from_point(result)
                return segment.calculate_point(t)
            
            elif isinstance(result,Segment):
                
                t0=segment2D.calculate_t_from_point(result.P0)
                t1=segment2D.calculate_t_from_point(result.P1)
                P0=segment.calculate_point(t0)
                P1=segment.calculate_point(t1)
                return Segment3D(P0,P1)
                
            raise Exception
    
        else:
            raise Exception
    
    
    def intersect_convex_polygon(self,convex_polygon):
        """Intersection of this convex polygon with another convex polygon
        
        :param convex_polygon SimpleConvexPolygon2D: a 3D convex polygon 
        
        :return result:
            - no intersection (None): 
                - for parallel, non-coplanar convex polygons
                - for skew convex polygons which do not intersect
            - a point: 
                - for skew convex polygons which intersect at a point
                - for a coplanar convex polygons which intersects at apoint
            - a polyline
                - for skew convex polygons which intersect at two points (a single segment)
                - for coplaner convex polygons which intersect
                         
        """
        ipoints=[]
        isegments=[]
        for ps in convex_polygon.polyline.segments:
            #print('ps',ps)
            result=self.intersect_segment(ps)
            #print('result',result)
            if isinstance(result,Point3D):
                if not result in ipoints:
                    ipoints.append(result)
            elif isinstance(result,Segment3D):
                isegments.append(result)
                
                
        if not ipoints and not isegments: # no intersections
            
            return None
                
        elif len(isegments)>0: # one or more segment intersections
            
            # order segments
            segments=[isegments[0]]
            for i in range(1,len(isegments)):
                s=isegments[i]
                if s.P0==segments[-1].P1:
                    segments+=[s]
                else:
                    segments=[s]+segments
                    
            # convert segements to polyline
            points=[s.P0 for s in segments]
            points+=[segments[-1].P1]
            return SimplePolyline3D(*points)
        
        elif len(ipoints)==1:
            
            return ipoints[0]
        
        elif len(ipoints)==2:
            
            return SimplePolyline3D(*ipoints)
            
        else:
            
            raise Exception
        
        
    def union_convex_polygon(self,convex_polygon):
        """Returns the union of this convex polygon with another convex polygon
        
        :param convex_polygon SimpleConvexPolygon3D: a 3D convex polygon 
        
        :return union_result:
            - return value can be:
                - None -> no intersection (for a convex polygon whose segments 
                                           do not intersect the segments of this
                                           convex polygon)
                - Point2D -> a point (for a convex polygon whose segments intersect
                                      this convex polygon at a single vertex)
                - SimplePolyline2D -> a polyline 
                    - (for convex polygons that intersect on one or more edges)
                    - (for skew convex polygons that intersect each other at points inside the polygon)
                - SimpleConvexPolygon2d -> a convex polygon (for convex polygons that intersect and overlap)
                            
        """
        if self==convex_polygon:
            
            return self # self intersection
        
        else:
        
            result1=self.intersect_convex_polygon(convex_polygon)
            #print(result1)
            
            if result1 is None:
                
                return None # no intersection
            
            else:
                
                result2=convex_polygon.intersect_convex_polygon(self)
                #print(result2)
            
                if isinstance(result1,Point) and isinstance(result2,Point):
                    
                    if result1==result2: # intersect at same point
                        
                        return result1
                    
                    else: # point intersection at 2 different points 
                          #   - i.e skew convex polygons that intersect each other at points inside the polygon
                        
                        return SimplePolyline3D(result1,result2)
                        
                elif isinstance(result1,SimplePolyline) and isinstance(result2,Point):
                    
                    return result1
                
                elif isinstance(result1,Point) and isinstance(result2,SimplePolyline):
                    
                    return result2
                    
                else: # both results are polylines
                    
                    if result1==result2: # edge intersection
                        
                        return result1 # return polyline
                    
                    else: # overlap intersection
                    
                        points=result1.points[:-1]+result2.points[:-1]
                        return SimpleConvexPolygon3D(*points)
                    
                    
                    
        
        
        
        
    
    
    
    
    
    
    
    
    
    
    

            
    
    