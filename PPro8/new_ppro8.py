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


class Quote:
    def __init__(self, code):
        self.cache = dict()

    def recv(self, data):
        if data["Symbol"] == "":
            return
        print(data)

        Price = data["Price"]
        Mmid = data["Mmid"]
        if Price in self.cache:
            if data["Side"] == self.cache[Price]["Side"]:
                if data["Volume"] == "0":
                    self.cache[Price].pop(Mmid)
                else:
                    self.cache[Price][Mmid] = data
            else:
                self.cache[Price] = {data["Mmid"]: data, "Side": data["Side"]}
                cover = []
                if data["Side"] == "A":
                    for k, v in self.cache.iteritems():
                        if k < Price and v["Side"] == "B":
                            cover.append(k)
                else:
                    for k, v in self.cache.iteritems():
                        if k > Price and v["Side"] == "A":
                            cover.append(k)
                for k in cover:
                    print "del", k
                    self.cache.pop(k)
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
        for k, v in self.cache.iteritems():
            for k, v in self.cache[k].iteritems():
                if k != "Side":
                    l2.append(v)
        return l2


class PPro8(object):
    L2 = {}
    # cache_TOS = {}
    live = False
    m_queue = Queue.Queue()
    last_symbol = None
    is_snapshot = True

    def recv(self, data):
        symbol = data["Symbol"]
        if symbol:
            if data['SequenceNumber'] == "0" and not self.last_symbol:
                self.last_symbol = symbol
                self.L2.pop(symbol)
                obj = self.L2[symbol] = Quote(symbol)
            if symbol in self.L2:
                obj = self.L2[symbol]
            else:
                obj = self.L2[symbol] = Quote(symbol)
            obj.recv(data)
            if data['SequenceNumber'] != "0":
                return {"code": symbol, "data": obj.get_l2()}
        else:
            if data["Side"] == "s":
                self.last_symbol = None
            elif data["Side"] == 'e' and not self.last_symbol:
                self.L2 = {}
            elif self.last_symbol and self.last_symbol in self.L2:
                obj = self.L2[self.last_symbol]
                return {"code": self.last_symbol, "data": obj.get_l2()}

    def on_recv(self, data):
        pass


def test(on_recv):
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
