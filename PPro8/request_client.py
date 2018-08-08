from net.RPCClient import request
import sys
import socket

class req_client(object):
    def __init__(self,symbol,feedtype,port=4135,status='on'):
        self.symbol = symbol
        self.feedtype = feedtype
        self.port = port
        self.status = status

    def req_send(self):
        #data = dict(symbol=self.symbol,feedtype=self.feedtype,port=self.port,status=self.status)
        data = {
            'symbol':self.symbol,
            'feedtype':self.feedtype,
            'port':self.port,
            'status':self.status
        }
        # while True:
        try:
            request("127.0.0.1:9001", "req_data", data)
        except Exception as err:
            print('error', err)

def main():
    '''
    python2 request_client.py symbol feedtype port status
    :return:
    '''

    #     symbol = sys.argv[1]
    #     feedtype = sys.argv[2]
    #     port = 4135
    #     status = 'on'
    # req_client(symbol,feedtype,port,status)

    req_cl = req_client(symbol='XII', feedtype="L1", port=4135, status="on")
    req_cl.req_send()


if __name__ == "__main__":
    main()