# builds python orbits module
# from http://docs.python.org/extending/building.html

from distutils.core import setup, Extension

angles_module = Extension('angles',
                          include_dirs=['../../libAngles'], # TODO meh.
                          libraries=['Angles'],
                          library_dirs=['../../libAngles'], # TODO meh**2.
                          sources=['angles.cpp'])

setup (name='angles',
       version='1.0',
       description='angles package',
       ext_modules=[angles_module])

