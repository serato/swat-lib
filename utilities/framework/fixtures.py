# coding: utf-8
"""
Shared pytest fixtures for web team.  imported by spec/conftest.py, which is
itself auto-discovered by pytest.
Don't forget to document anything you add here ಠ_ಠ
"""
import os
import time

import pytest

from framework import base
from framework import helpers
from framework.api.ecom import EcomAPI
from framework.api.id import IdApi
from framework.base import set_environment_from_file

from framework.emails import ImapHelper
from datetime import datetime, timedelta
from pytz import timezone
from framework.log import Log
from framework.models import Address, CreditCard
from framework.slack_integration import Slack
from pages.express_checkout.checkout import CheckoutPage
from pages.id_serato_com.login import LoginPage
from steps.express_checkout.checkout import CheckoutSteps
from steps.id_serato_com.ui.login import LoginSteps


def pytest_addoption(parser):
    """
    Arguments passed through --pytest-args.  Parsed by standard python module
    argparse.  
    """
    parser.addoption('--env', action='store', default='staging',
                     help='test env to run tests against')
    parser.addoption('--browser', action='append', choices=('chrome',
                                                            'firefox', 'safari', 'edge'),
                     help='browser(s) to test against')
    parser.addoption('--logging-level', action='store', default='debug',
                     help='Logging level (e.g. debug, warn, error, info...)')
    parser.addoption('--env-file', action='store', default=None,
                     help='.env file from which to load environment variables (e.g. client app credentials). These'
                          'variables will override the ones already defined in the environment (if they collide).')
    parser.addoption('--name', action='store', default=None, help='Name used to identify this testing session ('
                                                                  'optional; used for logging/notifications).')
    parser.addoption('--jenkins-url', action='store', default=None, help='URL of this build/build output on Jenkins;'
                                                                         'optional; used for logging/notifications).')
    parser.addoption('--slack', action='store', default=None, help='List of Slack recipients (comma delimited--no '
                                                                   'spaces) to send notifications to on failure. '
                                                                   'Format: #channel,@user')
    parser.addoption('--output', action='store', default='output', help='Relative path within the workspace of the '
                                                                        'directory in which to store output artifacts'
                                                                        ' (such as screenshots).')
    parser.addoption('--email-retries', action='store', default=8, help='Number of times (at 10 second intervals) to '
                                                                        'poll the IMAP server for matching emails if '
                                                                        'a fetch request returns nothing. This should '
                                                                        'depend on how long it takes the server to '
                                                                        'send the email, and the speed of the '
                                                                        'connection.')
    parser.addoption('--email-search-errors', action='store', default=False, help='Whether to throw errors when the '
                                                                                 'email helper fails to find an email '
                                                                                 'on the server. These errors cause '
                                                                                 'inconsistent test failures and are '
                                                                                 'generally due to a slow network and '
                                                                                 'slow server processes. If false, '
                                                                                 'errors will be downgraded to '
                                                                                 'warnings.')


def pytest_generate_tests(metafunc):
    """
    This is called for every test. Only get/set command line arguments if the
    argument is specified in the list of test "fixturenames" (i.e. parameters
    declared in the test function).
    """
    for param in ['env', 'browser', 'logging_level', 'env_file', 'name', 'jenkins_url', 'slack', 'output', 'email_retries',
                  'email_search_errors']:
        option_value = getattr(metafunc.config.option, param)
        if param in metafunc.fixturenames:
            metafunc.parametrize(param, [option_value], scope='session')


@pytest.fixture(params=helpers.get_all_browsers().keys())
def driver(request, browser):
    if browser is not None and request.param not in browser:
        pytest.skip('Test filtered by command line parameters (--browser)')
    # do some os checking or something here to determine which webdrivers are actually available
    all_browsers = helpers.get_all_browsers()
    driverclass = all_browsers[request.param]['driver']
    if 'args' in all_browsers[request.param]:
        if type(all_browsers[request.param]['args']) is dict:
            browserdriver = driverclass(**all_browsers[request.param]['args'])
        else:
            browserdriver = driverclass(all_browsers[request.param]['args'])
    else:
        browserdriver = driverclass()
    request.addfinalizer(lambda *args: browserdriver.quit())
    return browserdriver


# @pytest.fixture()
# def selenium(selenium):
#     selenium.implicitly_wait(10)
#     selenium.maximize_window()
#     return selenium

# @pytest.fixture
# def configuration_yaml():
#     return os.path.join(os.path.dirname(__file__), 'default_configuration.yaml')


@pytest.fixture
def web_browser(selenium):
    browser = base.Browser(selenium)
    return browser


def get_root_dir():
    current = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current, os.pardir))


@pytest.fixture(scope='session')
def global_config(env, configuration_yaml, env_config_map_yaml, env_file):
    # Alias staging to test1
    if env == 'staging':
        env = 'test1'

    config = base.Configuration(env)

    # Load environment variables from the file provided as the --env-file argument, if given
    if env_file:
        set_environment_from_file(env_file)

    try:
        # Load environment variables from the environment
        config.load_env_vars(env_config_map_yaml)
    except KeyError as e:
        # Missing environment variables. Try to use the .env file in the project root instead.
        if env == 'dev':
            env_path = os.path.join(get_root_dir(), 'dev.env')
        elif env.startswith('test'):
            env_path = os.path.join(get_root_dir(), 'test.env')
        else:
            raise e
        set_environment_from_file(env_path)

        # Try to load the environmental configuration again
        config.load_env_vars(env_config_map_yaml)

    config.load(configuration_yaml)
    return config


@pytest.fixture
def managed_data():
    created_records = []

    def _make_customer_record(name):
        # models.Customer(name=name, orders=[])
        record = {'name': name, 'orders': []}
        created_records.append(record)
        return record

    yield _make_customer_record

    for record in created_records:
        pass  # record.destroy()


@pytest.fixture(scope='session')
def ecom_api(global_config):
    return EcomAPI(global_config.ecom_home, global_config.urls.ecom.api)


@pytest.fixture(scope='session')
def id_api(global_config):
    client_app = global_config.client_apps.test_automation
    return IdApi(global_config.id_home, client_app.id, client_app.password, global_config.urls.id.api)


@pytest.fixture(scope='class')
def existing_user(global_config, id_api):
    # Get the 'valid user' credentials for this test stack
    email = global_config.users.existing.email
    password = global_config.users.existing.password

    # Retrieve the user's data, or create the user if the user does not exist
    return id_api.create_user_if_not_exists(email, password)


@pytest.fixture(scope='class')
def default_user(global_config, id_api):
    email = global_config.users.default.email
    password = global_config.users.default.password
    return id_api.create_user_if_not_exists(email, password)


@pytest.fixture(scope='class')
def add_existing_user(existing_user, request):
    # Add the existing user data as a field of the test class
    request.cls.existing_user = existing_user


@pytest.fixture(scope='class')
def add_config(global_config, request):
    request.cls.config = global_config


@pytest.fixture
def test_specific_email(env, global_config, request):
    """
    Returns a test-specific email address (really, the default test user address with a '+{some suffix}' added)
    """
    # Get the default test user email address from config
    test_user_email = global_config.users.default.email
    parts = test_user_email.split('@')

    # Grab a bit of test metadata to identify this user in the database
    test_name = request.node.originalname
    tag = '%s_%s' % (env, test_name)

    # Limit the length of this 'tag' to 30 characters (truncating it, if necessary)
    tag = tag[:30]

    # Email address in the format 'test.user+testclass_test_name@serato.com' (or similar)
    yield '%s+%s@%s' % (parts[0], tag, parts[-1])


@pytest.fixture
def test_specific_user(global_config, test_specific_email, id_api):
    """
    Creates (or retrieves) a user, adding the test class/name to the email address
    """
    yield id_api.create_user_if_not_exists(test_specific_email, global_config.users.default.password)


@pytest.fixture
def timestamped_email(test_specific_email):
    """
    Yields a Unix-timestamped version of the test-specific user email for this stack
    """
    parts = test_specific_email.split('@')
    yield '%s_%d@%s' % (parts[0], time.time(), parts[-1])


@pytest.fixture
def new_user(global_config, timestamped_email, id_api):
    """
    Creates a new user for use in tests.
    """
    yield id_api.create_user_if_not_exists(timestamped_email, global_config.users.default.password)


@pytest.fixture
def a_date():
    def _date(future=True):
        if future:
            reset_date = datetime.utcnow() + timedelta(hours=1)
        else:
            reset_date = datetime.utcnow() - timedelta(hours=1)
        reset_date = reset_date.replace(microsecond=0, tzinfo=timezone('UTC')).isoformat()
        return reset_date

    return _date


@pytest.fixture
def email_helper(global_config, email_retries, email_search_errors, log):
    """
    Yields an ImapHelper (for interacting with a user's inbox) initialised with the default user's credentials.
    """
    retries = int(email_retries)
    yield ImapHelper(global_config.users.default.email, global_config.users.default.password, retries=retries,
                     email_search_errors=email_search_errors, logger=log)


@pytest.fixture(scope='session')
def slack_recipients(slack):
    """
    Provides a list of slack recipients, from the slack fixture (command line argument): a comma-delimited list.
    """
    if not slack or not isinstance(slack, str):
        yield None
    else:
        yield slack.split(',')


@pytest.fixture(scope='session')
def log(global_config, logging_level):
    """
    Returns a logger that extends `logging` with the ability to take screenshots on error, a Slack integration, and a
    formatting helper.
    """
    slack_integration = Slack(global_config.urls.slack_webhook)
    return Log(slack_integration=slack_integration, level=logging_level)


@pytest.fixture(scope='class')
def add_logger(log, request):
    """
    Gives tests access to a logger (e.g. for logging errors) as a class attribute.
    """
    request.cls.log = log


@pytest.fixture
def access_token(global_config, existing_user, id_api):
    """
    Returns an access token for the 'existing' user.

    Uses the test automation client app credentials, which gives requests made using this token access to the
    admin-user-read and admin-user-write scopes on ecom-serato-com.
    """
    yield id_api.get_access_token_for_user(existing_user.email, existing_user.password)


@pytest.fixture
def access_token_profile(global_config, existing_user):
    """
    Returns an access_token for the 'existing' user.

    Uses the profile app client app credentials, which does not provide access to controllers wih the admin JWT scopes
    on ecom-serato-com.
    """
    client_app = global_config.client_apps.profile_app
    api = IdApi(global_config.id_home, client_app.id, client_app.password, global_config.urls.id.api)
    yield api.get_access_token_for_user(existing_user.email, existing_user.password)


@pytest.fixture
def create_dj_suite_subscription_for_user(global_config, web_browser):
    """
    Proof of concept: returns a function that can be called to create a subscription for a user
    """

    def create_dj_suite_sub(user):
        address = Address()
        credit_card = CreditCard()
        login_page = LoginPage(global_config, web_browser.driver)
        login_steps = LoginSteps(login_page)
        page = CheckoutPage(global_config, web_browser.driver)
        steps = CheckoutSteps(page, login_steps)
        steps.purchase_dj_suite_subscription(web_browser, user, credit_card, address)

    return create_dj_suite_sub


@pytest.fixture
def create_dj_pro_subscription_for_user(global_config, web_browser):
    """
    Proof of concept: returns a function that can be called to create a subscription for a user
    """

    def create_dj_pro_sub(user):
        address = Address()
        credit_card = CreditCard()
        login_page = LoginPage(global_config, web_browser.driver)
        login_steps = LoginSteps(login_page)
        page = CheckoutPage(global_config, web_browser.driver)
        steps = CheckoutSteps(page, login_steps)
        steps.purchase_dj_pro_subscription(web_browser, user, credit_card, address)

    return create_dj_pro_sub


@pytest.fixture
def create_wailshark_monthly_subscription_for_user(global_config, web_browser):
    """
    Proof of concept: returns a function that can be called to create a subscription for a user
    """

    def create_wailshark_monthly_sub(user):
        address = Address()
        credit_card = CreditCard()
        login_page = LoginPage(global_config, web_browser.driver)
        login_steps = LoginSteps(login_page)
        page = CheckoutPage(global_config, web_browser.driver)
        steps = CheckoutSteps(page, login_steps)
        steps.purchase_wailshark_monthly_subscription(web_browser, user, credit_card, address)

    return create_wailshark_monthly_sub


@pytest.fixture
def create_wailshark_annual_subscription_for_user(global_config, web_browser):
    """
    Proof of concept: returns a function that can be called to create a subscription for a user
    """

    def create_wailshark_annual_sub(user, is_logged_in=False):
        address = Address()
        credit_card = CreditCard()
        login_page = LoginPage(global_config, web_browser.driver)
        login_steps = LoginSteps(login_page)
        page = CheckoutPage(global_config, web_browser.driver)
        steps = CheckoutSteps(page, login_steps)
        steps.purchase_wailshark_annual_subscription(web_browser, user, credit_card, address, is_logged_in)

    return create_wailshark_annual_sub


@pytest.fixture(scope='session', autouse=True)
def add_session_logger(request, log):
    """
    Adds a log attribute to the session (giving it access to the same logger used in the tests)
    """
    request.session.log = log


@pytest.fixture(scope='session')
def output_url(global_config, name, output):
    """
    URL of the output folder for build artifacts such as screenshots, if possible.
    """
    if name and output:
        url = global_config.jenkins_output_url.format(job_name=name, output=output)
    else:
        url = ''

    return url
