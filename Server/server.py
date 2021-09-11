'''
Calls the client and orders the functions according to the client's request and sends back (in json).
uses the functions in the funcs.py script.
'''
from socket import socket,gethostname, gethostbyname
from json import *
from pprint import pprint# to print in a pretty way
from funcs import *# to use all the functions i wrote in the funcs script
import sys


print('Please write this address to get into the website (without the whitespace between them): ', gethostbyname(gethostname()), ":", "8000")

server = socket()
IP_address = gethostname()
Port = 1927
try:
    server.bind(('', Port))
except:
    print("cannot connect")
    sys.exit()


def handle(client):
    '''
    get data(requests) in json from client and send the result to the client
    :param client: data(requests) from client
    :return: send to the client the response for the requests (in json)
    '''
    data = (client.recv(4096)).decode("utf-8")
    data1 = loads(data)
    reason = ""
    extra = {}
    result = False
    if data1 == '':
        print('Connection broken!')
    else:
        pprint('Received: ' + str(data1))
        if data1['request'] == 'register':
            result, reason = register(data1)
        elif data1['request'] == 'login':
            result, reason = login(data1)
        elif data1['request'] == 'get_user_groups':
            result, reason, extra = get_user_groups(data1)
        elif data1['request'] == 'get_group_name':
            result, reason, extra = getgroup_name(data1)
        elif data1['request'] == 'send_message':
            result, reason = send_message(data1)
        elif data1['request'] == 'get_messages':
            result, reason, extra = get_messages(data1)
        elif data1['request'] == 'add_to_group':
            result, reason = add_to_group(data1)
        elif data1['request'] == 'create_group':
            result, reason = create_group(data1)
        elif data1['request'] == 'log_out':
            result = log_out(data1)
        elif data1['request'] == 'users_in_group':
            result, reason, extra = users_in_group(data1)
        pprint(dumps({'result': result, 'reason': reason,'extra': extra}))
        try:
            client.send(dumps({'result': result, 'reason': reason, 'extra': extra}))
        except:
            conn.close()
            print('client disconnected')
            print("connection is broken")

if __name__ == '__main__':
    server.listen(5)
    while True:
        # Wait for a connection
        print('waiting for a connection')
        conn, addr = server.accept()
        handle(conn)
