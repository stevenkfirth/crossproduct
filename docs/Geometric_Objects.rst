
Geometric Objects
=================

*crossproduct* defines a series of Python classes to represent the major geometric objects.

Instance creation
-----------------

An instance of a geometric class is created by providing the underlying information needed to form the object, 
such as the x and y coordinates of a 2D point:

.. code-block:: python

   >>> from crossproduct import Point
   >>> pt = Point(1,0)
   >>> print(pt)
   Point(1,0)
   
Objects are immutable
---------------------
   
Once a geometric object instance is formed, it is considered immutable and cannot be changed. 
Operations, such as adding a vector to a point, result in a new `Point` instance being returned:

.. code-block:: python

   >>> from crossproduct import Point
   >>> pt1 = Point(1,0)
   >>> pt2 = pt1 + Vector(1,0)
   >>> print(pt1, pt2)
   Point(1,0), Point(2,0)
   
Some objects are sequences
--------------------------

Some of the geometric objects are implemented as immutable sequences (more formally they are subclasses of `collections.abc.Sequence`).
Iterating over the object will return the items belonging to that object.
For example, iterating over a `Polygon` will return the points of the polygon:
   
.. code-block:: python

   >>> from crossproduct import Point, Polygon
   >>> pg = Polygon(Point(0,0),Point(1,0),Point(1,1))
   >>> for pt in pg: print pt
   Point(0,0)
   Point(1,0)
   Point(1,1)
   
Indexing, slicing etc. will also work on these objects. 
The objects that this applies to are: `Point`, `Vector`, `Segment`, `Polyline`, `Polygon` and `Polyhedron`.
   
Objects can be 2D or 3D
-----------------------
   
Geometric objects can be specified as 2D or 3D, as given by the number of coordinates passes when they are formed.
   
.. code-block:: python

   >>> from crossproduct import Point, Line
   >>> pt = Point(1,0)                             # 2D Point
   >>> line = Line(Point(0,0,0), Vector(1,1,1))    # 3D Line
   
   




