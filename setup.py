from setuptools import find_packages
from setuptools import setup

setup(
    name="app",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=['fastapi'],
    extras_require={"test": ["pytest", "coverage"]},
)
