# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d

from .point import Point2D, Point3D
from .points import Points
from .segment import Segment2D, Segment3D
from .segments import Segments
from .polyline import Polyline2D, Polyline3D
from .polylines import Polylines
from .polygons import Polygons
from .plane import Plane3D
from .vector import Vector3D
#from .triangles import Triangles 


class Polygon():
    """A n-D simple polygon
    """
    
    classname='Polygon'    
    
    def __init__(self,*points,known_convex=False,known_simple=True):
        ""
        
        self._points=Points(*points)
        self._known_convex=known_convex
        self._known_simple=known_simple
        self._triangles=None
        self._ccw=None
        
        # # merge any codirectional adjacent segments
        # pl1=self.polyline
        # pl2=pl1.merge_codirectional_segments
        # points=list(pl2.points)
        # if (points[1]-points[0]).is_codirectional(points[-1]-points[-2]):
        #     points.pop(0)
        # self.points=tuple(points[:-1])
        # #print(self.points)
        
        # # triangulate
        # self.triangles=self.triangulate
    
    
    def __add__(self,polygon):
        """Returns the addition of this polygon and another polygon.
        
        :param polygon: A polygon.
        :type polygon: Polygon2D, Polygon3D
            
        :return: A new polygon which is the sum of the two polylines.
            If the polygons are not adjacent (i.e share a (part) segment)
            then ValueError is raised.
        :rtype: Polygon2D, Polygon3D
        
        :Example:
    
        .. code-block:: python
           
           # 2D example
           >>> pg1 = Polygon2D(Point2D(0,0), Point2D(1,0), Point2D(1,1))
           >>> pg2 = Polygon2D(Point2D(0,0), Point2D(1,1), Point2D(0,1))
           >>> result = pg1 + pg2
           >>> print(result)
           Polygon2D(Point2D(0,0), Point2D(0,1), Point2D(1,1), Point2D(1,0))
        
        """ 
        pls1=self.polyline.difference_polyline(polygon.polyline)
        
        if pls1[0]==self.polyline:
            raise ValueError
        
        #print(pls1)
        pls2=polygon.polyline.difference_polyline(self.polyline)
        #print(pls2)
        
        pls=pls1
        for pl in pls2:
            pls.append(pl)
                
        pls=pls.add_all
        pl=pls[0]
        pg=self.__class__(*pl.points[:-1])
        pg=pg.add_segments
        return pg
        
        
        
    def __eq__(self,polygon):
        """Tests if this polygon and the supplied polygon are equal.
        
        :param polygon: A polygon.
        :type polygon: Polygon2D, Polygon3D
        
        :return: True if the two polygons have the same points and 
            the points are in the same order (from any start point), 
            either forward or reversed;       
            otherwise False.
        :rtype: bool
        
        :Example:
    
        .. code-block:: python
           
           # 2D example
           >>> pg1 = Polygon2D(Point2D(0,0), Point2D(1,0), Point2D(1,1))
           >>> pg2 = Polygon2D(Point2D(0,0), Point2D(1,1), Point2D(1,0))
           >>> result = pl1 = pl2
           >>> print(result)
           True
            
        """
        if isinstance(polygon,Polygon):
            
            for i in range(len(self._points)):
                if self.reorder(i)._points==polygon._points:
                    return True
            for i in range(len(self._points)):
                if self.reverse.reorder(i)._points==polygon._points:
                    return True
            return False
            
        else:
            return False
    
    
    # def difference_simple_polygon_interior(self,simple_polygon_interior):
    #     """Returns the difference between this polygon and another polygon which is interior to it.
        
    #     :param simple_polygon SimpleConvexPolygon: a simple convex polygon which is interior (including on one or more edges)
        
    #     :return result:
    #         - None
    #         - Polygons
        
    #     """
        
    #     if self==simple_polygon_interior:
    #         return None

    #     else:
    #         #print(self.polyline.segments)
    #         #print(simple_polygon.polyline.segments)
            
    #         pls1=self.polyline.segments.difference_segments(simple_polygon_interior.polyline.segments).polylines 
    #         #print('pls1',pls1)
            
    #         pls2=simple_polygon_interior.polyline.segments.difference_segments(self.polyline.segments).polylines
    #         #print('pls2',pls2)
            
    #         spgs=Polygons()
            
    #         for pl1 in pls1:
    #             for pl2 in pls2:
    #                 pl3=pl1.union(pl2)
    #                 if not pl3 is None: 
    #                     spgs.append(Polygon2D(*pl3.points[:-1]))
            
    #         if len(spgs)>0:
    #             return spgs
        
    #         else: # interior intersection
                
    #             return NotImplementedError #self.doughnut(simple_polygon_interior) # perhaps return a polygon with a hole??
    

    @property
    def add_segments(self):
        """Returns a polygon with any adjacent segments added together if possible.
        
        :rtype: Polygon2D, Polygon3D
        
        """
        pl=self.polyline.add_segments
        points=pl.points
        #print(points)
        v=points[1]-points[0]
        w=points[-1]-points[-2]
        if v.is_codirectional(w):
            #print(points)
            points=points[1:-1]
            points.append(points[0])
        return self.__class__(*points[:-1])
              

    @property
    def known_convex(self):
        """The known_convex property of the polyline.
        
        :return: True if the polygon is known to be a convex polygon.
            False if it is not known if the polygon is convex or not, 
            or if it is known that the polygon is a concave polygon.
        :rtype: bool
        
        :Example:
    
        .. code-block:: python
           
           >>> pg = Polygon2D(Point2D(0,0), Point2D(1,0), Point2D(1,1), known_convex=True)
           >>> print(pg.known_convex)
           True        
        
        """
        return self._known_convex
        
    
    @property
    def known_simple(self):
        """The known_simple property of the polyline.
        
        :return: True if the polygon is known to be a simple polygon.
            False if it is not known if the polygon is simple or not, 
            or if it is known that the polygon is a non-simple polygon.
        :rtype: bool
        
        :Example:
    
        .. code-block:: python
           
           >>> pg = Polygon2D(Point2D(0,0), Point2D(1,0), Point2D(1,1), known_simple=True)
           >>> print(pg.known_simple)
           True        
        
        """
        return self._known_simple
    
    # def intersect_halfline(self,halfline):
    #     ""
    #     ipts, isegments = self.triangles.intersect_halfline(halfline)
    #     ipts.remove_points_in_segments(isegments)
    #     isegments=isegments.union
    #     return ipts, isegments
    
    
    # def intersect_line(self,line):
    #     ""
    #     ipts, isegments = self.triangles.intersect_line(line)
    #     ipts.remove_points_in_segments(isegments)
    #     isegments=isegments.union
    #     return ipts, isegments
    
    
    def intersect_polyline(self,polyline):
        """Returns the intersection of this polygon and the supplied polyline.
        
        The intersection is the intersection of the polyline segments within the area described by the polygon.
        
        :param polyline: A polyline.
        :type polyline: Polyline2D, Polyline3D
        
        :return: A tuple of intersection points and intersection polylines 
            (Points,Polylines). 
        :rtype: tuple      
            
        :Example:
    
        .. code-block:: python
           
           >>> pg = Polygon2D(Point2D(0,0), Point2D(1,0), Point2D(1,1))
           >>> pl = Polyline2D(Point2D(0,0), Point2D(1,0))
           >>> result = pg.intersect_polyline(pl)
           >>> print(result)
           Points(), Polylines(Polyline2D(Point2D(0,0), Point2D(1,0)))
        
        """
        ipts, isegments = self.intersect_segments(polyline.segments)
        ipolylines=Polylines(*[polyline.__class__(*s.points) for s in isegments])
        ipolylines=ipolylines.add_all
        return ipts, ipolylines
    
    
    def _intersect_polygon_simple_convex_and_simple_convex(self,polygon):
        ""
        ipts1,ipolylines1=self.intersect_polyline(polygon.polyline)
        #print(ipts1,ipolylines1)
        
        if len(ipts1)==0 and len(ipolylines1)==0:
            return Points(),Polylines(),Polygons() # returns None - no intersection
        elif len(ipts1)==1 and len(ipolylines1.segments)==0:
            return Points(ipts1[0]),Polylines(),Polygons() # returns a Point2D - point intersection
        elif len(ipts1)>1:
            raise Exception
        elif len(ipts1)==0 and len(ipolylines1.segments)==1:
            return Points(),Polylines(ipolylines1[0]),Polygons() # returns a Segment2D - edge segment intersection
        else: # a simple convex polygon intersection
            ipts2,ipolylines2=polygon.intersect_polyline(self.polyline)
            #print(ipts2,ipolylines2)
            
            pls=Polylines()
            
            if self.dimension=='2D':
                for s in ipolylines1.segments:
                    pls.append(Polyline2D(*s.points),unique=True)
                for s in ipolylines2.segments:
                    pls.append(Polyline2D(*s.points),unique=True)
                pls=pls.add_all
                pg=Polygon2D(*pls[0].points[:-1])
            else:
                for s in ipolylines1.segments:
                    pls.append(Polyline3D(*s.points),unique=True)
                for s in ipolylines2.segments:
                    pls.append(Polyline3D(*s.points),unique=True)
                pls=pls.add_all
                pg=Polygon3D(*pls[0].points[:-1],known_convex=True)
            
            return Points(),Polylines(),Polygons(pg)
        
        
    def _intersect_polygon_simple_and_simple_convex(self,polygon):
        ""
        pts=Points()
        pls=Polylines()
        pgs=Polygons()
            
        for pg in self.triangles:
            
            ipts,ipls,ipgs=pg._intersect_polygon_simple_convex_and_simple_convex(polygon)
        
            for pt in ipts: pts.append(pt,unique=True)
            for pl in ipls: pls.append(pl,unique=True)
            for pg in ipgs: pgs.append(pg,unique=True)
    
        pts=pts.remove_points_in_segments(pls.segments)
        pts=pts.remove_points_in_segments(pgs.polylines.segments)
        
        sgmts=pls.segments.remove_segments_in_polygons(pgs)
        if self.dimension=='2D':
            pls=Polylines(*[Polyline2D(*s.points) for s in sgmts])
        else:
            pls=Polylines(*[Polyline3D(*s.points) for s in sgmts])
        pls=pls.add_all
        
        pgs=pgs.add_all
    
        return pts,pls,pgs
    
    
    def _intersect_polygon_simple_and_simple(self,polygon):
        ""
        pts=Points()
        pls=Polylines()
        pgs=Polygons()
            
        for pg1 in self.triangles:
        
            for pg2 in polygon.triangles:
                
                ipts,ipls,ipgs=pg1._intersect_polygon_simple_convex_and_simple_convex(pg2)
            
                for pt in ipts: pts.append(pt,unique=True)
                for pl in ipls: pls.append(pl,unique=True)
                for pg in ipgs: pgs.append(pg,unique=True)
            
        pts=pts.remove_points_in_segments(pls.segments)
        pts=pts.remove_points_in_segments(pgs.polylines.segments)
        
        sgmts=pls.segments.remove_segments_in_polygons(pgs)
        if self.dimension=='2D':
            pls=Polylines(*[Polyline2D(*s.points) for s in sgmts])
        else:
            pls=Polylines(*[Polyline3D(*s.points) for s in sgmts])
        pls=pls.add_all
        
        pgs=pgs.add_all
        
        return pts,pls,pgs
    
    
    def intersect_polygon(self,polygon):
        """Returns the intersection of this polygon and the supplied polygon.
        
        :param segment: A polygon.
        :type segment: Polygon2D, Polygon3D
        
        :return: A tuple of intersection points, intersection segments 
            and intersection polygons in the form (Points, Segments, Polygons). 
        :rtype: tuple      
            
        :Example:
    
        .. code-block:: python
           
           >>> pg = Polygon2D(Point2D(0,0), Point2D(1,0), Point2D(1,1))
           >>> result = pg.intersect_segment(pg)
           >>> print(result)
           Points(), Segments(), Polygons(Polygon2D(Point2D(0,0), Point2D(1,0), Point2D(1,1)))
            
        """

        if self._known_simple and polygon._known_simple:
            
            if self._known_convex and polygon._known_convex:
                
                return self._intersect_polygon_simple_convex_and_simple_convex(polygon)
            
            elif not self._known_convex and polygon._known_convex:
                
                return self._intersect_polygon_simple_and_simple_convex(polygon)
            
            elif self._known_convex and not polygon._known_convex:

                return polygon._intersect_polygon_simple_and_simple_convex(self)
            
            elif not self._known_convex and not polygon._known_convex:
                
                return self._intersect_polygon_simple_and_simple(polygon)

            else:
                
                raise Exception

        else:

            raise NotImplementedError('This function is not implemented at present for a possible non-simple polygon')

        return

    
    def _intersect_line_t_values_simple_convex(self,line):
        """Returns t values of the intersection of this polygon with a line.
        
        Polygon must be simple and convex, with points in a counterclockwise orientation.
        
        :param line: A line.
        :type line: Line2D, Line3D
        
        :return: Returns None for no intersection (i.e. for a line which does not intersect the polygon).
            Returns a tuple with two items for a line which intersects 
            the polygon at a single vertex - items are the same point). 
            Returns a tuple with two items for a line which intersects 
            the polygon at 2 edges.
        :rtype: None, tuple
        
        """
        
        if self.dimension=='2D':
            polygon=self
            l=line
        else:
            coordinate_index,polygon=self.project_2D
            l=line.project_2D(coordinate_index)
        
        t_entering=[]
        t_leaving=[]
        for ps in polygon.ccw.polyline.segments:
            #print(ps)
            
            ev=ps.line.vL # edge vector
            n=ev.perp_vector*-1 #  normal to edge vector facing outwards
            try:
                t=(ps.P0-l.P0).dot(n) / l.vL.dot(n) # the t values of the line where the segment and line intersect
                
            except ZeroDivisionError: # the line and polygon segment are parallel
                if (l.P0-ps.P0).dot(n) > 0: # test if the line is outside the edge
                    #print('line is outside the edge')
                    return None # line is outside of the edge, there is no intersection with the polygon
                else:
                    continue # line is inside of the edge, ignore this segment and continue with others
            
            if l.vL.dot(n)<0:
                t_entering.append(t)
            else:
                t_leaving.append(t)
            
        t_entering_max=max(t_entering) # the line enters the polygon at the maximum t entering value
        
        t_leaving_min=min(t_leaving) # the line leaves the polygon at the minimum t leavign value
        
        if t_entering_max > t_leaving_min:
            
            return None
        
        else:
            
            return t_entering_max,t_leaving_min
    
    
    def _intersect_segment_simple_convex(self,segment):
        """Intersection of this polygon with a segment.
        
        Polygon must be simple and convex.
        
        The intersection is the intersection of the segment with the area described by the polygon.
        
        :param segment: A segment.
        :type segment: Segment2D, Segment3D
        
        :return: Returns None for no intersection (i.e. for a segment which does not intersect the polygon).
            Returns a point for a segment which only intersects a polygon edge at single point.
            Returns a point for a segment which only intersects a polygon point at single point.
            Returns a segment for a segment which lies on a polygon edge.
            Returns a segment for a segment which starts and/or ends inside the polygon.
        :rtype: None, Point2D, Point3D, Segment2D, Segment3D
        
        """
        result=self._intersect_line_t_values_simple_convex(segment.line)
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
                    if self.dimension=='2D':
                        return Segment2D(P0,P1)  
                    else:
                        return Segment3D(P0,P1)
    
    
    def _intersect_segment_simple(self,segment):
        """Intersection of this polygon with a segment.
        
        Polygon must be simple.
        
        The intersection is the intersection of the segment with the area described by the polygon.
        
        :param segment: A segment.
        :type segment: Segment2D, Segment3D
        
        :return: A tuple of intersection points and intersection segments 
            (Points,Segments). 
        :rtype: tuple   
        
        """
        if not self._triangles:
            self._triangles=self._triangulate

        #print(self._triangles)
        ipts, isegments = self._triangles.intersect_segment(segment)
        #print(ipts,isegments)
        ipts=ipts.remove_points_in_segments(isegments)
        isegments=isegments.add_all
        return ipts, isegments
    
    
    def intersect_segment(self,segment):
        """Returns the intersection of this polygon and the supplied segment.
        
        The intersection is the intersection of the segment with the area described by the polygon.
        
        :param segment: A segment.
        :type segment: Segment2D, Segment3D
        
        :return: A tuple of intersection points and intersection segments 
            (Points,Segments). 
        :rtype: tuple      
            
        :Example:
    
        .. code-block:: python
           
           >>> pg = Polygon2D(Point2D(0,0), Point2D(1,0), Point2D(1,1))
           >>> s = Segment2D(Point2D(0,0), Point2D(1,0))
           >>> result = pg.intersect_segment(s)
           >>> print(result)
           Points(), Segments(Segment2D(Point2D(0,0), Point2D(1,0)))
            
        """

        if self._known_simple:
            
            if self._known_convex:
        
                
                result=self._intersect_segment_simple_convex(segment)        
                if result is None:
                    return Points(), Segments()
                elif result.classname=='Point':
                    return Points(result),Segments()
                elif result.classname=='Segment':
                    return Points(),Segments(result)
                else:
                    raise Exception
        
            else:
        
                #print('test_simple')
                return self._intersect_segment_simple(segment)   
                
        else:
            raise NotImplementedError('This function is not implemented at present for a possible non-simple polygon')
    
    
    def intersect_segments(self,segments):
        """Returns the intersection of this polygon and the supplied segments sequence.
        
        The intersection is the intersection of the segments with the area described by the polygon.
        
        :param segment: A segment sequence.
        :type segment: Segments
        
        :return: A tuple of intersection points and intersection segments 
            (Points,Segments). 
        :rtype: tuple      
            
        :Example:
    
        .. code-block:: python
           
           >>> pg = Polygon2D(Point2D(0,0), Point2D(1,0), Point2D(1,1))
           >>> sgmts = Segments(Segment2D(Point2D(0,0), Point2D(1,0)))
           >>> result = pg.intersect_segments(sgmts)
           >>> print(result)
           Points(), Segments(Segment2D(Point2D(0,0), Point2D(1,0)))
            
        """
        #print(self)
        #print(segments)
        ipts=Points()
        isegments=Segments()
        
        for s in segments:
            pts,sgmts=self.intersect_segment(s)
            for pt in pts:
                ipts.append(pt,unique=True)
            for sgmt in sgmts:
                isegments.append(sgmt,unique=True)
        
        #print(ipts)
        #print(isegments)
        
        ipts=ipts.remove_points_in_segments(isegments)
        isegments=isegments.add_all        
        return ipts, isegments
    

    # def intersect_simple_convex_polygon(self,simple_convex_polygon):
    #     ""
    #     if not simple_convex_polygon.classname in ['Triangle','Quadrilateral','Parallelogram','SimpleConvexPolygon']:
    #         raise Exception
    
    #     ipts, isegments, iPolygons=self.triangles.intersect_simple_convex_polygon(simple_convex_polygon)
    #     #print(ipts, isegments, iPolygons)
    #     isegments.remove_segments_in_polygons(iPolygons)
    #     ipts=ipts.remove_points_in_segments(isegments)
    #     iPolygons=iPolygons.union_adjacent
    #     #print(ipts, isegments, iPolygons)
    #     return ipts, isegments, iPolygons
    
    
    # def intersect_simple_polygon(self,simple_polygon):
    #     ""
        
    #     if simple_polygon.classname in ['Triangle','Quadrilateral','Parallelogram','SimpleConvexPolygon']:
    #         return self.intersect_simple_convex_polygon(simple_polygon)
        
    #     if not simple_polygon.classname=='Polygon':
    #         raise TypeError
        
    #     ipts,isegments,iPolygons=self.triangles.intersect_triangles(simple_polygon.triangles)
        
    #     isegments.remove_segments_in_polygons(iPolygons)
    #     ipts=ipts.remove_points_in_segments(isegments)
    #     iPolygons=iPolygons.union_adjacent
        
    #     return ipts,isegments,iPolygons
    
    
    # def is_adjacent(self,simple_polygon):
    #     """Test to see if this simple polygon is adjacent to another simple polygon
        
    #     :return result:
    #         - returns True if a segment from one polygon contains a segment from another
    #     :rtype true:
        
    #     """
    #     for s in self.polyline.segments:
    #         for s1 in simple_polygon.polyline.segments:
    #             result=s.intersect_segment(s1)
    #             if result is None or result.classname=='Point':
    #                 continue
    #             elif result.classname=='Segment':
    #                 return True
    #             else:
    #                 raise Exception
    #     return False
    
    
    # def union_adjacent_simple_polygon(self,simple_polygon):
    #     ""
    #     pl1=self.polyline.segments.difference_segments(simple_polygon.polyline.segments).polyline
    #     pl2=simple_polygon.polyline.segments.difference_segments(self.polyline.segments).polyline
    #     pl3=pl1.union(pl2)
    #     if pl3:
    #         return Polygon2D(*pl3.points[:-1])
    #     else:
    #         return None
    
    
    def next_index(self,i):
        """Returns the next point index in the polygon.
        
        :param i: A point index.
        :type i: int
        
        :return: Returns the index of the next point in the polygon. 
            If i is the index of the last point, then the index of 
            the first point (i.e. 0) is returned.
        :rtype: int
        
        :Example:
    
        .. code-block:: python
           
           >>> pg = Polygon2D(Point2D(0,0), Point2D(1,0), Point2D(1,1))
           >>> result = pg.next_index(0)
           >>> print(result)
           1
        
        """
        n=len(self.points)
        if i==n-1:
            return 0
        else:
            return i+1
    
    
    def plot(self,ax=None,normal=False,**kwargs):
        """Plots the polygon on the supplied axes.
        
        :param ax: An Axes or Axes3D instance.
        :type ax: matplotlib.axes.Axes, mpl_toolkits.mplot3d.axes3d.Axes3D
        :param normal: If True then a normal vector is plotted for a 3D polygon;
            default False.
        :type normal: bool
        :param kwargs: Keyword arguments to be supplied to the matplotlib plot call.
                    
        """
        if not ax:
            if self.dimension=='2D':
                fig, ax = plt.subplots()
            else:
                fig = plt.figure()
                ax = fig.add_subplot(111, projection='3d')
        
        self.polyline.plot(ax,**kwargs)
        
        if normal and self.dimension=='3D':
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
    
    
    @property
    def points(self):
        """The points of the polyline.
        
        :rtype: Points
        
        :Example:
    
        .. code-block:: python
           
           >>> pg = Polygon2D(Point2D(0,0), Point2D(1,0), Point2D(1,1))
           >>> print(pg.points)
           Points(Point2D(0,0), Point2D(1,0), Point2D(1,1))
        
        """
        return self._points
    
    
    def previous_index(self,i):
        """Returns the previous point index in the polygon.
        
        :param i: A point index.
        :type i: int
        
        :return: Returns the index of the previous point in the polygon. 
            If i is the index of the first point (i.e. 0), then the index of 
            the last point is returned.
        :rtype: int
        
        :Example:
    
        .. code-block:: python
           
           >>> pg = Polygon2D(Point2D(0,0), Point2D(1,0), Point2D(1,1))
           >>> result = pg.previous_index(0)
           >>> print(result)
           2
        
        """
        n=len(self.points)
        if i==0:
            return n-1
        else:
            return i-1
        
        
    def reorder(self,i):
        """Returns a polygon with reordered points from a new start point.
        
        :param i: The index of the new start point.
        :type i: int
        
        :return: A polygon equal to this polygon with points
            starting at the new start point.
        :rtype: Polygon2D, Polygon3D
        
        :Example:
    
        .. code-block:: python
           
           # 2D example
           >>> pg = Polygon2D(Point2D(0,0), Point2D(1,0), Point2D(1,1))
           >>> result = pg.reorder(1)
           >>> print(result)
           Polygon2D(Point2D(1,0), Point2D(1,1), Point2D(0,0))
        
           # 3D example
           >>> pg = Polygon3D(Point3D(0,0,0), Point3D(1,0,0), Point3D(1,1,0))
           >>> result = pg.reorder(1)
           >>> print(result)
           Polygon3D(Point3D(1,0,0), Point3D(1,1,0), Point3D(0,0,0))
        
        """
        points=[]
        for _ in range(len(self.points)):
            points.append(self.points[i])
            i=self.next_index(i)
        return self.__class__(*points)
        
    
    @property
    def reverse(self):
        """Returns a polygon with the points reversed.
        
        :return: A new polygon with the points in reverse order.
        :rtype: Polygon2D, Polygon3D
        
        :Example:
    
        .. code-block:: python
           
           # 2D example
           >>> pg = Polygon2D(Point2D(0,0), Point2D(1,0), Point2D(1,1))
           >>> print(pg.reverse)
           Polygon2D(Point2D(1,1), Point2D(1,0), Point2D(0,0))
        
           # 3D example
           >>> pg = Polygon3D(Point3D(0,0,0), Point3D(1,0,0), Point3D(1,1,0))
           >>> print(pg.reverse)
           Polygon3D(Point3D(1,1,0), Point3D(1,0,0), Point3D(0,0,0))
        
        """
        points=[self.points[i] 
                for i in range(len(self.points)-1,-1,-1)]
        return self.__class__(*points)
    
    
    @property
    def _triangulate(self):
        """Returns a Polygon sequence of triangles which when combined have 
            the same  shape as the polygon.
        
        :rtype: Polygons
        
        """
        
        result=[]
        points=[x for x in self.points]
        
        while len(points)>2:
            
            n=len(points)
            
            for i in range(n-2):
                #print('i',i)
                #print('n',n)
                #print('len(points)',len(points))
                
                if i==n-1:
                    i_next=0
                else:
                    i_next=i+1
                
                if i==0:
                    i_prev=n-1
                else:
                    i_prev=i-1
                
                
                test_triangle=self.__class__(points[i],
                                             points[i_next],
                                             points[i_prev],
                                             known_convex=True)
                # test_triangle=t(points[i],
                #                 points[i_next]-points[i],
                #                 points[i_prev]-points[i])
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
                
    
        return Polygons(*result)
    
    
    @property
    def triangles(self):
        """A polygons sequence of triangles with the same combined shape as this polygon.
        
        :rtype: Polygons
        
        """    
        if not self._triangles:
            self._triangles=self._triangulate
        return self._triangles
       

class Polygon2D(Polygon):
    """A two dimensional polygon, situated on an x, y plane. 
    
    The default polygon is one which is known to be a simple polygon,
    but it is not known if it is convex or not.
    
    :param points: The points of the vertices of the polygon, in order. 
    :type points: Points
    :param known_convex: True if the polygon is known to be a convex polygon;
        otherwise False. 
        Default is False.
    :type known_convex: bool
    :param known_simple: True if the polygon is known to be a simple polygon;
        otherwise False.  
        A simple polygon is one whose edges do not intersect and whose
        vertices do not share any common points.
        Default is True.
    :type known_simple: bool
    
    :Example:
    
    .. code-block:: python
       
       >>> pg = Polygon2D(Point2D(0,0), Point2D(1,0), Point2D(1,1))
       >>> print(pg)
       Polygon2D(Point2D(0,0), Point2D(1,0), Point2D(1,1))
    
    """
        
    def __contains__(self,obj):
        """Tests if the polygon contains the geometric object.
        
        :param obj: A point. 
        :type obj: Point2D, Point3D
            
        :return: For point, True if the point lies inside the polygon 
            or on a polygon edge; otherwise False.
        :rtype: bool
        
        :Example:
    
        .. code-block:: python
           
           >>> pg = Polygon2D(Point2D(0,0), Point2D(1,0), Point2D(1,1))
           >>> result = Point2D(0,0) in pg
           >>> print(result)
           True
            
        """
        if isinstance(obj,Point2D):
            
            return self._winding_number(obj) > 0 or obj in self.polyline
                    
        else:
            
            return TypeError
        
        
    def __repr__(self):
        ""
        return 'Polygon2D(%s)' % ','.join([str(p) for p in self.points])
    
    
    @property
    def area(self):
        """Returns the area of the polygon.
        
        :rtype: float
        
        :Example:
    
        .. code-block:: python
           
           >>> pg = Polygon2D(Point2D(0,0), Point2D(1,0), Point2D(1,1))
           >>> print(pg.area)
           0.5

        """
        return abs(self.signed_area)
    
    
    @property
    def ccw(self):
        """An equivalent polygon with points in a counterclockwise orientation
        
        :rtype: Polygon2D
        
        """
        if not self._ccw:
            if self.is_counterclockwise:
                self._ccw=self
            else:
                self._ccw=self.reverse
        return self._ccw
    
    
    @property
    def centroid(self):
        """Returns the centroid of the polygon.
        
        :rtype: Point2D
        
        :Example:
    
        .. code-block:: python
           
           >>> pg = Polygon2D(Point2D(0,0), Point2D(1,0), Point2D(1,1),Point2D(0,1))
           >>> print(pg.centroid)
           Point2D(0.5,0.5)
        
        """
        x=sum([pt.x for pt in self.points])/len(self.points)
        y=sum([pt.y for pt in self.points])/len(self.points)
        return Point2D(x,y)        
        
    
    @property
    def dimension(self):
        """The dimension of the polygon.
        
        :return: '2D'
        :rtype: str
        
        :Example:
    
        .. code-block:: python
           
           >>> pg = Polygon2D(Point2D(0,0), Point2D(1,0), Point2D(1,1),Point2D(0,1))
           >>> print(pg.dimension)
           '2D'
        
        """
        return '2D'
    
    
    def _crossing_number(self,point):
        """Returns the crossing number for the supplied point.
        
        :param point: A 2D point.
        :type point: Point2D 
        
        :return: The number of times a line extending to the right of the point
            crosses the polygon segments. 
            Note: does not include a point on a top or right hand edge.
            
        :rtype: int
        """
        cp=0
        
        for ps in self.polyline.segments:
            
            if ((ps.P0.y <= point.y) and (ps.P1.y > point.y) or 
                (ps.P0.y > point.y) and (ps.P1.y <= point.y)):
                
                t=ps.line.calculate_t_from_y(point.y)
                ipt=ps.calculate_point(t)
                
                if point.x < ipt.x:
                    cp+=1
                
        return cp
    
    
    @property
    def is_counterclockwise(self):
        """Tests if the polygon points are in a counterclockwise direction.
        
        :raises ValueError: If the three polygon points being tested
            all lie on a straight line. 
        :return: Returns True if the three polygon points centered around the 
            rightmost lowest point are in a counterclockwise order.
            Returns False if these polygon points are in a clockwise order.
        
        :Example:
    
        .. code-block:: python
           
           >>> pg = Polygon2D(Point2D(0,0), Point2D(1,0), Point2D(1,1),Point2D(0,1))
           >>> print(pg.is_counterclockwise)
           True        
        
        """
        i=self.rightmost_lowest_vertex
        P0=self.points[self.previous_index(i)]
        P1=self.points[i]
        P2=self.points[self.next_index(i)]
        v0=P1-P0
        v1=P2-P1
        result=v0.perp_product(v1)
        if result>0:
            return True
        elif result<0:
            return False
        else:
            raise ValueError
        
    
    
    # @property
    # def orientation(self):
    #     """Returns the orientation of a 2D polygon.
        
    #     :return: Returns a value greater than 0 for counterclockwise.
    #         Returns 0 for none (degenerate).
    #         Returns a value less than 0 for clockwise.
    #     :rtype: float
    #     """
    #     i=self.rightmost_lowest_vertex
    #     P0=self.points[self.previous_index(i)]
    #     P1=self.points[i]
    #     P2=self.points[self.next_index(i)]
    #     return ((P1.x - P0.x) * (P2.y - P0.y)
    #             - (P2.x - P0.x) * (P1.y - P0.y) )
        
    
    @property
    def polyline(self):
        """Returns a polyline of the polygon points.
        
        :return: A polyline of the polygon points which starts and ends at 
            the first polygon point.
        :rtype: Polyline2D        
        
        :Example:
    
        .. code-block:: python
           
           >>> pg = Polygon2D(Point2D(0,0), Point2D(1,0), Point2D(1,1))
           >>> print(pg.polyline)
           Polyline2D(Point2D(0,0), Point2D(1,0), Point2D(1,1))
        
        """
        closed_points=tuple(list(self.points) + [self.points[0]])
        return Polyline2D(*closed_points)
    
    
    def project_3D(self,plane,coordinate_index):
        """Projection of 2D polygon on a 3D plane.
        
        :param plane: The plane for the projection.
        :type plane: Plane3D
        :param coordinate_index: The index of the coordinate which was ignored 
            to create the 2D projection. For example, coordinate_index=0
            means that the x-coordinate was ignored and this point
            was originally projected onto the yz plane.
        :type coordinate_index: int
        
        :return: 3D polygon which has been projected from the 2D polygon.
        :rtype: Polygon3D
        
        :Example:
    
        .. code-block:: python
           
           >>> pg = Polygon2D(Point2D(0,0), Point2D(1,0), Point2D(1,1))
           >>> pl = Plane3D(Point3D(0,0,1), Vector3D(0,0,1))
           >>> result = pg.project_3D(pl, 2)
           >>> print(result)
           Polygon3D(Point3D(0,0,1), Point3D(1,0,1), Point3D(1,1,1))
        
        """
        points=[pt.project_3D(plane,coordinate_index) for pt in self.points]
        return Polygon3D(*points)
        
    
    @property
    def rightmost_lowest_vertex(self):
        """Returns the index of the rightmost lowest point of the polygon.
        
        :rtype: int
        
        :Example:
    
        .. code-block:: python
           
           >>> pg = Polygon2D(Point2D(0,0), Point2D(1,0), Point2D(1,1))
           >>> print(pg.rightmost_lowest_vertex)
           Point2D(1,0)
        
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
        """Returns the signed area of the polygon.
        
        :return: Returns a value greater than 0 if polygon points are ordered counterclockwise.
            Returns a value less than 0 if polygon points are ordered clockwise.
        :rtype: float
                
        :Example:
    
        .. code-block:: python
           
           >>> pg = Polygon2D(Point2D(0,0), Point2D(1,1), Point2D(1,0))
           >>> print(pg.signed_area)
           -0.5
        
        """
        n=len(self.points)
        points=self.polyline.points
        if n<3: return 0  # a degenerate polygon
        a=0
        for i in range(1,n):
            a+=points[i].x * (points[i+1].y - points[i-1].y)
        a+=points[n].x * (points[1].y - points[n-1].y) # wrap-around term
        return a / 2.0
    
    
    def _winding_number(self,point):
        """Returns the winding number of the point for the polygon.
        
        :param point: A 2D point.
        :type point: Point2D
        
        :return: The number of times the polygon segments wind around the point.
            Note: does not include a point on a top or right hand edge.
        :rtype: int
        
        """
        
        wn=0 # the  winding number counter
    
        # loop through all edges of the polygon
        for ps in self.polyline.segments: # edge from V[i] to  V[i+1]
            if ps.P0.y <= point.y: # start y <= P.y
                if ps.P1.y > point.y: # an upward crossing
                    if ps.line.vL.perp_product(point-ps.P1)>0: # P left of  edge
                        wn+=1
            else:
                if ps.P1.y <= point.y: # a downward crossing
                    if ps.line.vL.perp_product(point-ps.P1)<0: # P right of  edge
                        wn-=1
        
        return wn
                    
        
    
class Polygon3D(Polygon):
    """A 3D polygon
    """
    
    dimension='3D'
       
    def __contains__(self,obj):
        """Tests if the polygon contains the object
        
        :param obj: a 3D geometric object 
            - Point3D, Segement3D, Polygon3D etc.
            
        :return result:
            - for point, True if the point lies within the polygon (including on an edge)
            - for segment...
            - for polygon ...
        :rtype bool:
            
        """
        if obj.classname=='Point':
            
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
        return 'Polygon3D(%s)' % ','.join([str(p) for p in self.points])
    
    
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
        return Polygon2D  
    

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
        closed_points=tuple(list(self.points) + [self.points[0]])
        return Polyline3D(*closed_points)
    
    
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
        #absolute_coords=[abs(x) for x in self.plane.N.coordinates]
        #i=absolute_coords.index(max(absolute_coords)) # the coordinate to ignore for projection
        
        i=self.plane.N.index_largest_absolute_coordinate
        
        if i==0:
            pg=self.class_2D(*[Point2D(pt.y,pt.z) for pt in self.points])
        elif i==1:
            pg=self.class_2D(*[Point2D(pt.z,pt.x) for pt in self.points])
        elif i==2:
            pg=self.class_2D(*[Point2D(pt.x,pt.y) for pt in self.points])
        else:
            raise Exception
                    
        return i, pg
        
    
    def __intersect_plane(self,plane):
        """Returns the intersection of this 3D simple polygon and a plane
        
        :param plane Plane3D: a 3D plane 
        
        :return result: (Points,Segments)
            
        """
        if self.plane==plane:
            return self
        
        elif self.plane.is_parallel(plane):
            return None
        
        else:
        
            ipts,isegments=self.triangles.intersect_plane(plane)
            
            ipts.remove_points_in_segments(isegments)
            isegments=isegments.union
            
            return ipts,isegments
    
    
    def __intersect_simple_polygon_coplanar(self,simple_polygon):
        """Intersection of this polygon with another coplanar polygon
        
        """
        i,self_2D=self.project_2D
        i,scp_2D=simple_polygon.project_2D
        
        ipts,isegments,iPolygons=self_2D.intersect_simple_polygon(scp_2D)
    
        return (ipts.project_3D(self.plane,i),
                isegments.project_3D(self.plane,i),
                iPolygons.project_3D(self.plane,i))
    
    
    def ___intersect_simple_polygon_skew(self,simple_polygon):
        """Intersection of this polygon with another skew polygon
        
        """
        ipts,isegments=self.intersect_plane(simple_polygon.plane)
        
        if len(ipts)==0 and len(isegments)==0:
            return ipts,isegments
        
        else:
        
            i,sp_2D=simple_polygon.project_2D
            ipts_2D=ipts.project_2D(i)
            isegments_2D=isegments.project_2D(i)
            
            ipts2,isegments2=sp_2D.intersect_segments(isegments_2D)
                
            for pt in ipts_2D:
                if pt in sp_2D:
                    ipts2.append(pt,unique=True)
            
            return ipts2,isegments2
            
        
    def __intersect_simple_polygon(self,simple_polygon):
        """Intersection of this simple polygon with another simple polygon
        
        :param simple_polygon Polygon: a simple polygon 
        
        :return intersection:
            - return value can be:
                - if the two polygons are on the same plane:
                    - Points -> a point (for a convex polygon whose segments intersect
                                      this convex polygon at a single vertex)
                    - Segments -> a segment (for a convex polygon whose segments
                                          intersect this convex polygon at an edge segment)
                    - Polygons - > a simple convex polygon (for a convex
                                            polygon which overlaps this polygon)
                
                - if the two polygons are on skew planes
                    - Points -> for two polygons which intersect at a single point
                    - Segments -> for two polygons that intersect along a segment
                         
        """
        if self.plane==simple_polygon.plane:
            
            return self._intersect_simple_polygon_coplanar(simple_polygon)
            
        else: # polygons exist in different planes
            
            return self._intersect_simple_polygon_skew(simple_polygon)
                    
    
    
    
    
    def __intersect_halfline(self,halfline):
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
        result=self.plane.intersect_line(halfline) # intersection of polygon plane with halfline
        
        if result is None:
            return Points(),Segments()
        
        elif result.classname=='Point':
            if result in self:
                return Points(result),Segments()
            else:
                return None
            
        elif result.classname=='Halfline':
            # coplanar, look for intersections on 2D plane
            raise Exception('Not implemented yet')
    
        else:
            raise Exception
    
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
            
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#class Polygon3D():
#    ""
#    
#    def __init__(self,*points):
#        ""
#        self.points=tuple(points)
#    
#    def __repr__(self):
#        return 'Polygon2D(%s)' % ','.join([str(p) for p in self.points])
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
#            pg=Polygon2D([Point2D(pt.y,pt.z) for pt in self.points])
#            return pg.area*(normal_vector.length/(2*normal_vector.x))
#        if i=='1':
#            pg=Polygon2D([Point2D(pt.x,pt.z) for pt in self.points])
#            return pg.area*(normal_vector.length/(2*normal_vector.y))
#        if i=='2':
#            pg=Polygon2D([Point2D(pt.x,pt.y) for pt in self.points])
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
#        #       ._polygon_segment (the PolygonSegment or None)
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
    