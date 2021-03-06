
Differences
===========

The difference of one gemetric object with another geometric object is the part of the original gemetric object which does not intersect with the second geometric object.

General rules:

	- if object #1 and object #2 do not intersect, then the difference of object #1 to object #2 is itself, i.e. object #1.
	- if object #2 contains object #1, then the difference of object #1 to object #2 is None or an Empty Sequence.

The following difference methods are available:

+---------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------+
| Geometric class                                                                 | Intersection method                                                                                              | Return classes                                                              |
+=================================================================================+==================================================================================================================+=============================================================================+
| :py:class:`~crossproduct.segment.Segment2D`                                     | :py:class:`~crossproduct.segment.Segment2D.difference_segment`                                                   | :py:class:`~crossproduct.segments.Segments`                                 |
|                                                                                 +------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------+
|                                                                                 | :py:class:`~crossproduct.segment.Segment2D.difference_segments`                                                  | :py:class:`~crossproduct.segments.Segments`                                 |
+---------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------+
| :py:class:`~crossproduct.segment.Segment3D`                                     | :py:class:`~crossproduct.segment.Segment3D.difference_segment`                                                   | :py:class:`~crossproduct.segments.Segments`                                 |
|                                                                                 +------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------+
|                                                                                 | :py:class:`~crossproduct.segment.Segment3D.difference_segments`                                                  | :py:class:`~crossproduct.segments.Segments`                                 |
+---------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------+
| :py:class:`~crossproduct.segments.Segments`                                     | :py:class:`~crossproduct.segments.Segments.difference_segments`                                                  | :py:class:`~crossproduct.segments.Segments`                                 |
+---------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------+
| :py:class:`~crossproduct.polyline.Polyline2D`                                   | :py:class:`~crossproduct.polyline.Polyline2D.difference_polyline`                                                | :py:class:`~crossproduct.polylines.Polylines`                               |
+---------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------+
| :py:class:`~crossproduct.polyline.Polyline3D`                                   | :py:class:`~crossproduct.polyline.Polyline3D.difference_polyline`                                                | :py:class:`~crossproduct.polylines.Polylines`                               |
+---------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------+


 
