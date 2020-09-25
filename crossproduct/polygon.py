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
        #print('polyline',polyline)
        ipts, isegments = self.intersect_segments(polyline.segments)
        #print('ipts',ipts)
        #print('isegments',isegments)
        ipolylines=Polylines(*[polyline.__class__(*s.points) for s in isegments])
        ipolylines=ipolylines.add_all
        return ipts, ipolylines
    
    
    def _intersect_polygon_simple_convex_and_simple_convex(self,polygon,debug=False):
        ""
        
        if debug: print('_intersect_polygon_simple_convex_and_simple_convex')
        
        ipts1,ipolylines1=self.intersect_polyline(polygon.polyline)
        #print(ipts1,ipolylines1)
        
        
        if len(ipts1)==0 and len(ipolylines1)==0:
            return Points(),Polylines(),Polygons() # returns None - no intersection
        elif len(ipts1)==1 and len(ipolylines1.segments)==0:
            return Points(ipts1[0]),Polylines(),Polygons() # returns a Point2D - point intersection
        elif len(ipts1)>1:
            raise Exception
        #elif len(ipts1)==0 and len(ipolylines1.segments)==1:
        #    return Points(),Polylines(ipolylines1[0]),Polygons() # returns a Segment2D - edge segment intersection
        else: 
            ipts2,ipolylines2=polygon.intersect_polyline(self.polyline)
            #print(ipts2,ipolylines2)
            
            if len(ipolylines1.segments)==1 and len(ipolylines2.segments)==1:
                return Points(),Polylines(ipolylines1[0]),Polygons() # returns a Segment2D - edge segment intersection
            
            else: # a simple convex polygon intersection
                
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
                
                if debug:
                    ax=self.plot(linestyle='--')
                    polygon.plot(ax=ax,linestyle='--')
                    pg.plot(ax=ax,color='red')
                    ax.set_title('The intersection result')
                
                return Points(),Polylines(),Polygons(pg)
        
        
    def _intersect_polygon_simple_and_simple_convex(self,polygon,debug=False):
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
    
    
    def _intersect_polygon_simple_and_simple(self,polygon,debug=False):
        ""
        
        if debug: print('_intersect_polygon_simple_and_simple')
        
        pts=Points()
        pls=Polylines()
        pgs=Polygons()
            
        if debug:
            ax=None
            for pg in self.triangles:
                ax=pg.plot(ax)
            ax.set_title('First polygon triangles')
        
            ax=None
            for pg in polygon.triangles:
                ax=pg.plot(ax)
            ax.set_title('Second polygon triangles')
            
        
        for pg1 in self.triangles:
        
            for pg2 in polygon.triangles:
                
                ipts,ipls,ipgs=pg1._intersect_polygon_simple_convex_and_simple_convex(pg2)
            
                if debug:
                    ax=pg1.plot(linestyle='--')
                    pg2.plot(ax,linestyle='--')
                    ipgs.plot(ax,color='red')
                    ax.set_title('Intersecting triangle pair')
            
            
                #print(pg1,pg2)
                #print(pg1.known_convex, pg2.known_convex)
                #raise Exception
                #print(ipts,ipls,ipgs)
            
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
        
        #print(pls)
        
        #print(pgs)
        
        pgs=pgs.add_all
        
        #print(pgs)
        
        if debug:
            ax=self.plot(linestyle='--')
            polygon.plot(ax=ax,linestyle='--')
            pgs.plot(ax=ax,color='red')
            ax.set_title('The intersection result')
        
        
        return pts,pls,pgs
    
    
    def intersect_polygon(self,polygon,debug=False):
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

        if debug:
            ax=self.plot()
            polygon.plot(ax)
            ax.set_title('The two intersecting polygons')
            
        if self._known_simple and polygon._known_simple:
            
            if self._known_convex and polygon._known_convex:
                
                return self._intersect_polygon_simple_convex_and_simple_convex(polygon, debug=debug)
            
            elif not self._known_convex and polygon._known_convex:
                
                return self._intersect_polygon_simple_and_simple_convex(polygon, debug=debug)
            
            elif self._known_convex and not polygon._known_convex:

                return polygon._intersect_polygon_simple_and_simple_convex(self, debug=debug)
            
            elif not self._known_convex and not polygon._known_convex:
                
                return self._intersect_polygon_simple_and_simple(polygon,debug=debug)

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
        #print(self)
        #print(line)
        
        if self.dimension=='2D':
            polygon=self
            l=line
        else:
            plane=self.plane
            
            if line in plane:
                
                coordinate_index,polygon=self.project_2D
                l=line.project_2D(coordinate_index)
                
            else:
                
                result=plane.intersect_line(line)
                
                if result is None: # polygon and line are parallel
                    return None
                else:
                    if result in self:
                        t=line.calculate_t_from_point(result)
                        return (t,t)
                    else:
                        return None
        
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
            
        #print(t_entering)
            
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
        
        .. seealso:: `<https://geomalgorithms.com/a13-_intersect-4.html>`_
        
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
                        
            #x=abs(N.dot(ax_vector)/N.length)
           
            #print('c',c.coordinates)
            #print('N',N.normalise.coordinates)
            
            ax.quiver(*c.coordinates,
                      *N.normalise.coordinates, 
                      #length=x*0.2,
                      lw=3)
    
        return ax
    
    
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
    def _first_triangle(self):
        """Finds the first triangle in the polygon
        
        :param polygon: A 2D polygon which is counterclockwise.
        
        :rtype: tuple (triangle,remaining_polygon)
        
        """
        
        for i in range(len(self.points)):
            #print(i)
            
            pg=self.reorder(i)
                        
            triangle=Polygon2D(*pg.points[0:3],known_convex=True)
            
            if triangle.is_counterclockwise:
                
                inside_point=False
                remaining_points=pg.points[3:]
                for pt in remaining_points:
                    if pt in triangle:
                        inside_point=True
                
                if not inside_point:
                
                    points=list(pg.points)
                    points.pop(1)
                    
                    # merge any codirectional segments
                    pl=Polyline2D(*points)
                    #print(pl)
                    sgmts=pl.segments
                    #print(sgmts)
                    sgmts=sgmts.add_all
                    
                    pts=[s.P0 for s in sgmts]+[sgmts[-1].P1]
                    
                    return triangle, Polygon2D(*pts)
            
        raise Exception
    
    
    @property
    def _triangulate(self):
        """Returns a Polygon sequence of triangles which when combined have 
            the same  shape as the polygon.
        
        :rtype: Polygons
        
        """
        
        debug=False
        
        triangles=Polygons()
        
        # project to 2D if needed
        if self.dimension=='2D':
            pg=self
        elif self.dimension=='3D':
            coordinate_index,pg=self.project_2D
        
        # orientate the 2D polygon counterclockwise
        pg=pg.ccw
        
        if debug: ax=pg.plot()
        
        n=len(pg.points)
        while n>2: # keep looping if pghas more than two points
        
            t,pg=pg._first_triangle
            #print(t)
            triangles.append(t)
            n=len(pg.points)
            
            if debug: ax=t.plot(ax)
            
            
        # project to 3D if needed
        if self.dimension=='2D':
            return triangles
        elif self.dimension=='3D':
            return triangles.project_3D(self.plane, coordinate_index)
            
        
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

        .. seealso:: `<https://geomalgorithms.com/a01-_area.html>`_

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
        
        .. seealso:: `<https://geomalgorithms.com/a03-_inclusion.html>`_
        
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
           Polyline2D(Point2D(0,0), Point2D(1,0), Point2D(1,1), Point2D(0,0))
        
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
        return Polygon3D(*points,known_convex=self.known_convex)
        
    
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
        
        .. seealso:: `<https://geomalgorithms.com/a01-_area.html>`_
        
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
        
        .. seealso:: `<https://geomalgorithms.com/a03-_inclusion.html>`_
        
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
        
        :param obj: A 3D point. 
        :type obj: Point3D
            
        :return: For point, True if the point lies inside the polygon 
            or on a polygon edge; otherwise False.
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

        .. seealso:: `<https://geomalgorithms.com/a01-_area.html>`_            

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
    
    
    def _intersect_plane_volume_simple_convex(self,plane_volume):
        """Intersection of a simple convex polygon with a plane volume.
        
        :rtype: None, Point3D, Segment3D, Polygon3D
        
        """
        if self.polyline in plane_volume:
            return self
        
        result=self._intersect_plane_simple_convex_skew(plane_volume.plane)
        
        if result is None:
            return None
        elif result.classname=='Point': # single point intersection on plane of plane volume
            return result
        elif result.classname=='Polygon': # polygon on plane of plane volume
            return result
        elif result.classname=='Segment':
            
            if result in self.polyline.segments: # one of the polygon sides intersects with plane of plane volume
                return result
            
            else: # a skew polygon intersection

                pts,polylines=plane_volume.intersect_polyline(self.polyline)
                polylines.append(Polyline3D(result.P0,result.P1))
                polylines=polylines.add_all
                return Polygon3D(*polylines[0].points[:-1],known_convex=True)
                
        else:
            raise Exception
            
    
    def _intersect_plane_volume_simple(self,plane_volume):
        """Intersection of a simple polygon with a plane volume.
        
            :rtype: tuple (Points,Segments,Polygons)
        
        """
        pts=Points()
        sgmts=Segments()
        pgs=Polygons()
            
        for pg in self.triangles:
            
            result=pg._intersect_plane_volume_simple_convex(plane_volume)
        
            if result is None:
                pass
            elif result.classname=='Point':
                pts.append(result,unique=True)
            elif result.classname=='Segment':
                sgmts.append(result,unique=True)
            elif result.classname=='Polygon':
                pgs.append(result,unique=True)
                
        pts=pts.remove_points_in_segments(sgmts)
        sgmts=sgmts.remove_segments_in_polygons(pgs)
        sgmts=sgmts.add_all
        pgs=pgs.add_all
        
        return pts,sgmts,pgs
    
    
    def intersect_plane_volume(self,plane_volume):
        """Returns the intersection of this 3D polygon and a plane volume.
        
        :param plane_volume: A 3D plane volume.
        :type plane_volume: PlaneVolume3D
        
        :return: A tuple of intersection points, intersection segments 
            and intersection polygons in the form (Points, Segments, Polygons).
        :rtype: tuple      
            
        """
        
        if self.polyline in plane_volume:
            return (Points(),Segments(),Polygons(self))
        
        else:
        
            if self.known_simple:    
        
                if self.known_convex:
                    
                    result=self._intersect_plane_volume_simple_convex(plane_volume)
                    if result is None:
                        return (Points(),Segments(),Polygons())
                    elif result.classname=='Point':
                        return (Points(result),Segments(),Polygons())
                    elif result.classname=='Segment':
                        return (Points(),Segments(result),Polygons())
                    elif result.classname=='Polygon':
                        return (Points(),Segments(),Polygons(result))
                    else:
                        raise Exception
                
                else:
                    
                    return self._intersect_plane_volume_simple(plane_volume)

            else:
                
                raise NotImplementedError('This function is not implemented at present for a possible non-simple polygon')
                
        
        
    
    
    def _intersect_plane_simple_convex_skew(self,plane):
        """Returns the intersection of this 3D simple convex polygon and a skew plane
        
        :param plane: A 3D plane.
        :type plane: Plane3D
        
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
    
    
    def _intersect_plane_simple_skew(self,plane):
        """Returns the intersection of this 3D simple polygon and a skew plane
        
        :param plane: A 3D plane.
        :type plane: Plane3D
        
        :return: A tuple of intersection points and intersection segments 
            in the form (Points, Segments). 
        :rtype: tuple      
        
        """
        pts=Points()
        sgmts=Segments()
            
        for pg in self.triangles:
            
            result=pg._intersect_plane_simple_convex_skew(plane)
        
            if result is None:
                pass
            elif result.classname=='Point':
                pts.append(result,unique=True)
            elif result.classname=='Segment':
                sgmts.append(result,unique=True)
                
        pts=pts.remove_points_in_segments(sgmts)
        sgmts=sgmts.add_all
        
        return pts,sgmts
        
    
    def intersect_plane(self,plane):
        """Returns the intersection of this 3D polygon and a plane
        
        :param plane: A 3D plane.
        :type plane: Plane3D
        
        :return: A tuple of intersection points, intersection segments 
            and intersection polygons in the form (Points, Segments, Polygons).
        :rtype: tuple      
            
        """
        if self.plane==plane:
            return (Points(),Segments(),Polygons(self))
        
        elif self.plane.N.is_collinear(plane.N):
            return (Points(),Segments(),Polygons())
        
        else:
        
            if self.known_simple:    
        
                if self.known_convex:
                    
                    result=self._intersect_plane_simple_convex_skew(plane)
                    if result is None:
                        return (Points(),Segments(),Polygons())
                    elif result.classname=='Point':
                        return (Points(result),Segments(),Polygons())
                    elif result.classname=='Segment':
                        return (Points(),Segments(result),Polygons())
                
                else:
                    
                    pts,sgmts=self._intersect_plane_simple_skew(plane)
                    return (pts,sgmts,Polygons())

            else:
                
                raise NotImplementedError('This function is not implemented at present for a possible non-simple polygon')
                

    @property
    def plane(self):
        """Returns the plane of the 3D polygon
        
        :return plane: a 3D plane which contains all the polygon points
        :rtype: Plane3D
        
        """
        P0,P1,P2=self.points[:3]
        N=(P1-P0).cross_product(P2-P1)
        return Plane3D(P0,N)
    
    
    @property
    def polyline(self):
        """Returns a polyline of the polygon points.
        
        :return: A polyline of the polygon points which starts and ends at 
            the first polygon point.
        :rtype: Polyline3D        
        
        :Example:
    
        .. code-block:: python
           
           >>> pg = Polygon3D(Point3D(0,0,0), Point3D(1,0,0), Point3D(1,1,0))
           >>> print(pg.polyline)
           Polyline3D(Point3D(0,0,0), Point3D(1,0,0), Point3D(1,1,0), Point3D(0,0,0))
        
        """
        closed_points=tuple(list(self.points) + [self.points[0]])
        return Polyline3D(*closed_points)
    
    
    @property
    def project_2D(self):
        """Projects the 3D polygon to a 2D polygon.
        
        :return: A tuple (coordinate_index,polygon). 
            coordinate_index=0 to ignore the x-coordinate, coordinate_index=1 
            for the y-coordinate and coordinate_index=2 for the z-coordinate.
            polygon is the 2D projected polygon.
        :rtype: tuple
            
        """
        i=self.plane.N.index_largest_absolute_coordinate
        
        if i==0:
            pg=Polygon2D(*[Point2D(pt.y,pt.z) for pt in self.points],
                         known_convex=self.known_convex)
        elif i==1:
            pg=Polygon2D(*[Point2D(pt.z,pt.x) for pt in self.points],
                         known_convex=self.known_convex)
        elif i==2:
            pg=Polygon2D(*[Point2D(pt.x,pt.y) for pt in self.points],
                         known_convex=self.known_convex)
        else:
            raise Exception
                    
        return i, pg
        
    
    
    