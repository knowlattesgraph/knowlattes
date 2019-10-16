import os
from setuptools import setup


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def requirements_from_pip(filename='requeriments.txt'):
    with open(filename, 'r') as pip:
        return [l.strip() for l in pip if not l.startswith('#') and l.strip()]

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


core_deps = requirements_from_pip()

setup(
    name='knowlattes',
    version="0.0.1",
    author="Henrique & Thiago",
    author_email="henrique.facioli & tdsfarias [at] gmail [dot] com",
    description=("Knowlattes graph to run"),
    license="GLP3",
    keywords=".",
    url="http://github.com/knowlattes/knowlattes",
    long_description=read('README.md'),
    package_dir={'': 'src'},
    install_requires=core_deps,
    include_package_data=True,
    zip_safe=False,
    classifiers=['Programming Language :: Python :: 3.6']
)