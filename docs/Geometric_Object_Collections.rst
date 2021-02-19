
Geometric Object Collections
============================

*crossproduct* also defines classes for collections of geometric objects.

Instance creation
-----------------

Geometric collection instances are created by providing one or more itmes:

.. code-block:: python

   >>> from crossproduct import Point, Points
   >>> pts = Points(Point(0,0), Point(1,1))
   >>> print(pts)
   Points(Point(0,0), Point(1,1)) 

The available collection classes are `Points`, `Segments`, `Polylines` and `Polygons`.

Collections are mutable sequences
---------------------------------

The geometric collection classes are implemented as mutable sequences (more formally they are subclasses of `collections.abc.MutableSequence`).

Therefore they can be used like a sequence and can be changed in place:

.. code-block:: python

   >>> from crossproduct import Point, Points
   >>> pts = Points(Point(0,0), Point(1,1))
   >>> pts[0] = Point(2,2)
   Points(Point(2,2), Point(1,1)) 





