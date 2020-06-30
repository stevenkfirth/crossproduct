# -*- coding: utf-8 -*-

SMALL_NUM=0.00000001


class Vector():
    "A n-D vector"
    
    def is_codirectional(self,vector):
        """Tests if this vector and the supplied vector are codirectional
        
        :return result: the result of the test
            - returns True if the vectors point in the same direction
            - otherwise False
        :rtype bool:
            
        """
        if isinstance(vector,Vector):
            return self.is_collinear(vector) and self.dot(vector)>0
        else:
            raise TypeError
              
            
    def is_opposite(self,vector):
        """Test is the vector and the supplied vector are opposites
        
        :return result: the result of the test
            - returns True if the vectors point in opposite directions
            - otherwise False
        :rtype bool:
        """
        if isinstance(vector,Vector):
            return self.is_collinear(vector) and self.dot(vector)<0
        else:
            raise TypeError
    
    
    def is_perpendicular(self,vector):
        """Test if the vector and the supplied vector are perpendicular
        
        :param vector Vector 3D: a 3D vector
        
        :return result: the result of the test
            - returns True if the vectors are perpendicular
            - otherwise False
        :rtype bool:
        
        """
        if isinstance(vector,Vector):
            return abs(self.dot(vector))<SMALL_NUM
        else:
            raise TypeError
    
    @property
    def opposite(self):
        """Returns the opposite vector of this vector
        
        :return vector:
            - a collinear vector which points in the opposite direction
        :rtype: Vector 2D
        
        """
        return self*-1



class Vector2D(Vector):
    "A 2D vector"

    def __init__(self,x=0,y=0):
        """
        :param x int/float: the x coordinate of the vector
        :param y int/float: the y coordinate of the vector
        
        """
        self.x=x
        self.y=y        
    
    
    def __add__(self,vector):
        """Addition of this vector and a supplied vector
        
        :param vector Vector2D: a 2D vector
        
        :return vector: the resulting vector
        :rtype Vector2D:
        
        """
        if isinstance(vector,Vector2D):
            return Vector2D(self.x+vector.x,
                            self.y+vector.y)
        else:
            raise TypeError
    
    
    def __eq__(self,vector):
        """Tests if this vector and the supplied vector are equal
        
        :param vector Vector2D: a 2D vector
        
        :return result: 
            - True if the vector coordinates are the same
            - otherwise False
        :rtype bool:
            
        """
        if isinstance(vector,Vector2D):
            return (abs(self.x-vector.x)<SMALL_NUM and 
                    abs(self.y-vector.y)<SMALL_NUM)
        else:
            return False
    
    
    def __repr__(self):
        """The string of this vector for printing
        
        :return result:
        :rtype str:
            
        """
        return 'Vector2D(%s)' % ','.join([str(c) for c in self.coordinates])
    
    
    def __mul__(self,scalar):
        """Multiplication of this vector and a supplied scalar value
        
        :param scalar int/float: a numerical value
        
        :return vector: the resulting vector
        :rtype Vector2D:
        
        """
        if isinstance(scalar,int) or isinstance(scalar,float):
            return Vector2D(self.x*scalar,
                            self.y*scalar)
        else:
            raise TypeError
    
    
    def __sub__(self,vector):
        """Subtraction of this vector and a supplied vector
        
        :param vector Vector2D: a 2D vector
        
        :return vector: the resulting vector
        :rtype Vector2D:
        
        """
        if isinstance(vector,Vector2D):
            return Vector2D(self.x-vector.x,
                            self.y-vector.y)
        else:
            raise TypeError
    
    
    @property
    def coordinates(self):
        """Returns the coordinates of the vector
        
        :return coordinates: the x and y coordinates (x,y)
        :rtype tuple:
        
        """
        return self.x, self.y
    
    
    def dot(self,vector):
        """Return the dot product of this vector and the supplied vector
        
        :param vector Vector2D: a 2D vector
        
        :return result: the dot product
            - returns 0 if self and vector are perpendicular
            - returns >0 if the angle between self and vector is an acute angle (i.e. <90deg)
            - returns <0 if the angle between seld and vector is an obtuse angle (i.e. >90deg)
        :rtype float:
        
        """
        if isinstance(vector,Vector2D):
            return self.x*vector.x+self.y*vector.y
        else:
            raise TypeError
    

    def is_collinear(self,vector):
        """Tests if this vector and the supplied vector are collinear
        
        :return result: the result of the test
            - returns True if the vectors lie on the same line
            - otherwise False
        :rtype bool:
            
        """
        if isinstance(vector,Vector2D):
            return abs(self.perp_product(vector)) < SMALL_NUM 
        else:
            raise TypeError

    
    @property
    def length(self):
        """Returns the length of the vector
        
        :return length:
        :rtype: float
        
        """
        return (self.x**2+self.y**2)**0.5
    
    
    @property
    def normalise(self):
        """Returns the normalised vector of this vector
        
        :return vector:
            - a codirectional vector of length 1
        :rtype: Vector 2D
        
        """
        l=self.length
        return Vector2D(self.x/l,
                        self.y/l)
    
    
    def perp_product(self,vector):
        """Returns the perp product of this vector and the supplied vector
        
        :return result:
            - The perp product is the dot product of 
                the perp_vector of this vector and the supplied vector
            - if vector is collinear with self, returns 0
            - if vector is on the left of self, returns >0 (i.e. counterclockwise)
            - if vector is on the right of self, returns <0 (i.e. clockwise)
        :rtype float:
            
        """
        if isinstance(vector,Vector2D):
            return self.perp_vector.dot(vector)
        else:
            raise TypeError
        
    
    @property
    def perp_vector(self):
        """Returns the perp vector of this vector
        
        :return vector:
            - The perp vector is the normal vector on the left 
                (counterclockwise) side of self.
        :rtype Vector2D:
        
        """
        return Vector2D(-self.y,self.x)



class Vector3D(Vector):
    "A 3D vector"

    def __init__(self,x=0,y=0,z=0):
        """
        :param x int/float: the x coordinate of the vector
        :param y int/float: the y coordinate of the vector
        :param z int/float: the z coordinate of the vector
        
        """
        self.x=x
        self.y=y
        self.z=z
        
    
    def __add__(self,vector):
        """Addition of this vector and a supplied vector
        
        :param vector Vector3D: a 3D vector
        
        :return vector: the resulting vector
        :rtype Vector3D:
        
        """
        if isinstance(vector,Vector3D):
            return Vector3D(self.x+vector.x,
                            self.y+vector.y,
                            self.z+vector.z)
        else:
            raise TypeError
            
    
    def __eq__(self,vector):
        """Tests if this vector and the supplied vector are equal
        
        :param vector Vector3D: a 3D vector
        
        :return result: 
            - True if the vector coordinates are the same
            - otherwise False
        :rtype bool:
            
        """
        if isinstance(vector,Vector3D):
            return (abs(self.x-vector.x)<SMALL_NUM 
                    and abs(self.y-vector.y)<SMALL_NUM
                    and abs(self.z-vector.z)<SMALL_NUM)
        else:
            return False
            
        
    def __repr__(self):
        """The string of this vector for printing
        
        :return result:
        :rtype str:
            
        """
        return 'Vector3D(%s)' % ','.join([str(c) for c in self.coordinates])

    def __mul__(self,scalar):
        """Multiplication of this vector and a supplied scalar value
        
        :param scalar int/float: a numerical value
        
        :return vector: the resulting vector
        :rtype Vector3D:
        
        """
        if isinstance(scalar,int) or isinstance(scalar,float):
            return Vector3D(self.x*scalar,
                            self.y*scalar,
                            self.z*scalar)
        else:
            raise TypeError
    
    
    def __sub__(self,vector):
        """Subtraction of this vector and a supplied vector
        
        :param vector Vector3D: a 3D vector
        
        :return vector: the resulting vector
        :rtype Vector3D:
        
        """
        if isinstance(vector,Vector3D):
            return Vector3D(self.x-vector.x,
                            self.y-vector.y,
                            self.z-vector.z)
        else:
            raise TypeError


    def cross_product(self,vector):
        """Returns the 3D cross product of this vector and the supplied vector
        
        :return vector:
            - returns a new vector which is perpendicular to 
                this vector (self) and the supplied vector
            - returned vector has direction according to the right hand rule
            - if this vector (self) and the supplied vector are collinear,
                then the returned vector is (0,0,0)
        
        :rtype Vector3D:
        
        """
        if isinstance(vector,Vector3D):
            (v1,v2,v3),(w1,w2,w3)=self.coordinates,vector.coordinates
            return Vector3D(v2*w3-v3*w2,
                            v3*w1-v1*w3,
                            v1*w2-v2*w1)
        else:
            raise TypeError


    @property
    def coordinates(self):
        """Returns the coordinates of the vector
        
        :return coordinates: the x, y and z coordinates (x,y,z)
        :rtype tuple:
        
        """
        return self.x, self.y, self.z
    
    
    def dot(self,vector):
        """Return the dot product of this vector and the supplied vector
        
        :param vector Vector3D: a 3D vector
        
        :return result: the dot product
            - returns 0 if self and vector are perpendicular
            - returns >0 if the angle between self and vector is an acute angle (i.e. <90deg)
            - returns <0 if the angle between seld and vector is an obtuse angle (i.e. >90deg)
        :rtype float:
        
        """
        if isinstance(vector,Vector3D):
            return self.x*vector.x + self.y*vector.y + self.z*vector.z
        else:
            raise TypeError('%s is not a Vector3D' % vector)


    def is_collinear(self,vector):
        """Tests if this vector and the supplied vector are collinear
        
        :return result: the result of the test
            - returns True if the vectors lie on the same line
            - otherwise False
        :rtype bool:
            
        """
        if isinstance(vector,Vector3D):
            return self.cross_product(vector).length < SMALL_NUM 
        else:
            raise TypeError
    
    
    @property
    def length(self):
        """Returns the length of the vector
        
        :return length:
        :rtype: float
        
        """
        return (self.x**2 + self.y**2 + self.z**2)**0.5
    
    
    @property
    def normalise(self):
        """Returns the normalised vector of this vector
        
        :return vector:
            - a codirectional vector of length 1
        :rtype: Vector 3D
        
        """
        l=self.length
        return Vector3D(self.x/l,
                        self.y/l,
                        self.z/l)
    
          
    def triple_product(self,vector1,vector2):
        """Returns the triple product of this vector and 2 supplied vectors
        
        :return result:
            - result is equal to the volume of the parallelepiped (3D equivalent of a parallelogram)
            - result * 1/6 is equal to the volume of the tetrahedron (3D shape with 4 vertices)
            
        :rtype float:
        
        """
        if isinstance(vector1,Vector3D) and isinstance(vector2,Vector3D):
            return self.dot(vector1.cross_product(vector2))
        else:
            raise TypeError
            
        
        
        
        
        
        
    
    
    