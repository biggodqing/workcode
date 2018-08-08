# -*- coding: utf-8 -*-
# @Time    : 2018/5/29 10:35
# @Author  : tao.shao
# @File    : transfer.py


import socket
from net.RPCClient import request

UDP_PORT = 4135


class Transfer(object):
    def __init__(
            self,
            port=UDP_PORT,
    ):
        self.com = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.com.bind(("127.0.0.1", port))

    def run(self):
        while True:
            try:
                data, addr = self.com.recvfrom(1024)
                request("127.0.0.1:9000", "recv", {"data": data}, 0)
            except Exception as err:
                print(err)


def main():
    transfer = Transfer()
    transfer.run()


def send(data):
    try:
        request("127.0.0.1:9000", "recv", {"data": data})
    except Exception as err:
        print('error', err)


def sim_transfer():
    with open("./L2_1_PLI.TO.log") as fp:
        for line in fp.readlines():
            send(line)

if __name__ == "__main__":
    #main()
    sim_transfer()