#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DND Campaign Library - Setup Configuration
"""

from setuptools import setup, find_packages
import os

# Read README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    requirements = []
    if os.path.exists("requirements.txt"):
        with open("requirements.txt", "r", encoding="utf-8") as fh:
            requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]
    return requirements

setup(
    name="cursor-based-dnd",
    version="1.0.0",
    author="billbarra",
    author_email="billbarrazz@gmail.com",
    description="A complete DND campaign system designed for AI-assisted gameplay",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/billbarra/Cursor_Based_DND",
    project_urls={
        "Bug Tracker": "https://github.com/billbarra/Cursor_Based_DND/issues",
        "Documentation": "https://github.com/billbarra/Cursor_Based_DND/wiki",
        "Source Code": "https://github.com/billbarra/Cursor_Based_DND",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Games/Entertainment :: Role-Playing",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Natural Language :: Chinese (Simplified)",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
    },
    entry_points={
        "console_scripts": [
            "dnd-check=utils.system_checker:main",
            "dnd-dice=rules.dice_roller:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.json", "*.md", "*.txt"],
    },
    keywords="dnd, d&d, dungeons, dragons, roleplaying, game, ai, automation",
    license="MIT",
    zip_safe=False,
)
