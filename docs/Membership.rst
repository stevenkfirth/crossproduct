
Membership
==========

Membership tests whether a geometric object is contained within another geometric object. 
For example if a point lies on a line, then it can be considered that the line *contains* the point.

`crossproduct` uses the **__contains__** method to test for membership. 
This is called using the **in** operator:

.. code-block:: python

   >>> from crossproduct import Point2D, Vector2D, Line2D 
   >>> pt = Point2D(2,2)
   >>> l = Line2D(Point2D(0,0), Vector2D(1,1))
   >>> result = pt in l
   >>> print(result)
   True

The following membership tests are available:

+----------------------------------------------------------------------------+---------------------------------------------------------------------+
| Geometric class                                                            | Contains                                                            |
+============================================================================+=====================================================================+
| :py:class:`~crossproduct.line.Line2D`                                      | :py:class:`~crossproduct.point.Point2D`                             |
|                                                                            | :py:class:`~crossproduct.halfline.Halfline2D`                       |
|                                                                            | :py:class:`~crossproduct.segment.Segment2D`                         |
+----------------------------------------------------------------------------+---------------------------------------------------------------------+
| :py:class:`~crossproduct.line.Line3D`                                      | :py:class:`~crossproduct.point.Point3D`                             |
|                                                                            | :py:class:`~crossproduct.halfline.Halfline3D`                       |
|                                                                            | :py:class:`~crossproduct.segment.Segment3D`                         |
+----------------------------------------------------------------------------+---------------------------------------------------------------------+
| :py:class:`~crossproduct.halfline.Halfline2D`                              | :py:class:`~crossproduct.point.Point2D`                             |
|                                                                            | :py:class:`~crossproduct.segment.Segment2D`                         |   
+----------------------------------------------------------------------------+                                                                     |
| :py:class:`~crossproduct.segment.Segment2D`                                |                                                                     |
+----------------------------------------------------------------------------+---------------------------------------------------------------------+
| :py:class:`~crossproduct.halfline.Halfline3D`                              | :py:class:`~crossproduct.point.Point3D`                             |
|                                                                            | :py:class:`~crossproduct.segment.Segment3D`                         |
+----------------------------------------------------------------------------+                                                                     |
| :py:class:`~crossproduct.segment.Segment3D`                                |                                                                     |
|                                                                            |                                                                     |
+----------------------------------------------------------------------------+---------------------------------------------------------------------+
| :py:class:`~crossproduct.plane.Plane3D`                                    | :py:class:`~crossproduct.point.Point3D`                             |
|                                                                            | :py:class:`~crossproduct.line.Line3D`                               |
|                                                                            | :py:class:`~crossproduct.halfline.Halfline3D`                       |
|                                                                            | :py:class:`~crossproduct.segment.Segment3D`                         |
+----------------------------------------------------------------------------+---------------------------------------------------------------------+
| :py:class:`~crossproduct.triangle.Triangle2D`                              | :py:class:`~crossproduct.point.Point2D`                             |
+----------------------------------------------------------------------------+                                                                     |
| :py:class:`~crossproduct.parallelogram.Parallelogram2D`                    |                                                                     |
+----------------------------------------------------------------------------+                                                                     |
| :py:class:`~crossproduct.quadrilateral.Quadrilateral2D`                    |                                                                     |
+----------------------------------------------------------------------------+                                                                     |
| :py:class:`~crossproduct.simple_convex_polygon.SimpleConvexPolygon2D`      |                                                                     |
+----------------------------------------------------------------------------+                                                                     |
| :py:class:`~crossproduct.simple_polygon.SimplePolygon2D`                   |                                                                     |
+----------------------------------------------------------------------------+---------------------------------------------------------------------+
| :py:class:`~crossproduct.triangle.Triangle3D`                              | :py:class:`~crossproduct.point.Point3D`                             |
+----------------------------------------------------------------------------+                                                                     |
| :py:class:`~crossproduct.parallelogram.Parallelogram3D`                    |                                                                     |
+----------------------------------------------------------------------------+                                                                     |
| :py:class:`~crossproduct.quadrilateral.Quadrilateral3D`                    |                                                                     |
+----------------------------------------------------------------------------+                                                                     |
| :py:class:`~crossproduct.simple_convex_polygon.SimpleConvexPolygon3D`      |                                                                     |
+----------------------------------------------------------------------------+                                                                     |
| :py:class:`~crossproduct.simple_polygon.SimplePolygon3D`                   |                                                                     |
+----------------------------------------------------------------------------+---------------------------------------------------------------------+


