# -*- coding: utf-8 -*-

from .simple_convex_polygon import SimpleConvexPolygon3D
from .halfline import Halfline3D
from .simple_polygon import SimplePolygon3D
from .simple_polyhedron import SimplePolyhedron3D

class SimpleExtrudedPolyhedron3D(SimplePolyhedron3D):
    """A 3D extruded polyhedron
    """
    
    def __init__(self,base_polygon,vector):
        """
        """
        self.base_polygon=base_polygon
        self.vector=vector
        
        #top polygon
        top_polygon=SimplePolygon3D(*[pt+vector for pt in base_polygon.points])
                    
        #side polygons
        points=base_polygon.closed_points
        side_polygons=[]
        for i in range(len(points)-1):
            pt0=points[i]
            pt1=points[i+1]
            pt2=pt1+vector
            pt3=pt0+vector
            side_polygons.append(SimplePolygon3D(pt0,pt1,pt2,pt3))
            
        polygons=[base_polygon,top_polygon] + side_polygons
            
        SimplePolyhedron3D.__init__(self,*polygons) # sets self.polygons
            
        self.height=base_polygon.plane.distance_point(top_polygon.plane.P0)
        self.base_polygon_area=self.base_polygon.area
        
        self.volume=self.base_polygon_area*self.height
        
        
    def __repr__(self):
        """The string of this line for printing
        
        :return result:
        :rtype str:
            
        """
        return 'SimpleExtrudedPolyhedron3D(%s,%s)' % (self.base_polygon,
                                                      self.vector)
    