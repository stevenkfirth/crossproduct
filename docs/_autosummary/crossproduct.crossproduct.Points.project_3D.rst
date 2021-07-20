Points.project_3D
=================

.. automethod:: crossproduct.crossproduct.Points.project_3D

.. rubric:: Code Example

.. code-block:: python

   >>> from crossproduct import Point, Points, Vector, Plane
   >>> pts = Points(Point(0,0,0), Point(1,0,0))
   >>> pl = Plane(Point(0,0,1), Vector(0,0,1))
   >>> result = pts.project_3D(pl,2)
   >>> print(result)
   Points(Point(0.0, 0.0, 1.0), Point(1.0, 0.0, 1.0))
