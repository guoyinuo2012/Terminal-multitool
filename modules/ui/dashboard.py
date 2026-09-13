"""
Main Rich TUI Dashboard for Terminal Multi Tool application
Created by Yinuo
"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align
from typing import Dict, Any, Optional
import sys

from modules.utils.logger import setup_logger
from modules.utils.error_handler import ErrorHandler
from modules.customization.theme_manager import ThemeManager
from modules.customization.menu_customizer import MenuCustomizer


class Dashboard:
    """Main TUI dashboard for navigation and tool selection."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the dashboard."""
        self.config = config
        self.console = Console()
        self.logger = setup_logger()
        self.error_handler = ErrorHandler()
        self.running = True
        
        # Initialize customization managers
        self.theme_manager = ThemeManager()
        self.menu_customizer = MenuCustomizer()
        
        # Load custom menu or use default
        self.categories = self.menu_customizer.get_custom_menu()
    
    def run(self) -> None:
        """Run the main dashboard loop."""
        try:
            while self.running:
                self.display_main_menu()
                choice = self.get_user_choice()
                self.handle_choice(choice)
        except KeyboardInterrupt:
            self.logger.info("Dashboard interrupted by user")
            print("\n[!] Thank you for using Terminal Multi Tool!")
            print("Created by Yinuo")
            sys.exit(0)
        except Exception as e:
            self.error_handler.handle_exception(e, "Dashboard")
            print(f"\n[!] Fatal error: {e}")
            sys.exit(1)
    
    def display_main_menu(self) -> None:
        """Display the main menu dashboard."""
        self.console.clear()
        
        # Simple header (using static colors for now to avoid theme errors)
        self.console.print("[bold cyan]Terminal Multi Tool - Terminal-Based Multitool[/bold cyan]")
        self.console.print("[bold green]Created by Yinuo[/bold green]\n")
        
        # Simple table
        table = Table(show_header=False)
        table.add_column("Opt", style="cyan", width=4)
        table.add_column("Tool", style="green", width=15)
        table.add_column("Description", style="white")
        
        # Display only non-hidden categories
        for key, cat in self.categories.items():
            if not cat.get('hidden', False):
                table.add_row(key, cat['name'], cat['desc'])
        
        self.console.print(table)
        self.console.print("\n[yellow]DISCLAIMER: Education & authorized research only[/yellow]")
        self.console.print("[bold cyan]Choice:[/bold cyan] ", end="")
    
    def get_user_choice(self) -> str:
        """
        Get and validate user choice.
        
        Returns:
            Validated user choice
        """
        try:
            choice = input().strip()
            if choice in self.categories:
                return choice
            else:
                self.console.print("[red]Invalid choice. Please try again.[/red]")
                return self.get_user_choice()
        except (EOFError, KeyboardInterrupt):
            self.running = False
            return '0'
    
    def handle_choice(self, choice: str) -> None:
        """
        Handle user menu choice.
        
        Args:
            choice: User's menu selection
        """
        if choice == '0':
            self.running = False
            self.console.print("\n[bold green]Thank you for using Terminal Multi Tool![/bold green]")
            self.console.print("[bold cyan]Created by Yinuo[/bold cyan]")
            return
        
        category = self.categories[choice]
        self.logger.info(f"User selected category: {category['name']}")
        
        # Import and run the selected module
        try:
            if category['module']:
                self.load_and_run_module(category['module'], category['name'])
            else:
                self.console.print("[red]Module not yet implemented[/red]")
                input("\nPress Enter to continue...")
        except ImportError:
            self.console.print(f"[yellow]Module {category['name']} not yet implemented[/yellow]")
            input("\nPress Enter to continue...")
        except Exception as e:
            self.error_handler.handle_exception(e, f"Loading {category['name']}")
            self.console.print(f"[red]Error loading module: {e}[/red]")
            input("\nPress Enter to continue...")
    
    def load_and_run_module(self, module_path: str, module_name: str) -> None:
        """Load and run a module."""
        try:
            parts = module_path.split('.')
            module = __import__(module_path)
            for part in parts[1:]:
                module = getattr(module, part)
            
            if hasattr(module, 'main') and callable(module.main):
                module.main()
            else:
                self.console.print(f"[red]No entry point found[/red]")
                input()
                
        except Exception as e:
            self.error_handler.handle_exception(e, module_name)
            self.console.print(f"[red]Error: {e}[/red]")
            input()
    
    def display_module_menu(self, module_name: str, tools: list) -> Optional[str]:
        """Display a menu for a specific module's tools."""
        self.console.clear()
        self.console.print(f"[bold cyan]{module_name}[/bold cyan]\n")
        
        table = Table(show_header=False)
        table.add_column("Opt", style="cyan", width=4)
        table.add_column("Tool", style="green", width=25)
        table.add_column("Description", style="white")
        
        for i, tool in enumerate(tools, 1):
            table.add_row(str(i), tool['name'], tool['description'])
        
        table.add_row("0", "Back", "Return to main menu")
        
        self.console.print(table)
        self.console.print("[bold cyan]Choice:[/bold cyan] ", end="")
        
        try:
            choice = input().strip()
            if choice == '0':
                return None
            elif choice.isdigit() and 1 <= int(choice) <= len(tools):
                return tools[int(choice) - 1]
            else:
                self.console.print("[red]Invalid choice[/red]")
                return self.display_module_menu(module_name, tools)
        except (EOFError, KeyboardInterrupt):
            return None