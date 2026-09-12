"""
Customization Module
Created by Yinuo
"""

from .theme_manager import ThemeManager
from .config_editor import ConfigEditor
from .menu_customizer import MenuCustomizer
from .customization_tools import CustomizationTools, main as customization_main

__all__ = ['ThemeManager', 'ConfigEditor', 'MenuCustomizer', 'CustomizationTools', 'customization_main']

# Module-level entry point
def main():
    """Entry point for customization module."""
    customization_main()