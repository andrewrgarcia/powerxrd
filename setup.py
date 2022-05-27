from setuptools import find_packages, setup

setup(name='powerxrd',
      version='0.0.1',
      description='Simple tools to handle powder XRD (and XRD) data with Python',
      url='https://github.com/andrewrgarcia/powerxrd',
      author='Andrew Garcia, PhD',
      license='MIT',
      packages=find_packages(include=['powerxrd']),
      zip_safe=False)
