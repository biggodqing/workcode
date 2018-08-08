# -*- coding: utf-8 -*-
# @Time    : 2018/2/28 9:13
# @Author  : tao.shao
# @File    : test.py

import errno
from tornado.ioloop import IOLoop
import socket
from tornado import process
from tornado import gen


class UDPServer(object):
    def __init__(self, io_loop=None, ssl_options=None, max_buffer_size=None,
                 read_chunk_size=None):
        self.io_loop = io_loop
        # self.ssl_options = ssl_options
        self._sockets = {}  # fd -> socket object
        self._pending_sockets = []
        self._started = False
        self._stopped = False
        self.max_buffer_size = max_buffer_size
        self.read_chunk_size = read_chunk_size

    def add_sockets(self, sockets):
        """Makes this server start accepting connections on the given sockets.

        The ``sockets`` parameter is a list of socket objects such as
        those returned by `~tornado.netutil.bind_sockets`.
        `add_sockets` is typically used in combination with that
        method and `tornado.process.fork_processes` to provide greater
        control over the initialization of a multi-process server.
        """
        if self.io_loop is None:
            self.io_loop = IOLoop.current()

        for sock in sockets:
            self._sockets[sock.fileno()] = sock
            self.io_loop.add_handler(sock, self._recv, IOLoop.READ)

    def add_socket(self, socket):
        self.add_sockets([socket])

    def bind(self, port, address=None, family=socket.SOCK_DGRAM):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(("", 4135))
        if self._started:
            self.add_sockets(sock)
        else:
            self._pending_sockets.extend([sock])

    def _recv(self, fd, events):
        try:
            data, addr = fd.recvfrom(1024)
        except socket.error as e:
            if e.args[0] not in (errno.EWOULDBLOCK, errno.EAGAIN):
                raise
            return
        self.on_recv(fd, data, addr)
        print (data)

    @gen.coroutine
    def on_recv(self, scok, data, addr):
        yield gen.sleep(10)
        print(1, data)

    def start(self, num_processes=1):
        assert not self._started
        self._started = True
        if num_processes != 1:
            process.fork_processes(num_processes)
        sockets = self._pending_sockets
        self._pending_sockets = []
        self.add_sockets(sockets)



if __name__ == '__main__':
    udp = UDPServer()
    udp.bind(4135)
    udp.start()
    IOLoop.current().start()