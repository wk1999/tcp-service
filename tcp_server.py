import select
import socket
import Queue
import tcp_session_svr

class tcp_server:
    def __init__(self, service_ins, listen_backlog = 100, recv_buffer = 1024, idle_second = 1):
        self._service = service_ins
        self._server_addr = service_ins.addr()
        self._server_port = service_ins.port()
        self._server_listen_backlog = listen_backlog
        self._server_recv_buffer = recv_buffer
        self._server_select_timeout = idle_second

        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server.setblocking(False)
        self._server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server.bind((self._server_addr, self._server_port))
        self._server.listen(self._server_listen_backlog)

        self._read_socks = [self._server,]
        self._write_socks = []
        self._msgq_write = {}
        self._server_sessions = {}

    def _send_back(self, sock, data):
        if sock not in self._msgq_write:
            return
        self._msgq_write[sock].put(data)
        if sock not in self._write_socks:
            self._write_socks.append(sock)

    def _get_reply_api(self, sock):
        def reply(data):
            self._send_back(sock, data)
        return reply

    def _close_sock(self, sock):
        self._server_sessions[sock].on_sock_close();
        self._read_socks.remove(sock)
        if sock in self._write_socks:
            self._write_socks.remove(sock)
        sock.close()
        del self._msgq_write[sock]
        del self._server_sessions[sock]
        print('close sock=', sock, "left num=", len(self._server_sessions))

    def run(self):
        while True:
            read_ready, write_ready, exceptional = select.select(
                    self._read_socks, self._write_socks, self._read_socks, self._server_select_timeout)

            if not (read_ready or write_ready or exceptional):
                for session in self._server_sessions.values():
                    session.on_idle()

            for sock in read_ready:
                if sock is self._server:
                    new_sock, addr_client = self._server.accept()
                    new_sock.setblocking(False)
                    self._read_socks.append(new_sock)
                    self._msgq_write[new_sock] = Queue.Queue()
                    session = tcp_session_svr.tcp_session_svr(
                            self._service, new_sock, addr_client, self._get_reply_api(new_sock))
                    self._server_sessions[new_sock] = session
                    print('new connection=', addr_client, 'sock=', new_sock)
                else:
                    data = sock.recv(self._server_recv_buffer)
                    if data:
                        self._server_sessions[sock].handle(data)
                    else:
                        self._close_sock(sock)
            for sock in write_ready:
                try:
                    msg = self._msgq_write[sock].get_nowait()
                except Queue.Empty:
                    self._write_socks.remove(sock)
                else:
                    sock.send(msg)
            for sock in exceptional:
                self._close_sock(sock)

            # check the closed sessions
            socks_to_close = []
            for sock, session in self._server_sessions.items():
                if session.is_closed():
                    socks_to_close.append(sock)
            for sock in socks_to_close:
                sock.send('\n% server closed socket\r\n')
                self._close_sock(sock)
