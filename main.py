#!/usr/bin/env python3
"""
Void - Comprehensive Terminal-Based Multitool Application
Main Entry Point

DISCLAIMER: This tool is for education and authorized research only.
Use only on systems you own or have explicit permission to test.
"""

import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from modules.ui.dashboard import Dashboard
from modules.utils.logger import setup_logger
from modules.utils.config import ConfigManager


def main():
    """Main entry point for the Void application."""
    try:
        # Setup logging
        logger = setup_logger()
        logger.info("Starting Void application")
        
        # Load configuration
        config_manager = ConfigManager()
        config = config_manager.load_config()
        
        # Display disclaimer
        print("\n" + "="*60)
        print("VOID - Terminal-Based Multitool Application")
        print("Created by Yinuo")
        print("="*60)
        print("\nDISCLAIMER: This tool is for education and authorized")
        print("research only. Use only on systems you own or have")
        print("explicit permission to test.")
        
        # Auto-continue for non-interactive environments
        try:
            print("\nPress Enter to continue...")
            input()
        except EOFError:
            # Non-interactive mode, continue automatically
            print("(Auto-continuing...)")
        except:
            print("(Continuing...)")
        
        # Launch the dashboard
        dashboard = Dashboard(config)
        dashboard.run()
        
    except KeyboardInterrupt:
        print("\n\n[!] Application interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n[!] Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()