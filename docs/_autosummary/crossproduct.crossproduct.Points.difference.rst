Points.difference
=================

.. automethod:: crossproduct.crossproduct.Points.difference

.. rubric:: Code Example

.. code-block:: python

   >>> from crossproduct import Point, Points
   >>> pts = Points(Point(0,0), Point(1,0))
   >>> result = pts.difference(Point(0,0))
   >>> print(result)
   GeometryObjects(Point(1.0, 0.0))
