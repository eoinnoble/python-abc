import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="python-abc",
    version="0.2.0",
    description="A python implementation of the ABC Software metric",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/eoinnoble/python-abc",
    author="Eoin Noble",
    author_email="eoin@eoinnoble.com",
    classifiers=[
        "License :: Freely Distributable",
        "Programming Language :: Python :: 3.9",
        "Typing :: Typed",
    ],
    packages=["python_abc"],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "python_abc=python_abc.__main__:main",
        ]
    },
)
