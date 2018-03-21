"""
Setup module.
"""
from setuptools import setup
from ommr import __version__


setup(
    name='ommr',
    version=__version__,
    description='A simple Micromouse Maze Simulator server',
    long_description='''Take an image of a micromouse maze setup and convert
        it to the standard micromouse maze text format.''',
    url='https://github.com/Theseus/ommr',
    author='Miguel Sánchez de León Peque',
    author_email='peque@neosit.es',
    license='BSD License',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Utilities',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    keywords='micromouse optical maze server recognition',
    entry_points={
        'console_scripts': [
            'ommr = ommr.commands:run',
        ],
    },
    packages=['ommr'],
    install_requires=[
        'click',
        'imageio',
        'scipy',
    ],
    extras_require={
        'test': ['tox'],
    },
)
