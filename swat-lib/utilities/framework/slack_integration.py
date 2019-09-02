"""
This module implements posting messages to Slack. It utilises Slack incoming WebHooks integration
See https://api.slack.com/incoming-webhooks for the integration details.

Steps to create a new WebHook are documented in Confluence here...
http://confluence.akld.serato.net:8090/display/DEV/Test+Automation+Slack+WebHook+Integration

This was copied (with a tiny bit of refactoring) from `utilities` in `at-core`.
"""

import requests


class Slack(object):

    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    @staticmethod
    def _send_post(recipient, message, url):
        """
        Sends the HTTP POST to Slack.

        @param recipient:
        User or Channel name (Requires preceding @ or # respectively).

        @param message:
        The message to post.

        @param url:
        The URL to the Slack HTTP endpoint.
        A private channel requires a dedicated webhook endpoint URL to be supplied. I.e. cannot use the WEBHOOK_URL
        constant.

        To post to a user, the recipient should be '@user.name'
        To post to a channel, the recipient should be '#channel-name'
        """
        payload = {"channel": recipient, "text": message, "mrkdwn": "false"}
        response = requests.post(url, json=payload)

        if response.status_code != 200:
            raise SlackWebhookException("Error posting to Slack. %d: %s." % (response.status_code, response.text),
                                        response.status_code)

    def post_to_slack(self, recipient, message):
        """
        Posts a message to the specified recipient in Slack.

        @param recipient:
        User or Channel name (requires preceding @ or # respectively).
        Note: Private channels require a dedicated integration endpoint so this function cannot post to private channels.

        @param message:
        The message to post.
        """
        Slack._send_post(recipient=recipient, message=message, url=self.webhook_url)


class SlackWebhookException(Exception):
    """
    Thrown when there is an error posting to the Slack webhook
    """
    def __init__(self, message, status_code):
        """
        :param message: Message for the exception
        :param status_code: HTTP response code for the error response
        """
        super(Exception, self).__init__(message)
        self.status_code = status_code
