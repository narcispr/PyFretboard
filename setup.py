import setuptools

setuptools.setup(
        name="PyFretboard",
        version="0.4",
        author="Narcis Palomeras",
        description="PyFretboard is an API for drawing diagrams on the guitar fretboard.",
        long_description="PyFretboard is an API for drawing diagrams (aka shapes) on the guitar fretboard using Python as well as to automatically generate new shapes.",
        long_description_content_type="text/markdown",
        url="https://github.com/narcispr/PyFretboard",
        classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: BSD License",
          "Operating System :: OS Independent",
        ],
        packages=["PyFretboard"],
        install_requires=[
          'matplotlib',
      ]
)

