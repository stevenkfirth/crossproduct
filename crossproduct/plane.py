# -*- coding: utf-8 -*-

from .line import Line3D
from .point import Point3D
from .points import Points
from .segments import Segments


SMALL_NUM=0.00000001


class Plane3D():
    """A three dimensional plane, situated on an x, y, z plane.
    
    Equation of plane: N . (P - P0) = 0 where:
        
        - N is a normal 3D vector to the plane
        - P is any point on the plane
        - P0 is the start point of the plane
    
    :param P0: A 3D point on the plane.
    :type P0: Point3D
    :param N: A 3D vector which is normal to the plane.
    :type N: Vector3D 
    
    :Example:
    
    .. code-block:: python
       
       >>> pl = Polyline2D(Point2D(0,0), Point2D(1,0), Point2D(1,1))
       >>> print(pl)
       Polyline2D(Point2D(0,0), Point2D(1,0), Point2D(1,1))

    """    
    
    
    def __init__(self,P0,N):
        ""
        self._P0=P0
        self._N=N
        
        
    def __contains__(self,obj):
        """Tests if the plane contains the object.
        
        :param obj: A 3D geometric object.
        :type obj: Point3D, Line3D, Halfline3D, Segment3D
            
        :rtype: bool
        
        """
        if obj.__class__.__name__=='Point3D':
            
            point=obj
            return self._N.is_perpendicular(point-self._P0)
            
        elif obj.__class__.__name__=='Line3D':
            
            return obj.P0 in self and self._N.is_perpendicular(obj.vL)
          
        elif obj.__class__.__name__ in ['Halfline3D','Segment3D']:
            
            return obj.P0 in self and self._N.is_perpendicular(obj.line.vL)
          
        
        else:

            raise Exception('%s in Plane not yet implemented' % obj.__class__.__name__)
        
        
    def __eq__(self,plane):
        """Tests if this plane and the supplied plane are equal, i.e. coplanar.
        
        :param plane: A 3D plane.
        :type plane: Plane3D 
        
        :return: True if the normal vectors are collinear and 
            a point can exist on both planes;
            otherwise False.
        :rtype: bool
            
        """
        if isinstance(plane,Plane3D):
            return self._N.is_collinear(plane.N) and plane.P0 in self
        else:
            return False
        
        
    def __repr__(self):
        ""
        return 'Plane3D(%s, %s)' % (self._P0,self._N)
    
    
    def distance_point(self,point):
        """Returns the distance to the supplied point.
        
        :param point: A 3D point.
        :type point: Point3D
        
        :return: The distance between the plane and the point
        :rtype: float
        
        """
        return abs(self.signed_distance_point(point))
    
    
    def intersect_halfline(self,halfline):
        """Returns the intersection of this plane and a halfline.
        
        :param halfline: A 3D halfline. 
        :type halfline: Halfline3D 
        
        :return: Returns None for parallel, non-collinear plane and halfline.
            Returns None for skew, non-intersecting plane and halfline.
            Returns halfline for a halfline on the plane.
            Return point for a skew halfline which intersects the plane.
        :rtype: None, Point3D, Halfline3D
            
        """
        if halfline in self: # plane and halfline are collinear
            return halfline
        elif self._N.is_perpendicular(halfline.line.vL): # plane and halfline are parallel 
            return None
        else:
            ipt=self._intersect_line_skew(halfline.line)
            if ipt in halfline:
                return ipt
            else:
                return None
        
        
    def intersect_line(self,line):
        """Returns the intersection of this plane and a line.
        
        :param line: A 3D line. 
        :type line: Line3D 
        
        :return: Returns None for parallel, non-collinear plane and line.
            Returns a line for a line on the plane.
            Returns a point for a skew line which intersects the plane.
        :rtype: None, Point3D, Line3D            
        
        """
        if line in self: # plane and line are collinear
            return line
        elif self._N.is_perpendicular(line.vL): # plane and line are parallel 
            return None
        else:
            return self._intersect_line_skew(line)
            
        
    def _intersect_line_skew(self,skew_line):
        """Returns the intersection of this plane and a skew line.
        
        :param skew_line: A 3D line which is skew to the plane.
        :type skew_line: Line3D
        
        :return: The intersection point.
        :rtype: Point3D
        
        """
        if not self._N.is_perpendicular(skew_line.vL):
            n=self._N
            u=skew_line.vL
            w=skew_line.P0-self._P0
            t=-n.dot(w) / n.dot(u)
            return skew_line.calculate_point(t)
        else:
            raise ValueError('%s and %s are not skew' % (self,skew_line))
        
        
    def intersect_segment(self,segment):
        """Returns the intersection of this plane and a segment.
        
        :param segment: A 3D segment.
        :type segment: Segment3D
        
        :return: Returns None for parallel, non-collinear plane and segment.
            Returns None for skew, non-intersecting plane and segment.
            Returns a segment for a segment on the plane.
            Returns a point for a skew segment which intersects the plane.
        :rtype: None, Point3D, Segment3D
            
        """
        if segment in self: # segment lies on the plane
            return segment
        elif self._N.is_perpendicular(segment.line.vL): # plane and segment are parallel 
            return None
        else:
            ipt=self._intersect_line_skew(segment.line)
            if ipt in segment:
                return ipt
            else:
                return None
            
            
    def intersect_segments(self,segments):
        """Returns the intersection of this plane and a Segment sequence.
        
        :param segments: A sequence of 3D segments. 
        :type segments: Segments 
        
        :return: A tuple of intersection points and intersection segments 
            (Points,Segments)
        :rtype: tuple
        
        """
        ipts=Points()
        isegments=Segments()
        for s in segments:
            result=self.intersect_segment(s)
            if result is None:
                continue
            elif result.__class__.__name__=='Point3D':
                ipts.append(result,unique=True)
            elif result.__class__.__name__=='Segment3D':
                isegments.append(result,unique=True)
            else:
                raise Exception
        ipts.remove_points_in_segments(isegments)
        return ipts,isegments
        
            
            
    def intersect_plane(self,plane):
        """Returns the intersection of this plane and another plane.
        
        :param plane: A 3D plane.
        :type plane: Plane3D 
        
        :return: Returns None for parallel, non-coplanar planes.
            Returns a plane for two coplanar planes.
            Returns a line for non-parallel planes.
        :rtype: None, Line3D, Plane3D            
        
        """
        if plane==self:
            return self
        elif plane.N.is_collinear(self._N):
            return None
        else:
            n1=self._N
            d1=-n1.dot(self._P0-Point3D(0,0,0))
            n2=plane.N
            d2=-n2.dot(plane.P0-Point3D(0,0,0))
            n3=n1.cross_product(n2)
            P0=Point3D(0,0,0) + ((n1*d2-n2*d1).cross_product(n3) * (1 / (n3.length**2)))
            u=n3
            return Line3D(P0,u)
            
            
    # def is_parallel(self,obj):
    #     """Tests if this plane and the supplied object are parallel
        
    #     :param linelike_obj: a Line3D, Halfline3D, Segment3D, Plane3D or Polygon3D
        
    #     :return result: the result of the test
    #         - returns True if the object is collinear with the plane
    #         - otherwise False
    #     :rtype bool:
            
    #     """
    #     if obj.__class__.__name__ in ['Line3D','Halfline3D','Segment3D']:
    #         return self.N.is_perpendicular(obj.vL)
        
    #     elif isinstance(obj,Plane3D):
    #         return self.N.is_collinear(obj.N)
        
    #     else:
    #         raise Exception('Not implemented yet')
            
            
    # def is_perpendicular(self,obj):
    #     """Tests if this plane and the supplied object are perpendicular
        
    #     :param linelike_obj: a Line3D, Halfline3D, Segment3D, Plane3D or Polygon3D
        
    #     :return result: the result of the test
    #         - returns True if the object is perpendicular with the plane
    #         - otherwise False
    #     :rtype bool:
            
    #     """
    #     if obj.__class__.__name__ in ['Line3D','Halfline3D','Segment3D']:
    #         return self.N.is_collinear(obj.vL)
        
    #     elif isinstance(obj,Plane3D):
    #         return self.N.is_perpendicular(obj.N)
        
    #     else:
    #         raise Exception('Not implemented yet')
        
        
    @property
    def P0(self):
        """The start point of the plane.
        
        :rtype: Point2D
        
        """
        return self._P0
        
    
    def point_xy(self,x,y):
        """Returns a point on the plane given a x and y coordinates.
        
        :param x: An x-coordinate.
        :type x: float
        :param y: A y-coordinate.
        :type y: float
        
        :rtype: Point3D
        
        """
        z=self._P0.z-(self._N.x*(x-self._P0.x)+self._N.y*(y-self._P0.y))/self._N.z
        return Point3D(x,y,z)
    
    
    def point_zx(self,z,x):
        """Returns a point on the plane given a x and y coordinates.
        
        :param z: A z-coordinate.
        :type z: float
        :param x: An x-coordinate.
        :type x: float
        
        :rtype: Point3D
        
        """
        y=self._P0.y-(self._N.z*(z-self._P0.z)+self._N.x*(x-self._P0.x))/self._N.y
        return Point3D(x,y,z)
    
    
    def point_yz(self,y,z):
        """Returns a point on the plane given a x and y coordinates.
        
        :param y: A y-coordinate.
        :type y: float
        :param z: A z-coordinate.
        :type z: float
        
        :rtype: Point3D
        
        """
        x=self._P0.x-(self._N.y*(y-self._P0.y)+self._N.z*(z-self._P0.z))/self._N.x
        return Point3D(x,y,z)
    
    
    @property
    def N(self):
        """The vector normal to the plane.
        
        :rtype: Vector3D
        
        """
        return self._N
    
    
    def signed_distance_point(self,point):
        """Returns the signed distance to the supplied point.
        
        :param point: A 3D point.
        :type point:  Point3D
        
        :return: The signed distance between the plane and the point.
            The return value is positive for one side of the plane 
            (the side in the direction of the normal) and is negative for
            the other side.
        :rtype: float
            
        """
        return self._N.dot(point-self._P0) / self._N.length
    
        
    
    
    
    
            
    
    
    
    