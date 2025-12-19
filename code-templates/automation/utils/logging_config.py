"""
Logging configuration for conversion uploads
"""

import logging
import os
from datetime import datetime


def setup_logging(log_level=logging.INFO):
    """
    Configure logging to file and console
    
    Args:
        log_level: Logging level (default: INFO)
    
    Returns:
        Configured logger instance
    """
    # Create logs directory if it doesn't exist
    log_dir = os.path.join(os.path.dirname(__file__), '../../../logs')
    os.makedirs(log_dir, exist_ok=True)
    
    # Log file with date
    log_file = os.path.join(log_dir, f'conversions_{datetime.now().strftime("%Y%m%d")}.log')
    
    # Configure logging format
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    
    # Configure root logger
    logger = logging.getLogger('conversion_upload')
    logger.setLevel(log_level)
    
    # Remove existing handlers to avoid duplicates
    logger.handlers = []
    
    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    logger.info(f"Logging initialized. Log file: {log_file}")
    
    return logger


if __name__ == "__main__":
    # Test logging configuration
    logger = setup_logging()
    
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    
    print("\nCheck the logs/ directory for output file")
