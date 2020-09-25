
Membership
==========

Membership tests whether a geometric object is contained within another geometric object. 
For example if a point lies on a line, then it can be considered that the line *contains* the point.

`crossproduct` uses the **__contains__** method to test for membership. 
This is called using the :code:`in` operator:

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
+----------------------------------------------------------------------------+---------------------------------------------------------------------+
| :py:class:`~crossproduct.halfline.Halfline3D`                              | :py:class:`~crossproduct.point.Point3D`                             |
|                                                                            | :py:class:`~crossproduct.segment.Segment3D`                         |
+----------------------------------------------------------------------------+---------------------------------------------------------------------+
| :py:class:`~crossproduct.segment.Segment2D`                                | :py:class:`~crossproduct.point.Point2D`                             |
|                                                                            | :py:class:`~crossproduct.segment.Segment3D`                         |
+----------------------------------------------------------------------------+---------------------------------------------------------------------+
| :py:class:`~crossproduct.segment.Segment3D`                                | :py:class:`~crossproduct.point.Point3D`                             |
|                                                                            | :py:class:`~crossproduct.segment.Segment3D`                         |
+----------------------------------------------------------------------------+---------------------------------------------------------------------+
| :py:class:`~crossproduct.polyline.Polyline2D`                              | :py:class:`~crossproduct.point.Point2D`                             |
+----------------------------------------------------------------------------+---------------------------------------------------------------------+
| :py:class:`~crossproduct.polyline.Polyline3D`                              | :py:class:`~crossproduct.point.Point3D`                             |
+----------------------------------------------------------------------------+---------------------------------------------------------------------+
| :py:class:`~crossproduct.plane.Plane3D`                                    | :py:class:`~crossproduct.point.Point3D`                             |
|                                                                            | :py:class:`~crossproduct.line.Line3D`                               |
|                                                                            | :py:class:`~crossproduct.halfline.Halfline3D`                       |
|                                                                            | :py:class:`~crossproduct.segment.Segment3D`                         |
+----------------------------------------------------------------------------+---------------------------------------------------------------------+
| :py:class:`~crossproduct.plane_volume.PlaneVolume3D`                       | :py:class:`~crossproduct.point.Point3D`                             |
|                                                                            | :py:class:`~crossproduct.line.Line3D`                               |
|                                                                            | :py:class:`~crossproduct.halfline.Halfline3D`                       |
|                                                                            | :py:class:`~crossproduct.segment.Segment3D`                         |
|                                                                            | :py:class:`~crossproduct.plane_volume.PlaneVolume3D`                |
+----------------------------------------------------------------------------+---------------------------------------------------------------------+
| :py:class:`~crossproduct.polygon.Polygon2D`                                | :py:class:`~crossproduct.point.Point2D`                             |
+----------------------------------------------------------------------------+---------------------------------------------------------------------+
| :py:class:`~crossproduct.polygon.Polygon3D`                                | :py:class:`~crossproduct.point.Point3D`                             |
+----------------------------------------------------------------------------+---------------------------------------------------------------------+
| :py:class:`~crossproduct.polyhedron.Polyhedron3D`                          | TO BE COMPLETED                                                     |
+----------------------------------------------------------------------------+---------------------------------------------------------------------+


