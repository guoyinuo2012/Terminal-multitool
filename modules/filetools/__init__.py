"""
File Management Tools Module
Created by Yinuo
"""

from .file_tools import FileTools, main as filetools_main

__all__ = ['FileTools', 'filetools_main']

# Module-level entry point
def main():
    """Entry point for file tools module."""
    filetools_main()