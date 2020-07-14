# -*- coding: utf-8 -*-

from .vector import Vector2D, Vector3D

SMALL_NUM=0.00000001


class Point():
    " A n-D point"

    classname='Point'
    
    def distance_point(self,point):
        """Returns the distance to the supplied point
        
        :param point Point: a n-D point
        
        :return distance: the distance from the point to the object
        :rtype float:
            
        """
        return (point-self).length
    


class Point2D(Point):
    """A two dimensional point, situated on an x, y plane.
    
    :param x: The x coordinate of the point.
    :type x: float
    :param y: The y coordinate of the point.
    :type y: float
    
    :Example:
    
    .. code-block:: python
       
       >>> p = Point2D(1,2)
       >>> print(p)
       Point2D(1,2)
    
    """
    
    def __init__(self,x,y):
        ""
        self.x=x
        self.y=y
            
        
    def __add__(self,vector):
        """The addition of this point and a vector.
        
        :param vector: The vector to be added to the point.
        :type vector: Vector2D
        
        :rtype: Point2D
        
        :Example:
    
        .. code-block:: python
        
            >>> p = Point2D(1,2)
            >>> result = p + Vector2D(1,1)
            >>> print(result)
            Point2D(2,3)
        
        
        """
        if isinstance(vector,Vector2D):
            return Point2D(self.x+vector.x,
                           self.y+vector.y)
        else:
            raise TypeError('%s is not a Vector2D' % vector)
        
        
    def __eq__(self,point):
        """Tests if this point and the supplied point are equal.
        
        :param point: The point to be tested.
        :type point: Point2D
        
        :return: True if the point coordinates are the same, otherwise False.
        :rtype: bool
        
        :Example:
    
        .. code-block:: python
        
            >>> result = Point2D(1,2) == Point(2,2)
            >>> print(result)
            False
            
        """
        if isinstance(point,Point2D):
            return (abs(self.x-point.x)<SMALL_NUM and 
                    abs(self.y-point.y)<SMALL_NUM)
        else:
            return False
    
    
    def __lt__(self,point):
        """Tests if the coordinates of this point are lower than the supplied point.
        
        :param point: The point to be tested.
        :type point: Point2D
        
        :return: True if the x coordinate of this point is lower than the 
            supplied point, otherwise False. If both x coordinates are equal, then 
            True if the y coordinate of this point is lower than the 
            supplied point, otherwise False. 
        :rtype: bool
        
        :Example:
    
        .. code-block:: python
        
            >>> result = Point2D(1,2) < Point(2,2)
            >>> print(result)
            True
        
        """
        if isinstance(point,Point2D):
            if self.x < point.x:
                return True
            else:
                if self.x == point.x and self.y < point.y:
                    return True
                else:
                    return False
        
        else:
            raise TypeError
        
    
    def __repr__(self):
        """The string of this point for printing
        
        :return result:
        :rtype str:
            
        """
        return 'Point2D(%s)' % ','.join([str(c) for c in self.coordinates])
    
    
    def __sub__(self,obj):
        """Substraction of supplied object from this point.
        
        :param obj: either a 2D point or a 2D vector
        :type obj: Point2D or Vector2D
        
        :return obj: the resulting point or vector
            - if obj is a point, then a vector is returned i.e. v=P1-P0
            - if obj is vector, then a point is returned i.e. P1=P0-v
        :rtype Point2D or Vector2D:
        
        """
        if isinstance(obj,Point2D):
            return Vector2D(self.x-obj.x,
                            self.y-obj.y)
        elif isinstance(obj,Vector2D):
            return Point2D(self.x-obj.x,
                           self.y-obj.y)
        else:
            raise TypeError
    
    
    @property
    def coordinates(self):
        """Returns the coordinates of the point
        
        :return coordinates: the x and y coordinates (x,y)
        :rtype tuple:
        
        """
        return self.x, self.y
    
    
    @property
    def dimension(self):
        """Returns the dimension of the object instance
        
        :return: '2D'
        :rtype: str
        
        """
        
        return '2D'
    
    
    def project_3D(self,plane,i):
        """Returns a projection of the point on a 3D plane
        
        :param plane Plane3D: the plane for the projection
        :param i int: the index of the coordinate which was ignored to create the 2D projection
        
        :return result:
               
        """
        
        if i==0:
            point=plane.point_yz(self.x,self.y)
        elif i==1:
            point=plane.point_zx(self.x,self.y)
        elif i==2:
            point=plane.point_xy(self.x,self.y)
        else:
            raise Exception
            
        return point
    

class Point3D(Point):
    "A 3D point"
    
    dimension='3D'
    
    def __init__(self,x,y,z):
        """
        :param x int/float: the x coordinate of the point
        :param y int/float: the y coordinate of the point
        :param z int/float: the z coordinate of the point
        
        """
        self.x=x
        self.y=y
        self.z=z
    
    
    def __add__(self,vector):
        """Addition of this point and a vector
        
        :param vector Vector3D: a 3D vector
        
        :return point: the resulting point
        :rtype Point3D:
        
        """
        if isinstance(vector,Vector3D):
            return Point3D(self.x+vector.x,
                           self.y+vector.y,
                           self.z+vector.z)
        else:
            raise TypeError 
            
    
    def __eq__(self,point):
        """Tests if this point and the supplied point are equal
        
        :param point Point3D: a 3D point
        
        :return result: 
            - True if the point coordinates are the same
            - otherwise False
        :rtype bool:
            
        """
        if isinstance(point,Point3D):
            return (abs(self.x-point.x)<SMALL_NUM 
                    and abs(self.y-point.y)<SMALL_NUM
                    and abs(self.z-point.z)<SMALL_NUM
                    )
        else:
            return False
            
        
    def __lt__(self,point):
        """Tests is the coordinates of this point are lower than the supplied point
        
        """
        if isinstance(point,Point3D):
            if self.x < point.x:
                return True
            else:
                if self.x == point.x and self.y < point.y:
                    return True
                else:
                    if self.y == point.y and self.z < point.z:
                        return True
                    else:
                        return False
        else:
            raise TypeError
        
    
    def __repr__(self):
        """The string of this point for printing
        
        :return result:
        :rtype str:
            
        """
        return 'Point3D(%s)' % ','.join([str(c) for c in self.coordinates])
    
    
    def __sub__(self,obj):
        """Substraction of supplied object from this point
        
        :param obj: either a 3D point or a 3D vector
        
        :return obj: the resulting point or vector
            - if obj is a point, then a vector is returned i.e. v=P1-P0
            - if obj is vector, then a point is returned i.e. P1=P0-v
        :rtype Point3D or Vector3D:
        
        """
        if isinstance(obj,Point3D):
            return Vector3D(self.x-obj.x,
                            self.y-obj.y,
                            self.z-obj.z)
        elif isinstance(obj,Vector3D):
            return Point3D(self.x-obj.x,
                           self.y-obj.y,
                           self.z-obj.z)
        else:
            raise TypeError
            
    
    @property
    def coordinates(self):
        """Returns the coordinates of the point
        
        :return coordinates: the x, y and z coordinates (x,y,z)
        :rtype tuple:
        
        """
        return self.x, self.y, self.z
    
    
    def project_2D(self,i):
        """Projects the 3D point to a 2D point
        
        :param i int: the coordinte index to ignore
            - index is the index of the coordinate which is ignored in the projection
                - 0 for x
                - 1 for y
                - 2 for z
                
        :return: point
        :rtype: Point2D
            
        """
        
        if i==0:
            return Point2D(self.y,self.z)
        elif i==1:
            return Point2D(self.z,self.x)
        elif i==2:
            return Point2D(self.x,self.y)
        else:
            raise Exception
                    
        

    
    
    
    
    