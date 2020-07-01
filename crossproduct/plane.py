# -*- coding: utf-8 -*-

import bspy.geometry

from .halfline import Halfline3D
from .line import Line3D
from .point import Point3D
from .segment import Segment3D
from .vector import Vector3D

SMALL_NUM=0.00000001



class Plane3D():
    """A 3D plane
    
    Equation of plane: N . (P - P0) = 0
        where:
            - N is a normal 3D vector to the plane
            - P is any point on the plane
            - P0 is the start point of the plane
    
    """    
    
    
    def __init__(self,P0,N):
        """
        
        :param P0 Point3D: a 3D point on the plane
        :param N Vector3D: a 3D vector which is normal to the plane
        
        """
        
        if isinstance(P0,Point3D):
            self.P0=P0
        else:
            raise TypeError
            
        if isinstance(N,Vector3D):
            self.N=N
        else:
            raise TypeError
        
        
    def __contains__(self,obj):
        """Tests if the line contains the object
        
        :param obj: a 3D geometric object 
            - Point3D, Halfline3D Segement3D etc.
            
        :return result:
            - for point, ...
            - for line,
            - for halfline,
            - for segment,
            - for polygon
        :rtype bool:
        
        """
        if isinstance(obj,Point3D):
            
            point=obj
            return self.N.is_perpendicular(point-self.P0)
            
        elif isinstance(obj,Line3D) or isinstance(obj,Halfline3D) or isinstance(obj,Segment3D):
            
            linelike_obj=obj            
            return linelike_obj.P0 in self and self.is_parallel(linelike_obj)
          
        
        else:

            raise Exception('%s in Plane not yet implemented' % obj.__class__.__name__)
        
        
    def __eq__(self,plane):
        """Tests if this plane and the supplied plane are equal, i.e. coplanar
        
        :param plane Plane3D: a 3D plane
        
        :return result: 
            - True if 
                - the normal vectors are collinear and
                - a point can exist on both planes
            - otherwise False
        :rtype bool:
            
        A plane is equivalent to another plane if:
            - the normal vectors are parallel and
            - a point can exist on both planes        
        
        """
        if isinstance(plane,Plane3D):
            return self.is_parallel(plane) and plane.P0 in self
        else:
            return False
        
        
    def __repr__(self):
        """The string of this line for printing
        
        :return result:
        :rtype str:
            
        """
        return 'Plane3D(%s, %s)' % (self.P0,self.N)
    
    
    def distance_point(self,point):
        """Returns the distance to the supplied point
        
        :param point Point3D: 
        
        :return result: the absolute value of the signed distance
            see Plane.signed_distance_point
        :rtype float:
        """
        return abs(self.signed_distance_point(point))
    
    
    def intersect_halfline(self,halfline):
        """Returns the intersection of this plane and a halfline
        
        :param halfline Halfline3D: a 3D halfline 
        
        :return result:
            - no intersection (None): 
                - for parallel, non-collinear plane and halfline
                - for skew, non-intersecting plane and halfline
            - a halfline: for a halfline on the plane
            - a point: for a skew halfline which intersects the plane
            
        
        """
        if halfline in self: # plane and halfline are collinear
            return halfline
        elif self.is_parallel(halfline): # plane and halfline are parallel 
            return None
        else:
            ipt=self.intersect_line_skew(halfline.line)
            if ipt in halfline:
                return ipt
            else:
                return None
        
        
    def intersect_line(self,line):
        """Returns the intersection of this plane and a line
        
        :param line Line3D: a 3D line 
        
        :return result:
            - no intersection (None): for parallel, non-collinear plane and line
            - a line: for a line on the plane
            - a point: for a skew line which intersects the plane
            
        
        """
        if line in self: # plane and line are collinear
            return line
        elif self.is_parallel(line): # plane and line are parallel 
            return None
        else:
            return self.intersect_line_skew(line)
            
        
    def intersect_line_skew(self,skew_line):
        """Returns the intersection of this plane and a skew line
        
        :param skew_line Line3D: a 3D line which is skew to the plane
        
        :return result:
        :rtype Point3D:
        """
        if not self.is_parallel(skew_line):
            n=self.N
            u=skew_line.vL
            w=skew_line.P0-self.P0
            t=-n.dot(w) / n.dot(u)
            return skew_line.calculate_point(t)
        else:
            raise ValueError('%s and %s are not skew' % (self,skew_line))
        
        
    def intersect_segment(self,segment):
        """Returns the intersection of this plane and a segment
        
        :param segment Segment3D: a 3D segment 
        
        :return result:
            - no intersection (None): 
                - for parallel, non-collinear plane and segment
                - for skew, non-intersecting plane and segment
            - a segment: for a segment on the plane
            - a point: for a skew segment which intersects the plane
            
        
        """
        if segment in self: # segment lies on the plane
            return segment
        elif self.is_parallel(segment): # plane and segment are parallel 
            return None
        else:
            ipt=self.intersect_line_skew(segment.line)
            if ipt in segment:
                return ipt
            else:
                return None
            
            
    def intersect_plane(self,plane):
        """Returns the intersection of this plane and another plane
        
        :param plane Plane3D: a 3D plane 
        
        :return result:
            - no intersection (None): for parallel, non-coplanar planes
            - a plane: for two coplanar planes
            - a line: for non-parallel planes
            
        
        """
        if plane==self:
            return self
        elif plane.is_parallel(self):
            return None
        else:
            n1=self.N
            d1=-n1.dot(self.P0-Point3D(0,0,0))
            n2=plane.N
            d2=-n2.dot(plane.P0-Point3D(0,0,0))
            n3=n1.cross_product(n2)
            P0=Point3D(0,0,0) + ((n1*d2-n2*d1).cross_product(n3) * (1 / (n3.length**2)))
            u=n3
            return Line3D(P0,u)
            
            
        
    def intersect_polygon(self,polygon):
        """
        """
        return polygon.intersect_plane(self)
        
    def intersect_polyhedron(self,polyhedron):
        """
        """
        return polyhedron.intersect_plane(self)
    
    
    def is_parallel(self,obj):
        """Tests if this plane and the supplied object are parallel
        
        :param linelike_obj: a Line3D, Halfline3D, Segment3D, Plane3D or Polygon3D
        
        :return result: the result of the test
            - returns True if the object is collinear with the plane
            - otherwise False
        :rtype bool:
            
        """
        if isinstance(obj,Line3D) or isinstance(obj,Halfline3D) or isinstance(obj,Segment3D):
            return self.N.is_perpendicular(obj.vL)
        
        elif isinstance(obj,Plane3D):
            return self.N.is_collinear(obj.N)
        
        else:
            raise Exception('Not implemented yet')
            
            
    def is_perpendicular(self,obj):
        """Tests if this plane and the supplied object are perpendicular
        
        :param linelike_obj: a Line3D, Halfline3D, Segment3D, Plane3D or Polygon3D
        
        :return result: the result of the test
            - returns True if the object is perpendicular with the plane
            - otherwise False
        :rtype bool:
            
        """
        if isinstance(obj,Line3D) or isinstance(obj,Halfline3D) or isinstance(obj,Segment3D):
            return self.N.is_collinear(obj.vL)
        
        elif isinstance(obj,Plane3D):
            return self.N.is_perpendicular(obj.N)
        
        else:
            raise Exception('Not implemented yet')
        
    
    def point_xy(self,x,y):
        """Returns a point on the plane given a x and y coordinates
        
        """
        z=self.P0.z-(self.N.x*(x-self.P0.x)+self.N.y*(y-self.P0.y))/self.N.z
        return Point3D(x,y,z)
    
    
    def point_xz(self,x,z):
        """Returns a point on the plane given a x and y coordinates
        
        """
        y=self.P0.y-(self.N.x*(x-self.P0.x)+self.N.z*(z-self.P0.z))/self.N.y
        return Point3D(x,y,z)
    
    
    def point_yz(self,y,z):
        """Returns a point on the plane given a x and y coordinates
        
        """
        x=self.P0.x-(self.N.y*(y-self.P0.y)+self.N.z*(z-self.P0.z))/self.N.x
        return Point3D(x,y,z)
    
    
    def signed_distance_point(self,point):
        """Returns the signed distance to the supplied point
        
        :param point Point3D: 
        
        :return signed_distance: distance is positive on one side of the plane 
            (the side in the direction of the normal) or is negative for
            the other side
        :rtype float:
            
        """
        return self.N.dot(point-self.P0) / self.N.length
    
        
            
    
    
    
    