# custom script to generate autosummary stub pages

import os
import sys
import inspect
import crossproduct
from collections.abc import Sequence
import nbformat

stub_dir='_autosummary'

def read__code_example_notebooks(mydir):
    "Returns a dictionary of the code examples"
    d={}
    for f in os.listdir(mydir):
        if f.endswith('.ipynb'):
            nb=nbformat.read(os.path.join(mydir,f), nbformat.NO_CONVERT)
            for cell in nb.cells:
                source=cell.source
                if source.startswith('#'):
                    # code
                    lines=source.split('\n')
                    key=lines[0][1:].strip()
                    #print(key)
                    #print(cell)
                    code='   >>> ' + '\n   >>> '.join(lines[1:])
                    d[key]={'code':code}
                    # output
                    outputs=filter(lambda x: 'text' in x, cell.outputs)
                    d[key]['output']='   '+ ''.join([x.text for x in outputs])
    return d

nb_dir='_code_example_notebooks'
code_examples_dict=read__code_example_notebooks(nb_dir)


def is_property(v):
    "Returns True if v is a property of an object."
    return isinstance(v, property)

def is_property_or_function(v):
    "Returns True if v is an object property or a function."
    return isinstance(v, property) or inspect.isfunction(v)


def get_properties_and_methods(klass): 
    "Returns the properties and methods of an object to be documented"
    result=[name for (name, value) in inspect.getmembers(klass, is_property_or_function)]
    exclusions=['__init__','__repr__','__getitem__','__contains__','__iter__',
                '__len__','__reversed__','count','index']
    result=list(filter(lambda x: ((not x.startswith('_') or x.startswith('__')) 
                                  and not x in exclusions),
                       result))
    #print(result)
    return result


def create_stub_pages(klass):
    "Writes the stub pages."
    for name in get_properties_and_methods(klass):
        filename='.'.join([klass.__module__,
                           klass.__name__,
                           name,
                           'rst'])
        with open(os.path.join(stub_dir,filename),'w') as f:
            f.write(klass.__name__ + '.' + name + '\n')
            f.write('=' * len(klass.__name__ + '.' + name) + '\n')
            f.write('\n')
            if is_property(getattr(klass,name)):
                f.write('.. autoattribute:: %s' % '.'.join([klass.__module__,
                                                            klass.__name__,
                                                            name]))
            else:
                f.write('.. automethod:: %s' % '.'.join([klass.__module__,
                                                         klass.__name__,
                                                         name]))
            try:
                code_example=code_examples_dict[klass.__name__ + '.' + name]
                f.write('\n\n')
                f.write('.. rubric:: Code Example\n')
                f.write('\n')
                f.write('.. code-block:: python\n')
                f.write('\n')
                f.write(code_example['code']+'\n')
                f.write(code_example['output'])
            except KeyError:
                pass
        
        
        
def create_class_page(klass):
    "Writes te class page."
    filename=klass.__name__ + '_class.rst'
    with open(filename,'w') as f:
        f.write(klass.__name__ + '\n')
        f.write('=' * len(klass.__name__) + '\n')
        f.write('\n')
        f.write('.. autoclass:: %s\n' % (klass.__module__+'.'+klass.__name__))
        f.write('   :show-inheritance:\n')
        f.write('\n')
        try:
            code_example=code_examples_dict[klass.__name__]
            f.write('.. rubric:: Code Example\n')
            f.write('\n')
            f.write('.. code-block:: python\n')
            f.write('\n')
            f.write(code_example['code']+'\n')
            f.write(code_example['output']+'\n')
        except KeyError:
            pass
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


def delete_all_files_in_directory(mydir):
    for f in os.listdir(mydir):
        os.remove(os.path.join(mydir, f))


klasses=[crossproduct.Point,
         crossproduct.Points,
         crossproduct.Vector,
         crossproduct.Line,
         crossproduct.Polyline,
         crossproduct.Polylines,
         crossproduct.Plane,
         crossproduct.Polygon,
         crossproduct.Polygons]

def run():
    delete_all_files_in_directory(stub_dir)
    for klass in klasses[:]:
        create_pages(klass)
    

run()