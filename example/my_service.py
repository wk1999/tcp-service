
import cli_session
import cli_user

class service:
    def name(self):
        return "CLI EXAMPLE !!"
    def addr(self):
        return ''
    def port(self):
        return 10004
    def create_session(self, *args, **kwargs):
        return cli_session.session(*args, **kwargs)
    def is_frame(self, *args, **kwargs):
        return False
    def user_data(self):
        return cli_user.users
