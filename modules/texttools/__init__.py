"""
Text Processing & Encoding Tools Module
Created by Yinuo
"""

from .text_tools import TextTools, main as texttools_main

__all__ = ['TextTools', 'texttools_main']

# Module-level entry point
def main():
    """Entry point for text tools module."""
    texttools_main()
