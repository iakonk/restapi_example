import os
from setuptools import setup, find_packages
from glob import glob


# details about App
with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

# App version
with open(os.path.join(os.path.dirname(__file__), 'VERSION.txt')) as fd:
    version = fd.read()

with open('requirements.txt', 'r') as fd:
    requirements_list = [line for line in fd.read().splitlines() if line.strip()]

setup(
    name='restapi_project',
    description='REST API example project',
    version=version,
    license='',
    long_description=README,
    author='Konkina Iana',
    author_email='konkina.iana@gmail.com',
    url='',
    packages=find_packages(),
    install_requires=requirements_list,
    data_files=[
        ('', glob('README.rst'))
    ],
    include_package_data=True,
    platforms=['Any'],
    zip_safe=False
)
