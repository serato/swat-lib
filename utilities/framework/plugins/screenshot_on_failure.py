import os
import uuid

import pytest


"""
Plugin for taking a screenshot whenever a test that uses the browser fails or has an error.
"""


def pytest_sessionstart(session):
    session.screenshots = dict()


@pytest.fixture(scope='session', autouse=True)
def add_output_data(request, global_config, output_url):
    """
    Add the Jenkins build artifacts output URL to the session (or an empty string if not available)
    """
    request.session.output_url = output_url


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    """
    Make the test failure status available to finalizers by adding it to the node.
    """
    outcome = yield
    result = outcome.get_result()

    # No point asking the driver to take a screen shot if the error did not occur when the test was running
    if result.when == 'call':  # vs. setup, teardown
        item.take_screenshot = result.failed


@pytest.fixture(autouse=True)
def screenshot_on_failure(request, driver, output, log):
    """
    Adds a finalizer to each test that uses the driver to take a screenshot if the test fails.
    """
    request.addfinalizer(screenshot(request, driver, output, log))


def screenshot(request, driver, output, log):
    """
    Take a screenshot at the point of error/failure. It is Jenkins'/the build jobs' responsibility to clean up the
    output directory in its workspace.
    """
    def _screenshot():
        # Attribute will not be there if the failure was during test setup
        take_screenshot = hasattr(request.node, 'take_screenshot') and request.node.take_screenshot

        # Take a screenshot if the test failed (or had an error), but don't bother if it's of a blank page
        if take_screenshot and not is_page_blank(driver):
            # File-safe name for the screenshot
            current_dir = os.path.dirname(__file__)
            suffix = '_%s.png' % uuid.uuid4()
            test_name = request.node.originalname[:255 - len(suffix)]
            filename = test_name + suffix

            # Find and create the path at which to save the screenshot
            path = os.path.join(current_dir, os.pardir, os.pardir, output, filename)
            output_dir = os.path.dirname(path)
            if not os.path.exists(output_dir):
                os.mkdir(output_dir)

            # Save the screenshot, and delete the file if it failed
            result = driver.save_screenshot(path)
            if not result:
                if os.path.exists(path):
                    os.remove(path)
                log.error('Failed to create screenshot for node %s' % request.node.originalname)

            # Save the screenshot path so that we can aggregate them all later
            request.session.screenshots[request.node.nodeid] = os.path.basename(path)

    return _screenshot


def pytest_sessionfinish(session):
    # Log attribute will not exist if there is an error during collection
    if hasattr(session, 'log'):
        log = session.log

        # Title + list of failures with screenshots
        if session.screenshots.items():
            message = log.format.info_separator('Screenshots: errors and failures')
            message.add_line()

            for k, v in session.screenshots.items():
                # Test descriptor
                if hasattr(session, 'failures') and session.failures.get(k):
                    identifier = session.failures[k][0]  # Test name (short)
                else:
                    identifier = k  # Node ID (verbose)

                # Screenshot of browser at point of failure
                message.add_line('%s: %s%s\n' % (identifier, session.output_url, v))

            log.info(message)


def is_page_blank(driver):
    return driver.current_url == u'data:,'
