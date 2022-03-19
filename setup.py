import setuptools

setuptools.setup(
        name="PyFreatboard",
        version="0.2",
        author="Narcis Palomeras",
        description="PyFreatboard is an API for drawing diagrams on the guitar freatboard.",
        long_description="PyFreatboard is an API for drawing diagrams (aka shapes) on the guitar freatboard using Python as well as to automatically generate new shapes.",
        long_description_content_type="text/markdown",
        url="https://github.com/narcispr/PyFreatboard",
        classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: BSD License",
          "Operating System :: OS Independent",
        ],
        packages=["PyFreatboard"],
        install_requires=[
          'matplotlib',
      ]
)

