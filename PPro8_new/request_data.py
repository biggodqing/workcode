# -*- coding: utf-8 -*-
# @Time    : 2018/8/1 09:17
# @Author  : hlq
# @File    : request_data.py

from net.RPCServer import RPCServer
from send_data import Send_Data
import utils


class Request_Data(object):

    def __init__(self):
        pass

    def req_data(self,seq,param,session): # request and parse data
        utils.register(**param)
        # return {'status':1}
        print('register success')
        send_data = Send_Data()
        send_data.run() #transfer data
        return {'status':1}


def main(conf): # conf ??
    server = RPCServer('0.0.0.0', 9001, handler=Request_Data())
    server.run()


if __name__ == "__main__":
    main(conf=None)