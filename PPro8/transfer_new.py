import socket
from ppro8 import PPro8
from net.RPCClient import request

UDP_PORT = 4135

def parser(text):
    m_data = dict()
    text=text.replace("\n", "")
    for t in text.split(","):
        _tupe = t.split("=")
        m_data[_tupe[0]] = _tupe[1]
    # pre-process
    if 'Volume' in m_data and 'Price' in m_data:
        m_data['Price'] = float(m_data['Price'])
        m_data['Volume'] = int(m_data['Volume'])
    elif 'Size' in m_data:
        m_data['Size'] = int(m_data['Size'])

    return m_data


class Transfer(object):
    def __init__(
            self,
            port=UDP_PORT,
    ):
        self.com = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.com.bind(("127.0.0.1", port)) # port4135

    def run(self):
        while True:
            # try:
            #     with open("./L2_1_PLI.TO.log",'r') as fp:
            #         for data in fp.readlines():
            #             m_data = parser(data)
            #         return(m_data)
            # except:
            #     print('err')
            try:
                data, addr = self.com.recvfrom(1024) #get data
                m_data = parser(data)
                if m_data["Message"] == "L2": #l2 data
                    ppro8 = PPro8()
                    data_l2 = ppro8.recv(m_data) #??
                elif m_data["Message"] == "TOS": #??
                    pass
                return m_data
            except Exception as err:
                print(err)


def main():
    transfer = Transfer()
    transfer.run()

if __name__ == '__main__':
    main()