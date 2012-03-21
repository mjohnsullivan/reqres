from distutils.core import setup

version = '0.1.0'

setup(name='reqres',
      version=version,
      description='HTTP request/response',
      long_description='A simple HTTP request/response wrapper for Python',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache V2',
        'Topic :: Other/Nonlisted Topic',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
      ],
      keywords='http',
      author='Matt Sullivan',
      author_email='matt.j.sullivan@gmail.com',
      url='http://www.github.com/mjohnsullivan/reqres',
      license='Apache V2',
      py_modules=['reqres']
      )
