from setuptools import find_packages
from distutils.core import setup
from glob import glob


setup(
    name='django-mothulity',
    version='v0.0.0',
    author='Dariusz Izak, IBB PAS',
    packages=find_packages(exclude=['*test*']),
    include_package_data=True
)
