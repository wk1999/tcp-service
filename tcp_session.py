
class tcp_session:
    def __init__(self, addr, send_api):
        self._addr = addr
        self._send = send_api
        self._user = None
        self._exit = False
    def send(self, data):
        return self._send(data)
    def set_user(self, user):
        if not self._user:
            self._user = user
    def get_user(self):
        return self._user
    def exit(self):
        self._exit = True
    def is_exit(self):
        return self._exit
