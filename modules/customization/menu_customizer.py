"""
Menu Customizer for Terminal Multi Tool Application
Created by Yinuo
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional, List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from modules.utils.logger import setup_logger
from modules.utils.config import ConfigManager


class MenuCustomizer:
    """Customizes menu structure and categories."""
    
    def __init__(self):
        """Initialize menu customizer."""
        self.logger = setup_logger()
        self.config_manager = ConfigManager()
        self.config = self.config_manager.load_config()
        self.console = Console()
        
        # Custom menu directory
        self.menu_dir = Path(__file__).parent.parent.parent / "config" / "menus"
        self.menu_dir.mkdir(exist_ok=True)
        
        # Default menu structure
        self.default_menu = {
            '1': {'name': 'OSINT', 'desc': 'Open-source intelligence', 'module': 'modules.osint'},
            '2': {'name': 'Network', 'desc': 'Network analysis & tools', 'module': 'modules.network'},
            '3': {'name': 'Security', 'desc': 'Security testing & analysis', 'module': 'modules.security'},
            '4': {'name': 'Crypto', 'desc': 'Encryption & hashing tools', 'module': 'modules.crypto'},
            '5': {'name': 'Gen', 'desc': 'Data generators', 'module': 'modules.generators'},
            '6': {'name': 'Utils', 'desc': 'General utilities', 'module': 'modules.utils'},
            '7': {'name': 'Discord', 'desc': 'Discord tools', 'module': 'modules.discord'},
            '8': {'name': 'Resources', 'desc': 'OSINT resources', 'module': 'modules.resources'},
            '9': {'name': 'Files', 'desc': 'File management tools', 'module': 'modules.filetools'},
            '10': {'name': 'Text', 'desc': 'Text processing tools', 'module': 'modules.texttools'},
            '11': {'name': 'System', 'desc': 'System monitoring tools', 'module': 'modules.systemtools'},
            '12': {'name': 'Customize', 'desc': 'Themes, menu, settings', 'module': 'modules.customization'},
            '0': {'name': 'Exit', 'desc': 'Exit application', 'module': None}
        }
    
    def get_custom_menu(self) -> Dict[str, Dict]:
        """Get custom menu structure."""
        custom_menu_file = self.menu_dir / "custom_menu.json"
        
        if custom_menu_file.exists():
            try:
                with open(custom_menu_file, 'r') as f:
                    return json.load(f)
            except:
                self.logger.warning("Could not load custom menu, using default")
        
        return self.default_menu
    
    def save_custom_menu(self, menu_structure: Dict[str, Dict]) -> bool:
        """Save custom menu structure."""
        try:
            custom_menu_file = self.menu_dir / "custom_menu.json"
            
            with open(custom_menu_file, 'w') as f:
                json.dump(menu_structure, f, indent=2)
            
            self.logger.info("Custom menu saved")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving custom menu: {e}")
            return False
    
    def reset_menu(self) -> bool:
        """Reset menu to default structure."""
        try:
            custom_menu_file = self.menu_dir / "custom_menu.json"
            
            if custom_menu_file.exists():
                custom_menu_file.unlink()
            
            self.logger.info("Menu reset to default")
            return True
            
        except Exception as e:
            self.logger.error(f"Error resetting menu: {e}")
            return False
    
    def rename_category(self, category_key: str, new_name: str) -> bool:
        """Rename a menu category."""
        try:
            menu = self.get_custom_menu()
            
            if category_key in menu:
                menu[category_key]['name'] = new_name
                self.save_custom_menu(menu)
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error renaming category: {e}")
            return False
    
    def hide_category(self, category_key: str) -> bool:
        """Hide a menu category."""
        try:
            menu = self.get_custom_menu()
            
            if category_key in menu:
                menu[category_key]['hidden'] = True
                self.save_custom_menu(menu)
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error hiding category: {e}")
            return False
    
    def show_category(self, category_key: str) -> bool:
        """Show a hidden menu category."""
        try:
            menu = self.get_custom_menu()
            
            if category_key in menu:
                menu[category_key]['hidden'] = False
                self.save_custom_menu(menu)
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error showing category: {e}")
            return False
    
    def reorder_categories(self, new_order: List[str]) -> bool:
        """Reorder menu categories."""
        try:
            menu = self.get_custom_menu()
            new_menu = {}
            
            for key in new_order:
                if key in menu:
                    new_menu[key] = menu[key]
            
            # Add any remaining categories
            for key, value in menu.items():
                if key not in new_menu:
                    new_menu[key] = value
            
            self.save_custom_menu(new_menu)
            return True
            
        except Exception as e:
            self.logger.error(f"Error reordering categories: {e}")
            return False
    
    def add_custom_category(self, key: str, name: str, desc: str, module: str) -> bool:
        """Add a custom menu category."""
        try:
            menu = self.get_custom_menu()
            
            menu[key] = {
                'name': name,
                'desc': desc,
                'module': module,
                'custom': True
            }
            
            self.save_custom_menu(menu)
            return True
            
        except Exception as e:
            self.logger.error(f"Error adding custom category: {e}")
            return False
    
    def remove_category(self, category_key: str) -> bool:
        """Remove a menu category."""
        try:
            menu = self.get_custom_menu()
            
            if category_key in menu and menu[category_key].get('custom', False):
                del menu[category_key]
                self.save_custom_menu(menu)
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error removing category: {e}")
            return False
    
    def display_menu_structure(self) -> None:
        """Display current menu structure."""
        menu = self.get_custom_menu()
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Key", style="cyan")
        table.add_column("Name", style="green")
        table.add_column("Description", style="white")
        table.add_column("Module", style="yellow")
        table.add_column("Status", style="magenta")
        
        for key, category in menu.items():
            status = "[green]Active[/green]"
            if category.get('hidden', False):
                status = "[red]Hidden[/red]"
            if category.get('custom', False):
                status = "[cyan]Custom[/cyan]"
            
            table.add_row(key, category['name'], category['desc'], 
                        category.get('module', 'N/A'), status)
        
        self.console.print(Panel(table, title="[bold]Menu Structure[/bold]"))