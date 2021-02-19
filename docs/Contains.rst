
Contains
========

The *crossproduct* geometric object classes have a 'contains' method which test whether a geometric object is contained within another geometric object. 

For example if a point lies on a line, then it can be considered that the line contains the point.

.. code-block:: python

   >>> from crossproduct import Point, Vector, Line
   >>> pt = Point(2,2)
   >>> l = Line(Point(0,0), Vector(1,1))
   >>> print(l.contains(pt)
   True

The following geometic object classes use a 'contains' method:

+----------------------------------------------------------------------------+---------------------------------------------------------------------+
| 'contains' methods                                                         | Objects that the 'contains' method tests for                        |
+============================================================================+=====================================================================+
| `Line.contains`                                                            | `Point`                                                             |
|                                                                            | `Halfline`                                                          |
|                                                                            | `Segment`                                                           |
+----------------------------------------------------------------------------+---------------------------------------------------------------------+
| `Halfline.contains`                                                        | `Point`                                                             |
|                                                                            | `Segment`                                                           |
+----------------------------------------------------------------------------+---------------------------------------------------------------------+
| `Segment.contains`                                                         | `Point`                                                             |
|                                                                            | `Segment`                                                           |
+----------------------------------------------------------------------------+---------------------------------------------------------------------+
| `Polyline.contains`                                                        | `Point`                                                             |
|                                                                            | `Segment`                                                           |
+----------------------------------------------------------------------------+---------------------------------------------------------------------+
| `Plane.contains`                                                           | `Point`                                                             |
|                                                                            | `Line`                                                              |   
|                                                                            | `Halfline`                                                          |   
|                                                                            | `Segment`                                                           |
+----------------------------------------------------------------------------+---------------------------------------------------------------------+
| `Polygon.contains`                                                         | `Point`                                                             |
+----------------------------------------------------------------------------+---------------------------------------------------------------------+


