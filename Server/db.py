'''
This script includes the functions that deal with mongodb.
These functions are called by functions in the Script funcs.py.
'''
from pymongo import MongoClient

client = MongoClient()
db = client.chat_database
user_collection = db.user_collection
group_collection = db.group_collection


def insert_user(data):
    '''
    insert user name to user collection
    :param data: data received from client include user_name, and password
    if Global group dose'nt exists it create the group with the create_global_group() function.
    '''
    if not (group_exists('Global')):
        create_global_group()  # create global group- the fist and main group
    post_user = {'user_name': data['user_name'], 'password': data['password'], 'group_ids': ['0']}
    user_collection.insert_one(post_user)


def insert_group(data):
    '''
    insert group to group collection.
    :param data: data received from client include group name and group id.
    '''
    post_group = {'messages': [], 'group_name': data['group_name'], 'group_ids': data['group_id']}
    group_collection.insert_one(post_group)


def create_global_group():
    # create the main group Global
    insert_group({'group_name': 'Global','group_id': '0'})


def sum_groups():
    # return: how many groups exist
    num = db.group_collection.count()
    return num


def group_exists(name):
    '''
    :param name: group name
    :return: True if group name exists in group collection else return False
    '''
    for group in group_collection.find():
        if name == group['group_name']:
            return True
    return False


def find_user(name):
    '''
    find user name in user_collection
    :param name: user name
    :return: return True if the user name exist in user_collection else return False
    '''
    for user in user_collection.find():
        if name == user['user_name']:
            return True
    return False


def right_password(password, name):
    '''
    :param password: entered password
    :param name: user name
    :return: True if the entered password match the user name password else return False
    '''
    for user in user_collection.find({}, {'user_name': 1, 'password': 1}):
        if name == user['user_name'] and password == user['password']:
            return True
    return False


def find_group_messages(group_id):
    '''
    get group messages by the group id
    :param: group_id
    :return: return list of group messages
    '''
    group = group_collection.find_one({'group_ids': group_id})
    if group['messages'] is None:
        return [[]]
    return group['messages']


def get_groups_user(name):
    '''
     get all the groups the user at
    :param name: user name
    :return: a dictionary include list of the groups the user in them
    '''
    user = user_collection.find_one({'user_name': name})
    result = []
    if user is None: return {'groups': result}
    for group_id in user['group_ids']:
        result.append([group_id, get_group_name(group_id)])
    return {'groups': result}


def get_group_name(idg):
    '''
    get the group name and id group by the id group
    :param idg:  group id
    :return: group name (type = string) if not found return None
    '''
    group = group_collection.find_one({'group_ids': idg})
    if group is None:
        return None
    return group['group_name']


def find_users_groups(group_id):
    """
    get list of users in the group
    :param group_id: group id
    :return: return list of users in the group
    """
    list1 = []
    for user in user_collection.find():
        for id in user['group_ids']:
            if id == group_id:
                list1.append([user['user_name']])
    return list1
