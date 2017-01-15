from setuptools import setup, find_packages

setup(name='almaany',
      version='01.beta',
      description='python API for almaany.com',
      keywords='almaany arabic arabic translate',
      author='ihfazhillah',
      author_email='mihfazhillah@gmail.com',
      url='ihfazhillah.github.io',
      #namespace_packages=['almaany'],
      install_requires=['requests'],
      packages=find_packages(),
      )
