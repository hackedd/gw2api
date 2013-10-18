#!/usr/bin/env python
from distutils.core import setup

setup(name="gw2api",
      version="1.0.1",
      description="Guild Wars 2 API",
      author="Paul Hooijenga",
      author_email="paulhooijenga@gmail.com",
      url="https://github.com/hackedd/gw2api",
      packages=["gw2api"],
      requires=["requests"],
      classifiers=["Development Status :: 3 - Alpha",
                   "Environment :: Console",
                   "Environment :: Web Environment",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: MIT License",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python",
                   "Topic :: Games/Entertainment"]
      )
