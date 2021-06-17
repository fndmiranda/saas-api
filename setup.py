from setuptools import find_packages
from setuptools import setup

# with io.open("README.rst", "rt", encoding="utf8") as f:
#     readme = f.read()

# setup(
#     name='flask-app-commands',
#     entry_points={
#         'flask.commands': [],
#     }, install_requires=['click', 'flask']
# )

setup(
    name="app",
    # long_description=readme,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=['fastapi'],
    extras_require={"test": ["pytest", "coverage"]},
)
