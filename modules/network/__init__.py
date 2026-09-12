"""
Network Module
"""

from .network_tools import NetworkTools, main as network_main
from .advanced_tools import AdvancedNetworkTools, main as advanced_main

__all__ = ['NetworkTools', 'network_main', 'AdvancedNetworkTools', 'advanced_main']

# Module-level entry point
def main():
    """Entry point for network module."""
    network_main()