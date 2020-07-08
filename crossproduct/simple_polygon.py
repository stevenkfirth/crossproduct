# -*- coding: utf-8 -*-

import itertools

from .halfline import Halfline3D
from .line import Line3D
from .segment import Segment, Segment3D
from .point import Point, Point2D, Point3D
from .points import Points
from .segments import Segments
from .simple_polyline import SimplePolyline, SimplePolyline2D, SimplePolyline3D
from .plane import Plane3D
from .vector import Vector3D



class SimplePolygon():
    """A n-D simple polygon
    
    The polygon does not self intersect and has no holes
    
    Adjacent polygon segments are not collinear.
    
    """
    
    def __init__(self,*points):
        """
        
        param points: an array of points 
            - the first point is not repeated at the end of the array
        
        """
        
        self.points=tuple(points)
        
        # merge any codirectional adjacent segments
        pl1=self.polyline
        pl2=pl1.merge_codirectional_segments
        points=list(pl2.points)
        if (points[1]-points[0]).is_codirectional(points[-1]-points[-2]):
            points.pop(0)
        self.points=tuple(points[:-1])
        #print(self.points)
        
        
        # check for intersection
        if pl2.is_intersecting:
            return ValueError('A simple polygon should not self intersect')
                
        # triangulate
        self.triangles=self.triangulate
        
        
        
    
    def __eq__(self,polygon):
        """Tests if this polygon and the supplied polygon are equal
        
        :param line SimplePolygon2D: a 2D polygon
        
        :return result: 
            - True if 
                - it has the same points, and
                - the points are in the same order (from an arbitrary start point), 
                    either forward or reversed      
            - otherwise False
        :rtype bool:
            
        """
        if isinstance(polygon,SimplePolygon):
            
            for i in range(len(self.points)):
                if self.reorder(i).points==polygon.points:
                    return True
            for i in range(len(self.points)):
                if self.reverse.reorder(i).points==polygon.points:
                    return True
            return False
            
        else:
            return False
    
    
    @property
    def closed_points(self):
        """Returns an array of polygon points which are closed
        
        :return points: array of points where the last point is the same as the first point
        :rtype tuple:
        """
        return tuple(list(self.points) + [self.points[0]])
    
    
    def intersect_simple_polygon(self,simple_polygon):
        ""
        ipts,isegments,isimplepolygons=self.triangles.intersect_triangles(simple_polygon.triangles)
        
        return ipts,isegments,isimplepolygons
        
    
    def is_adjacent(self,simple_polygon):
        """Test to see if this simple polygon is adjacent to another simple polygon
        
        :return result:
            - returns True if a segment from one polygon contains a segment from another
        :rtype true:
        
        """
        for s in self.polyline.segments:
            for s1 in simple_polygon.polyline.segments:
                if isinstance(s.intersect_segment(s1),Segment):
                    return True
        return False
    
    
    def union_simple_polygon(self,simple_polygon):
        ""
        ipts,isegments,isimplepolygons=self.triangles.union_triangles(simple_polygon.triangles)
        
        
    
#    
#    def _intersect_results(self,ipts,isegments):
#        """Sorts and cleans the intersection results
#        
#        :param ipts list: a list of intersection points
#        :param isegments list: a list of intersection segments
#        
#        :return result: a tuple of (points,segments)
#            - if a point exists in a segment, then it is removed
#            - if a union of two segments exist, then this is added and the individual segments removed
#        :rtype tuple:
#        
#        """
#        
#        # order segments so P0 < P1
#        isegments=[s.order for s in isegments]     
#                
#        # sort segments by P0 and P1
#        d={(s.P0.coordinates,s.P1.coordinates):s for s in isegments}
#        isegments=[d[c] for c in sorted(d)]
#        
#        # join segments if applicable
#        l=isegments
#        n=None
#        while not len(l)==n:
#            n=len(l)
#            for i in range(len(l)-1):
#                u=l[i].union(l[i+1])
#                if u and isinstance(u,Segment):
#                    l[i]=u
#                    l.pop(i+1)
#                    break
#        isegments=l
#                
#        # remove points which exist in the segments
#        l1=[]
#        for ipt in ipts:
#            flag=True
#            for s in l:
#                if ipt in s:
#                    flag=False
#                    break
#            if flag:
#                l1.append(ipt)
#        ipts=l1
#        
#        return ipts, isegments
#    
#    
#    def intersect_halfline(self,halfline):
#        """Intersection of this polygon with a halfline
#        
#        :param halfline Halfline: a halfline 
#        
#        :return tuple: (list of points, list of segments) or None
#        
#                    
#        """
#        ipts=Points()
#        isegments=Segments()
#        for tri in self.triangles:
#            
#            #print(tri)
#            #print(line)
#            result_pts,result_segments=tri.intersect_halfline(halfline)
#            for x in result_pts:
#                ipts.append(x,unique=True)
#            for x in result_segments:
#                isegments.append(x,unique=True)
#            
#        isegments.self_union
#        ipts.remove_points_in_segments(isegments)
#            
##            print(result)
##            if isinstance(result,Point):
##                if not result in ipts:
##                    ipts.append(result)
##            elif isinstance(result,Segment):
##                isegments.append(result)
#                
#        print(ipts,isegments)
#        #return self._intersect_results(ipts,isegments)
#    
#    
#    def intersect_line(self,line):
#        """Intersection of this polygon with a line
#        
#        :param line Line: a line 
#        
#        :return tuple: (list of points, list of segments) or None
#                    
#        """
#        ipts=[]
#        isegments=[]
#        for tri in self.triangles:
#            
#            #print(tri)
#            #print(line)
#            result=tri.intersect_line(line)
#            #print(result)
#            if isinstance(result,Point):
#                if not result in ipts:
#                    ipts.append(result)
#            elif isinstance(result,Segment):
#                isegments.append(result)
#                
#        #print(isegments)
#        return self._intersect_results(ipts,isegments)
#    
#        
#    def intersect_segment(self,segment):
#        """Intersection of this polygon with a segment
#        
#        :param segment Segment: a segment 
#        
#        :return tuple: (list of points, list of segments) or None
#                    
#        """
#        ipts=[]
#        isegments=[]
#        for tri in self.triangles:
#            
#            #print('tri',tri)
#            #print('segment',segment)
#            result=tri.intersect_segment(segment)
#            #print('result',result)
#            if isinstance(result,Point):
#                if not result in ipts:
#                    ipts.append(result)
#            elif isinstance(result,Segment):
#                isegments.append(result)
#                
#        #print('ipts',ipts)
#        #print('isegments',isegments)
#        return self._intersect_results(ipts,isegments)
#    
#    
#    
        
    
#    def intersect_polygon(self,polygon):
#        """Intersection of this polygon with another polygon
#        
#        :param polygon SimplePolygon: a polygon 
#        
#        :return result: one of
#            - tuple -> (list of points, list of segments)
#            - None
#                    
#        """
#        ipts=[]
#        isegments=[]
#        for tri in self.triangles:
#            #print('tri',tri)
#            
#            for segment in polygon.polyline.segments:
#                #print('segment',segment)
#                
#                result=tri.intersect_segment(segment) # ipts,isegments
#                #print('result',result)
#                
#                if isinstance(result,Point):
#                    if not result in ipts:
#                        ipts.append(result)
#                elif isinstance(result,Segment):
#                    isegments.append(result)
#                
#        #print('ipts',ipts)
#        #print('isegments',isegments)
#       
#        return self._intersect_results(ipts,isegments)
        
        
#    def union_polygon(self,polygon):
#        """Returns the union of this polygon with another polygon
#        
#        :param polygon SimplePolygon: a polygon 
#        
#        :return result: one of
#            - tuple -> (list of points, list of segments, list of polygons)
#            - None        
#        
#        """
#        if self==polygon:
#            
#            return self
#        
#        else:
#        
#            result=self.intersect_polygon(polygon)
#            
#            result2=polygon.intersect_polygon(self)
#            
#            ipts=result[0]
#            for p in result2[0]:
#                if not p in ipts:
#                    ipts.append(p)
#                    
#            isegments=result[1]
#            for s in result2[1]:
#                if not s in isegments:
#                    isegments.append(s)
#            
#            # do any of the segments form polylines?
#            test_polylines=[s.polyline for s in isegments]
#            n=len(test_polylines)
#            
#            if n>1:
#                
#                i=0
#                while True:
#                    j=i+1
#                    test_polyline=test_polylines[i]
#                    while True:
#                        u=test_polyline.union(test_polylines[j])
#                        #print('u',u)
#                        if u is None:
#                            j+=1
#                        else:
#                            test_polylines[i]=u
#                            test_polylines.pop(j)
#                            break
#                        if j>=n:
#                            i+=1
#                            break
#                    n=len(test_polylines)
#                    #print(test_polylines)
#                    #print(i,n)
#                    if i>=n-1:
#                        break
#            
#             # do any of the polylines form polygons?
#            isegments=[]
#            ipolygons=[]
#            for pl in test_polylines:
#                if pl.points[0]==pl.points[-1]:
#                    polygon=self.__class__(*pl.points[:-1])
#                    ipolygons.append(polygon)
#                else:
#                    isegments+=pl.segments
#            
#            
#            return tuple(ipts), tuple(isegments), tuple(ipolygons)
#    
        
    
    def next_index(self,i):
        """Returns the next point index in the polygon
        
        :param i int: a point index
        
        :return index:
            - if i is the index of the last point, then 0 is returned
        :rtype int:
        
        """
        n=len(self.points)
        if i==n-1:
            return 0
        else:
            return i+1
    
    
    def plot(self,ax,normal=False,**kwargs):
        """Plots the segment on the supplied axes
        
        :param ax: an Axes or Axes3D instance
            - matplotlib.axes.Axes (for 2D)
            - mpl_toolkits.mplot3d.axes3d.Axes3D (for 3D)
        :param **kwargs: keyword arguments to be supplied to the matplotlib plot call
                    
        """
        self.polyline.plot(ax,**kwargs)
        
        if normal:
            c=self.centroid
            N=self.plane.N
            
            x0,x1=ax.get_xlim()
            y0,y1=ax.get_ylim()
            z0,z1=ax.get_zlim()
            ax_vector=Vector3D(x1-x0,y1-y0,z1-z0)
                        
            x=abs(N.dot(ax_vector)/N.length)
           
            ax.quiver(*c.coordinates,*N.coordinates, 
                      length=x*0.2,
                      lw=3)
        
            
        
    
    def previous_index(self,i):
        """Returns the previous point index in the polygon
        
        :param i int: a point index
        
        :return index:
            - if i is 0 then the index of the last point is returned
        :rtype int:
        
        """
        n=len(self.points)
        if i==0:
            return n-1
        else:
            return i-1
        
        
    def reorder(self,i):
        """Returns a polygon with reordered points
        
        :param i: the index of the start point
        
        """
        points=[]
        for _ in range(len(self.points)):
            points.append(self.points[i])
            i=self.next_index(i)
        return self.__class__(*points)
        
    
    @property
    def reverse(self):
        """Return a polygon with the points reversed
        
        :return polygon:
        :rtype SimplePolygon:
        """
        points=[self.points[i] 
                for i in range(len(self.points)-1,-1,-1)]
        return self.__class__(*points)
    
    
    @property
    def triangulate(self):
        """Returns a Triangles sequence of triangles which have the same overall shape as the polygon
        
        
        :return result: a list of Triangle2D instances
        :rtype list:
        
        
        """
        from .triangles import Triangles
        
        if isinstance(self,SimplePolygon2D):
            from .triangle import Triangle2D as t
        elif isinstance(self,SimplePolygon3D):
            from .triangle import Triangle3D as t
        else:
            raise Exception
        
        result=[]
        points=[x for x in self.points]
        
        while len(points)>2:
            
            n=len(points)
            
            for i in range(n):
                #print('i',i)
                
                if i==n-1:
                    i_next=0
                else:
                    i_next=i+1
                
                if i==0:
                    i_prev=n-1
                else:
                    i_prev=i-1
                
                test_triangle=t(points[i],
                                points[i_next]-points[i],
                                points[i_prev]-points[i])
                #print('test_triangle',test_triangle)
            
            
                point_inside=False
                i2=i+2
                for j in range(n-3):
                    
                    #print('i2',i2)
                    #print('points[i2]',points[i2])
                    #print(points[i2] in test_triangle)
                    if points[i2] in test_triangle:
                        point_inside=True
                        break
                                                
                    if i2==n-1:
                        i2=0
                    else:
                        i2=i2+1
    
                #print('point_inside',point_inside)
                if point_inside:
                    continue
    
                # the test_triangle is an ear
                
                result.append(test_triangle)
                #print('result',result)
                
                points.pop(i)
                #print('len(points)',len(points))
                break
                
    
        return Triangles(*result)
       

class SimplePolygon2D(SimplePolygon):
    """A 2D polygon
    """
    
    
    def __contains__(self,obj):
        """Tests if the polygon contains the object
        
        :param obj: a 2D geometric object 
            - Point2D, Segement2D, SimplePolygon2D etc.
            
        :return result:
            - for point, 
                - True if the point lies within the polygon 
                    - Includes a left hand or bottom edge
                    - Does not include a point on a top or right hand edge
            - for segment...
            - for polygon ...
        :rtype bool:
            
        """
        if isinstance(obj,Point2D):
            
            return self.winding_number(obj) > 0
                    
        else:
            
            return NotImplementedError
        
        
    def __repr__(self):
        """The string of this line for printing
        
        :return result:
        :rtype str:
            
        """
        return 'SimplePolygon2D(%s)' % ','.join([str(p) for p in self.points])
    
    
    @property
    def area(self):
        """Returns the area of the polygon
        
        :return result:
        :rtype float:

        """
        return abs(self.signed_area)
    
    
    @property
    def centroid(self):
        """Returns the centroid of the polygon
        
        :return point:
        :rtype Point2D:
                
        """
        x=sum([pt.x for pt in self.points])/len(self.points)
        y=sum([pt.y for pt in self.points])/len(self.points)
        return Point2D(x,y)        
        
    
    def crossing_number(self,point):
        """Returns the crossing number for the supplied point
        
        :param point Point2D:
        
        :return crossing_number:
            - the number of times a line extending to the right of the point
                crosses the polygon segments
            - does not include a point on a top or right hand edge
            
        :rtype tuple:
        """
        cp=0
        
        for ps in self.polyline.segments:
            
            if ((ps.P0.y <= point.y) and (ps.P1.y > point.y) or 
                (ps.P0.y > point.y) and (ps.P1.y <= point.y)):
                
                t=ps.calculate_t_from_y(point.y)
                ipt=ps.calculate_point(t)
                
                if point.x < ipt.x:
                    cp+=1
                
        return cp
    
    
    @property
    def orientation(self):
        """Returns the orientation of a 2D polygon
        
        :return result: 
            - >0 for counterclockwise
            - =0 for none (degenerate)
            - <0 for clockwise
        :rtype float: 
        """
        i=self.rightmost_lowest_vertex
        P0=self.points[self.previous_index(i)]
        P1=self.points[i]
        P2=self.points[self.next_index(i)]
        return ((P1.x - P0.x) * (P2.y - P0.y)
                - (P2.x - P0.x) * (P1.y - P0.y) )
        
    
    @property
    def polyline(self):
        return SimplePolyline2D(*self.closed_points)
    
    
    @property
    def rightmost_lowest_vertex(self):
        """Returns the index of the rightmost lowest point
        
        :return point: the lowest point
            - if more then one point is joint lowest, then the rightmost is returned
        :rtype Point2D:
        
        """
        min_i=0
        for i in range(1,len(self.points)):
            if self.points[i].y>self.points[min_i].y:
                continue
            if (self.points[i].y==self.points[min_i].y) and (self.points[i].x < self.points[min_i].x):
                continue
            min_i=i
        return min_i
    
    
    @property
    def signed_area(self):
        """Returns the signed area of the polygon
        
        :return result:
            - return value >0 if polygon points are ordered counterclockwise
            - return value <0 if polygon points are ordered clockwise
        :rtype float:
                
        """
        n=len(self.points)
        points=self.closed_points
        if n<3: return 0  # a degenerate polygon
        a=0
        for i in range(1,n):
            a+=points[i].x * (points[i+1].y - points[i-1].y)
        a+=points[n].x * (points[1].y - points[n-1].y) # wrap-around term
        return a / 2.0
    
    
    def winding_number(self,point):
        """Returns the winding number of the point for the polygon
        
        :param point Point2D:
        
        :return winding_number:
            - the number of times the polygon segments wind around the point
            - does not include a point on a top or right hand edge
        :rtype int:
        
        """
        
        wn=0 # the  winding number counter
    
        # loop through all edges of the polygon
        for ps in self.polyline.segments: # edge from V[i] to  V[i+1]
            if ps.P0.y <= point.y: # start y <= P.y
                if ps.P1.y > point.y: # an upward crossing
                    if ps.vL.perp_product(point-ps.P1)>0: # P left of  edge
                        wn+=1
            else:
                if ps.P1.y <= point.y: # a downward crossing
                    if ps.vL.perp_product(point-ps.P1)<0: # P right of  edge
                        wn-=1
        
        return wn
                    
        
    
class SimplePolygon3D(SimplePolygon):
    """A 3D polygon
    """
    
       
    def __contains__(self,obj):
        """Tests if the polygon contains the object
        
        :param obj: a 3D geometric object 
            - Point3D, Segement3D, SimplePolygon3D etc.
            
        :return result:
            - for point, True if the point lies within the polygon (including on an edge)
            - for segment...
            - for polygon ...
        :rtype bool:
            
        """
        if isinstance(obj,Point):
            
            point=obj
            if point in self.plane:
                
                i,self2D=self.project_2D
                point2D=point.project_2D(i)
                
                return point2D in self2D
                
            else:
                
                return False
        
        else:
    
            raise Exception('Not implemented')
        
    
    def __repr__(self):
        """The string of this line for printing
        
        :return result:
        :rtype str:
            
        """
        return 'SimplePolygon3D(%s)' % ','.join([str(p) for p in self.points])
    
    
    @property
    def area(self):
        """Returns the area of the polygon
        
        :return result:
        :rtype float:

        """
        
        i,pg=self.project_2D
        N=self.plane.N
        
        if i==0:
            return pg.signed_area*(N.length/(N.x))
        elif i==1:
            return pg.signed_area*(N.length/(N.y))
        elif i==2:
            return pg.signed_area*(N.length/(N.z))
        else:
            raise Exception
    
    
    @property
    def centroid(self):
        """Returns the centroid of the polygon
        
        :return point:
        :rtype Point3D:
                
        """
        x=sum([pt.x for pt in self.points])/len(self.points)
        y=sum([pt.y for pt in self.points])/len(self.points)
        z=sum([pt.z for pt in self.points])/len(self.points)
        return Point3D(x,y,z)    
    
    
    @property
    def class_2D(self):
        return SimplePolygon2D  
    
    
#    def intersect_halfline(self,halfline):
#        """Returns the intersection of this polygon and a halfline
#        
#        :param line Halfline3D: a 3D halfline 
#        
#        :return result:
#            - no intersection (None): 
#                - for parallel, non-coplanar polygon plane and halfline
#                - for skew polygon plane and halfline which do not intersect
#            - a segment:
#                - for a coplanar halfline which intersects the polygon at two points
#            - a point: 
#                - for a halfline skew to the polygon plane which intersects the polygon at a point
#                - for a coplanar halfline which intersects the polygon one point
#        
#        """
#        result=self.plane.intersect_line(halfline) # intersection of triangle plane with halfline
#        
#        if result is None:
#            return None
#        
#        elif isinstance(result,Point3D):
#            if result in self:
#                return result
#            else:
#                return None
#            
#        elif isinstance(result,Halfline3D):
#            # coplanar, look for intersections on 2D plane
#            raise Exception('Not implemented yet')
#    
#        else:
#            raise Exception
#    
#    
#    def intersect_line(self,line):
#        """Returns the intersection of this polygon and a line
#        
#        :param line Line3D: a 3D line 
#        
#        :return result:
#            - no intersection (None): 
#                - for parallel, non-coplanar polygon plane and line
#                - for skew polygon plane and line which do not intersect
#            - a segment:
#                - for a coplanar line which intersects the polygon at two points
#            - a point: 
#                - for a line skew to the polygon plane which intersects the polygon at a point
#                - for a coplanar line which intersects the polygon at a vertex
#        
#        """
#        result=self.plane.intersect_line(line) # intersection of triangle plane with line
#        
#        if result is None:
#            return None
#        
#        elif isinstance(result,Point3D):
#            if result in self:
#                return result
#            else:
#                return None
#            
#        elif isinstance(result,Line3D):
#            # coplanar, look for intersections on 2D plane
#            raise Exception('Not implemented yet')
#    
#        else:
#            raise Exception
#    
#    
#    def intersect_segment(self,segment):
#        """Returns the intersection of this polygon and a segment
#        
#        :param line Segment3D: a 3D segment 
#        
#        :return result:
#            - no intersection (None): 
#                - for parallel, non-coplanar polygon plane and segment
#                - for skew polygon plane and segment which do not intersect
#            - a segment:
#                - for a coplanar segment which intersects the polygon at two points
#                - for a coplanar segment which is inside the polygon
#            - a point: 
#                - for a segment skew to the polygon plane which intersects the polygon at a point
#                - for a coplanar segment which intersects the polygon one point
#        
#        """
#        result=self.plane.intersect_line(segment) # intersection of triangle plane with segment
#        
#        if result is None:
#            return None
#        
#        elif isinstance(result,Point3D):
#            if result in self:
#                return result
#            else:
#                return None
#            
#        elif isinstance(result,Segment3D):
#            # coplanar, look for intersections on 2D plane
#            raise Exception('Not implemented yet')
#    
#        else:
#            raise Exception
            
        
    @property
    def plane(self):
        """Returns the plane of the 3D polygon
        
        :return plane: a 3D plane which contains all the polygon points
        :rtype Plane3D:
        
        """
        P0,P1,P2=self.points[:3]
        N=(P1-P0).cross_product(P2-P1)
        return Plane3D(P0,N)
    
    
    @property
    def polyline(self):
        return SimplePolyline3D(*self.closed_points)
    
    
    @property
    def project_2D(self):
        """Projects the 3D polygon to a 2D polygon
        
        :return (index,polygon): a tuple of results
            - index is the index of the coordinate which is ignored in the projection
                - 0 for x
                - 1 for y
                - 2 for z
            - polygon is the 2D projected polygon
        :rtype tuple:
            
        """
        absolute_coords=[abs(x) for x in self.plane.N.coordinates]
        i=absolute_coords.index(max(absolute_coords)) # the coordinate to ignore for projection
        
        if i==0:
            pg=self.class_2D(*[Point2D(pt.y,pt.z) for pt in self.points])
        elif i==1:
            pg=self.class_2D(*[Point2D(pt.z,pt.x) for pt in self.points])
        elif i==2:
            pg=self.class_2D(*[Point2D(pt.x,pt.y) for pt in self.points])
        else:
            raise Exception
                    
        return i, pg
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#class SimplePolygon3D():
#    ""
#    
#    def __init__(self,*points):
#        ""
#        self.points=tuple(points)
#    
#    def __repr__(self):
#        return 'SimplePolygon2D(%s)' % ','.join([str(p) for p in self.points])
#    
#    @property
#    def points_closed(self):
#        return tuple(list(self.points) + [self.points[0]])
#    
#    @property
#    def area(self):
#        ""
#        
#        normal_vector=self.normal        
#        
#        absolute_coords=[abs(x for x in self.coordinates)]
#        i=absolute_coords.index(max(absolute_coords)) # the coordinate to ignore for projection
#        
#        if i=='0':
#            pg=SimplePolygon2D([Point2D(pt.y,pt.z) for pt in self.points])
#            return pg.area*(normal_vector.length/(2*normal_vector.x))
#        if i=='1':
#            pg=SimplePolygon2D([Point2D(pt.x,pt.z) for pt in self.points])
#            return pg.area*(normal_vector.length/(2*normal_vector.y))
#        if i=='2':
#            pg=SimplePolygon2D([Point2D(pt.x,pt.y) for pt in self.points])
#            return pg.area*(normal_vector.length/(2*normal_vector.z))
#        
#        
#    def normal(self):
#        "Returns a normal vector"
#        p0,p1,p2=self.points[0],self.points[1],self.points[2]
#        v1,v2=Vector3D.from_points(p0,p1),Vector3D.from_points(p1,p2)
#        return v1.cross_product(v2)
        
        
    
    
    
    

    
#    def _intersect_linelike(self,linelike_obj):
#        """Returns the intersection of a linelike object
#        
#        The intersection of a polygon and a line can be:
#            - no intersection, for:
#                - a line which do not intersect with any of the polygon segments
#            - one or more of the following:
#                - a segment where the line contains a polygon segment
#                - a point where the line intersects a convex polygon point but does not enter the polygon
#                - a segment where the line intersects two polygon segments or points, 
#                        and the resulting segment is inside the polygon 
#                
#        :return: (points,segments)
#    
#        """
#        d={}
#        # find intersecting points in all segments        
#        for ps in self.polygon_segments:
#            
#            # finds the intersections of the halfline, line or segment with the polygon segments
#            if isinstance(linelike_obj,Halfline2D):
#                result=ps.intersect_halfline(linelike_obj)
#            elif isinstance(linelike_obj,Line2D):
#                result=ps.intersect_line(linelike_obj)
#            elif isinstance(linelike_obj,Segment2D):
#                result=ps.intersect_segment(linelike_obj)
#            else:
#                raise Exception('Intersection object not valid: %s' % linelike_obj)
#            #print('result',result)
#            
#            # gets the points in the result of the intersection
#            if result is None:
#                continue
#            elif isinstance(result,Segment2D):
#                result=(result.P0,result.P1) # a 2-item tuple of intersection points
#            elif isinstance(result,Point2D):
#                result=result, # a 1-item tuple of intersection points
#            
#            for pt in result:
#                #print(pt)
#                pt._polygon_segment=ps # the polygon segment which this point lies on
#                t=linelike_obj.calculate_t_from_point(pt) #  the t value of the point on the halfline, line or segment
#                d[t]=pt # points with the same t value are not repeated in the dictionary       
#        
#                
#        # add start and end points for halfline and segments if they are 
#        #  inside the polygon and don't intersect with a polygon segment
#        if isinstance(linelike_obj,Halfline2D):
#            if not 0 in d:
#                if linelike_obj.P0 in self:
#                    linelike_obj.P0._polygon_segment=None
#                    d[0]=linelike_obj.P0
#                    
#        # add start and end points for halfline and segments if they are 
#        #  inside the polygon and don't intersect with a polygon segment
#        elif isinstance(linelike_obj,Segment2D):
#            if not 0 in d:
#                if linelike_obj.P0 in self:
#                    linelike_obj.P0._polygon_segment=None
#                    d[0]=linelike_obj.P0
#            if not 1 in d:
#                if linelike_obj.P1 in self:
#                    linelike_obj.P1._polygon_segment=None
#                    d[1]=linelike_obj.P1
#        #print(d)
#                
#        # order points by linelike object t-value
#        #  and calculate intersection attributes
#        ipts=[d[t] for t in sorted(d.keys())] 
#        ipts=[self._calculate_intersection_attributes(pt,linelike_obj) for pt in ipts]
#        #print('ipts',ipts)
#        
#        # so, ipts is now 
#        #   - a list of unique points with intersect the polygon
#        #   - ordered according to their position on the intersection halfline, line or segment
#        #   - points have the attributes 
#        #       ._polygon_segment (the SimplePolygonSegment or None)
#        #       ._crossing_point (bool) - True is a crossing point occurs, or if the point is inside the polygon and not on an edge
#        #       ._vertex (bool) - True if the point is a polygon point
#        #       ._v0_collinear (bool) - True if the entering polygon segment is collinear with linelike_obj
#        #       ._v1_collinear (bool) - True if the leaving polygon segment is collinear with linelike_obj
#        
#        # create final results
#        result=[]
#        cp=False # a crossing point segment is being formed...
#        s=False # a non crossing point segment is being formed...
#        cp_p0=None
#        s_p0=None
#        for pt in ipts:
#    
#            #print(pt,pt._crossing_point,pt._vertex,pt._v0_collinear,pt._v1_collinear)
#            
#            if cp: # if a crossing point segment is being formed
#                if pt._crossing_point:
#                    result.append(Segment2D(Point2D(cp_p0.x,cp_p0.y),Point2D(pt.x,pt.y)))
#                    cp=False
#                    cp_p0=None
#                    continue
#                
#            elif s: # if a non-crossing point segment is being formed
#                if pt._v0_collinear and pt._v1_collinear:
#                    continue
#                elif pt._v0_collinear and not pt._v1_collinear:
#                    result.append(Segment2D(Point2D(s_p0.x,s_p0.y),Point2D(pt.x,pt.y)))
#                    s=False
#                    s_p0=None
#                    if pt._crossing_point: #  if the start of a crossing point segment
#                        cp=True
#                        cp_p0=pt
#                    continue
#                else:
#                    raise Exception()
#                
#            elif pt._crossing_point: #  if the start of a crossing point segment
#                cp=True
#                cp_p0=pt
#                
#            elif not pt._v0_collinear and pt._v1_collinear: # if the start of a non-crossing point segment
#                s=True
#                s_p0=pt
#                
#            elif not pt._v0_collinear and not pt._v1_collinear: # if a non crossing point outside of a segment
#                result.append(Point2D(pt.x,pt.y))
#        
#            elif not pt._vertex and pt._v0_collinear and pt._v1_collinear: # if the start of a non-crossing point segment
#                # formed by a segment or halfline start point on a polygon edge and extending collinearly
#                s=True
#                s_p0=pt
#        
#            else:
#                raise Exception()
#        
#        return result
#    
#    
#    def _calculate_intersection_attributes(self,pt,linelike_obj):
#        """
#        
#        
#        Calculates the intersection attributes give the linelike object
#        
#        Uses the polygon segment if present in ._polygon_segment
#        
#        #       ._crossing_point (bool) - True is a crossing point occurs, or if the point is inside the polygon and not on an edge
#        #       ._vertex (bool) - True if the point is a polygon point
#        #       ._v0_collinear (bool) - True if the entering polygon segment is collinear with linelike_obj
#        #       ._v1_collinear (bool) - True if the leaving polygon segment is collinear with linelike_obj
#        
#        
#        """
#        ps=pt._polygon_segment
#            
#        #print(ps)
#        #print(pt)
#        
#        if ps: # if the point has an associated polygon segment
#                
#            t=ps.calculate_t_from_point(pt)
#            #print(t)
#            
#            if t==0 or t==1: # a segment start point or end point
#            
#                vertex=True
#                
#                if t==0 : # if it is a start point of a polygon segment
#                    
#                    # get v0 and v1 - these are dependent on the orientation of the polygon and the intersecting linelike object
#                    ps_previous=ps.previous_segment
#                    if (ps.vL.is_opposite(linelike_obj.vL) or ps_previous.vL.is_opposite(linelike_obj.vL)):
#                        v0=ps.vL*-1
#                        v1=ps_previous.vL*-1
#                    else:
#                        v0=ps_previous.vL 
#                        v1=ps.vL
#    
#                elif t==1: # the end point of a polygon segment
#                    
#                    # get v0 and v1 - these are dependent on the orientation of the polygon and the intersecting linelike object
#                    ps_next=ps.next_segment
#                    if (ps.vL.is_opposite(linelike_obj.vL) or ps_next.vL.is_opposite(linelike_obj.vL)):
#                        v0=ps_next.vL*-1
#                        v1=ps.vL*-1
#                    else:
#                        v0=ps.vL
#                        v1=ps_next.vL
#                    
#                #print(v0,v1)
#                
#                pp_vL_v0=linelike_obj.vL.perp_product(v0) # >0 is ccw
#                pp_vL_v1=linelike_obj.vL.perp_product(v1) # >0 is ccw
#                #print(pp_vL_v0,pp_vL_v1)
#                
#                v0_collinear=True if linelike_obj.vL.is_collinear(v0) else False
#                v1_collinear=True if linelike_obj.vL.is_collinear(v1) else False
#                
#                
#                # crossing point?
#                if v1_collinear:
#                    crossing_point=False
#                    
#                elif not v0_collinear and not v1_collinear:
#                    if (pp_vL_v0>0)==(pp_vL_v1>0): # if vectors are both ccw or both cw
#                        crossing_point=True
#                    else:
#                        crossing_point=False
#                
#                elif not v1_collinear:
#                    # find v0 for a previous segment which is not collinear
#                    s=ps.previous_segment
#                    while True:
#                        #print(s)
#                        v0=s.vL
#                        if not linelike_obj.vL.is_collinear(v0):
#                            pp=linelike_obj.vL.perp_product(v0)
#                            break
#                        s=s.previous_segment
#                        
#                    if pp>0==pp_vL_v1>0: # if vectors are both ccw or both cw
#                        crossing_point=True
#                    else:
#                        crossing_point=False
#                
#                else:
#                    raise Exception()
#                
#            else: # pt is not a segment endpoint
#                
#                if ps.vL.is_collinear(linelike_obj.vL):
#                    
#                    crossing_point=False
#                    vertex=False
#                    v0_collinear=True
#                    v1_collinear=True
#                    
#                else:
#                
#                    crossing_point=True
#                    vertex=False
#                    v0_collinear=False
#                    v1_collinear=False
#                
#        else: # a Point2D
#    
#            crossing_point=True # a point inside the polygon (not on a segment) is counted as a crossing point
#            vertex=False
#            v0_collinear=False
#            v1_collinear=False
#            
#        #print(crossing_point,vertex,v0_collinear,v1_collinear)
#            
#        pt._crossing_point=crossing_point
#        pt._vertex=vertex
#        pt._v0_collinear=v0_collinear
#        pt._v1_collinear=v1_collinear
#        
#        return pt
#    
#    
#    
#    
    
    
    