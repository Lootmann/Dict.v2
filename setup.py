# setup.py
from setuptools import find_packages, setup


def load_requirements() -> list:
    with open("./requirements.txt", "r") as req:
        return req.read().splitlines()


setup(
    name="tmp",
    version="0.1",
    description="Simple English Japanese Dictionary via WeblioAPI",
    author="Lootmann",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "dict=src.main:main",
        ],
    },
    install_requires=load_requirements(),
)
