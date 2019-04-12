
class tcp_session:
    def __init__(self, addr, send_api, prompt = 'Mongo# '):
        self._addr = addr
        self._send = send_api
        self._user = None
        self._exit = False
        self._in_cli = False
        self._prompt = prompt
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
    def in_cli(self):
        return self._in_cli
    def set_cli(self):
        self._in_cli = True
    def set_prompt(self, prompt):
        self._prompt = prompt
    def prompt(self):
        return self._prompt
