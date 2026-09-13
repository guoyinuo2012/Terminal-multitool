"""
Theme Manager for Terminal Multi Tool Application
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


class ThemeManager:
    """Manages themes and visual customization for Void."""
    
    def __init__(self):
        """Initialize theme manager."""
        self.logger = setup_logger()
        self.config_manager = ConfigManager()
        self.config = self.config_manager.load_config()
        
        # Theme directory
        self.theme_dir = Path(__file__).parent.parent.parent / "config" / "themes"
        self.theme_dir.mkdir(exist_ok=True)
        
        # Default themes
        self.default_themes = {
            'dark': {
                'name': 'Dark',
                'description': 'Default dark theme',
                'colors': {
                    'header': 'cyan',
                    'subtitle': 'green',
                    'table_header': 'magenta',
                    'table_col_1': 'cyan',
                    'table_col_2': 'green',
                    'table_col_3': 'white',
                    'highlight': 'yellow',
                    'error': 'red',
                    'success': 'green',
                    'warning': 'yellow',
                    'info': 'blue',
                    'border': 'blue'
                },
                'styles': {
                    'bold': True,
                    'italic': False,
                    'underline': False
                }
            },
            'light': {
                'name': 'Light',
                'description': 'Light theme for bright environments',
                'colors': {
                    'header': 'blue',
                    'subtitle': 'green',
                    'table_header': 'cyan',
                    'table_col_1': 'blue',
                    'table_col_2': 'green',
                    'table_col_3': 'black',
                    'highlight': 'magenta',
                    'error': 'red',
                    'success': 'green',
                    'warning': 'yellow',
                    'info': 'blue',
                    'border': 'green'
                },
                'styles': {
                    'bold': True,
                    'italic': False,
                    'underline': False
                }
            },
            'hacker': {
                'name': 'Hacker',
                'description': 'Green terminal theme',
                'colors': {
                    'header': 'green',
                    'subtitle': 'bright_green',
                    'table_header': 'green',
                    'table_col_1': 'green',
                    'table_col_2': 'bright_green',
                    'table_col_3': 'white',
                    'highlight': 'yellow',
                    'error': 'red',
                    'success': 'green',
                    'warning': 'yellow',
                    'info': 'cyan',
                    'border': 'green'
                },
                'styles': {
                    'bold': True,
                    'italic': False,
                    'underline': False
                }
            },
            'purple': {
                'name': 'Purple',
                'description': 'Purple accent theme',
                'colors': {
                    'header': 'magenta',
                    'subtitle': 'purple',
                    'table_header': 'magenta',
                    'table_col_1': 'magenta',
                    'table_col_2': 'purple',
                    'table_col_3': 'white',
                    'highlight': 'cyan',
                    'error': 'red',
                    'success': 'green',
                    'warning': 'yellow',
                    'info': 'blue',
                    'border': 'magenta'
                },
                'styles': {
                    'bold': True,
                    'italic': False,
                    'underline': False
                }
            }
        }
    
    def get_available_themes(self) -> Dict[str, Dict]:
        """Get all available themes."""
        themes = self.default_themes.copy()
        
        # Load custom themes
        for theme_file in self.theme_dir.glob("*.json"):
            try:
                with open(theme_file, 'r') as f:
                    custom_theme = json.load(f)
                    themes[theme_file.stem] = custom_theme
            except:
                self.logger.warning(f"Could not load theme: {theme_file}")
        
        return themes
    
    def get_current_theme(self) -> Dict[str, Any]:
        """Get current theme from config."""
        theme_name = self.config.get('ui', {}).get('theme', 'dark')
        themes = self.get_available_themes()
        return themes.get(theme_name, self.default_themes['dark'])
    
    def set_theme(self, theme_name: str) -> bool:
        """Set current theme."""
        themes = self.get_available_themes()
        
        if theme_name not in themes:
            self.logger.warning(f"Theme not found: {theme_name}")
            return False
        
        # Update config
        self.config['ui']['theme'] = theme_name
        self.config_manager.save_config(self.config)
        
        self.logger.info(f"Theme set to: {theme_name}")
        return True
    
    def create_custom_theme(self, theme_name: str, theme_data: Dict[str, Any]) -> bool:
        """Create a custom theme."""
        try:
            theme_file = self.theme_dir / f"{theme_name}.json"
            
            with open(theme_file, 'w') as f:
                json.dump(theme_data, f, indent=2)
            
            self.logger.info(f"Custom theme created: {theme_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error creating theme: {e}")
            return False
    
    def delete_custom_theme(self, theme_name: str) -> bool:
        """Delete a custom theme."""
        theme_file = self.theme_dir / f"{theme_name}.json"
        
        if theme_file.exists():
            try:
                theme_file.unlink()
                self.logger.info(f"Custom theme deleted: {theme_name}")
                return True
            except Exception as e:
                self.logger.error(f"Error deleting theme: {e}")
                return False
        
        return False
    
    def apply_theme_to_console(self, console: Console) -> None:
        """Apply current theme to console (placeholder for Rich theme support)."""
        # Rich has limited theme support, but we can use this for future expansion
        current_theme = self.get_current_theme()
        # Theme application logic would go here
        pass
    
    def display_themes(self) -> None:
        """Display available themes."""
        console = Console()
        themes = self.get_available_themes()
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Theme", style="cyan")
        table.add_column("Description", style="green")
        table.add_column("Status", style="yellow")
        
        current_theme = self.config.get('ui', {}).get('theme', 'dark')
        
        for name, theme in themes.items():
            status = "[green]ACTIVE[/green]" if name == current_theme else ""
            table.add_row(theme['name'], theme['description'], status)
        
        console.print(Panel(table, title="[bold]Available Themes[/bold]"))
    
    def get_theme_color(self, color_name: str) -> str:
        """Get a specific color from current theme."""
        theme = self.get_current_theme()
        return theme.get('colors', {}).get(color_name, 'white')
    
    def get_theme_style(self, style_name: str) -> bool:
        """Get a specific style from current theme."""
        theme = self.get_current_theme()
        return theme.get('styles', {}).get(style_name, False)