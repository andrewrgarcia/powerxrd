#--Adapted from: https://towardsdatascience.com/deep-dive-create-and-publish-your-first-python-library-f7f618719e14
# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# This call to setup() does all the work
setup(
    name="powerxrd",
    version="2.1.2",
    description="Simple tools to handle powder XRD (and XRD) data with Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/andrewrgarcia/powerxrd",
    author="Andrew Garcia, PhD",
    license="MIT",
    classifiers=[
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    packages=["powerxrd"],
    include_package_data=True,
    install_requires=["numpy"]
)
