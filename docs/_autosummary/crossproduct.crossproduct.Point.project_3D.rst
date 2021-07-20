Point.project_3D
================

.. automethod:: crossproduct.crossproduct.Point.project_3D

.. rubric:: Code Example

.. code-block:: python

   >>> from crossproduct import Point, Plane
   >>> pt = Point(2,2)
   >>> pl = Plane(Point(0,0,1), Vector(0,0,1))
   >>> result = pt.project_3D(pl, 2)
   >>> print(result)
   Point(2.0, 2.0, 1.0)
