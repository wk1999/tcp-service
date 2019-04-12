
import mongo_session
import mongo_user

class service:
    def name(self):
        return "MONGO!!"
    def addr(self):
        return ''
    def port(self):
        return 10005
    def create_session(self, *args, **kwargs):
        return mongo_session.session(*args, **kwargs)
    def is_frame(self, *args, **kwargs):
        return False
    def user_data(self):
        return mongo_user.users
