"""
Crypto & Utils Module
"""

from .crypto_tools import CryptoTools, main as crypto_main

__all__ = ['CryptoTools', 'crypto_main']

# Module-level entry point
def main():
    """Entry point for crypto module."""
    crypto_main()