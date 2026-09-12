"""
Customization Tools Module
Created by Yinuo
"""

from typing import Dict, Any
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from modules.utils.logger import setup_logger
from modules.utils.validators import InputValidator
from modules.utils.error_handler import ErrorHandler, handle_errors
from modules.utils.config import ConfigManager
from .theme_manager import ThemeManager
from .config_editor import ConfigEditor
from .menu_customizer import MenuCustomizer


class CustomizationTools:
    """Main customization tools class."""
    
    def __init__(self):
        """Initialize customization tools."""
        self.logger = setup_logger()
        self.validator = InputValidator()
        self.error_handler = ErrorHandler()
        self.console = Console()
        self.config_manager = ConfigManager()
        self.config = self.config_manager.load_config()
        
        self.theme_manager = ThemeManager()
        self.config_editor = ConfigEditor()
        self.menu_customizer = MenuCustomizer()
    
    @handle_errors("List themes", show_user=True)
    def list_themes(self) -> None:
        """List available themes."""
        self.theme_manager.display_themes()
    
    @handle_errors("Set theme", show_user=True)
    def set_theme(self, theme_name: str) -> bool:
        """Set current theme."""
        if self.theme_manager.set_theme(theme_name):
            self.console.print(f"[green]Theme set to: {theme_name}[/green]")
            return True
        else:
            self.console.print(f"[red]Theme not found: {theme_name}[/red]")
            return False
    
    @handle_errors("Create custom theme", show_user=True)
    def create_theme(self, theme_name: str) -> bool:
        """Create a custom theme."""
        theme_data = {
            'name': theme_name,
            'description': 'Custom theme',
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
        }
        
        if self.theme_manager.create_custom_theme(theme_name, theme_data):
            self.console.print(f"[green]Custom theme created: {theme_name}[/green]")
            return True
        else:
            self.console.print(f"[red]Failed to create theme[/red]")
            return False
    
    @handle_errors("Edit config", show_user=True)
    def edit_config(self) -> None:
        """Edit configuration."""
        self.config_editor.display_current_config()
    
    @handle_errors("Reset config", show_user=True)
    def reset_config(self) -> bool:
        """Reset configuration to defaults."""
        if self.config_editor.reset_to_defaults():
            self.console.print("[green]Configuration reset to defaults[/green]")
            return True
        else:
            self.console.print("[red]Failed to reset configuration[/red]")
            return False
    
    @handle_errors("Edit menu", show_user=True)
    def edit_menu(self) -> None:
        """Edit menu structure."""
        self.menu_customizer.display_menu_structure()
    
    @handle_errors("Rename category", show_user=True)
    def rename_category(self, category_key: str, new_name: str) -> bool:
        """Rename a menu category."""
        if self.menu_customizer.rename_category(category_key, new_name):
            self.console.print(f"[green]Category renamed: {category_key} -> {new_name}[/green]")
            return True
        else:
            self.console.print(f"[red]Failed to rename category[/red]")
            return False
    
    @handle_errors("Hide category", show_user=True)
    def hide_category(self, category_key: str) -> bool:
        """Hide a menu category."""
        if self.menu_customizer.hide_category(category_key):
            self.console.print(f"[green]Category hidden: {category_key}[/green]")
            return True
        else:
            self.console.print(f"[red]Failed to hide category[/red]")
            return False
    
    @handle_errors("Show category", show_user=True)
    def show_category(self, category_key: str) -> bool:
        """Show a hidden category."""
        if self.menu_customizer.show_category(category_key):
            self.console.print(f"[green]Category shown: {category_key}[/green]")
            return True
        else:
            self.console.print(f"[red]Failed to show category[/red]")
            return False
    
    @handle_errors("Reset menu", show_user=True)
    def reset_menu(self) -> bool:
        """Reset menu to default."""
        if self.menu_customizer.reset_menu():
            self.console.print("[green]Menu reset to default[/green]")
            return True
        else:
            self.console.print("[red]Failed to reset menu[/red]")
            return False
    
    def main(self) -> None:
        """Main entry point for customization tools."""
        tools = [
            {
                'name': 'List Themes',
                'description': 'Show available themes',
                'function': self.run_list_themes
            },
            {
                'name': 'Set Theme',
                'description': 'Change current theme',
                'function': self.run_set_theme
            },
            {
                'name': 'Create Theme',
                'description': 'Create custom theme',
                'function': self.run_create_theme
            },
            {
                'name': 'Edit Config',
                'description': 'View current configuration',
                'function': self.run_edit_config
            },
            {
                'name': 'Reset Config',
                'description': 'Reset to default settings',
                'function': self.run_reset_config
            },
            {
                'name': 'Edit Menu',
                'description': 'View menu structure',
                'function': self.run_edit_menu
            },
            {
                'name': 'Rename Category',
                'description': 'Rename menu category',
                'function': self.run_rename_category
            },
            {
                'name': 'Hide Category',
                'description': 'Hide menu category',
                'function': self.run_hide_category
            },
            {
                'name': 'Show Category',
                'description': 'Show hidden category',
                'function': self.run_show_category
            },
            {
                'name': 'Reset Menu',
                'description': 'Reset menu to default',
                'function': self.run_reset_menu
            }
        ]
        
        while True:
            from modules.ui.dashboard import Dashboard
            dashboard = Dashboard(self.config)
            choice = dashboard.display_module_menu("Customization", tools)
            
            if choice is None:
                break
            
            try:
                choice['function']()
            except Exception as e:
                self.error_handler.handle_exception(e, choice['name'])
                self.console.print(f"[red]Error: {e}[/red]")
            
            input("\nPress Enter to continue...")
    
    def run_list_themes(self) -> None:
        """Run list themes."""
        self.console.print("\n[bold cyan]Available Themes[/bold cyan]")
        self.list_themes()
    
    def run_set_theme(self) -> None:
        """Run set theme."""
        self.console.print("\n[bold cyan]Set Theme[/bold cyan]")
        self.list_themes()
        theme_name = input("Enter theme name: ").strip()
        if theme_name:
            self.set_theme(theme_name)
    
    def run_create_theme(self) -> None:
        """Run create theme."""
        self.console.print("\n[bold cyan]Create Custom Theme[/bold cyan]")
        theme_name = input("Enter theme name: ").strip()
        if theme_name:
            self.create_theme(theme_name)
    
    def run_edit_config(self) -> None:
        """Run edit config."""
        self.console.print("\n[bold cyan]Current Configuration[/bold cyan]")
        self.edit_config()
    
    def run_reset_config(self) -> None:
        """Run reset config."""
        self.console.print("\n[bold cyan]Reset Configuration[/bold cyan]")
        confirm = input("Reset to defaults? (yes/no): ").strip().lower()
        if confirm == 'yes':
            self.reset_config()
    
    def run_edit_menu(self) -> None:
        """Run edit menu."""
        self.console.print("\n[bold cyan]Menu Structure[/bold cyan]")
        self.edit_menu()
    
    def run_rename_category(self) -> None:
        """Run rename category."""
        self.console.print("\n[bold cyan]Rename Category[/bold cyan]")
        self.menu_customizer.display_menu_structure()
        category_key = input("Enter category key: ").strip()
        new_name = input("Enter new name: ").strip()
        if category_key and new_name:
            self.rename_category(category_key, new_name)
    
    def run_hide_category(self) -> None:
        """Run hide category."""
        self.console.print("\n[bold cyan]Hide Category[/bold cyan]")
        self.menu_customizer.display_menu_structure()
        category_key = input("Enter category key to hide: ").strip()
        if category_key:
            self.hide_category(category_key)
    
    def run_show_category(self) -> None:
        """Run show category."""
        self.console.print("\n[bold cyan]Show Category[/bold cyan]")
        category_key = input("Enter category key to show: ").strip()
        if category_key:
            self.show_category(category_key)
    
    def run_reset_menu(self) -> None:
        """Run reset menu."""
        self.console.print("\n[bold cyan]Reset Menu[/bold cyan]")
        confirm = input("Reset menu to default? (yes/no): ").strip().lower()
        if confirm == 'yes':
            self.reset_menu()


def main():
    """Entry point for customization tools."""
    tools = CustomizationTools()
    tools.main()


if __name__ == "__main__":
    main()