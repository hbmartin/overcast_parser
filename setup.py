from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="overcast_parser",
    version="0.1.0",
    description="Overcast podcast link parser especially for pythonista.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hbmartin/overcast_parser",
    author="Harold Martin",
    author_email="harold.martin@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: iOS",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup :: XML",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Typing :: Typed",
    ],
    install_requires=["requests"],
    extras_require={
        "dev": ["black", "pythonista-stubs"],
        "lint": ["ruff", "pyroma", "pytype", "types-python-dateutil", "types-requests"],
    },
    keywords=[
        "podcast",
        "parser",
        "rss",
        "feed",
        "pythonista",
        "overcast",
        "shortcuts",
        "ios",
    ],
    packages=find_packages(exclude=["contrib", "docs", "tests"]),
    project_urls={
        "Bug Reports": "https://github.com/hbmartin/overcast_parser/issues",
    },
    python_requires=">=3.11",
)
