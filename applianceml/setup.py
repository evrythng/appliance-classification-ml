# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup
import os

if os.getenv('ML_DEV_ENV') and os.getenv('ML_DEV_ENV') == 'LOCAL':
    setup(
        name='trainer',
        author='joel@evrythng.com',
        version='0.1',
        packages=['evt'] + find_packages(),
        package_dir={"evt": "../evt"},
        install_requires=['keras', 'h5py', 'tensorflow>=1.5', 'sklearn', 'ujson', 'numpy'],
        include_package_data=True,
        description='Keras trainer application',
        requires=[]
    )
else:
    setup(
        name='trainer',
        author='joel@evrythng.com',
        version='0.1',
        packages=find_packages(),
        install_requires=['keras', 'h5py', 'tensorflow>=1.5', 'sklearn', 'ujson', 'numpy'],
        include_package_data=True,
        description='Keras trainer application',
        requires=[]
    )
