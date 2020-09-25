
Distances
=========

Distances between two geometric objects are calculated using `distance_to` methods:

.. code-block:: python

   >>> from crossproduct import Point2D
   >>> p1 = Point2D(1,2)
   >>> p2 = Point2D(2,2)
   >>> result = p1.distance_to_point(p2)
   >>> print(result)
   1

The following distance methods are available:

+----------------------------------------------------------------------------+---------------------------------------------------------------------+
| Geometric class                                                            | `distance_to` method                                                |
+============================================================================+=====================================================================+
| :py:class:`~crossproduct.point.Point2D`                                    | :py:meth:`~crossproduct.point.Point2D.distance_to_point`            |
+----------------------------------------------------------------------------+---------------------------------------------------------------------+
| :py:class:`~crossproduct.point.Point3D`                                    | :py:meth:`~crossproduct.point.Point3D.distance_to_point`            |
+----------------------------------------------------------------------------+---------------------------------------------------------------------+
| :py:class:`~crossproduct.line.Line2D`                                      | :py:meth:`~crossproduct.line.Line2D.distance_to_point`              |
|                                                                            | :py:meth:`~crossproduct.line.Line2D.distance_to_line`               |
+----------------------------------------------------------------------------+---------------------------------------------------------------------+
| :py:class:`~crossproduct.line.Line3D`                                      | :py:meth:`~crossproduct.line.Line3D.distance_to_point`              |
|                                                                            | :py:meth:`~crossproduct.line.Line3D.distance_to_line`               |
+----------------------------------------------------------------------------+---------------------------------------------------------------------+
| :py:class:`~crossproduct.halfline.Halfline2D`                              | :py:meth:`~crossproduct.halfline.Halfline2D.distance_to_point`      |
+----------------------------------------------------------------------------+---------------------------------------------------------------------+
| :py:class:`~crossproduct.halfline.Halfline3D`                              | :py:meth:`~crossproduct.halfline.Halfline3D.distance_to_point`      |
+----------------------------------------------------------------------------+---------------------------------------------------------------------+
| :py:class:`~crossproduct.segment.Segment2D`                                | :py:meth:`~crossproduct.segment.Segment2D.distance_to_point`        |
+----------------------------------------------------------------------------+---------------------------------------------------------------------+
| :py:class:`~crossproduct.segment.Segment3D`                                | :py:meth:`~crossproduct.segment.Segment3D.distance_to_point`        |
|                                                                            | :py:meth:`~crossproduct.segment.Segment3D.distance_to_segment`      |
+----------------------------------------------------------------------------+---------------------------------------------------------------------+
| :py:class:`~crossproduct.plane.Plane3D`                                    | :py:meth:`~crossproduct.plane.Plane3D.distance_to_point`            |
|                                                                            | :py:meth:`~crossproduct.plane.Plane3D.signed_distance_to_point`     |
+----------------------------------------------------------------------------+---------------------------------------------------------------------+