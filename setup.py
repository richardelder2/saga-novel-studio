from setuptools import setup, find_packages

setup(
    name="saga-cli",
    version="1.0.0",
    py_modules=["saga_cli"],
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "saga=saga_cli:main",
        ],
    },
)
