'''
A script where the client sends and receives information from the server.
The script has functions that the script views.py use. Basically this script links the client to the server.
'''

from __future__ import print_function
from socket import socket, gethostname
from json import dumps, loads
IP_address = gethostname()
Port = 1927


def __feed(json):
    '''
    This function sends JSON to the server, gets a response, turns it to JSON and returns it.
    :param json: The JSON to send.
    :return: The result as JSON.
    '''
    server = socket()
    try:
        server.connect(("127.0.0.1", Port))
        print("connection have been made", IP_address)
    except:
        print('can not connect')
    print("send to server")
    server.send(bytes(dumps(json), encoding='utf8'))
    result = loads(server.recv(4096))
    server.close()
    return result


def auth(action, user_name, password):
    '''
    This function registers or logs a user in.
    :param action: either 'register' or 'login'
    :param user_name: The user's username
    :param password: The user's password
    :return: True or False to indicate success, and None or a reason.
    using function: __feed(json)
    '''
    if action.lower() not in ['login', 'register']:
        return False, 'Invalid action'
    result = __feed({
        'request': action.lower(),
        'user_name': user_name,
        'password': password
    })
    if result['result']:
        return True, None
    else:
        return False, result['reason']


def get_user_groups(user_name):
    '''
    get the users' groups
    :param user_name: The user's user name
    :return: True or False to indicate success, and a list of groups or a reason.
    using function: __feed(json)
    '''
    result = __feed({
        'request': 'get_user_groups',
        'user_name': user_name
    })
    if result['result']:
        return True, result['extra']['groups']
    else:
        return False, result['reason']


def get_group_name(id):
    '''
    get group name by the id of the group.
    :param id: The group's ID.
    :return: True or False to indicate success, and the group's name or a reason.
    using function: __feed(json)
    '''
    result = __feed({
        'request': 'get_group_name',
        'group_id': id
    })
    if result['result']:
        return True, result['extra']['group_name']
    else:
        return False, result['reason']


def get_messages(id, user_name):
    '''
    Returns a list of messages from a group by group ID.
    :param id: The ID of the group
    :param user_name: user name
    :return:True or False to indicate success
    using function: __feed(json)
    '''
    result = __feed({
        'request': 'get_messages',
        'group_id': id,
        'user_name': user_name
    })
    if result['result']:
        return True, '<br>'.join(['<b>%s</b>: %s' % tuple(x) for x in result['extra']['messages']])
    else:
        return False, result['reason']


def send_message(id, user_name, msg):
    '''
    returns True or False if the user can send the message to the group.
    :param id: the id of the group
    :param user_name:  user name
    :param msg: the message the user want to send.
    :return: True or False to indicate success.
    using function: __feed(json)
    '''
    result = __feed({
        'request': 'send_message',
        'group_id': id,
        'user_name': user_name,
        'message': msg
    })
    if result['result']:
        return True, None
    else:
        return False, result['reason']


def add_to_group(id, adder, addee):
    '''
    return True or False if the user name can add another user.
    :param id: the id of the group
    :param adder: the user name that want to add another user.
    :param addee: the user name the adder want to add.
    :return:True or False to indicate success.
    using function: __feed(json)
    '''
    result = __feed({
        'request': 'add_to_group',
        'group_id': id,
        'adder': adder,
        'addee': addee
    })
    if result['result']:
        return True, None
    else:
        return False, result['reason']


def log_out(user):
    '''
    return True or False if the user can logout.
    :param user: user name
    :return: True or False if the user can logout.
    using function: __feed(json)
    '''
    result = __feed({
        'request': 'log_out',
        'user_name': user
    })
    if result['result']:
        return True, None
    else:
        return False, result['reason']


def create_group(user_name, group_name):
    '''
    return True or False if the user can create a group
    :param user_name: user name
    :param group_name: the name of the group the user wants to create.
    :return: True or False to indicate success.
    using function: __feed(json)
    '''
    result = __feed({
        'request': 'create_group',
        'user_name': user_name,
        'group_name': group_name
    })
    if result['result']:
        return True, None
    else:
        return False, result['reason']


def users_in_group(id, user_name):
    """
    Returns a list of users in a group by group ID.
    :param id: group id
    :param user_name: user name
    :return:True or False to indicate success.
    using function: __feed(json)
    """
    result = __feed({
        'request': 'users_in_group',
        'group_id': id,
        'user_name': user_name
    })
    if result['result']:
        return True, '<br>'.join(['%s' % tuple(x) for x in result['extra']['users_list']])
    else:
        return False, result['reason']
