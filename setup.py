from setuptools import setup
from distutils.util import convert_path


def find_version():
    environment = {}
    version_path = convert_path('wif/version.py')
    with open(version_path) as file:
        contents = file.read()
        exec(contents, environment)
    version = environment['__version__']
    return version



setup(
    name='wif',
    version=find_version(),
    description='WIF tools',
    url='http://github.com/UCLeuvenLimburg/wif',
    author='Frederic Vogels',
    author_email='frederic.vogels@ucll.be',
    license='MIT',
    packages=['wif'],
    entry_points = {
          'console_scripts': [ 'wif=wif.main:main']
    },
    install_requires=['pillow', 'numpy', 'opencv-contrib-python'],
    zip_safe=False)