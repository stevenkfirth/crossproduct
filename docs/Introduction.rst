
Introduction
============

*crossproduct* does 2D and 3D geometry calculations in Python. 
It builds on the `Shapely <https://pypi.org/project/Shapely/>`_ package by including additional geometric objects (such as vectors, lines and polyhedrons) 
and by extending the geometric algorithms to work in 3D space. 
It also uses the `triangle <https://pypi.org/project/triangle/>`_ package 
and implements a number of the geometric algorithms previous available on the `website by Dan Sunday <https://geomalgorithms.com/index.html>`_ (now available as a book).

*crossproduct* is a Python package designed for applications with complex, small-scale geometries. 
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

Installation
------------

The project is available on PyPi here: https://pypi.org/project/crossproduct/

To install:

- first install Shapely (use :code:`conda install shapely` if using the Anaconda distribution)
- then install triangle (:code:`pip install triangle`)
- then install crossproduct (:code:`pip install crossproduct`)


GitHub
------

To view the source code, raise issues and suggest improvements - visit the projects GitHub page: `<https://github.com/stevenkfirth/crossproduct>`_

References
----------

- `<https://pypi.org/project/Shapely/>`_
- `<https://pypi.org/project/triangle/>`_
- `<https://geomalgorithms.com/index.html>`_



