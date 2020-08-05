# # -*- coding: utf-8 -*-

# from .polyline import Polyline2D, Polyline3D


# class SimplePolyline():
#     """A n-D non-inersecting polyline
        
#     """
    
#     classname='SimplePolyline'
    
#     def __init__(self,*points,validate=False):
#         """
        
#         param points: an array of points 
                    
#         """
        
#         if validate:
#             for pt in points:
#                 if not pt.classname=='Point':
#                     raise TypeError
        
#         self.points=tuple(points)
        
#         if validate:
#             if self.is_intersecting:
#                 raise ValueError('A simple polyline cannot have self intersecting points')
                
    
        
# class SimplePolyline2D(SimplePolyline,Polyline2D):
#     """A 2-D polyline
#     """
    
#     def __repr__(self):
#         """The string of this polyline for printing
        
#         :return result:
#         :rtype str:
            
#         """
#         return 'SimplePolyline2D(%s)' % ','.join([str(p) for p in self.points])
    
    
    
# class SimplePolyline3D(SimplePolyline,Polyline3D):
#     """A 3-D polyline
#     """
    
#     def __repr__(self):
#         """The string of this polyline for printing
        
#         :return result:
#         :rtype str:
            
#         """
#         return 'SimplePolyline3D(%s)' % ','.join([str(p) for p in self.points])


    