import pytest


"""
Plugin for recording session data, as well as test failures/errors, so that we can generate better reports.
"""


@pytest.fixture(scope='session', autouse=True)
def add_session_data(request, global_config, name, jenkins_url):
    request.session.jenkins_url = jenkins_url or global_config.jenkins_url
    request.session.name = name


def pytest_sessionstart(session):
    session.failures = dict()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    result = outcome.get_result()

    # result.longrepr may be a string if there's an error in setup
    if result.failed and hasattr(result.longrepr, 'reprcrash'):
        item.session.failures[item.nodeid] = (item.originalname, result.longrepr.reprcrash)
