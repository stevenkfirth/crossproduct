# -*- coding: utf-8 -*-

from .simple_convex_polygon import SimpleConvexPolygon3D
from .halfline import Halfline3D
from .simple_polygon import SimplePolygon3D
from .vector import Vector3D


class SimplePolyhedron3D():
    """A 3D simple polyhedron
    """
    
    def __init__(self,*polygons):
        """
        
        :param polygons: an array of polygons 
                    
        Polygons may be reversed to ensure that all polygon plane normals are outfacing
        
        
        """
        
        for polygon in polygons:
            if not isinstance(polygon,SimplePolygon3D):
                raise TypeError
        
        polygons=list(polygons
                      )
        
        # reverse polygons if needed to ensure all polygon plane normals are facing outwards
        for i in range(len(polygons)):
            
            pg=polygons[i]
            
            if isinstance(pg,SimpleConvexPolygon3D):
                c=pg.centroid
            else:
                c=pg.triangles[0].centroid
    
            halfline=Halfline3D(c,pg.plane.N)
            
            for pg1 in polygons:
                
                flag=False
                if pg1==pg:
                    continue
                else:
                    #print(pg1.intersect_halfline(halfline))
                    #print(pg1)
                    ipts,isegments=pg1.intersect_halfline(halfline)
                    if len(ipts)>0 or len(isegments)>0:
                        flag=True
                        break
                
            #print(flag)
            if flag:
                polygons[i]=pg.reverse
                

        self.polygons=tuple(polygons)



    def plot(self,ax,normal=False,**kwargs):
        """Plots the segment on the supplied axes
        
        :param ax:  Axes3D instance
            - mpl_toolkits.mplot3d.axes3d.Axes3D (for 3D)
        :param **kwargs: keyword arguments to be supplied to the matplotlib plot call
                    
        """
        for pg in self.polygons:
            pg.plot(ax,normal=False,**kwargs)
        
        if normal:
            for pg in self.polygons:
                
                c=pg.centroid
                N=pg.plane.N
                
                x0,x1=ax.get_xlim()
                y0,y1=ax.get_ylim()
                z0,z1=ax.get_zlim()
                ax_vector=Vector3D(x1-x0,y1-y0,z1-z0)
                            
                x=abs(N.dot(ax_vector)/N.length)
               
                ax.quiver(*c.coordinates,*N.coordinates, 
                          length=x*0.2,
                          lw=3)
    