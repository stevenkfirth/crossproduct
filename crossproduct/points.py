# -*- coding: utf-8 -*-

from collections.abc import Sequence
from .point import Point


class Points(Sequence):
    """A sequence of points    
    
    """
    
    def __init__(self,*points):
        """
        """
    
        self.points=list(points)
        
        
    def __eq__(self,obj):
        """
        """
        if isinstance(obj,Points) and self.points==obj.points:
            return True
        else:
            return False
        
        
    def __getitem__(self,i):
        """
        """
        return self.points[i]
        
    
    def __len__(self):
        """
        """
        return len(self.points)
    
    
    def __repr__(self):
        """The string of this point for printing
        
        :return result:
        :rtype str:
            
        """
        return 'Points(%s)' % ', '.join([str(s) for s in self.points])
    
    
    def append(self,point,unique=False):
        """
        """
        if isinstance(point,Point):
            if unique:
                if not point in self:
                    self.points.append(point)
            else:
                self.points.append(point)
                
        else:
            raise TypeError
    
    
    def project_2D(self,i):
        """Returns a projection of the points on a 2D plane
        
        :param i int: the index of the coordinate which was ignored to create the 2D projection
        
        :return result:
               
        """
        points=[pt.project_2D(i) for pt in self]
        return Points(*points)
    
    
    def project_3D(self,plane,i):
        """Returns a projection of the points on a 3D plane
        
        :param plane Plane3D: the plane for the projection
        :param i int: the index of the coordinate which was ignored to create the 2D projection
        
        :return result:
               
        """
        points=[pt.project_3D(plane,i) for pt in self]
        return Points(*points)
    
    
    def remove_points_in_segments(self,segments):
        """Removes any points that lie on any of the segments
        """
        self.points=[pt for pt in self if not segments.intersect_point(pt)]
        
    
    