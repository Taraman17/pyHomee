import setuptools

__version__ = "1.2.0"

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyHomee",
    version=__version__,
    author="Taraman17",
    description="a python library to interact with homee",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Taraman17/pyHomee",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
)
