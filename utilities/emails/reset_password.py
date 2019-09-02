from emails.base import BaseEmail


class ResetPasswordEmail(BaseEmail):

    @property
    def links(self):
        return lambda tag: tag.name == 'a'

    @property
    def reset_password_links(self):
        return lambda tag: tag.name == 'a' and 'reset password' in tag.text.lower()


class PasswordUpdatedEmail(BaseEmail):

    @property
    def get_support_links(self):
        return lambda tag: tag.name == 'a' and 'get support' in tag.text.lower()
