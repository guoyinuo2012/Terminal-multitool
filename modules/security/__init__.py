"""
Security Module
Created by Yinuo
"""

from .security_tools import SecurityTools, main as security_main
from .defensive.defensive_tools import DefensiveSecurityTools, main as defensive_main
from .ip_logger import IPLogger, main as ip_logger_main

__all__ = ['SecurityTools', 'security_main', 'DefensiveSecurityTools', 'defensive_main', 'IPLogger', 'ip_logger_main']

# Module-level entry point
def main():
    """Entry point for security module."""
    security_main()