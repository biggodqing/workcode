# -*- coding: utf-8 -*-
# @Time    : 2018/2/2 13:36
# @Author  : tao.shao
# @File    : server.py


from ppro8 import PPro8

UDP_PORT = 4135
CACHE_PATH = "./root"


def parser(text): #解析数据:input 'data';return 'data dict'(u'xx':u'xx')
    m_data = dict()
    text=text.replace("\n", "")
    for t in text.split(","):
        _tupe = t.split("=")
        m_data[_tupe[0]] = _tupe[1]
    # pre-process
    if 'Volume' in m_data and 'Price' in m_data:
        m_data['Price'] = float(m_data['Price']) #trans to number
        m_data['Volume'] = int(m_data['Volume'])
    elif 'Size' in m_data:
        m_data['Size'] = int(m_data['Size']) #??

    return m_data


ppro8 = PPro8()


class PPro8Server(object):
    L2_CACHE = {}

    def recv(self, seq, param, session):
        #print(param)
        if "data" in param: #param?
            data = param["data"] #获得data属性
            m_data = parser(data) #m_data(dict)
        else:
            m_data = param

        if m_data["Message"] == "L2":
            data = ppro8.recv(m_data)
            if data:
                self._on_price(data)
        elif m_data["Message"] == "TOS":
            self._on_tos(m_data)

        if hasattr(self, "analyse"):
            self.analyse()
        print(m_data)
        return m_data
        #return {"status": 1}

    def _on_recv(self, data):
        try:
            if hasattr(self, "on_recv"):
                self.on_recv(data)
        except:
            pass

    def _on_tos(self, data):
        try:
            if hasattr(self, "on_tos"):
                self.on_recv(data)
        except:
            pass

    def _on_price(self, data):
        try:
            if hasattr(self, "on_price"):
                self.on_price(data)
        except:
            pass

    def on_recv(self):
        pass

    def on_analyse(self, data):
        pass


def main(conf):
    from net.RPCServer import RPCServer
    server = RPCServer("0.0.0.0", 9001, handler=PPro8Server())
    server.run()


def create_source(on_price, on_tos):
    from net.RPCServer import RPCServer
    ppro8 = PPro8Server()
    # ppro8.on_recv = on_recv
    ppro8.on_price = on_price
    ppro8.on_tos = on_tos
    server = RPCServer("0.0.0.0", 9000, handler=ppro8)
    return server


if __name__ == "__main__":
    # import ConfigParser
    # import sys
    #
    # conf = ConfigParser.ConfigParser()
    # if len(sys.argv) > 1:
    #     conf.read(sys.argv[1])
    # else:
    #     conf.read("conf/PPro8.ini")
    main(conf=None)

    # #pp = PPro8Server()
    # #pp.recv(0,data,1)
