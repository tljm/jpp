from setuptools import setup

from jpp import __version__ as version

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='jpp',
      version='.'.join(map(str,version)),
      description='Journal preprocessor',
      long_description=readme(),
      classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Text Processing :: Markup',
      ],
      url='http://github.com/tljm/jpp',
      author='Tomasz Magdziarz',
      author_email='tljm@wp.pl',
      test_suite='nose.collector',
      tests_require=['nose'],
      scripts=['apps/mdjpp.py'],
      license='ISC',
      packages=['jpp'],
      zip_safe=False)
