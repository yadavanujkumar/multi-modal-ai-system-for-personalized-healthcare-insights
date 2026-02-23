# src/utils/logging.py

"""
Structured logging setup for observability with production-safe defaults for the Multi-Modal AI System.

This module provides a centralized logging configuration, ensuring consistent and informative log messages
across the application. It utilizes the `logging` module from the Python Standard Library, with additional
features for log formatting, level configuration, and error handling.

Classes:
    Logger: A custom logger class with advanced features for logging.

Functions:
    get_logger: Returns a logger instance with the specified name.
    configure_logging: Configures the logging system with production-safe defaults.

Variables:
    LOGGING_CONFIG: A dictionary containing the logging configuration.
"""

import logging
import logging.config
from typing import Dict

# Define the logging configuration
LOGGING_CONFIG: Dict = {
    "version": 1,
    "formatters": {
        "default": {
            "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "formatter": "default",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "app.log",
            "maxBytes": 1024 * 1024 * 10,  # 10 MB
            "backupCount": 5,
            "formatter": "default",
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["console", "file"],
    },
}

class Logger:
    """
    A custom logger class with advanced features for logging.

    Attributes:
        name (str): The name of the logger.
        logger (logging.Logger): The underlying logger instance.
    """

    def __init__(self, name: str):
        """
        Initializes a new logger instance.

        Args:
            name (str): The name of the logger.
        """
        self.name = name
        self.logger = logging.getLogger(name)

    def debug(self, message: str):
        """
        Logs a debug message.

        Args:
            message (str): The message to log.
        """
        self.logger.debug(message)

    def info(self, message: str):
        """
        Logs an info message.

        Args:
            message (str): The message to log.
        """
        self.logger.info(message)

    def warning(self, message: str):
        """
        Logs a warning message.

        Args:
            message (str): The message to log.
        """
        self.logger.warning(message)

    def error(self, message: str):
        """
        Logs an error message.

        Args:
            message (str): The message to log.
        """
        self.logger.error(message)

    def critical(self, message: str):
        """
        Logs a critical message.

        Args:
            message (str): The message to log.
        """
        self.logger.critical(message)

def get_logger(name: str) -> Logger:
    """
    Returns a logger instance with the specified name.

    Args:
        name (str): The name of the logger.

    Returns:
        Logger: A logger instance with the specified name.
    """
    return Logger(name)

def configure_logging():
    """
    Configures the logging system with production-safe defaults.
    """
    logging.config.dictConfig(LOGGING_CONFIG)

# Configure logging on module import
configure_logging()

# Example usage:
if __name__ == "__main__":
    logger = get_logger(__name__)
    logger.info("This is an info message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
    logger.critical("This is a critical message.")