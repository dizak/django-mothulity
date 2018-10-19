from setuptools import find_packages, setup
from mothulity import __version__ as VERSION
from mothulity import __author__ as AUTHOR


setup(
    name='django-mothulity',
    version=VERSION,
    author=AUTHOR,
    packages=['mothulity'],
    include_package_data=True,
    install_requires=open('requirements.txt').readlines(),
    scripts=['sched.py'],
    description='Web fron-end for mothulity',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author_email='dariusz.izak@ibb.waw.pl',
    url='https://github.com/dizak/django-mothulity',
    classifiers=[
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
    ]
)
