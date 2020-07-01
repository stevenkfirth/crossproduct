# -*- coding: utf-8 -*-


from .point import Point, Point2D
from .vector import Vector, Vector2D


SMALL_NUM=0.00000001


class Line():
    "A n-D line"
    
    def __init__(self,P0,vL):
        """
        
        :param P0 Point: a point on the line
        :param vL Vector: a vector on the line
        
        """
        if isinstance(P0,Point):
            self.P0=P0
        else:
            raise TypeError
        
        if isinstance(vL,Vector):
            if vL.length>SMALL_NUM:
                self.vL=vL
            else:
                raise ValueError('length of vL must be greater than zero')
        else:
            raise TypeError
    
    
    def __contains__(self,obj):
        """Tests if the line contains the object
        
        :param obj: a geometric object 
            - Point, HalfLine or Segement
            
        :return result:
            - for point, True if the point lies on the line
            - for halfline, True if the halfline startpoint is on the line and 
                the halfline vector is collinear to the line vector
            - for segment, True if the segment start and endpoints are on the line
        :rtype bool:
        
        """
        import crossproduct
        
        if isinstance(obj,Point):
            t=self.calculate_t_from_point(obj)
            pt=self.calculate_point(t)           
            return obj==pt 
                    
        elif isinstance(obj,crossproduct.halfline.Halfline):
            return obj.P0 in self and obj.vL.is_collinear(self.vL)
        
        elif isinstance(obj,crossproduct.segment.Segment):
            return obj.P0 in self and obj.P1 in self
        
        else:
            raise TypeError
        
        
    def __eq__(self,line):
        """Tests if this line and the supplied line are equal
        
        :param line Line: a line
        
        :return result: 
            - True if the start point of supplied line lies on line (self),
                and the vL of supplied line is collinear to the vL of line (self)
            - otherwise False
        :rtype bool:
            
        """
        if isinstance(line,Line):
            return line.P0 in self and line.vL.is_collinear(self.vL)
        else:
            return False
        
        
    def calculate_point(self,t):
        """Returns a point on the line for a given t value
        
        :param t int/float: the t value
        
        :return point:
        :rtype Point
        
        """
        return self.P0 + (self.vL * t)
        
    
    def closest_point_of_approach(self,line):
        """This algorithm is for points moving along lines with respect to time
        
        https://geomalgorithms.com/a07-_distance.html
        
        """
        raise NotImplementedError
    
    
    def distance_point(self,point):
        """Returns the distance to the supplied point
        
        :param point Point: a point instance
                    
        :return distance: the distance from the point to the object
        :rtype float:
            
        """
        w=point-self.P0
        b=w.dot(self.vL) / self.vL.dot(self.vL)
        ptB=self.P0+self.vL*b
        return (ptB-point).length
        
    
    def intersect_line(self,line):
        """Returns the intersection of this line with the supplied line
        
        :param line Line: a line 
        
        :return result:
            - return value can be:
                - self -> a line (for collinear lines) 
                - None -> no intersection (for parallel lines)
                - Point -> a point (for skew lines)
        
        """
        if self==line: # test for collinear lines
            return self
        elif self.is_parallel(line): # test for parallel lines
            return None 
        else: # a skew line
            return self.intersect_line_skew(line)
    
        
    def is_collinear(self,linelike_obj):
        """Tests if this line and the supplied line-like object are collinear
        
        :param linelike_obj: a Line, HalfLine or Segment
        
        :return result: the result of the test
            - returns True if the linkline_obj is contained in line (self)
            - otherwise False
        :rtype bool:
            
        """
        try:
            return self==linelike_obj.line
        except AttributeError:
            return self==linelike_obj
        
    
    def is_parallel(self,linelike_obj):
        """Tests if this line and the supplied line-like object are parallel
        
        :param linelike_obj: a Line, HalfLine or Segment
        
        :return result: the result of the test
            - returns True if the linkline_obj vector is collinear with the line (self) vector
            - otherwise False
        :rtype bool:
            
        """
        return self.vL.is_collinear(linelike_obj.vL)
        


class Line2D(Line):
    """A 2D Line
    
    Equation of the line is P(t) = P0 + vL*t
        where:
            - P(t) is a point on the line
            - P0 is the start point of the line
            - vL is the line vector
            - t is any real number
    
    """

    
    def __repr__(self):
        """The string of this line for printing
        
        :return result:
        :rtype str:
            
        """
        return 'Line2D(%s, %s)' % (self.P0,self.vL)
    
    
    def calculate_t_from_point(self,point):
        """Returns t for a given point
        
        :param point Point2D:
        
        :return t: the calculated t value
        :rtype float:
        """
        try:
            return self.calculate_t_from_x(point.x)
        except ValueError:
            return self.calculate_t_from_y(point.y)
        
    
    def calculate_t_from_x(self,x):
        """Returns t for a given x coordinate
        
        :param x int/float: a x coordinate
        
        :return t: the calculated t value
        :rtype float:
        
        """
        try:
            return (x-self.P0.x) / (self.vL.x)
        except ZeroDivisionError:
            raise ValueError('%s has a vector with an x component of 0' % self)
    
    
    def calculate_t_from_y(self,y):
        """Returns t for a given y coordinate
        
        :param y int/float: a y coordinate
        
        :return t: the calculated t value
        :rtype float:
        
        """
        try:
            return (y-self.P0.y) / (self.vL.y)
        except ZeroDivisionError:
            raise ValueError('%s has a vector with an y component of 0' % self)
    
    
    def distance_line(self,line):
        """Returns the distance to the supplied line
        
        :param line Line: a line
        
        :return distance: the distance from the point to the object
        :rtype float:
            
        """
        if self.is_parallel(line):
            return self.distance_point(line.P0)
        else:
            return 0 # as these are skew infinite 2D lines
                    
        
    def intersect_line_skew(self,skew_line):
        """Returns the point of intersection of this line and the supplied (skew) line
        
        :param line Line2D: a 2D line which is skew to this line (self)
        
        :return intersection:
        :rtype Point2D:
        
        """
        if not self.is_parallel(skew_line):
            u=self.vL
            v=skew_line.vL
            w=self.P0-skew_line.P0 
            t=-v.perp_product(w) / v.perp_product(u)
            return self.calculate_point(t)
        else:
            raise ValueError('%s and %s are not skew lines' % (self,skew_line))
        
        
        
class Line3D(Line):
    """A 3D Line
    
    Equation of the line is P(t) = P0 + vL*t
        where:
            - P(t) is a point on the line
            - P0 is the start point of the line
            - vL is the line vector
            - t is any real number
    
    """        
    
    def __repr__(self):
        """The string of this line for printing
        
        :return result:
        :rtype str:
            
        """
        return 'Line3D(%s, %s)' % (self.P0,self.vL)
        
        
    def calculate_t_from_point(self,point):
        """Returns t for a given point
        
        :param point Point3D:
        
        :return t: the calculated t value
        :rtype float:
        """
        try:
            return self.calculate_t_from_x(point.x)
        except ValueError:
            try:
                return self.calculate_t_from_y(point.y)
            except ValueError:
                return self.calculate_t_from_z(point.z)
    
    
    def calculate_t_from_x(self,x):
        """Returns t for a given x coordinate
        
        :param x int/float: a x coordinate
        
        :return t: the calculated t value
        :rtype float:
        
        """
        try:
            return (x-self.P0.x) / (self.vL.x)
        except ZeroDivisionError:
            raise ValueError('%s has a vector with an x component of 0' % self)
    
    
    def calculate_t_from_y(self,y):
        """Returns t for a given y coordinate
        
        :param y int/float: a y coordinate
        
        :return t: the calculated t value
        :rtype float:
        
        """
        try:
            return (y-self.P0.y) / (self.vL.y)
        except ZeroDivisionError:
            raise ValueError('%s has a vector with an y component of 0' % self)
            
            
    def calculate_t_from_z(self,z):
        """Returns t for a given z coordinate
        
        :param y int/float: a z coordinate
        
        :return t: the calculated t value
        :rtype float:
        
        """
        try:
            return (z-self.P0.z) / (self.vL.z)
        except ZeroDivisionError:
            raise ValueError('%s has a vector with an z component of 0' % self)
    
    
    def distance_line(self,line):
        """Returns the distance to the supplied line
        
        :param line Line: a line
        
        :return distance: the distance from the point to the object
        :rtype float:
            
        """
        if self.is_parallel(line):
                
            return self.distance_point(line.P0)
        
        else:
            
            w0=self.P0-line.P0
            u=self.vL
            v=line.vL
            a=u.dot(u)
            b=u.dot(v)
            c=v.dot(v)
            d=u.dot(w0)
            e=v.dot(w0)
            
            sc=(b*e-c*d) / (a*c-b**2)
            tc=(a*e-b*d) / (a*c-b**2)
            
            Pc=self.calculate_point(sc)
            Qc=line.calculate_point(tc)
            
            return (Pc-Qc).length

        
    def intersect_line_skew(self,skew_line):
        """Returns the point of intersection of this line and the supplied (skew) line
        
        :param line Line3D: a 3D line which is skew to this line (self)
        
        :return intersection:
            - return value can be:
                - None -> no intersection (for skew lines which do not intersect in 3D space)
                - Point3D -> a point (for skew lines which intersect)
        
        """
        if not self.is_parallel(skew_line):
        
            # find the coordinate to ignore for the projection
            absolute_coords=[abs(x) for x in self.vL.coordinates] + [abs(x) for x in skew_line.vL.coordinates]
            i=absolute_coords.index(min(absolute_coords)) % 3 # the coordinate to ignore for projection
                    
            #print('i',i)
            
            # project 3D lines to 2D
            self2D=self.project_2D(i)
            skew_line2D=skew_line.project_2D(i)
            
            #print('self2D', self2D)
            #print('skew_line2D',skew_line2D)
            
            # find intersection point for 2D lines
            ipt=self2D.intersect_line_skew(skew_line2D)
            
            # find t values for the intersection point on each 2D line
            t1=self2D.calculate_t_from_point(ipt)
            t2=skew_line2D.calculate_t_from_point(ipt)
            
            # calculate the 3D intersection points from the t values
            ipt1=self.calculate_point(t1)
            ipt2=skew_line.calculate_point(t2)
            
            #print(ipt1,ipt2)
            
            if ipt1==ipt2: # test the two 3D intersection points are the same
                return ipt1
            else:
                return None
        
        else:
            raise ValueError('%s and %s are not skew lines' % (self,skew_line))
        
        
    def project_2D(self,i):
        """Projects the 3D line to a 2D line
        
        :param i int: the coordinte index to ignore
            - index is the index of the coordinate which is ignored in the projection
                - 0 for x
                - 1 for y
                - 2 for z
                
        :return line: 
        :rtype Line2D:
            
        """
        
        if i==0:
            return Line2D(Point2D(self.P0.y,self.P0.z),
                          Vector2D(self.vL.y,self.vL.z))
        elif i==1:
            return Line2D(Point2D(self.P0.z,self.P0.x),
                          Vector2D(self.vL.z,self.vL.x))
        elif i==2:
            return Line2D(Point2D(self.P0.x,self.P0.y),
                          Vector2D(self.vL.x,self.vL.y))
        else:
            raise Exception
                    
        



















#    def is_vector_ccw(self,vector):
#        """
#        """
#        return self.vL.perp_product(vector)>0


    
    
    
        
        
        