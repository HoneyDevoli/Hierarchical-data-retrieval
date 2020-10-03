import os
from importlib.machinery import SourceFileLoader

from pkg_resources import parse_requirements
from setuptools import setup

module_name = 'employees'

module = SourceFileLoader(
    module_name, os.path.join(module_name, '__init__.py')
).load_module()


def load_requirements(fname: str) -> list:
    requirements = []
    with open(fname, 'r') as fp:
        for req in parse_requirements(fp.read()):
            extras = '[{}]'.format(','.join(req.extras)) if req.extras else ''
            requirements.append(
                '{}{}{}'.format(req.name, extras, req.specifier)
            )
    return requirements


setup(
    name=module_name,
    version='0.0.2',
    long_description=open('README.md').read(),
    python_requires='>=3.8',
    install_requires=load_requirements('requirements.txt'),
    entry_points={
        'console_scripts': [
            'init-db = {0}.__main__:init_db'.format(module_name),
            'get-names = {0}.__main__:get_names'.format(module_name),
        ]
    },
    include_package_data=True
)
