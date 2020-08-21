# custom script to generate autosummary stub pages

import os
import sys
import inspect
import crossproduct
from collections.abc import Sequence

stub_dir='_autosummary'

def isprop(v):
    return isinstance(v, property)

def is_property_or_function(attr):
    return isinstance(attr, property) or inspect.isfunction(attr)


def get_properties_and_methods(klass):   
    result=[name for (name, value) in inspect.getmembers(klass, is_property_or_function)]
    result=[name for name in result if not (name.startswith('_') and not name.startswith('__'))]
    result.remove('__init__')
    result.remove('__repr__')
    if hasattr(klass,'__getitem__'):
        result.remove('__contains__')
        result.remove('__getitem__')
        result.remove('__iter__')
        result.remove('__len__')
        result.remove('__reversed__')
        result.remove('count')
        result.remove('index')
    return result


def create_stub_pages(klass):
    for name in get_properties_and_methods(klass):
        filename='.'.join([klass.__module__,
                           klass.__name__,
                           name,
                           'rst'])
        with open(os.path.join(stub_dir,filename),'w') as f:
            f.write(klass.__name__ + '.' + name + '\n')
            f.write('=' * len(klass.__name__ + '.' + name) + '\n')
            f.write('\n')
            if isprop(getattr(klass,name)):
                f.write('.. autoattribute:: %s' % '.'.join([klass.__module__,
                                                            klass.__name__,
                                                            name]))
            else:
                f.write('.. automethod:: %s' % '.'.join([klass.__module__,
                                                         klass.__name__,
                                                         name]))
        
def create_class_page(klass):
    filename=klass.__name__ + '.rst'
    with open(filename,'w') as f:
        f.write(klass.__name__ + '\n')
        f.write('=' * len(klass.__name__) + '\n')
        f.write('\n')
        f.write('.. autoclass:: %s\n' % (klass.__module__+'.'+klass.__name__))
        f.write('   :show-inheritance:\n')
        f.write('\n')
        f.write('.. Rubric:: Properties and Methods\n')
        f.write('\n')
        f.write('.. autosummary::\n')
        f.write('   :toctree: _autosummary\n')
        f.write('\n')
        for name in get_properties_and_methods(klass):
            f.write('   ~%s\n' % '.'.join([klass.__module__,
                                          klass.__name__,
                                          name]))
        
def create_pages(klass):
    create_stub_pages(klass)
    create_class_page(klass)

create_pages(crossproduct.Point2D)
create_pages(crossproduct.Point3D)
create_pages(crossproduct.Points)
create_pages(crossproduct.Vector2D)
create_pages(crossproduct.Vector3D)
create_pages(crossproduct.Line2D)
create_pages(crossproduct.Line3D)
create_pages(crossproduct.Halfline2D)
create_pages(crossproduct.Halfline3D)
create_pages(crossproduct.Segment2D)
create_pages(crossproduct.Segment3D)
create_pages(crossproduct.Segments)
create_pages(crossproduct.Polyline2D)
create_pages(crossproduct.Polyline3D)
create_pages(crossproduct.Polylines)
create_pages(crossproduct.Plane3D)
create_pages(crossproduct.Polygon2D)
create_pages(crossproduct.Polygon3D)
create_pages(crossproduct.Polygons)