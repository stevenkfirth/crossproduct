
Geometric_Objects
=================

`crossproduct` defines a series of Python classes to represent the major geometric objects.

An instance of a geometric class is instanciated by providing the underlying information needed to form the object, 
such as the x and y coordinates of a 2D point:

.. code-block:: python

   >>> from crossproduct import Point2D 
   >>> pt = Point2D(1,0)
   >>> print(pt)
   Point2D(1,0)
   
Once a geometric object instance is formed, it is considered immutable and cannot be changed. 
Operations, such as adding a vector to a point, result in a new point being returned:

.. code-block:: python

   >>> from crossproduct import Point2D 
   >>> pt1 = Point2D(1,0)
   >>> pt2 = pt1 + Vector2D(1,0)
   >>> print(pt1, pt2)
   Point2D(1,0), Point2D(2,0)
   
`crossproduct` also defines sequences (i.e. collections) of geometric objects which act in a similar manner to python lists but with additional methods.
These sequences include :py:class:`~crossproduct.points.Points`, :py:class:`~crossproduct.segments.Segments` and :py:class:`~crossproduct.simple_polygons.SimplePolygons`. 
A sequence can contain any number of geometric object instances:

.. code-block:: python

   >>> from crossproduct import Segment2D, Segments
   >>> s1 = Segment2D(Point2D(0,0), Point2D(1,0))
   >>> s2 = Segment2D(Point2D(0,0), Point2D(0,1))
   >>> segments = Segments(s1,s2)
   >>> print(segments)
   Segments(Segment2D(Point2D(0,0), Point2D(1,0)), Segment2D(Point2D(0,0), Point2D(0,1)))

The geometric object classes available are:

+----------------------------------------------------------------------------+------------------------------------------------------------------------------------------+
| Group                                                                      | Geometric Object Classes                                                                 |
+============================================================================+==========================================================================================+
| Point                                                                      | :py:class:`~crossproduct.point.Point2D`                                                  |
|                                                                            | :py:class:`~crossproduct.point.Point3D`                                                  |
|                                                                            | :py:class:`~crossproduct.points.Points`                                                  |
+----------------------------------------------------------------------------+------------------------------------------------------------------------------------------+
| Vector                                                                     | :py:class:`~crossproduct.vector.Vector2D`                                                |
|                                                                            | :py:class:`~crossproduct.vector.Vector3D`                                                |
+----------------------------------------------------------------------------+------------------------------------------------------------------------------------------+
| Line                                                                       | :py:class:`~crossproduct.line.Line2D`                                                    |
|                                                                            | :py:class:`~crossproduct.line.Line3D`                                                    |
+----------------------------------------------------------------------------+------------------------------------------------------------------------------------------+
| Halfline                                                                   | :py:class:`~crossproduct.halfline.Halfline2D`                                            |
|                                                                            | :py:class:`~crossproduct.halfline.Halfline3D`                                            |
+----------------------------------------------------------------------------+------------------------------------------------------------------------------------------+
| Segment                                                                    | :py:class:`~crossproduct.segment.Segment2D`                                              |
|                                                                            | :py:class:`~crossproduct.segment.Segment3D`                                              |
|                                                                            | :py:class:`~crossproduct.segments.Segments`                                              |
+----------------------------------------------------------------------------+------------------------------------------------------------------------------------------+
| Polyline                                                                   | :py:class:`~crossproduct.polyline.Polyline2D`                                            |
|                                                                            | :py:class:`~crossproduct.polyline.Polyline3D`                                            |
|                                                                            | :py:class:`~crossproduct.polylines.Polylines`                                            |
+----------------------------------------------------------------------------+------------------------------------------------------------------------------------------+
| Plane                                                                      | :py:class:`~crossproduct.plane.Plane3D`                                                  |
+----------------------------------------------------------------------------+------------------------------------------------------------------------------------------+
| PlaneVolume                                                                | :py:class:`~crossproduct.plane_volume.PlaneVolume3D`                                     |
+----------------------------------------------------------------------------+------------------------------------------------------------------------------------------+
| Polygon                                                                    | :py:class:`~crossproduct.polygon.Polygon2D`                                              |
|                                                                            | :py:class:`~crossproduct.polygon.Polygon3D`                                              |
|                                                                            | :py:class:`~crossproduct.polygons.Polygons`                                              |
+----------------------------------------------------------------------------+------------------------------------------------------------------------------------------+
| Polyhedron                                                                 | :py:class:`~crossproduct.polyhedron.Polyhedron3D`                                        |
|                                                                            | :py:class:`~crossproduct.polyhedrons.Polyhedrons`                                        |
+----------------------------------------------------------------------------+------------------------------------------------------------------------------------------+







