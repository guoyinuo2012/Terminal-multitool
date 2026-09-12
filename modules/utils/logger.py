"""
Logging configuration for Void application
"""

import logging
import os
from pathlib import Path
from datetime import datetime
import colorlog


def setup_logger(name: str = "void", level: int = logging.INFO) -> logging.Logger:
    """
    Setup and configure logger with file and console handlers.
    
    Args:
        name: Logger name
        level: Logging level
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Prevent duplicate handlers
    if logger.handlers:
        return logger
    
    # Create logs directory if it doesn't exist
    logs_dir = Path(__file__).parent.parent.parent / "logs"
    logs_dir.mkdir(exist_ok=True)
    
    # File handler with timestamp
    log_file = logs_dir / f"void_{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(level)
    
    # Console handler with colors
    console_handler = colorlog.StreamHandler()
    console_handler.setLevel(level)
    
    # Formatters
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    console_formatter = colorlog.ColoredFormatter(
        '%(log_color)s%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        }
    )
    
    file_handler.setFormatter(file_formatter)
    console_handler.setFormatter(console_formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger