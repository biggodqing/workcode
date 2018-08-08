# -*- coding: utf-8 -*-
# @Time    : 2018/8/1 09:17
# @Author  : hlq
# @File    : request_data.py

from net.RPCServer import RPCServer
from transfer_new import Transfer
import utils

class request_data(object):
    def __init__(self):
        pass
    def req_data(self,seq,param, session): # request and parse data
        utils.register(**param)
        transfer = Transfer()
        res_data = transfer.run() #transfer data
        print('success')
        return res_data

def main(conf):
    server = RPCServer('0.0.0.0',9001,handler=request_data())
    server.run()

if __name__ == "__main__":
    main(conf=None)