
class framer:
    def __init__(self, session, is_frame_api):
        self._frame_buf = []
        self._handler = None
        self._last_char = '\0'
        self._session = session
        self._is_frame_api = is_frame_api
    def install_handler(self, handler):
        if self._handler:
            self._handler.on_close_session(self._session)
        self._handler = handler
        if handler:
            handler.on_start_session(self._session)
    def recv(self, data):
        if not self._handler:
            return
        #d = data.decode()
        for c in data:
            #if self._is_frame_api(c, frame, offset...):
            if c == '\n' or c == '\r':
                if (c == '\n' and self._last_char == '\r') or (c == '\r' and self._last_char == '\n'):
                    #do nothing
                    self._last_char = '\0'
                    continue
                frame = "".join(self._frame_buf).strip()
                self._frame_buf = []
                print("received frame:", frame)
                handled = self._handler.handle(frame, self._session)
                print("tokens were parsed:", frame,"with handler:", self._handler.name(), "result:", handled)
            elif c == '\x08': #backspace
                self._frame_buf.pop()
            else:
                self._frame_buf.append(c)
            self._last_char = c
