# -*- coding: utf-8 -*-
# @Time    : 2018/2/5 11:19
# @Author  : tao.shao
# @File    : client.py

#远程服务器
import requests
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# s.bind(("0", 4135))
# while True:
#     print(1)
#     data, addr = s.recvfrom(10)
#     print(data, addr)
# s.sendto(b"data", ("127.0.0.1", 4135))


def register(symbol, feedtype="L1"):
    params = {
        "symbol": symbol,
        "feedtype": feedtype,
        "output": "4135",
        "status": "on"
    }
    r = requests.get("http://127.0.0.1:8080/Register", params=params)
    return r.content
#
if __name__ == "__main__":
    register("1988.HK")
    register("1988.HK", "L2")
