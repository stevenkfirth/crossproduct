
Geometric_Objects
=================

`crossproduct` defines a series of python classes to represent the major geometric objects.

An instance of a geometric class is instanciated by providing the underlying information needed to form the object, 
such as the x and y coordinates of a 2D point:

.. code-block:: python

   >>> from crossproduct import Point2D 
   >>> pt = Point2D(1,0)
   >>> print(py)
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
| Line-like                                                                  | :py:class:`~crossproduct.line.Line2D`                                                    |
|                                                                            | :py:class:`~crossproduct.line.Line3D`                                                    |
|                                                                            +------------------------------------------------------------------------------------------+
|                                                                            | :py:class:`~crossproduct.halfline.Halfline2D`                                            |
|                                                                            | :py:class:`~crossproduct.halfline.Halfline3D`                                            |
|                                                                            +------------------------------------------------------------------------------------------+
|                                                                            | :py:class:`~crossproduct.segment.Segment2D`                                              |
|                                                                            | :py:class:`~crossproduct.segment.Segment3D`                                              |
|                                                                            | :py:class:`~crossproduct.segments.Segments`                                              |
|                                                                            +------------------------------------------------------------------------------------------+
|                                                                            | :py:class:`~crossproduct.simple_polyline.SimplePolyline2D`                               |
|                                                                            | :py:class:`~crossproduct.simple_polyline.SimplePolyline3D`                               |
|                                                                            +------------------------------------------------------------------------------------------+
|                                                                            | :py:class:`~crossproduct.polyline.Polyline2D`                                            |
|                                                                            | :py:class:`~crossproduct.polyline.Polyline3D`                                            |
|                                                                            | :py:class:`~crossproduct.polylines.Polylines`                                            |
+----------------------------------------------------------------------------+------------------------------------------------------------------------------------------+
| Plane                                                                      | :py:class:`~crossproduct.plane.Plane3D`                                                  |
+----------------------------------------------------------------------------+------------------------------------------------------------------------------------------+
| Simple Polygon                                                             | :py:class:`~crossproduct.triangle.Triangle2D`                                            |
|                                                                            | :py:class:`~crossproduct.triangle.Triangle3D`                                            |
|                                                                            | :py:class:`~crossproduct.triangles.Triangles`                                            |
|                                                                            +------------------------------------------------------------------------------------------+
|                                                                            | :py:class:`~crossproduct.parallelogram.Parallelogram2D`                                  |
|                                                                            | :py:class:`~crossproduct.parallelogram.Parallelogram3D`                                  |
|                                                                            +------------------------------------------------------------------------------------------+
|                                                                            | :py:class:`~crossproduct.quadrilateral.Quadrilateral2D`                                  |
|                                                                            | :py:class:`~crossproduct.quadrilateral.Quadrilateral3D`                                  |
|                                                                            +------------------------------------------------------------------------------------------+
|                                                                            | :py:class:`~crossproduct.simple_convex_polygon.SimpleConvexPolygon2D`                    |
|                                                                            | :py:class:`~crossproduct.simple_convex_polygon.SimpleConvexPolygon3D`                    |
|                                                                            +------------------------------------------------------------------------------------------+
|                                                                            | :py:class:`~crossproduct.simple_polygon.SimplePolygon2D`                                 |
|                                                                            | :py:class:`~crossproduct.simple_polygon.SimplePolygon3D`                                 |
|                                                                            | :py:class:`~crossproduct.simple_polygons.SimplePolygons`                                 |
+----------------------------------------------------------------------------+------------------------------------------------------------------------------------------+
| Simple Polyhedron                                                          | :py:class:`~crossproduct.tetrahedron.Tetrahedron3D`                                      |
|                                                                            +------------------------------------------------------------------------------------------+
|                                                                            | :py:class:`~crossproduct.simple_extruded_polyhedron.SimpleExtrudedPolyhedron3D`          |
|                                                                            +------------------------------------------------------------------------------------------+
|                                                                            | :py:class:`~crossproduct.simple_polyhedron.SimplePolyhedron3D`                           |
+----------------------------------------------------------------------------+------------------------------------------------------------------------------------------+







