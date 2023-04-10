"""
Setup module
"""
import os

from importlib.machinery import SourceFileLoader
from typing import List

from pkg_resources import parse_requirements
from setuptools import setup, find_packages

MODULE_NAME = 'app'

# pylint: disable = deprecated-method
module = SourceFileLoader(
    MODULE_NAME, os.path.join(MODULE_NAME, '__init__.py')
).load_module(MODULE_NAME)


# pylint: disable = consider-using-f-string
def load_requirements(requirements_files: List[str]) -> list:
    """ Loads requirements from a file """
    requirements = []
    for file in requirements_files:
        with open(file, 'r', encoding='utf-8') as file_with_requirements:
            for req in parse_requirements(file_with_requirements.read()):
                extras = '[{}]'.format(','.join(req.extras)) if req.extras else ''
                requirements.append('{}{}{}'.format(req.name, extras, req.specifier))
    return requirements


setup(
    name=MODULE_NAME,
    version=module.__version__,
    author=module.__author__,
    author_email=module.__email__,
    license=module.__license__,
    description=module.__doc__,
    url='https://github.com/kreoshine/kreoshine',
    platforms='all',
    classifiers=[
        'Natural Language :: Russian',
    ],
    python_requires='>=3.11',
    packages=find_packages(exclude=['tests']),
    install_requires=load_requirements(['requirements.txt']),
    entry_points={
        'console_scripts': [
            'index = index.run:main',
        ],
    },
    include_package_data=True
)
