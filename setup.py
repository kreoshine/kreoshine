import os

from importlib.machinery import SourceFileLoader

from pkg_resources import parse_requirements
from setuptools import setup, find_packages

MODULE_NAME = 'app'

module = SourceFileLoader(
    MODULE_NAME, os.path.join(MODULE_NAME, '__init__.py')
).load_module(MODULE_NAME)


def load_requirements(requirements_file: str) -> list:
    requirements = []
    with open(requirements_file, 'r') as f:
        for req in parse_requirements(f.read()):
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
    # long_description=open('README.md').read(),  # todo: add long description
    url='https://github.com/kreoshine/backend',
    platforms='all',
    classifiers=[
        'Natural Language :: Russian',
    ],
    python_requires='>=3.11',
    packages=find_packages(exclude=['tests']),
    install_requires=load_requirements('app/requirements.txt'),
    extras_require={'deploy': load_requirements('deploy/requirements.txt')},
    entry_points={
        # todo: add entry point for deploy.__main__
        # todo: add entry point for app.__main__
    },
    include_package_data=True
)
