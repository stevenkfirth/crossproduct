
Introduction
============

*crossproduct* does 2D and 3D geometry calculations in pure Python. 

*crossproduct* is a pure Python package designed for applications with complex, small-scale geometries. 
It provides open source and well documented algorithms which can be easily understood and modified as needed. 

The package is written as a series of classes which represent the major geometric objects such as 
`Point`, `Plane` and `Polygon`.

The methods of each class are used to perform geometric calculations. For example, the cross product of two vectors is performed using the 
`cross_product` method of the `Vector` class:

.. code-block:: python

   >>> from crossproduct import Vector
   >>> v1 = Vector(1,0,0)
   >>> v2 = Vector(0,1,0)
   >>> result = v1.cross_product(v2)
   >>> print(result)
   Vector(0,0,1))

GitHub
------

To view the source code, raise issues and suggest improvements - visit the projects GitHub page: `<https://github.com/stevenkfirth/crossproduct>`_

References
----------

`<https://geomalgorithms.com/index.html>`_
`<https://www.geometrictools.com/Documentation/TriangulationByEarClipping.pdf>`_


