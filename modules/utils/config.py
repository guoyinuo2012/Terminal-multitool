"""
Configuration management for Terminal Multi Tool application
"""

import json
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from modules.utils.logger import setup_logger


class ConfigManager:
    """Manages application configuration files."""
    
    def __init__(self, config_dir: Optional[Path] = None):
        """
        Initialize ConfigManager.
        
        Args:
            config_dir: Custom config directory path
        """
        self.logger = setup_logger()
        self.config_dir = config_dir or Path(__file__).parent.parent.parent / "config"
        self.config_dir.mkdir(exist_ok=True)
        self.config_file = self.config_dir / "config.yaml"
        self.api_keys_file = self.config_dir / "api_keys.yaml"
        
    def load_config(self) -> Dict[str, Any]:
        """
        Load main configuration file.
        
        Returns:
            Configuration dictionary
        """
        if not self.config_file.exists():
            self.logger.info(f"Config file not found, creating default: {self.config_file}")
            return self.create_default_config()
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                self.logger.info("Configuration loaded successfully")
                return config or {}
        except Exception as e:
            self.logger.error(f"Error loading config: {e}")
            return self.create_default_config()
    
    def save_config(self, config: Dict[str, Any]) -> bool:
        """
        Save configuration to file.
        
        Args:
            config: Configuration dictionary to save
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                yaml.dump(config, f, default_flow_style=False, sort_keys=False)
            self.logger.info("Configuration saved successfully")
            return True
        except Exception as e:
            self.logger.error(f"Error saving config: {e}")
            return False
    
    def create_default_config(self) -> Dict[str, Any]:
        """
        Create default configuration.
        
        Returns:
            Default configuration dictionary
        """
        default_config = {
            'app': {
                'name': 'Terminal Multi Tool',
                'version': '1.0.0',
                'debug': False,
                'log_level': 'INFO'
            },
            'ui': {
                'theme': 'dark',
                'refresh_rate': 1.0,
                'max_history': 100
            },
            'network': {
                'timeout': 30,
                'max_retries': 3,
                'user_agent': 'TerminalMultiTool/1.0'
            },
            'discord': {
                'enabled': False,
                'command_prefix': '!'
            },
            'osint': {
                'cache_enabled': True,
                'cache_duration': 3600
            }
        }
        
        self.save_config(default_config)
        return default_config
    
    def load_api_keys(self) -> Dict[str, str]:
        """
        Load API keys from secure file.
        
        Returns:
            Dictionary of API keys
        """
        if not self.api_keys_file.exists():
            return {}
        
        try:
            with open(self.api_keys_file, 'r', encoding='utf-8') as f:
                keys = yaml.safe_load(f)
                return keys or {}
        except Exception as e:
            self.logger.error(f"Error loading API keys: {e}")
            return {}
    
    def save_api_key(self, service: str, api_key: str) -> bool:
        """
        Save an API key securely.
        
        Args:
            service: Service name (e.g., 'discord', 'virustotal')
            api_key: API key to save
            
        Returns:
            True if successful, False otherwise
        """
        try:
            keys = self.load_api_keys()
            keys[service] = api_key
            
            with open(self.api_keys_file, 'w', encoding='utf-8') as f:
                yaml.dump(keys, f, default_flow_style=False)
            
            self.logger.info(f"API key saved for service: {service}")
            return True
        except Exception as e:
            self.logger.error(f"Error saving API key: {e}")
            return False