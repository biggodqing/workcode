import requests

CACHE_PATH = "./data_root"


def get_data_root():
    return CACHE_PATH


def register(symbol, feedtype="L1", port=4135, status="on"):  # 注册各类的数据
    params = {
        "symbol": symbol,
        "feedtype": feedtype,
        "output": port,
        "status": status
    }
    r = requests.get("http://127.0.0.1:8080/Register", params=params)  # 传递参数
    return r.content  # 二进制响应内容


def GetSnapshot(symbol, feedtype="L1", port=4135, status="off"):
    # GetSnapshot获取截图用这个命令获取代码当前的数据 (过去的100个记录，但不包含更新的数据)
    params = {
        "symbol": symbol,
        "feedtype": feedtype,
        "output": port,
        "status": status
    }
    r = requests.get("http://127.0.0.1:8080/GetSnapshot", params=params)
    return r.content


def SetOutput(symbol, feedtype="L1", port=4135, status="off"):
    # SetOutput设置输出：用这个命令设置代码输出的信息，定义数据写到哪里，可以是bykey 或者 bytype
    params = {
        "symbol": symbol,
        "feedtype": feedtype,
        "output": port,
        "status": status
    }
    r = requests.get("http://127.0.0.1:8080/SetOutput", params=params)
    return r.content


def unregister(symbol, feedtype="L1", port=4135, status="on"):
    params = {
        "symbol": symbol,
        "feedtype": feedtype,
        # "output": port,
        "status": status
    }
    r = requests.get("http://127.0.0.1:8080/Deregister", params=params)
    return r.content


if __name__ == "__main__":
    codes = ['NMX.TO', 'HUGE.CN', 'PLI.TO', '1988.HK', 'CRYP.CN']
    codes = ['HUGE.CN']
    # codes = ['1988.HK', "0700.HK"]
    isReister = True
    for code in codes:
        if isReister:
            # print GetSnapshot(code, feedtype="L2")
            # print SetOutput("code", "L2")
            register(code, "L2", port="bykey")
            register(code, "L2")
            # print register(code, "TOS")
        else:
            SetOutput("code", "L2")
