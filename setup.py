import setuptools

setuptools.setup(
        name="PyFreatboard",
        version="0.1",
        author="Narcis Palomeras",
        description="PyFreatboard is an API for drawing diagrams (aka shapes) on the guitar freatboard using Python as well as to automatically generate new shapes.",
        packages=["PyFreatboard"],
        install_requires=[
          'matplotlib',
      ]
)

