
class framer:
    def __init__(self, session, is_frame_api):
        self._frame_buf = []
        self._handlers = []
        self._session = session
        self._is_frame_api = is_frame_api
    def install_handlers(self, handlers):
        for handler in self._handlers:
            handler.on_close_session(self._session)
        self._handlers = handlers
    def recv(self, data):
        #d = data.decode()
        for c in data:
            #if self._is_frame_api(c, frame, offset...):
            if c == '\n' or c == '\r':
                frame = "".join(self._frame_buf).strip()
                self._frame_buf = []
                if len(frame) > 0:
                    print("received frame:", frame)
                    handled = False
                    for handler in self._handlers:
                        if handler.handle(frame, self._session):
                            handled = True
                            print("tokens were parsed:", frame,"with handler:",handler.name())
                            break
                    if not handled:
                        self._session.send("% unknown request\n")
                if self._session.in_cli() and c == '\n':
                    self._session.send(self._session.prompt())
            else:
                self._frame_buf.append(c)
