"""
Keybindings Manager for Void Application
Created by Yinuo
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from modules.utils.logger import setup_logger
from modules.utils.config import ConfigManager


class KeybindingsManager:
    """Manages custom keybindings for Void."""
    
    def __init__(self):
        """Initialize keybindings manager."""
        self.logger = setup_logger()
        self.config_manager = ConfigManager()
        self.config = self.config_manager.load_config()
        self.console = Console()
        
        # Keybindings directory
        self.keybindings_dir = Path(__file__).parent.parent.parent / "config" / "keybindings"
        self.keybindings_dir.mkdir(exist_ok=True)
        
        # Default keybindings
        self.default_keybindings = {
            'quit': 'q',
            'back': '0',
            'refresh': 'r',
            'help': 'h',
            'menu': 'm',
            'search': '/',
            'clear': 'c'
        }
    
    def get_keybindings(self) -> Dict[str, str]:
        """Get current keybindings."""
        keybindings_file = self.keybindings_dir / "custom_keybindings.json"
        
        if keybindings_file.exists():
            try:
                with open(keybindings_file, 'r') as f:
                    return json.load(f)
            except:
                self.logger.warning("Could not load custom keybindings, using default")
        
        return self.default_keybindings.copy()
    
    def save_keybindings(self, keybindings: Dict[str, str]) -> bool:
        """Save custom keybindings."""
        try:
            keybindings_file = self.keybindings_dir / "custom_keybindings.json"
            
            with open(keybindings_file, 'w') as f:
                json.dump(keybindings, f, indent=2)
            
            self.logger.info("Custom keybindings saved")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving keybindings: {e}")
            return False
    
    def set_keybinding(self, action: str, key: str) -> bool:
        """Set a specific keybinding."""
        try:
            keybindings = self.get_keybindings()
            keybindings[action] = key
            return self.save_keybindings(keybindings)
            
        except Exception as e:
            self.logger.error(f"Error setting keybinding: {e}")
            return False
    
    def reset_keybindings(self) -> bool:
        """Reset keybindings to default."""
        try:
            keybindings_file = self.keybindings_dir / "custom_keybindings.json"
            
            if keybindings_file.exists():
                keybindings_file.unlink()
            
            self.logger.info("Keybindings reset to default")
            return True
            
        except Exception as e:
            self.logger.error(f"Error resetting keybindings: {e}")
            return False
    
    def display_keybindings(self) -> None:
        """Display current keybindings."""
        keybindings = self.get_keybindings()
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Action", style="cyan")
        table.add_column("Key", style="green")
        
        for action, key in keybindings.items():
            table.add_row(action, key)
        
        self.console.print(Panel(table, title="[bold]Current Keybindings[/bold]"))
    
    def get_key_for_action(self, action: str) -> str:
        """Get key binding for a specific action."""
        keybindings = self.get_keybindings()
        return keybindings.get(action, '')