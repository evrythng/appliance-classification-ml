from setuptools import find_packages
from setuptools import setup
# -*- coding: utf-8 -*-

setup(
    name='trainer',
    version='0.3',
    packages=find_packages(),
    package_dir={".": "libs"},
    install_requires=['keras','h5py','tensorflow>=1.4','sklearn','ujson', 'pandas','aiohttp','uvloop','requests','numpy'],
    include_package_data=True,
    description='Keras trainer application',

)
