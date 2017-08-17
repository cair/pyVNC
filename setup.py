from setuptools import setup

setup(
    name='pyVNC',    # This is the name of your PyPI-package.
    version='0.1',                          # Update the version number for new releases
    install_requires=['twisted', 'numpy', 'pygame'],
    packages=["pyVNC"],
    scripts=['./pyVNC/pyvnc.py']                  # The name of your scipt, and also the command you'll be using for calling it
)