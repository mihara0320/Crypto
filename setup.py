from distutils.core import setup, Extension

setup(name='crypto',
      version='1.0',
      ext_modules=[Extension(
      'crypto', ['crypto.c'],
      libraries=['pycrypto'])]
      )
