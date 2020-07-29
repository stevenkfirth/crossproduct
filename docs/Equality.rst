
Equality
========

Equality tests whether two geometric objects are equal.

`crossproduct` considers two geometric objects to be equal if they describe the same geometric object. 
For example, two 2D line instances are equal if they describe the same line, even if they are instantiated with different arguments:

.. code-block:: python

   >>> from crossproduct import Line2D 
   >>> l1 = Line2D(Point2D(0,0), Vector2D(1,1))
   >>> l2 = Line2D(Point2D(0,0), Vector2D(2,2))
   >>> result = l1 == l2
   >>> print(result)
   True






