"""
Discord Module
"""

from .discord_tools import DiscordTools, main as discord_main

__all__ = ['DiscordTools', 'discord_main']

# Module-level entry point
def main():
    """Entry point for Discord module."""
    discord_main()