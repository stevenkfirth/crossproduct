# -*- coding: utf-8 -*-

from .plane import Plane3D
from .point import Point2D
from .points import Points
from .polyline import Polyline2D, Polyline3D
from .simple_convex_polygon import SimpleConvexPolygon2D, SimpleConvexPolygon3D
from .segment import Segment2D, Segment3D
from .segments import Segments


class Triangle():
    """A n-D triangle
    """
    
    classname='Triangle'
    
    def __init__(self,P0,v,w):
        ""
        if P0.classname=='Point':
            self.P0=P0
        else:
            raise TypeError
            
        if v.classname=='Vector':
            self.v=v
        else:
            raise TypeError
        
        if w.classname=='Vector':
            self.w=w
        else:
            raise TypeError
    
        # orientate counterclockwise if a 2D triangle
        if P0.dimension=='2D':
            if self.orientation<0:
                self.v=w
                self.w=v
                

    @property
    def closed_points(self):
        """Returns an array of polygon points which are closed
        
        :return points: array of points where the last point is the same as the first point
        :rtype tuple:
        """
        return tuple(list(self.points) + [self.points[0]])


    @property
    def P1(self):
        """Returns point P1
        
        :return point:
        :rtype Point2D
        
        """
        return self.P0+self.v
    
    
    @property
    def P2(self):
        """Returns point P2
        
        :return point:
        :rtype Point2D
        
        """
        return self.P0+self.w
        
    
    @property
    def points(self):
        """Returns point P1, P2 and P3
        
        :return result:
        :rtype tuple:
        
        """
        return (self.P0,
                self.P1,
                self.P2)
        
        
    def reorder(self,i):
        """Returns a triangle with reordered points
        
        :param i: the index of the start point
        
        """
        points=[]
        for _ in range(len(self.points)):
            points.append(self.points[i])
            i=self.next_index(i)
        return self.__class__(points[0],
                              points[1]-points[0],
                              points[2]-points[0])
        
    
    @property
    def reverse(self):
        """Return a polygon with the points reversed
        
        :return polygon:
        :rtype Polygon:
        """
        points=[self.points[i] 
                for i in range(len(self.points)-1,-1,-1)]
        return self.__class__(points[0],
                              points[1]-points[0],
                              points[2]-points[0])



class Triangle2D(Triangle):#,SimpleConvexPolygon2D):
    """A two dimensional triangle, situated on an x, y plane.
         
    :param P0: A point on the triangle.
    :type P0: Point2D
    :param v: A vector on the triangle from P0 to P1.
    :type v: Vector2D
    :param w: A vector on the triangle from P0 to P2.
    :type w: Vector2D
        
    
    """
    
    def __contains__(self,obj):
        """Tests if the 2D triangle contains the object.
        
        :param obj: A 2D geometric object .
        :type obj: Point2D
            
        :return: For point, returns True if the point lies within the triangle 
            (including on an edge);
            otherwise False.
        :rtype: bool
            
        """
        if obj.__class__.__name__=='Point2D':
            
            point=obj
            
            u=self.v
            v=self.w
            w=point-self.P0
            
            denominator=(u.dot(v))**2 - (u.dot(u)*v.dot(v))
            
            si=(u.dot(v)*w.dot(v)-v.dot(v)*w.dot(u)) / denominator
            ti=(u.dot(v)*w.dot(u)-u.dot(u)*w.dot(v)) / denominator
            
            if si>=0 and ti>=0 and si+ti<=1:
                return True
            else:
                return False                
            
        else:
            raise Exception
        
        
    def __repr__(self):
        ""
        return 'Triangle2D(%s, %s, %s)' % (self.P0,self.v,self.w)
        
        
    @property
    def area(self):
        """Returns the area of the triangle.
        
        :return: The triangle area.
        :rtype: float

        """
        return abs(self.signed_area)
    
    
    # @property
    # def class_3D(self):
    #     return Triangle3D    

    
    def intersect_halfline(self,halfline):
        """Intersection of this triangle with a halfline.
        
        :param halfline: A 2D halfline.
        :type halfline: Halfline2D
        
        :return: Returns None for a halfline which does not intersect the polygon.
            Returns a point for a halfline which intersects the polygon at a single vertex.
            Return a segment for a halfline which intersects the polygon at 2 edges.
            Returns a segment for a halfline which starts inside the polygon and intersects one edge.
        :rtype: None, Point2D, Segment2D
        
        """
        result=self._intersect_line_t_values(halfline.line)
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
        """Intersection of this triangle with a line.
        
        :param line: A 2D line.
        :type line: Line2D 
        
        :return: Returns None for a line which does not intersect the polygon.
            Returns a point for a lien which intersects the polygon at a single vertex.
            Returns a segment for a line which intersects the polygon at 2 edges.
        :rtype: None, Point2D, Segment2D
        
        """
        result=self._intersect_line_t_values(line)
        if result is None:
            return None
        elif result[0]==result[1]:
            return line.calculate_point(result[0])
        else:
            P0=line.calculate_point(result[0])
            P1=line.calculate_point(result[1])
            return Segment2D(P0,P1)
        
    
    def _intersect_line_t_values(self,line):
        """Returns t values of the intersection of this triangle with a line.
        
        :param line: A 2D line.
        :type line: Line2D 
        
        :return: Returns None for a line which does not intersect the polygon.
            Returns tuple with two items for a line which intersects the polygon at a single vertex - items are the same point.
            Returns tuple with two items for a line which intersects the polygon at 2 edges.
        :rtype: None, tuple
                
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
        """Intersection of this triangle with a segment.
        
        :param segment: A 2D segment.
        :type segment: Segment2D
        
        :return: Returns None for a segment which does not intersect the polygon.
            Returns a point for a segment which intersects the polygon at a single vertex.
            Returns a segment for a segment which intersects the polygon at 2 edges.
            Returns a segment for a segment which starts or ends inside the polygon and intersects one edge.
        :rtype: None, Point2D, Segment2D
        
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
        """Intersection of this triangle with a Segments sequence.
        
        :param segments: A segments sequence.
        :type segments: Segments
        
        :return: A tuple of intersection points and intersection segments 
            (Points,Segments)
        :rtype: tuple
        
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
            pg=SimpleConvexPolygon2D(*pl.points[:-1]) # or a polyline??
            return pg

    
    @property
    def orientation(self):
        """Returns the orientation of a 2D triangle
        
        :return result: 
            - >0 for counterclockwise
            - =0 for none (degenerate)
            - <0 for clockwise
        :rtype float: 
        """
        return self.signed_area
    
    
    @property
    def polyline(self):
        return Polyline2D(*self.closed_points)
    
    
    @property
    def signed_area(self):
        """Returns the signed area of the triangle
        
        :return result:
            - return value >0 if triangle points are ordered counterclockwise
            - return value <0 if triangle points are ordered clockwise
        :rtype float:
                
        """
        return 0.5*(self.v.x*self.w.y-self.w.x*self.v.y)
    
        
    
class Triangle3D(Triangle):#,SimpleConvexPolygon3D):
    """"A 3D Triangle
    """
        
    def __contains__(self,obj):
        """Tests if the 3D triangle contains the object
        
        :param obj: a 3D geometric object 
            - Point3D, Segment3D, Polygon3D
            
        :return result:
            - for point, True if the point lies within the triangle (including on an edge)
            - for segment...
            - for polygon ...
        :rtype bool:
            
        """
        if obj.__class__.__name__=='Point3D':
            
            point=obj
            
            if point in self.plane:
            
                u=self.v
                v=self.w
                w=point-self.P0
                
                denominator=(u.dot(v))**2 - (u.dot(u)*v.dot(v))
                
                si=(u.dot(v)*w.dot(v)-v.dot(v)*w.dot(u)) / denominator
                ti=(u.dot(v)*w.dot(u)-u.dot(u)*w.dot(v)) / denominator
                
                if si>=0 and ti>=0 and si+ti<=1:
                    return True
                else:
                    return False                
            
            return False
            
        else:
            raise Exception
        
        
    def __repr__(self):
        ""
        return 'Triangle3D(%s, %s, %s)' % (self.P0,self.v,self.w)
        
        
    @property
    def area(self):
        """Returns the area of the triangle
        
        :return result:
        :rtype float:

        """
        return 0.5*self.v.cross_product(self.w).length
    
    
    # @property
    # def class_2D(self):
    #     return Triangle2D  
    
    
    
            
    
    def intersect_plane(self,plane):
        """Returns the intersection of this 3D triangle and a plane
        
        :param plane Plane3D: a 3D plane 
        
        :return result:
            - no intersection (None): 
                - for parallel, non-coplanar 3D triangle and plane
                - for skew 3D triangle and plane which do not intersect
            - a triangle:
                - for coplanar 3D triangle and plane
            - a segment:
                - for 3D triangle which intersects the plane at two points
            - a point: 
                - for 3D triangle which intersects the plane at one point
        
        """
        if self.plane==plane:
            return self
        
        elif self.plane.N.is_collinear(plane.N):
            return None
        
        else:
        
            ipts=[]
            for ps in self.polyline.segments:
                i=plane.intersect_segment(ps)
                if i is None:
                    continue
                elif i.__class__.__name__=='Segment3D': # if a segment, then this is the result
                    return i
                else:
                    if not i in ipts:
                        ipts.append(i)
            
            if len(ipts)==0: # no intersections
                
                return None
            
            elif len(ipts)==1: # point intersection
                
                return ipts[0]
            
            elif len(ipts)==2: # segment intersection
                
                return Segment3D(ipts[0],ipts[1])
            
            else:
                raise Exception('%s not in options' % ipts)
                
            
    def intersect_triangle(self,triangle):
        """Returns the intersection of this 3D triangle and another 3D triangle
        
        :param triangle Triangle3D: a 3D triangle 
        
        :return result:
            - no intersection (None): 
                - for parallel, non-coplanar 3D triangles
                - for skew non-coplanar 3D triangles which do not intersect
                = for coplanar triangles which do not intersect
            - a triangle:
                - for coplanar 3D triangles which are equal
            - a segment:
                - for coplanar 3D triangles which intersects at two points
                - for non-coplanar 3D triangles which intersects at two points
            - a point: 
                - for coplanar 3D triangles which intersect at one point
                - for non-coplanar 3D triangles which intersect at one point
            -a simple convex polygon
        
        """
        if self.plane==triangle.plane:
            
            return self._intersect_simple_convex_polygon_coplanar(triangle)
        
        else:
        
            iresult1=self.intersect_plane(triangle.plane)
            if iresult1 is None:
                return None
            
            iresult2=triangle.intersect_plane(self.plane)
            if iresult2 is None:
                return None
            
            if iresult1.__class__.__name__=='Point3D':
                if iresult1 in triangle:
                    return iresult1 
                else:
                    return None
                
            elif iresult2.__class__.__name__=='Point3D':
                if iresult2 in self:
                    return iresult2
                else:
                    return None
            
            elif iresult1.__class__.__name__=='Segment3D' and iresult2.__class__.__name__=='Segment3D':
            
                    return iresult1.intersect_segment(iresult2)
            
            else:
                raise Exception()     
    
    @property
    def plane(self):
        """Returns the plane of the 3D polygon
        
        :return plane: a 3D plane which contains all the polygon points
        :rtype Plane3D:
        
        """
        N=(self.P1-self.P0).cross_product(self.P2-self.P1)
        return Plane3D(self.P0,N)
    
    @property
    def polyline(self):
        return Polyline3D(*self.closed_points)
    
    @property
    def project_2D(self):
        """Projects the 3D triangle to a 2D triangle
        
        :return (index,triangle): a tuple of results
            - index is the index of the coordinate which is ignored in the projection
                - 0 for x
                - 1 for y
                - 2 for z
            - triangle is the 2D projected triangle
        :rtype tuple:
            
        """
        absolute_coords=[abs(x) for x in self.plane.N.coordinates]
        i=absolute_coords.index(max(absolute_coords)) # the coordinate to ignore for projection
        
        if i==0:
            points=[Point2D(pt.y,pt.z) for pt in self.points]
        elif i==1:
            points=[Point2D(pt.z,pt.x) for pt in self.points]
        elif i==2:
            points=[Point2D(pt.x,pt.y) for pt in self.points]
        else:
            raise Exception
                    
        pg=Triangle2D(points[0],points[1]-points[0],points[2]-points[0])
        return i, pg
   
    
    
    
    
    
    
    
    