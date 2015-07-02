#!/usr/bin/env python
import os
from distutils.core import setup


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as fp:
        return fp.read()

setup(name="gw2api",
      version="1.0.4",
      description="Guild Wars 2 API",
      author="Paul Hooijenga",
      author_email="paulhooijenga@gmail.com",
      url="https://github.com/hackedd/gw2api",
      license="MIT",
      long_description=read("README.rst"),
      packages=["gw2api"],
      install_requires=["requests"],
      classifiers=["Development Status :: 3 - Alpha",
                   "Environment :: Console",
                   "Environment :: Web Environment",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: MIT License",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python",
                   "Topic :: Games/Entertainment"]
      )
