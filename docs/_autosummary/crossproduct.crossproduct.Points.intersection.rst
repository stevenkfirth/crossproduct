Points.intersection
===================

.. automethod:: crossproduct.crossproduct.Points.intersection

.. rubric:: Code Example

.. code-block:: python

   >>> from crossproduct import Point, Points
   >>> pts = Points(Point(0,0), Point(1,0))
   >>> result = pts.intersection(Point(0,0))
   >>> print(result)
   GeometryObjects(Point(0.0, 0.0))
