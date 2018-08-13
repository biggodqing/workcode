from net.RPCClient import request
import sys


class Req_Client(object):

    def __init__(self,symbol,feedtype,port=4135,status='on'):
        self.symbol = symbol # code
        self.feedtype = feedtype # 'L1','L2'...
        self.port = port # 4135
        self.status = status # 'on'

    def req_send(self):
        data = {
            'symbol':self.symbol,
            'feedtype':self.feedtype,
            'port':self.port,
            'status':self.status
        }
        # while True:
        try:
            # data_res = request("113.108.181.146:29001", "req_data", data)
            status = request("218.77.104.29:8000", "req_data", data)  # call utils
            print(status) # return status

        except Exception as err:
            print('error', err)

def main():
    '''
    python2 request_client.py symbol feedtype port status
    :return:
    '''

    #     symbol = sys.argv[1] # '1988.HK'
    #     feedtype = sys.argv[2] # 'L2' 'L1'
    #     port = 4135
    #     status = 'on'
    # req_client(symbol,feedtype,port,status)

    req_cl = Req_Client(symbol='1988.HK', feedtype="L2")
    req_cl.req_send()


if __name__ == "__main__":
    main()