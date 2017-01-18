from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()]

setup(
    name='gulpster',
    version='0.1',
    description='An event orchestration package',
    long_description=LONG_DESCRIPTION,
    url='https://github.com/anvth/gulpster',
    author='Anvith Shivakumara',
    author_email='s.anvith@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Web',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='Micro services',
    packages=find_packages(),
    install_requires=REQUIREMENTS,
)