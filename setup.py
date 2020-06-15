from setuptools import setup

setup(name='uxps',
      version='0.1',
      description='some xpf functions',
      url='https://github.com/jonasangstrom/uxps',
      author='Jonas Angstrom',
      author_email='jonas.aangstroem@gmail.com',
      license='MIT',
      packages=['uxps'],
      zip_safe=False,
      install_requires=[
          'lmfit',
          'matplotlib',
          'numpy'
      ])
