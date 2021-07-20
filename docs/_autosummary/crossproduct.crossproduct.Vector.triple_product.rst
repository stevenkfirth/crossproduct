Vector.triple_product
=====================

.. automethod:: crossproduct.crossproduct.Vector.triple_product

.. rubric:: Code Example

.. code-block:: python

   >>> from crossproduct import Vector
   >>> v1 = Vector(1,0,0)
   >>> v2 = Vector(0,1,0)
   >>> v3 = Vector(0,0,1)
   >>> result = v1.triple_product(v2,v3)
   >>> print(result)
   1.0
