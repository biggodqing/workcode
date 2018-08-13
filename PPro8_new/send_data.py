import socket
from net.RPCClient import request

UDP_PORT = 4135


class Send_Data(object):
    def __init__(self,port=UDP_PORT):
        self.com = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.com.bind(("127.0.0.1", port))

    def run(self):
        while True:
            try:
                data, addr = self.com.recvfrom(1024)
                res = request("113.108.181.146:29001", "recv", {"data": data}, 0)
            except Exception as err:
                print(err)


def main():
    send_data = Send_Data()
    send_data.run()


if __name__ == "__main__":
    main()