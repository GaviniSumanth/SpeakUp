"""SpeakUp logger module."""

import importlib.resources as pkg_resources
import logging
import os
import sys
from abc import ABC, abstractmethod
from logging import getLogger

import colorlog
from omegaconf import OmegaConf


class ABCLogger(ABC):
    """Logger abstract class."""

    @abstractmethod
    def __init__(self: "ABCLogger", logger_name: str) -> None:
        """Initialize the logger.

        Args:
            logger_name (str): Logger name.
        """

    @abstractmethod
    def get_logger(self: "ABCLogger") -> logging.Logger:
        """Get the logger instance."""

    @abstractmethod
    def set_level(self: "ABCLogger", level: str) -> None:
        """Set the logger level.

        Args:
            level (str): Logger level.
        """

    @abstractmethod
    def get_level(self: "ABCLogger") -> str:
        """Get the logger level."""


class FileLogger(ABCLogger):
    """FileLogger class to log messages to a file.

    Attributes:
        cfg_path (str): Configuration file path.
        cfg (DictConfig): Configuration dictionary.
    """

    cfg_path = pkg_resources.files("speakup").joinpath("conf/logging/log.yaml")
    cfg = OmegaConf.load(cfg_path)

    def __init__(self: "FileLogger", logger_name: str) -> None:
        """Initialize the FileLogger.

        Args:
            logger_name (str): Logger name.

        Raises:
            ValueError: If the logger with a file handler is not found in config.
        """
        logger_name = logger_name.title()
        handler_conf = self.cfg.handlers.file

        self.logger = getLogger(logger_name)

        if (
            logger_name in self.cfg.loggers
            and "file" in self.cfg.loggers[logger_name].handlers
        ):
            self.logger.setLevel(self.cfg.loggers[logger_name].level)
            if not any(
                isinstance(h, logging.FileHandler) for h in self.logger.handlers
            ):
                os.makedirs(os.path.dirname(handler_conf.filename), exist_ok=True)
                handler = logging.FileHandler(handler_conf.filename)
                handler.setFormatter(
                    colorlog.ColoredFormatter(
                        fmt=handler_conf.formatter.fmt,
                        datefmt=handler_conf.formatter.datefmt,
                    )
                )
                self.logger.addHandler(handler)
        else:
            raise ValueError(
                f"Logger '{logger_name}' with a file handler not found in config."
            )

    def get_logger(self: "FileLogger") -> logging.Logger:
        """Get the logger instance.

        Returns:
            logging.Logger: Logger instance.
        """
        return self.logger

    def set_level(self: "FileLogger", level: str) -> None:
        """Set the logger level.

        Args:
            level (str): Logger level.
        """
        self.logger.setLevel(level)

    def get_level(self: "FileLogger") -> str:
        """Get the logger level.

        Returns:
            str: Logger level.
        """
        return self.logger.getEffectiveLevel()


class ConsoleLogger(ABCLogger):
    """ConsoleLogger class to log messages to stdout.

    Attributes:
        cfg_path (str): Configuration file path.
        cfg (DictConfig): Configuration dictionary.

    Raises:
        ValueError: If the logger with a console handler is not found in config.
    """

    cfg_path = pkg_resources.files("speakup").joinpath("conf/logging/log.yaml")
    cfg = OmegaConf.load(cfg_path)

    def __init__(self: "ConsoleLogger", logger_name: str) -> None:
        """Initialize the ConsoleLogger.

        Args:
            logger_name (str): Logger name.

        Raises:
            ValueError: If the logger with a console handler is not found in config
        """
        logger_name = logger_name.title()
        handler_conf = self.cfg.handlers.console

        self.logger = getLogger(logger_name)

        if (
            logger_name in self.cfg.loggers
            and "console" in self.cfg.loggers[logger_name].handlers
        ):
            self.logger.setLevel(self.cfg.loggers[logger_name].level)
            if not any(
                isinstance(h, colorlog.StreamHandler) for h in self.logger.handlers
            ):
                handler = colorlog.StreamHandler(stream=sys.stdout)
                handler.setFormatter(
                    colorlog.ColoredFormatter(
                        fmt=handler_conf.formatter.fmt,
                        datefmt=handler_conf.formatter.datefmt,
                    )
                )
                self.logger.addHandler(handler)
        else:
            raise ValueError(
                f"Logger '{logger_name}' with a console handler not found in config."
            )

    def get_logger(self: "ConsoleLogger") -> logging.Logger:
        """Get the logger instance.

        Returns:
            logging.Logger: Logger instance.
        """
        return self.logger

    def set_level(self: "FileLogger", level: str) -> None:
        """Set the logger level.

        Args:
            level (str): Logger level.
        """
        self.logger.setLevel(level)

    def get_level(self: "FileLogger") -> str:
        """Get the logger level.

        Returns:
            str: Logger level.
        """
        return self.logger.getEffectiveLevel()


class MultiLogger:
    """MultiLogger class to log messages to multiple handlers.

    Attributes:
        cfg_path (str): Configuration file path.
        cfg (DictConfig): Configuration dictionary.

    Raises:
        ValueError: If the logger is not found in the configuration.
    """

    cfg_path = pkg_resources.files("speakup").joinpath("conf/logging/log.yaml")
    cfg = OmegaConf.load(cfg_path)

    def __init__(self: "MultiLogger", logger_name: str) -> None:
        """Initialize the MultiLogger.

        Args:
            logger_name (str): Logger name.

        Raises:
            ValueError: If the logger is not found in the configuration.
        """
        self.logger_name = logger_name.title()
        self.logger = logging.getLogger(self.logger_name)

        if self.logger_name in self.cfg.loggers:
            handler_list = self.cfg.loggers[self.logger_name].handlers
            if "console" in handler_list and not any(
                isinstance(h, colorlog.StreamHandler) for h in self.logger.handlers
            ):
                console_logger = ConsoleLogger(self.logger_name).get_logger()
                self.logger.addHandler(console_logger.handlers[0])
            if "file" in handler_list and not any(
                isinstance(h, logging.FileHandler) for h in self.logger.handlers
            ):
                file_logger = FileLogger(self.logger_name).get_logger()
                self.logger.addHandler(file_logger.handlers[0])
        else:
            raise ValueError(
                f"Logger '{self.logger_name}' not found in the configuration."
            )

    def get_logger(self: "MultiLogger") -> logging.Logger:
        """Get the logger instance.

        Returns:
            logging.Logger: Logger instance.
        """
        return self.logger

    def log(self: "MultiLogger", level: str, message: str) -> None:
        """Log a message with the given level.

        Args:
            level (str): Log level (info, debug, warning, error, critical).
            message (str): Message to log.
        """
        getattr(self.logger, level)(message)

    def set_level(self: "MultiLogger", level: str) -> None:
        """Set the logger level.

        Args:
            level (str): Logger level.
        """
        self.logger.setLevel(level)

    def get_level(self: "MultiLogger") -> str:
        """Get the logger level.

        Returns:
            str: Logger level.
        """
        return self.logger.getEffectiveLevel()

    def info(self: "MultiLogger", message: str) -> None:
        """Log an info message.

        Args:
            message (str): Message to log.
        """
        self.log("info", message)

    def debug(self: "MultiLogger", message: str) -> None:
        """Log a debug message.

        Args:
            message (str): Message to log.
        """
        self.log("debug", message)

    def warning(self: "MultiLogger", message: str) -> None:
        """Log a warning message.

        Args:
            message (str): Message to log.
        """
        self.log("warning", message)

    def error(self: "MultiLogger", message: str) -> None:
        """Log an error message.

        Args:
            message (str): Message to log.
        """
        self.log("error", message)

    def critical(self: "MultiLogger", message: str) -> None:
        """Log a critical message.

        Args:
            message (str): Message to log.
        """
        self.log("critical", message)
