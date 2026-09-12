"""
OSINT & Research Module
"""

from .osint_tools import OSINTTools, main as osint_main
from .advanced_tools import AdvancedOSINTTools, main as advanced_main

__all__ = ['OSINTTools', 'osint_main', 'AdvancedOSINTTools', 'advanced_main']

# Module-level entry point
def main():
    """Entry point for OSINT module."""
    osint_main()