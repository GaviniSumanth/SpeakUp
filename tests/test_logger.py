"""Test cases for logger module."""

import logging
from io import StringIO
from typing import Any, Generator

import pytest

from speakup.loggers import ConsoleLogger, FileLogger, MultiLogger

__author__ = "GaviniSumanth"
__copyright__ = "GaviniSumanth"
__license__ = "MIT"


class TestLogger:
    """Test Logger class.

    Attributes:
        invalid_logger_name (str): Invalid logger name.
    """

    invalid_logger_name = "TEST_INVALID_LOGGER"

    def change_log_level(
        self: "TestLogger",
        logger: ConsoleLogger | FileLogger | MultiLogger,
    ) -> None:
        """Test change log level.

        Args:
            logger: Logger object.
        """
        assert logger.get_level() == logging.INFO
        logger.set_level(logging.DEBUG)
        assert logger.get_level() == logging.DEBUG
        logger.set_level(logging.INFO)
        assert logger.get_level() == logging.INFO

    def test_console_logger(self: "TestLogger") -> None:
        """Test ConsoleLogger class.

        This test verifies that the ConsoleLogger can change its log level.
        """
        logger = ConsoleLogger("Main")
        self.change_log_level(logger)

    def test_file_logger(self: "TestLogger") -> None:
        """Test FileLogger class.

        This test verifies that the FileLogger can change its log level.
        """
        logger = FileLogger("Main")
        self.change_log_level(logger)

    def test_multi_logger(self: "TestLogger") -> None:
        """Test MultiLogger class.

        This test verifies that the MultiLogger can change its log level.
        """
        logger = MultiLogger("Main")
        self.change_log_level(logger)

    def test_invalid_logger_name_console_logger(self: "TestLogger") -> None:
        """Test invalid logger name for ConsoleLogger.

        This test verifies that creating a ConsoleLogger
        with an invalid name raises a ValueError.
        """
        with pytest.raises(ValueError):
            ConsoleLogger(self.invalid_logger_name)

    def test_invalid_logger_name_file_logger(self: "TestLogger") -> None:
        """Test invalid logger name for FileLogger.

        This test verifies that creating a FileLogger
        with an invalid name raises a ValueError.
        """
        with pytest.raises(ValueError):
            FileLogger(self.invalid_logger_name)

    def test_invalid_logger_name_multi_logger(self: "TestLogger") -> None:
        """Test invalid logger name for MultiLogger.

        This test verifies that creating a MultiLogger
        with an invalid name raises a ValueError.
        """
        with pytest.raises(ValueError):
            MultiLogger(self.invalid_logger_name)

    @pytest.fixture
    def log_capture(self: "TestLogger") -> Generator[Any, Any, Any]:
        """Capture log output in a StringIO stream."""
        log_stream = StringIO()
        handler = logging.StreamHandler(log_stream)
        logger = logging.getLogger("Main")
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        yield log_stream
        logger.removeHandler(handler)

    def check_double_logging(
        self: "TestLogger", logger: ConsoleLogger | FileLogger | MultiLogger
    ) -> None:
        """Log the same message four times using the provided logger.

        Args:
            logger: The logger instance to use for logging messages.
        """
        for _ in range(4):
            logger_instance = logger.get_logger()
            logger_instance.info("Test Log")

    def test_check_double_logging_console_logger(
        self: "TestLogger", log_capture: StringIO
    ) -> None:
        """
        Test to check for double logging in ConsoleLogger.

        Uses the ConsoleLogger to log the same message four times
        and verifies that the log output.
        contains exactly four instances of the message.

        Args:
            log_capture: The fixture to capture log output.
        """
        self.check_double_logging(ConsoleLogger("Main"))

        log_capture.flush()
        log_output = log_capture.getvalue()

        expected_log = "Test Log\n" * 4
        assert log_output == expected_log

    def test_check_double_logging_file_logger(
        self: "TestLogger", log_capture: StringIO
    ) -> None:
        """
        Test to check for double logging in FileLogger.

        Uses the FileLogger to log the same message four times
        and verifies that the log output.
        contains exactly four instances of the message.

        Args:
            log_capture: The fixture to capture log output.
        """
        self.check_double_logging(FileLogger("Main"))

        log_capture.flush()
        log_output = log_capture.getvalue()

        expected_log = "Test Log\n" * 4
        assert log_output == expected_log

    def test_check_double_logging_multi_logger(
        self: "TestLogger", log_capture: StringIO
    ) -> None:
        """
        Test to check for double logging in MultiLogger.

        Uses the MultiLogger to log the same message four times
        and verifies that the log output.
        contains exactly four instances of the message.

        Args:
            log_capture: The fixture to capture log output.
        """
        self.check_double_logging(MultiLogger("Main"))

        log_capture.flush()
        log_output = log_capture.getvalue()

        expected_log = "Test Log\n" * 4
        assert log_output == expected_log
