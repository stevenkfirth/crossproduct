# -*- coding: utf-8 -*-

from .line import Line3D
from .point import Point, Point2D, Point3D
from .simple_convex_polygon import SimpleConvexPolygon, SimpleConvexPolygon2D, SimpleConvexPolygon3D
from .segment import Segment, Segment3D
from .vector import Vector, Vector2D, Vector3D
from .triangles import Triangles


class Triangle():
    """A n-D triangle
    """
    
    def __init__(self,P0,v,w):
        """
        
        :param P0 Point2D: a point on the triangle
        :param v Vector2D: a vector on the triangle from P0 to P1
        :param w Vector2D: a vector on the triangle from P0 to P2
        
        """
        if isinstance(P0,Point):
            self.P0=P0
        else:
            raise TypeError
            
        if isinstance(v,Vector):
            self.v=v
        else:
            raise TypeError
        
        if isinstance(w,Vector):
            self.w=w
        else:
            raise TypeError
    
        # orientate counterclockwise if a 2D triangle
        if isinstance(P0,Point2D):
            if self.orientation<0:
                self.v=w
                self.w=v
                
        #self.triangles=self.triangluate
                

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


    @property
    def triangles(self):
        return Triangles(self)



class Triangle2D(Triangle,SimpleConvexPolygon2D):
    """A 2D Triangle
    """
    
    def __contains__(self,obj):
        """Tests if the 2D triangle contains the object
        
            - includes points on all edges and inside
        
        :param obj: a 2D geometric object 
            - Point2D, Segment2D, Polygon2D
            
        :return result:
            - for point, True if the point lies within the triangle (including on an edge)
            - for segment...
            - for polygon ...
        :rtype bool:
            
        """
        if isinstance(obj,Point2D):
            
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
        """The string of this triangle for printing
        
        :return result:
        :rtype str:
            
        """
        return 'Triangle2D(%s, %s, %s)' % (self.P0,self.v,self.w)
        
        
    @property
    def area(self):
        """Returns the area of the triangle
        
        :return result:
        :rtype float:

        """
        return abs(self.signed_area)
    
    
#    def intersect_triangle(self,triangle):
#        """
#        
#        """
#        return self.intersect_simple_convex_polygon(triangle)
    
    
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
    def signed_area(self):
        """Returns the signed area of the triangle
        
        :return result:
            - return value >0 if triangle points are ordered counterclockwise
            - return value <0 if triangle points are ordered clockwise
        :rtype float:
                
        """
        return 0.5*(self.v.x*self.w.y-self.w.x*self.v.y)
    
    
    def union_triangle_edge_intersection(self,triangle):
        """Returns the union of two triangles that share edge intersection
        
        :return result:
        :rtype SimplePolygon or None:
        
        """
        
        # difference_segments instead of intersect segments ??
        
        ipts1,isegments1=self.intersect_segments(triangle.polyline.segments)
        print(ipts1,isegments1)
        
        if len(ipts1)==0 and len(isegments1)==0: # no union, no intersection
            return None
        
        elif len(ipts1)==1 and len(isegments1)==0: # no union, point intersection
            return None
        
        elif len(ipts1)==0 and len(isegments)==1: # segment intersection
            
            if isegments1[0] in self.polyline.segments: # exact segment
                
                pass
        
        
        else:
            raise Exception
        
        
    
class Triangle3D(Triangle,SimpleConvexPolygon3D):
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
        if isinstance(obj,Point3D):
            
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
        """The string of this triangle for printing
        
        :return result:
        :rtype str:
            
        """
        return 'Triangle3D(%s, %s, %s)' % (self.P0,self.v,self.w)
        
        
    @property
    def area(self):
        """Returns the area of the triangle
        
        :return result:
        :rtype float:

        """
        return 0.5*self.v.cross_product(self.w).length
    
    
    @property
    def class_2D(self):
        return Triangle2D  
    
    
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
        
        elif self.plane.is_parallel(plane):
            return None
        
        else:
        
            ipts=[]
            for ps in self.polyline.segments:
                i=plane.intersect_segment(ps)
                if i is None:
                    continue
                elif isinstance(i,Segment3D): # if a segment, then this is the result
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
            
            if isinstance(iresult1,Point3D):
                if iresult1 in triangle:
                    return iresult1 
                else:
                    return None
                
            elif isinstance(iresult2,Point3D):
                if iresult2 in self:
                    return iresult2
                else:
                    return None
            
            elif isinstance(iresult1,Segment3D) and isinstance(iresult2,Segment3D):
            
                    return iresult1.intersect_segment(iresult2)
            
            else:
                raise Exception()     
    
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
   
    
    
    
    
    
    
    
    