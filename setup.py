#!/usr/bin/env python3
"""
setup.py - Package configuration for comms comment removal tool

This allows the package to be installed via pip.
"""

from setuptools import setup, find_packages
from pathlib import Path


readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding='utf-8') if readme_path.exists() else ""

setup(
    name="comment-remover-cli",
    version="1.2.1",
    description="High-accuracy comment removal tool for 20+ programming languages with beautiful CLI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="guider23",
    author_email="sofiyasenthilkumar@gmail.com",
    url="https://github.com/guider23/Comms",
    project_urls={
        "Bug Tracker": "https://github.com/guider23/Comms/issues",
        "Documentation": "https://github.com/guider23/Comms#readme",
        "Source Code": "https://github.com/guider23/Comms",
    },
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "comment-remover=comms.cli:main",
            "comms=comms.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Pre-processors",
        "Topic :: Text Processing :: Filters",
        "Topic :: Utilities",
    ],
    python_requires=">=3.6",
    keywords="comments removal programming development tools parsing",
    install_requires=[],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black",
            "flake8",
            "mypy",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
