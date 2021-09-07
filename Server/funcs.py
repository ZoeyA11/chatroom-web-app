'''
In this script has lists of functions that perform client requests.
These functions are called by handle(client) at server.py.
uses functions in the db.py script.
'''
from pymongo.errors import DuplicateKeyError, ConnectionFailure
from db import *# to use all the functions i wrote in the db script


def is_valid_password(password):
    '''
    check if the password is valid(The password has to include 6-12 characters, letters and numbers)
    :param password:password that was entered
    :return:true if the password is valid else return False
    '''
    letter_flag = False
    number_flag = False
    for i in password:
        if i.isalpha():
            letter_flag = True
        if i.isdigit():
            number_flag = True
    return len(password) >= 6 and (len(password) <= 12) and letter_flag and number_flag


def register(data1):
    '''
    register to the web
    :param data1: data received from client include user_name, and password
    :return: true if the user_name not exist and the password is valid(checks if password is valid in
    is_valid_password function)
    returns False and reason(str1) when the password or user_name was not enter. Or password is not valid,
     or the user name already exist
    '''
    flag1 = False
    flag2 = False
    str1 = None
    user_name = data1['user_name']
    if user_name == '':
        str1 = 'you did not enter user name\ both - please check'
    else:
        try:
            flag1 = find_user(user_name)
        except ConnectionFailure:
            return False, "There is a problem with the server comeback later"
        if flag1 is False:
            flag1 = True
        else:
            flag1 = False
    password = data1['password']
    if password == '':
        str1 = "can't accept it"
    else:
        flag2 = is_valid_password(password)
        print ("i checked")
        if flag2 is False and flag1 is True:
            str1 = 'your password is not strong enough please enter another password :)'
        elif flag1 is False and flag2 is True:
            str1 = "can't accept it"
    if flag1 * flag2:
        try:
            insert_user(data1)
        except DuplicateKeyError or ConnectionFailure:
            return False, "There is a problem with the server comeback later"
    return flag1 * flag2, str1


def login(data1):
    '''
    login the web
    :param data1: data received from client include user_name, and password
    :return: true if the user name exists and offline and the password is correct. return False and reason(str1) if
    the user name
     not exist\ not entered \ if the password not entered\
     functions:
     find _user(user_name)= return True if user name exist else return False
     right_password(password, user_name) = returns True if the entered password match to the user name password else
     return False
    '''
    flag = False
    str1 = None
    user_name = data1['user_name']
    password = data1['password']
    if user_name == '':
        str1 = 'you did not enter user name\ both - please check'
    else:
        try:
            find = find_user(user_name)
        except ConnectionFailure:
            return False, "There is a problem with the server comeback later"
        if find:
            if password == '':
                str1 = 'you did not enter password'
            else:
                flag = right_password(password, user_name)
                if flag is False:
                    str1 = 'wrong user/password'
        else:
            str1 = 'wrong user name/password'
    return flag, str1


def get_user_groups(data1):
    '''
    get groups the user in them
    :param data1:data received from client include user_name
    :return: return True, dictionary includes all groups the user in them (if there are groups)
    else return False and reason
    *the function get_groups_user(name) return the groups the user in them as a dictionary that include groups list.
    '''
    reason = None
    name = data1['user_name']
    try:
        user_groups = get_groups_user(name)
    except ConnectionFailure:
        return False, "There is a problem with the server comeback later"
    if user_groups['groups'] is []:
        reason = "there's no groups the user in them"
        return False, reason, None
    return True, reason, user_groups


def getgroup_name(data1):
    '''
    get group name by group id
    :param data1: data received from client include group_id
    :return: True and the group name (type= string) else return False and reason
    function:
    get_group_name(idg) = return the group name by the group id
    '''
    id = data1['group_id']
    try:
        group_name = get_group_name(id)
    except ConnectionFailure:
        return False, "There is a problem with the server comeback later",None
    name = {'group_name': group_name}
    if group_name is None:
        return False, "there's no group with this id", name
    return True, None, name


def send_message(data1):
    '''
    add the message the user name want to sand to the list of messages group
    :param data1: data received from client include user_name, message, group_id
    :return: True if there is a message and added the message to the list of messages from a group given a group ID,
    else return False and reason.
    using functions:
    get_groups_user(name)
    find_group_messages(group_id)
    '''
    result = False
    message = data1['message']
    id = data1['group_id']
    try:
        group = group_collection.find_one({'group_ids': id})
    except ConnectionFailure:
        return False, "There is a problem with the server comeback later"
    mongo_id = group['_id']
    user_name = data1['user_name']
    try:
        groups = get_groups_user(user_name)
    except ConnectionFailure:
        return False, "There is a problem with the server comeback later"
    listg = groups['groups']
    for group in listg:
        if group[0] == id:
            result = True
    if result is True:
        try:
            messages = find_group_messages(id)
        except ConnectionFailure:
            return False, "There is a problem with the server comeback later"
        listm = [user_name, message]
        if message == '':
            return False, "You didn't send a message"
        else:
            messages.append(listm)
        try:
            db.group_collection.update({'_id': mongo_id}, {"$set": {'messages': messages}})
        except DuplicateKeyError or ConnectionFailure:  # Raised when an insert or update fails due to a duplicate key error.
            return False, DuplicateKeyError
        return True, None
    else:
        return False, 'you are not allowed to see the messages'


def get_messages(data1):
    '''
    Returns a list of messages from a group given a group ID.
    :param data1:data received from client include user_name, group_id
    :return:True or False to indicate success,if True returns also a list of messages from a group given a group ID.
    else, also return reason.
    using functions:
    get_groups_user(name)
    find_group_messages(group_id)
    '''
    result = False
    user_name = data1['user_name']
    group_id = data1['group_id']
    try:
        groups = get_groups_user(user_name)
    except ConnectionFailure:
        return False, "There is a problem with the server comeback later"
    listg = groups['groups']
    for group in listg:
        if group[0] == group_id:
            result = True
    if result is True:
        try:
            messages = find_group_messages(group_id)
        except ConnectionFailure:
            return False, "There is a problem with the server comeback later"
        return result, None, {'messages': messages}
    else:
        return False, 'you are not allowed to see the messages', None


def add_to_group(data1):
    '''
    Add user_name to group (given group_id).
    :param data1:data received from client include adder, addee(the user_name the adder wants to add), group_id
    :return:True or False to indicate success, if True ,add the given group id  to user name's group_ids'. If False also
    return a reason.
    using functions:
    find_user(name)
    get_groups_user(name)
    '''
    result1 = False
    result2 = True
    adder = data1['adder']
    group_id = data1["group_id"]
    addee = data1['addee']
    try:
        groups1 = get_groups_user(adder)  # the groups adder in them
        groups2 = get_groups_user(addee)  # the groups the addeee in them
        exist2 = find_user(addee)
    except ConnectionFailure:
        return False, "There is a problem with the server comeback later"

    if exist2:
        try:
            user = user_collection.find_one({'user_name': addee})
        except ConnectionFailure:
            return False, "There is a problem with the server comeback later"
        group_ids = user['group_ids']
        mongo_id = user['_id']
        for group1 in groups1['groups']:
            if group1[0] == group_id:
                result1 = True
        for group2 in groups2['groups']:
            if group2[0] == group_id:
                result2 = False
        if result1 is True and result2 is True:
            group_ids.append(group_id)
            try:
                db.user_collection.update({'_id': mongo_id}, {"$set": {'group_ids': group_ids}})
            except DuplicateKeyError or ConnectionFailure:
                return False, "There is a problem with the server comeback later"
            return True, None
        if result1 is False:
            return False, "adder is not in this group"
        if result2 is False:
            return False, 'the user_name is already in this group'
    else:
        for group1 in groups1['groups']:
            if group1[0] == group_id:
                result1 = True
        if result1 is False:
            return False, "adder is not in this group"
        return False, 'the user name you are trying to add is no exist'


def is_valid_group_name(group_name):
    '''
    check if the name of the group is valid.
    :param group_name: group name
    :return: return the name of the group if it according to the Instructions else return " ".
    '''
    if (len(group_name) >= 6) and len(group_name) <= 15:
        name = group_name.title()
        return name
    return ''


def create_group(data1):
    '''
    creates new group
    :param data1: data received from client include group name and user name.
    :return: True if the group can be created. False if the group can not be created.
    using functions:
    is_valid_group_name(group_name
    sum_groups()
    find_user(name)
    group_exists(name)
    insert_group(data)

    '''
    group_name = data1['group_name']
    print group_name
    user_name = data1['user_name']
    try:
        user = user_collection.find_one({'user_name': user_name})
        exist = find_user(user_name)
    except ConnectionFailure:
        return False, "There is a problem with the server comeback later"
    group_ids = user['group_ids']
    mongo_id = user['_id']
    if exist:
        name = is_valid_group_name(group_name)
        if not (name is ''):
            try:
                groupexist = group_exists(name)
            except ConnectionFailure:
                return False, "There is a problem with the server comeback later"
            if not (groupexist):
                data = {'group_name': name, 'group_id': str(sum_groups())}
                group_ids.append(data['group_id'])
                try:
                    db.user_collection.update({'_id': mongo_id}, {"$set": {'group_ids': group_ids}})
                    insert_group(data)
                except DuplicateKeyError or ConnectionFailure:
                    return False, "There is a problem with the server comeback later"
                return True, None
            return False, "can't accept it"
        return False, "can't accept it "
    return False, 'the user name that trying to create a group is not exist'


def log_out(data1):
    '''
    returns True or False if the user can logout.
    :param data1:data received from client include user name.
    :return:True or False if the user can logout.
    using functions:
    find_user(name)
    '''
    user_name = data1['user_name']
    try:
        user = user_collection.find_one({'user_name': user_name})
        finduser = find_user(user_name)
    except ConnectionFailure:
        return False, "There is a problem with the server comeback later"
    if finduser:
        return True
    else:
        return


def users_in_group(data1):
    """
    Returns a list of users in a group by given a group ID.
    :param data1:data received from client include user_name, group_id
    :return:True or False to indicate success,if True returns also a list of messages from a group given a group ID.
    else, also return reason.
    using functions:
    get_groups_user(name)
    find_user(user_name)
    find_users_groups(group_id)
    """
    result = False
    user_name = data1['user_name']
    group_id = data1["group_id"]
    try:
        exist = find_user(user_name)
        groups = get_groups_user(user_name)
    except ConnectionFailure:
        return False, "There is a problem with the server comeback later", None
    if exist:
        list_group = groups['groups']
        for group in list_group:
            if group[0] == group_id:
                result = True
        if result is True:
            try:
                users_list = find_users_groups(group_id)
            except ConnectionFailure:
                return False, "There is a problem with the server comeback later"
            return result, None, {'users_list': users_list}
        else:
            return False, 'You are not allowed to see the users list', None
    return False,  'You are not allowed to see the users list', None
