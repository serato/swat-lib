import logging
from abc import abstractmethod, ABCMeta
from pprint import pformat
from textwrap import wrap

from utilities.operatingsystem import screenshot
from framework.slack_integration import SlackWebhookException


"""
Logging utilities ported over from at-core (with a bit of tidy up).

Why carry this over?

- It allows us to take screenshots when we log test events
- It allows us to send Slack messages when errors occur
- It's a good place to put formatting code, especially if that code is meant to be parsed by a Jenkins parser

"""


class BaseLog(object):
    """
    Abstract class to make sure our loggers implement the expected methods for each logging level.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def debug(self, message):
        pass

    @abstractmethod
    def info(self, message):
        pass

    @abstractmethod
    def warning(self, message):
        pass

    @abstractmethod
    def error(self, message):
        pass


class Log(BaseLog):
    """
    TODO This is very repetitive and could be simplified using a meta class.

    E.g. Something similar to this (but in Python):
    https://github.com/justinkames/vuejs-logger/blob/master/src/vue-logger/vue-logger.ts
    """

    def __init__(self, logger_name='', slack_integration=None, formatter=None, level=logging.DEBUG):
        logging.basicConfig()  # We get an error if we use the logger without configuring it
        self.logger = logging.getLogger(logger_name)
        self.slack = slack_integration
        self.format = formatter or LogFormat()
        self.level = level

    @property
    def level(self):
        return self.logger.getEffectiveLevel()

    @level.setter
    def level(self, level):
        """
        :param level: Level as a string (upper or lowercase - e.g. 'debug') or int
        We'll let the logger handle validation.
        """
        if isinstance(level, str):
            self.logger.setLevel(level.upper())
        else:
            self.logger.setLevel(level)

    def debug(self, message, take_screenshot=False, slack_recipients=None):
        self.log(message, 'debug', take_screenshot, slack_recipients)

    def warning(self, message, take_screenshot=False, slack_recipients=None):
        self.log(message, 'warning', take_screenshot, slack_recipients)

    def info(self, message, take_screenshot=False, slack_recipients=None):
        self.log(message, 'info', take_screenshot, slack_recipients)

    def error(self, message, take_screenshot=False, slack_recipients=None):
        self.log(message, 'error', take_screenshot, slack_recipients)

    def log(self, message, level, take_screenshot, slack_recipients):
        """
        :param message:
        Error message string.

        :param take_screenshot:
        Specify whether to take a screenshot of not.

        :param slack_recipients:
        A list of users or channels (requires preceding @ or # respectively) to send the error message to.

        :param level:
        Logging level (e.g. 'error')

        Note: This won't work for posting to private channels.
        """
        getattr(self.logger, level)(message)

        if take_screenshot:
            screenshot.capture(message)

        # Send Slack message to each recipient (channel or user) if a Slack integration is set up
        if self.slack and slack_recipients:
            for recipient in slack_recipients:
                try:
                    self.slack.post_to_slack(recipient=recipient, message=message)
                except SlackWebhookException as e:
                    self.error(e.message)  # Recursive, but since slack_recipients is None we won't get an infinite loop


class LogFormat(object):
    """
    Formatter for log messages (e.g. with special formatting that can be parsed by a specific parser on Jenkins)
    """
    LINE_LENGTH = 79

    @staticmethod
    def info_separator(message):
        """
        *******************************************************************************
        ** Returns a message formatted like this                                     **
        *******************************************************************************
        """
        line_len = LogFormat.LINE_LENGTH - 6
        lines = ['*' * LogFormat.LINE_LENGTH] * 2
        lines[1:-1] = ['** %s **' % line.ljust(line_len) for line in wrap(message, line_len)]
        return MultilineMessage(*lines)

    @staticmethod
    def format_response(response):
        """
        Pretty-print a response (standard requests library)

        Adapted from spec/deprecated/WEB/API/common/request_debugger.py
        """
        try:
            body = pformat(response.json())
        except ValueError:
            body = 'None'  # Stop errors for requests without a json response

        return MultilineMessage(
            '',
            '======================================================================================================',
            '====================================== DEBUG SERVER RESPONSE =========================================',
            '======================================================================================================',
            'Status code: %d' % response.status_code,
            '\n'.join('{}: {}'.format(k, v) for k, v in response.headers.items()),
            'Body:',
            body,
            '======================================================================================================',
            '',
            ''
        )

    @staticmethod
    def format_request(request):
        """
        Pretty-print a request (standard requests library)

        Adapted from spec/deprecated/WEB/API/common/request_debugger.py
        """
        if request.method.lower() == 'post' and request.body:
            body = request.body
        else:
            body = 'None'

        return MultilineMessage(
            '',
            '======================================================================================================',
            '====================================== DEBUG ORIGINAL REQUEST ========================================',
            '======================================================================================================',
            request.method + ' ' + request.url,
            '\n'.join('{}: {}'.format(k, v) for k, v in request.headers.items()),
            'Body:',
            body,
            '======================================================================================================',
            '',
            ''
        )


class MultilineMessage(object):
    """
    Convenience class for formatting multiline log messages
    """
    def __init__(self, *args):
        self.lines = list(args) or []

    def __str__(self):
        return '\n' + '\n'.join(self.lines)

    def add_line(self, line=''):
        self.lines.append(line)


def _set_error_flag(error_flag):
    """
    This (and the screenshots) are the last vestigial dependencies on at-core in this module, and remains because
    'summary' is used by vruntest.py, which we still use to run our tests for consistency with the rest of AT.
    """
    import importlib
    # We need to distinguish between base.py in the parent module, and the base module in at-core
    summary = importlib.import_module('at-core.base.summary')  # Hyphens in a module name are a Python no-no
    if error_flag:
        if error_flag not in summary.get_summary():
            summary.add_error(error_flag)
