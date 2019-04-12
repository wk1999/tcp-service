
import sys

class redirector():

    def __init__(self, api):
        self._stdout = sys.stdout
        self._send_api = api

    def __del__(self):
        sys.stdout = self._stdout

    def write(self, mes):
        self._send_api(mes)

    def redirect(self):
        sys.stdout = self

    def restore(self):
        sys.stdout = self._stdout

    def write_stdout(self, mes):
        self._stdout.write(mes)
