from contextlib import contextmanager

from framework import atcore
import sys
import os
from selenium import webdriver


def get_chrome_driver_path():
    python_executable_path = sys.executable
    os_path = ''
    extension = ''
    if atcore.operatingsystem.is_mac:
        os_path = os.path
    elif atcore.operatingsystem.is_windows:
        import ntpath
        os_path = ntpath
        extension = ".exe"

    chrome_driver_path = os_path.abspath(os_path.join(
        python_executable_path + "/../..",
        "selenium",
        "webdriver",
        "chrome",
        "chromedriver" + extension
    ))
    return chrome_driver_path


def get_all_browsers():
    # Todo: add multiple browsers drivers here
    return {
        # 'firefox': {'driver': webdriver.Firefox, 'args': {'firefox_binary': '/Applications/FirefoxDeveloperEdition.app/Contents/MacOS/firefox'}},
        # 'safari': {'driver': webdriver.Safari},
        'chrome': {'driver': webdriver.Chrome, 'args': get_chrome_driver_path()}
    }


@contextmanager
def switch_to_iframe(driver, iframe):
    """
    Switch focus to an iframe, and then back again at the end of the block
    """
    driver.switch_to.frame(iframe)
    try:
        yield
    finally:
        driver.switch_to.default_content()


class MissingSubPathException(Exception):
    """
    Indicates that the requested sub-path was not found in the given path when generating a relative path.
    """
    pass


def get_path_rel_to_parent(abs_path, parent_of='test/system'):
    """
    Returns a path relative to the parent of `parent_of`. Returns False if `parent_of` cannot be found in the path.
    If a delimiter is specified, the path will use that in place of the OS's path separator.
    Replaces the default OS path separator with the Unix path separator.
    """
    norm_path = abs_path.replace(os.sep, '/')
    index = norm_path.find(parent_of)

    if index == -1:
        raise MissingSubPathException('Cannot find directory %s in path %s.' % (parent_of, abs_path))

    return norm_path[index:]


def request_to_curl_command(request):
    command = "curl -X {method} -H {headers} -d '{data}' '{uri}'"
    method = request.method
    uri = request.url
    data = request.body
    headers = ['"{0}: {1}"'.format(k, v) for k, v in request.headers.items()]
    headers = " -H ".join(headers)
    return command.format(method=method, headers=headers, data=data, uri=uri)
