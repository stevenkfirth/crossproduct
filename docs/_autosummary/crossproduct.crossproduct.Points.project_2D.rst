Points.project_2D
=================

.. automethod:: crossproduct.crossproduct.Points.project_2D

.. rubric:: Code Example

.. code-block:: python

   >>> from crossproduct import Point, Points
   >>> pts = Points(Point(0,0,0), Point(1,0,0))
   >>> result = pts.project_2D(1)
   >>> print(result)
   Points(Point(0.0, 0.0), Point(0.0, 1.0))
