
class guard:
    def __init__(self, session, userdata):
        self._state_guarding_username = 1
        self._state_guarding_password = 2
        self._state_ok = 3
        self._state_failed = 4
        self._state = self._state_guarding_username
        self._user = None
        self._users = userdata
        self._retry = 0
    def validated_failed(self):
        return self._state_failed == self._state
    def validated_ok(self):
        return self._state_ok == self._state
    def user(self):
        if self._state_ok == self._state:
            return self._user
        else:
            return None
    def handle(self, data, session):
        if self._state_guarding_username == self._state:
            if data in self._users:
                self._user = self._users[data]
                session.send("Password:")
                self._state = self._state_guarding_password
                self._retry = 0
            else:
                self._retry += 1
                if 3 == self._retry:
                    session.send("% Login failed\r\n")
                    self._state = self._state_failed
                else:
                    session.send("Username:")
        elif self._state_guarding_password == self._state:
            if data == self._user['password']:
                session.send("% Welcome\r\n")
                self._state = self._state_ok
            else:
                self._retry += 1
                if 3 == self._retry:
                    session.send("% Login failed\r\n")
                    self._state = self._state_failed
                else:
                    session.send("Password:")
        else:
            session.send("%% BUG...\r\n")
        return True
    def on_start_session(self, session):
        session.send("Username:")
    def on_close_session(self, session):
        pass
    def name(self):
        return "guard"
