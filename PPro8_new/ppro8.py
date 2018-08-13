# -*- coding: utf-8 -*-
# @Time    : 2018/3/16 17:32
# @Author  : tao.shao
# @File    : ppro8.py


import json
import Queue


def parser(text):
    m_data = dict()
    for t in text.split(","):
        _tupe = t.split("=")
        m_data[_tupe[0]] = _tupe[1]
    return m_data


class Quote: #行情
    def __init__(self, code):
        self.cache = {} #记录历史信息

    def recv(self, data): #data:dict包含信息
        if data["Symbol"] == "":  # error
            return
        # print(data)

        Price = data["Price"]  # 价格
        Mmid = data["Mmid"]  # 通道
        if Price in self.cache:
            if data["Side"] == self.cache[Price]["Side"]:  # price = key
                self.cache[Price][Mmid] = data  # add 通道
            else:
                if data["Volume"] == 0:  # 无交易
                    return
                self.cache[Price] = {data["Mmid"]: data, "Side": data["Side"]}  # cover
                cover = []
                if data["Side"] == "A":
                    for k, v in self.cache.iteritems():
                        if k < Price and v["Side"] == "B":  # bid(买方出价) < ask(卖方要价)
                            cover.append(k)
                else:
                    for k, v in self.cache.iteritems():
                        if k > Price and v["Side"] == "A":
                            cover.append(k)
                for k in cover:
                    # print "del", k
                    self.cache.pop(k)  # k信息无用
        else:
            self.cache[Price] = {data["Mmid"]: data, "Side": data["Side"]}

    def show(self):
        keys = self.cache.keys()
        keys.sort()
        for k in keys:
            for item in self.cache[k].values():
                print(k, item)

    def get_l2(self):
        l2 = []
        for k, _v in self.cache.iteritems():
            for k, v in self.cache[k].iteritems():
                if k != "Side":  # del side
                    l2.append(v)  # v = data
        return l2


class PPro8(object):
    L2 = {}  # L2行情
    cache_TOS = {}
    live = False
    m_queue = Queue.Queue()  # 队列

    def recv(self, data):
        symbol = data["Symbol"]  # 股票代码
        if symbol in self.L2:
            obj = self.L2[symbol]
        else:
            obj = self.L2[symbol] = Quote(symbol)
        obj.recv(data)
        return {"code": symbol, "data": obj.get_l2()}

    def on_recv(self, data):
        pass


def test(on_recv=None):
    ppro = PPro8()
    ppro.on_recv = on_recv
    with open("data1.txt") as fp:
        for line in fp.readlines():
            line = line.strip()
            line = line.replace('\'', '"')
            line = line.replace('u"', '"')
            line = line.replace('\n', '')
            mdata = json.loads(line)
            yield ppro.recv(mdata)


if __name__ == "__main__":
    test()
    # data = {"data":["d"]}
