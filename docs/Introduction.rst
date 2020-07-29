
Introduction
============

`crossproduct` does 2D and 3D geometry calculations in pure Python. 

`crossproduct` is a pure Python package designed for applications with complex, small-scale geometries. 
It provides open source and well documented algorithms which can be easily understood and modified as needed. 

The package is written as a series of classes which represent the major geometric objects such as 
:py:class:`~crossproduct.point.Point2D`, :py:class:`~crossproduct.plane.Plane3D` and :py:class:`~crossproduct.simple_polygon.Polygon3D`.

The methods of each class are used to perform geometric calculations. For example, the cross product of two vectors is performed using the 
:py:meth:`~crossproduct.vector.Vector3D.cross_product` method of the :py:class:`~crossproduct.vector.Vector3D` object:

.. code-block:: python

   >>> from crossproduct import Vector3D 
   >>> v1 = Vector3D(1,0,0)
   >>> v2 = Vector3D(0,1,0)
   >>> result = v1.cross_product(v2)
   >>> print(result)
   Vector3D(0,0,1))

