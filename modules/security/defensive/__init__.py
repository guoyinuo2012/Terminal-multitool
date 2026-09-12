"""
Defensive Security Module
Created by Yinuo
"""

from .defensive_tools import DefensiveSecurityTools, main as defensive_main

__all__ = ['DefensiveSecurityTools', 'defensive_main']

# Module-level entry point
def main():
    """Entry point for defensive security module."""
    defensive_main()