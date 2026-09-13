"""
Error handling utilities for Terminal Multi Tool application
"""

import sys
import traceback
from typing import Optional, Callable, Any
from functools import wraps
from modules.utils.logger import setup_logger


class ErrorHandler:
    """Centralized error handling for the application."""
    
    def __init__(self):
        self.logger = setup_logger()
    
    def handle_exception(self, exc: Exception, context: str = "") -> None:
        """
        Handle and log exceptions.
        
        Args:
            exc: Exception to handle
            context: Additional context about where error occurred
        """
        error_msg = f"{context}: {str(exc)}" if context else str(exc)
        self.logger.error(error_msg)
        
        if self.logger.level >= 10:  # DEBUG level
            self.logger.debug(traceback.format_exc())
    
    def handle_network_error(self, exc: Exception, url: str = "") -> None:
        """
        Handle network-related errors.
        
        Args:
            exc: Network exception
            url: URL that was being accessed
        """
        context = f"Network error accessing {url}" if url else "Network error"
        self.handle_exception(exc, context)
    
    def handle_api_error(self, status_code: int, response: str = "") -> None:
        """
        Handle API errors.
        
        Args:
            status_code: HTTP status code
            response: Response body
        """
        self.logger.error(f"API error - Status: {status_code}, Response: {response[:200]}")
    
    def handle_validation_error(self, field: str, value: Any) -> None:
        """
        Handle validation errors.
        
        Args:
            field: Field that failed validation
            value: Invalid value
        """
        self.logger.warning(f"Validation failed for field '{field}': {value}")


def handle_errors(context: str = "", show_user: bool = False):
    """
    Decorator for handling errors in functions.
    
    Args:
        context: Context description for error logging
        show_user: Whether to show error to user
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            error_handler = ErrorHandler()
            try:
                return func(*args, **kwargs)
            except KeyboardInterrupt:
                print("\n[!] Operation cancelled by user")
                sys.exit(0)
            except Exception as e:
                error_handler.handle_exception(e, context or func.__name__)
                if show_user:
                    print(f"\n[!] Error: {e}")
                return None
        return wrapper
    return decorator


def safe_execute(func: Callable, default: Any = None, context: str = "") -> Any:
    """
    Safely execute a function with error handling.
    
    Args:
        func: Function to execute
        default: Default value to return on error
        context: Context for error logging
        
    Returns:
        Function result or default value on error
    """
    error_handler = ErrorHandler()
    try:
        return func()
    except Exception as e:
        error_handler.handle_exception(e, context)
        return default