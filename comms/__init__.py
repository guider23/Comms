"""
comms - High-accuracy comment removal tool

A Python package for removing comments from programming files while preserving
important code patterns like color codes, URLs, and preprocessor directives.

Supports 20+ programming languages with state-machine based parsing.
"""

__version__ = "1.1.0"
__author__ = "guider23"
__email__ = "sofiyasenthilkumar@gmail.com"

from .core import CommentRemover
from .cli import main

__all__ = ["CommentRemover", "main"]
