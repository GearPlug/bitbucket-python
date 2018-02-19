import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='bitbucket-python',
      version='0.2',
      description='API wrapper for Bitbucket written in Python',
      long_description=read('README.md'),
      url='https://github.com/GearPlug/bitbucket-python',
      author='Miguel Ferrer',
      author_email='ingferrermiguel@gmail.com',
      license='GPL',
      packages=['bitbucket'],
      install_requires=[
          'requests',
      ],
      zip_safe=False)
1