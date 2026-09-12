"""
Resources Module
"""

from .resource_links import ResourceLinks, main as resources_main

__all__ = ['ResourceLinks', 'resources_main']

# Module-level entry point
def main():
    """Entry point for resources module."""
    resources_main()