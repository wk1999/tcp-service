
import session_guard
import tcp_frame
import datetime

class tcp_session_svr:
    def __init__(self, service, sock, addr, send_api):
        self._state_guarding = 1
        self._state_running = 2
        self._state_closed = 3
        self._state = self._state_guarding
        self._redirecter = None
        self._user = None
        self._timeout_running_seconds = 5*60
        self._timeout_guarding_seconds = 2*60

        #
        self._service = service
        self._sock = sock
        self._addr = addr
        self._session = service.create_session(addr, send_api)
        self._framer = tcp_frame.framer(self._session, service.is_frame)
        self._guarder = session_guard.guard(self._session, service.user_data())
        self._framer.install_handlers([self._guarder])
        self._last_time = datetime.datetime.now()
    def handle(self, data):
        if (self._state_closed == self._state):
            return

        self._last_time = datetime.datetime.now()
        self._framer.recv(data)
        if (self._state_guarding == self._state):
            if self._guarder.validated_ok():
                self._user = self._guarder.user()
                self._session.set_user(self._user['username'])
                self._framer.install_handlers(self._user['handlers'])
                self._state = self._state_running
            elif self._guarder.validated_failed():
                self._state = self._state_closed
    def is_closed(self):
        return self._state_closed == self._state
    def on_idle(self):
        if (self._state_closed == self._state):
            return

        # check if client exit the session
        if self._session.is_exit():
            self._state = self._state_closed
            return

        # check if session timeout due to no operation
        now = datetime.datetime.now()
        if (self._state_guarding == self._state):
            if now - self._last_time > datetime.timedelta(seconds=self._timeout_guarding_seconds):
                self._state = self._state_closed
        elif self._state_running == self._state:
            if now - self._last_time > datetime.timedelta(seconds=self._timeout_running_seconds):
                self._state = self._state_closed
    def on_sock_close(self):
        self._state = self._state_closed
        self._framer.install_handlers([]) # TO destruct handlers

