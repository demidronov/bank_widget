"""Logging configuration for the project.

This module provides a centralized logging configuration that sets up
loggers for different modules with file handlers that write to the logs directory.
"""

import logging
import logging.handlers
from pathlib import Path


def setup_logger(module_name: str) -> logging.Logger:
    """Set up and return a logger for the specified module.

    Creates a logger that writes to a file in the logs directory with the format:
    timestamp - module_name - level - message

    The log file is recreated (truncated) on each application run.

    Args:
        module_name: Name of the module (e.g., '__name__' from the calling module)

    Returns:
        Configured logger instance
    """
    # Create logs directory if it doesn't exist
    logs_dir = Path(__file__).parent.parent / "logs"
    logs_dir.mkdir(exist_ok=True)

    # Get logger
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.DEBUG)

    # Only add handler if not already added (to avoid duplicate handlers)
    if not logger.handlers:
        # Extract the module name from the full path (e.g., 'src.masks' -> 'masks')
        short_module_name = module_name.split('.')[-1]
        
        # Create file handler (mode 'w' truncates file on each run)
        log_file = logs_dir / f"{short_module_name}.log"
        file_handler = logging.FileHandler(log_file, mode='w', encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)

        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)

        # Add handler to logger
        logger.addHandler(file_handler)

    return logger
