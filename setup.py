"""Installer for sd-proxy
"""

import os
cwd = os.path.dirname(__file__)

try:
        from setuptools import setup, find_packages
except ImportError:
        from ez_setup import use_setuptools
        use_setuptools()
        from setuptools import setup, find_packages

setup(
    name='sd-proxy',
    description='Intelligent HTTP proxy for proxying Server Density'
                ' sd-agent payloads from within a private network',
    long_description=open('README.rst').read(),
    version='1.0.0',
    author='Wes Mason',
    author_email='wes@serverdensity.com',
    url='https://github.com/serverdensity/sd-proxy',
    packages=find_packages(exclude=['ez_setup']),
    install_requires=open('requirements.txt').readlines(),
    include_package_data=True,
    license='BSD',
    entry_points={
        'console_scripts': [
            'sd-proxy = serverdensity.proxy.runserver:main'
        ]
    }
)
