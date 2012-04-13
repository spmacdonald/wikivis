from setuptools import setup, Extension, find_packages
from Cython.Distutils import build_ext
import os

# os.environ.setdefault("CC", "/usr/bin/gcc-4.2")
# os.environ.setdefault("CPP", "/usr/bin/g++-4.2")

extensions = [
    Extension("wikivis.graph",
              ["wikivis/graph.pyx"],
              language="c++",
              include_dirs=["include"])
]

setup(name="wikivis",
      ext_modules=extensions,
      cmdclass={"build_ext": build_ext})

