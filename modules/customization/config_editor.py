"""
Configuration Editor for Void Application
Created by Yinuo
"""

import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from modules.utils.logger import setup_logger
from modules.utils.config import ConfigManager


class ConfigEditor:
    """Edits application configuration."""
    
    def __init__(self):
        """Initialize config editor."""
        self.logger = setup_logger()
        self.config_manager = ConfigManager()
        self.config = self.config_manager.load_config()
        self.console = Console()
    
    def edit_app_setting(self, key: str, value: Any) -> bool:
        """Edit application setting."""
        try:
            if 'app' not in self.config:
                self.config['app'] = {}
            
            self.config['app'][key] = value
            self.config_manager.save_config(self.config)
            
            self.logger.info(f"App setting updated: {key} = {value}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error editing app setting: {e}")
            return False
    
    def edit_ui_setting(self, key: str, value: Any) -> bool:
        """Edit UI setting."""
        try:
            if 'ui' not in self.config:
                self.config['ui'] = {}
            
            self.config['ui'][key] = value
            self.config_manager.save_config(self.config)
            
            self.logger.info(f"UI setting updated: {key} = {value}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error editing UI setting: {e}")
            return False
    
    def edit_network_setting(self, key: str, value: Any) -> bool:
        """Edit network setting."""
        try:
            if 'network' not in self.config:
                self.config['network'] = {}
            
            self.config['network'][key] = value
            self.config_manager.save_config(self.config)
            
            self.logger.info(f"Network setting updated: {key} = {value}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error editing network setting: {e}")
            return False
    
    def add_custom_tool_config(self, tool_name: str, config: Dict[str, Any]) -> bool:
        """Add custom tool configuration."""
        try:
            if 'tools' not in self.config:
                self.config['tools'] = {}
            
            self.config['tools'][tool_name] = config
            self.config_manager.save_config(self.config)
            
            self.logger.info(f"Custom tool config added: {tool_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error adding tool config: {e}")
            return False
    
    def reset_to_defaults(self) -> bool:
        """Reset configuration to defaults."""
        try:
            self.config = self.config_manager.create_default_config()
            self.config_manager.save_config(self.config)
            
            self.logger.info("Configuration reset to defaults")
            return True
            
        except Exception as e:
            self.logger.error(f"Error resetting config: {e}")
            return False
    
    def display_current_config(self) -> None:
        """Display current configuration."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Section", style="cyan")
        table.add_column("Setting", style="green")
        table.add_column("Value", style="white")
        
        for section, settings in self.config.items():
            if isinstance(settings, dict):
                for key, value in settings.items():
                    table.add_row(section, key, str(value))
        
        self.console.print(Panel(table, title="[bold]Current Configuration[/bold]"))
    
    def export_config(self, export_path: str) -> bool:
        """Export configuration to file."""
        try:
            export_file = Path(export_path)
            export_file.parent.mkdir(exist_ok=True)
            
            with open(export_file, 'w') as f:
                yaml.dump(self.config, f, default_flow_style=False)
            
            self.logger.info(f"Configuration exported to: {export_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error exporting config: {e}")
            return False
    
    def import_config(self, import_path: str) -> bool:
        """Import configuration from file."""
        try:
            import_file = Path(import_path)
            
            if not import_file.exists():
                self.logger.error(f"Config file not found: {import_path}")
                return False
            
            with open(import_file, 'r') as f:
                imported_config = yaml.safe_load(f)
            
            self.config = imported_config
            self.config_manager.save_config(self.config)
            
            self.logger.info(f"Configuration imported from: {import_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error importing config: {e}")
            return False