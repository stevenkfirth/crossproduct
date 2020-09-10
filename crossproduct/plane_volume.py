# -*- coding: utf-8 -*-

from .halfline import Halfline3D
from .points import Points
from .polyline import Polylines
from .segment import Segment3D
from .segments import Segments
from .plane import Plane3D


SMALL_NUM=0.00000001


class PlaneVolume3D():
    """A three dimensional plane volume, situated on an x, y, z plane.
    
    A plane volume is the volume described by a plane and the region below it.
    
    Equation of plane: N . (P - P0) <= 0 where:
        
        - N is a normal 3D vector to the plane
        - P is any point on the plane
        - P0 is the start point of the plane
    
    :param P0: A 3D point on the plane.
    :type P0: Point3D
    :param N: A 3D vector which is normal to the plane.
    :type N: Vector3D 
    
    :Example:
    
    .. code-block:: python
       
       >>> pv = PlaneVolume3D(Point3D(0,0,0), Vector3D(0,0,1))
       >>> print(pv)
       PlaneVolume3D(Point3D(0,0,0), Vector3D(0,0,1))

    """    
    
    
    def __init__(self,P0,N):
        ""
        self._P0=P0
        self._N=N
        
        
    def __contains__(self,obj):
        """Tests if the plane volume contains the object.
        
        :param obj: A 3D geometric object.
        :type obj: Point3D, Line3D, Halfline3D, Segment3D, Polyline3D
            
        :rtype: bool
        
        """
        if obj.__class__.__name__=='Point3D':
            
            point=obj
            return self._N.dot(point-self._P0)<=0
            
        elif obj.__class__.__name__=='Line3D':
            
            return obj.P0 in self and self._N.is_perpendicular(obj.vL)
          
        elif obj.__class__.__name__ =='Halfline3D':
            
            return obj.P0 in self and self._N.dot(obj.line.vL)<=0
          
        elif obj.__class__.__name__=='Segment3D':
          
            return obj.P0 in self and obj.P1 in self
        
        elif obj.__class__.__name__=='Polyline3D':
            
            for pt in obj.points:
                
                if not pt in self:
                    
                    return False
                
            return True
        
        else:

            raise Exception('%s in PlaneVolume not yet implemented' % obj.__class__.__name__)
        
        
    def __eq__(self,plane_volume):
        """Tests if this plane volume and the supplied plane volume are equal.
        
        :param plane_volume: A 3D plane volume.
        :type plane_volume: PlaneVolume3D 
        
        :return: True if the normal vectors are collinear and 
            a point can exist on both planes;
            otherwise False.
        :rtype: bool
            
        """
        if isinstance(plane_volume,PlaneVolume3D):
            return self._N.is_codirectional(plane_volume.N) and plane_volume.P0 in self.plane
        else:
            return False
        
        
    def __repr__(self):
        ""
        return 'PlaneVolume3D(%s, %s)' % (self._P0,self._N)
       
        
    def _intersect_line_skew(self,skew_line):
        """Returns the intersection of this plane volume and a skew line.
        
        :param skew_line: A 3D line which is skew to the plane.
        :type skew_line: Line3D
        
        :return: The intersection halfline.
        :rtype: Halfline3D
        
        """
        if not self._N.is_perpendicular(skew_line.vL):
            P0=self.plane._intersect_line_skew(skew_line)
            if self._N.dot(skew_line.vL)>0:
                vL=skew_line.vL.opposite
            else:
                vL=skew_line.vL
            return Halfline3D(P0,vL)
            
        else:
            raise ValueError('%s and %s are not skew' % (self,skew_line))
        
        
    def intersect_polyline(self,polyline):
        """Returns the intersection of this plane volume and the supplied polyline.
        
        :param polyline: A polyline.
        :type polyline: Polyline3D
        
        :return: A tuple of intersection points and intersection polylines 
            (Points,Polylines). 
        :rtype: tuple      
        
        """
        ipts, isegments = self.intersect_segments(polyline.segments)
        ipolylines=Polylines(*[polyline.__class__(*s.points) for s in isegments])
        ipolylines=ipolylines.add_all
        return ipts, ipolylines
        
        
        
    def intersect_segment(self,segment):
        """Returns the intersection of this plane volume and a segment.
        
        :param segment: A 3D segment.
        :type segment: Segment3D
        
        :return: Returns None for a segment that does not intersect the plane volume.
            Returns a point for a segment with one end point on the plane of the plane surface
            and the other end point not inside the plane surface.
            Returns a segment for a segment on the plane of the plane surface.
            Returns a segment for a skew segment which intersects the plane volume.
        :rtype: None, Point3D, Segment3D
            
        """
        if not segment.P0 in self and not segment.P1 in self:
            return None
        elif segment.P0 in self and segment.P1 in self:
            return segment
        elif segment.P0 in self.plane and not segment.P1 in self:
            return segment.P0
        elif not segment.P0 in self and segment.P1 in self.plane:
            return segment.P1
        else:
            hl=self._intersect_line_skew(segment.line)
            if segment.P0 in hl:
                return Segment3D(segment.P0,hl.P0)
            elif segment.P1 in hl:
                return Segment3D(hl.P0,segment.P1)
            else:
                raise Exception
        
        
    def intersect_segments(self,segments):
        """Returns the intersection of this plane volume and a Segments sequence.
        
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
        ipts=ipts.remove_points_in_segments(isegments)
        return ipts,isegments
        
    
    @property
    def plane(self):
        """The plane of the plane volume.
        
        :rtype: Plane3D
                
        """
        return Plane3D(self._P0,self._N)
    
        
    @property
    def P0(self):
        """The start point of the plane volume.
        
        :rtype: Point2D
        
        """
        return self._P0
        
    
    @property
    def N(self):
        """The vector normal to the plane.
        
        :rtype: Vector3D
        
        """
        return self._N
    
        
    
    
    
    
            
    
    
    
    