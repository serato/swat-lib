import pytest

from framework.helpers import get_path_rel_to_parent, MissingSubPathException
from framework.log import MultilineMessage

"""
Plugin for logging a summary of test failures to Slack.
"""

max_failures = 3  # Only log the first few failures, so as not to spam the chat


@pytest.fixture(scope='session', autouse=True)
def add_slack_data(request, log, global_config, slack_recipients):
    request.session.slack_recipients = slack_recipients


def pytest_sessionfinish(session):
    """
    Send a summary of failures to the list of Slack recipients (specified using the --slack argument) if present
    """
    has_failures = hasattr(session, 'failures') and len(session.failures)
    has_slack_recipients = hasattr(session, 'slack_recipients') and session.slack_recipients

    # If some tests failed and we have people to notify
    if has_failures and has_slack_recipients:
        message = MultilineMessage()

        # Session summary
        session_name = session.name if hasattr(session, 'name') and session.name else 'Session'
        plural_failure = 's' if session.testsfailed > 1 else ''
        plural_tests = 's' if session.testscollected > 1 else ''
        summary_args = (session_name, session.testsfailed, plural_failure, session.testscollected, plural_tests)
        message.add_line('*%s completed with %d failure%s.* _(%d test%s executed)_\n' % summary_args)

        # Test failures (formatted for Slack)
        for node_id, failure_data in session.failures.items()[:max_failures]:
            test_name, info = failure_data
            message.add_line('*%s*' % test_name)
            message.add_line('>%s' % node_id)

            # Exception/failure detail
            detail = (info.message, info.lineno, info.path)
            if all(detail):
                try:
                    rel_path = get_path_rel_to_parent(info.path)
                except MissingSubPathException:
                    # Error may be in a dependency
                    rel_path = info.path
                message.add_line('>```%s\n%s (line %d)```\n' % (info.message, rel_path, info.lineno))

        # (Indicate ellipsis)
        if len(session.failures) > max_failures:
            message.add_line('_..._\n')

        # Include either a link to the parent folder, or to the build output (if possible)
        if hasattr(session, 'jenkins_url'):
            message.add_line('See more at %s' % session.jenkins_url)

        # Send the session summary to the session's Slack recipient
        session.log.error(str(message), slack_recipients=session.slack_recipients)

