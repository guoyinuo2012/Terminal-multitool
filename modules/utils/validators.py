"""
Input validation utilities for Terminal Multi Tool application
"""

import re
import ipaddress
from typing import Optional, List
from modules.utils.logger import setup_logger


class InputValidator:
    """Validates user input across different modules."""
    
    def __init__(self):
        self.logger = setup_logger()
    
    def validate_email(self, email: str) -> bool:
        """
        Validate email address format.
        
        Args:
            email: Email address to validate
            
        Returns:
            True if valid, False otherwise
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(pattern, email):
            return True
        self.logger.warning(f"Invalid email format: {email}")
        return False
    
    def validate_ip_address(self, ip: str) -> bool:
        """
        Validate IP address (IPv4 or IPv6).
        
        Args:
            ip: IP address to validate
            
        Returns:
            True if valid, False otherwise
        """
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            self.logger.warning(f"Invalid IP address: {ip}")
            return False
    
    def validate_domain(self, domain: str) -> bool:
        """
        Validate domain name format.
        
        Args:
            domain: Domain name to validate
            
        Returns:
            True if valid, False otherwise
        """
        pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*\.[a-zA-Z]{2,}$'
        if re.match(pattern, domain):
            return True
        self.logger.warning(f"Invalid domain format: {domain}")
        return False
    
    def validate_url(self, url: str) -> bool:
        """
        Validate URL format.
        
        Args:
            url: URL to validate
            
        Returns:
            True if valid, False otherwise
        """
        pattern = r'^https?://[^\s/$.?#].[^\s]*$'
        if re.match(pattern, url):
            return True
        self.logger.warning(f"Invalid URL format: {url}")
        return False
    
    def validate_username(self, username: str) -> bool:
        """
        Validate username format (alphanumeric, underscores, hyphens).
        
        Args:
            username: Username to validate
            
        Returns:
            True if valid, False otherwise
        """
        pattern = r'^[a-zA-Z0-9_-]{3,32}$'
        if re.match(pattern, username):
            return True
        self.logger.warning(f"Invalid username format: {username}")
        return False
    
    def validate_port(self, port: str) -> bool:
        """
        Validate port number (1-65535).
        
        Args:
            port: Port number to validate
            
        Returns:
            True if valid, False otherwise
        """
        try:
            port_num = int(port)
            if 1 <= port_num <= 65535:
                return True
            self.logger.warning(f"Port out of range: {port}")
            return False
        except ValueError:
            self.logger.warning(f"Invalid port number: {port}")
            return False
    
    def sanitize_input(self, input_str: str) -> str:
        """
        Sanitize user input to prevent injection attacks.
        
        Args:
            input_str: Input string to sanitize
            
        Returns:
            Sanitized string
        """
        # Remove potentially dangerous characters
        sanitized = re.sub(r'[<>"\'\0]', '', input_str)
        # Limit length
        sanitized = sanitized[:1000]
        return sanitized.strip()
    
    def validate_discord_id(self, discord_id: str) -> bool:
        """
        Validate Discord user/snowflake ID format.
        
        Args:
            discord_id: Discord ID to validate
            
        Returns:
            True if valid, False otherwise
        """
        pattern = r'^\d{17,20}$'
        if re.match(pattern, discord_id):
            return True
        self.logger.warning(f"Invalid Discord ID format: {discord_id}")
        return False