"""Creats python wrappers from boost macro

ASSUMES: ../../libAngle exists and /usr/local/[include,lib] has boost installed.
"""

from distutils.core import setup, Extension

name = 'angles'
version = '1.0'
BOOST_ROOT = '/usr/local'

include_dirs=['../../libAngles',
              BOOST_ROOT + '/include',
              ]


library_dirs=['../../libAngles',
              BOOST_ROOT + '/lib'
              ]

libraries = ['boost_python', 'Angles']

sources = ['angles.cpp']

angle_module = Extension(name,
                         include_dirs=include_dirs,
                         libraries=libraries,
                         library_dirs=library_dirs,
                         sources=sources)

setup (name=name,
       version=version,
       description='angle package',
       ext_modules=[angle_module])
