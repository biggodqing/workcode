# -*- coding: utf-8 -*-
# @Time    : 2018/3/2 11:25
# @Author  : tao.shao
# @File    : utils.py

import requests


CACHE_PATH = "./data_root"


def get_data_root():
    return CACHE_PATH


def register(symbol, feedtype="L1", port=4135, status="on"):
    params = {
        "symbol": symbol,
        "feedtype": feedtype,
        "output": port,
        "status": status
    }
    #print(symbol,feedtype,port,status)
    r = requests.get("http://127.0.0.1:8080/Register", params=params)
    return r.content



