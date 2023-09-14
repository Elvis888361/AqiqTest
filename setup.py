from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in aquiq/__init__.py
from aquiq import __version__ as version

setup(
	name="aquiq",
	version=version,
	description="Aquiq",
	author="Aquiq",
	author_email="elvisndegwa90@gmail.coom",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)