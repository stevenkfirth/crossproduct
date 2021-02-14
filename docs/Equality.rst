
Equality
========

Equality tests whether two geometric objects are equal. The equality tests are implemented as '__eq__' methods. 

*crossproduct* considers two geometric objects to be equal if they describe the same geometric feature. 
For example, two 2D line instances are equal if they describe the same line, even if they are instantiated with different arguments:

.. code-block:: python

   >>> from crossproduct import Line 
   >>> l1 = Line(Point(0,0), Vector(1,1))
   >>> l2 = Line(Point(0,0), Vector(2,2))
   >>> print(l1 == l2)
   True
   
The available equality tests are:

+-------------------------------+
| '__eq__' methods              |
+===============================+
| `Point.__eq__`                |
+-------------------------------+
| `Vector.__eq__`               |
+-------------------------------+
| `Halfline.__eq__`             |
+-------------------------------+
| `Line.__eq__`                 |
+-------------------------------+
| `Segment.__eq__`              |
+-------------------------------+
| `Polyline.__eq__`             |
+-------------------------------+
| `Plane.__eq__`                |
+-------------------------------+
| `Polygon.__eq__`              |
+-------------------------------+
| `Polyhedron.__eq__`           |
+-------------------------------+










