# -*- coding: utf-8 -*-
'''
A view function, or view for short, is simply a Python function that takes a Web request and returns a Web response.
This response can be the HTML contents of a Web page, or a redirect, or a 404 error, or an XML document or anything else.
The view itself contains whatever arbitrary logic is necessary to return that response.
A view function placed in views.py
'''
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
import chatroom.client#to use all the functions in the client script.


SERVER_PROVIDED_REASON = 'The server has provided this reason for the refusal: '
SERVER_PROVIDED_NO_REASON = 'The server hasn\'t provided any reason for the refusal.'


def apply_vars(resp, vars):
    '''
    Replaces so called variables in the response's content with values provided in vars.
    :param resp: The response to apply the dictionary to.
    :param vars: A dictionary of variable names and their values.
    :return: The edited response.
    '''
    for key in vars:
        resp.content = resp.content.replace(bytes(key, 'utf8'), bytes(vars[key], 'utf8'))
    return resp


def build_groups_html(group_list):
    '''
    :param group_list: A list of groups, as received from the server.
    :return: HTML for the group list.
    '''
    res = ''
    for group in group_list:
        res += '<li><a href="group?id=%s">%s</a></li>' % tuple(group)
    return res


def home(request):
    '''
    A Django view that returns the homepage via HTTP.
    :param request: The HTTP request received by Django.
    :return: The HTTP response to be sent to the browser.
    using functions:
    client.get_user_groups(user_name), apply_vars(resp, vars) , build_groups_html(group_list)
    '''
    if 'user_name' not in request.COOKIES:
        return render(request, 'home_no_user.html')
    else:
        res = chatroom.client.get_user_groups(request.COOKIES['user_name'])
        if not res[0]:
            return apply_vars(render(request, 'groups_failed.html'), {
                '%reason': (SERVER_PROVIDED_REASON + res[1]) if res[1] != '' else SERVER_PROVIDED_NO_REASON
            })
        else:
            return apply_vars(render(request, 'home_user.html'), {
                '%user_name': request.COOKIES['user_name'],
                '%groups': build_groups_html(res[1])
            })


@csrf_exempt
def userauth(request):
    '''
    A Django view that returns the home page if the login is successful if not, appears an adjusted page , via HTTP.
    :param request: A HTTP request with parameters for username and password.
    :return:The HTTP response to be sent to the browser.
    using functions:
    client.auth(action, user_name, password) , apply_vars(resp, vars)
    '''
    vars = request.POST if request.POST else request.GET
    res = chatroom.client.auth(vars['action'], vars['user_name'], vars['password'])
    if res[0]:
        resp = redirect('/home')
        resp.set_cookie('user_name', vars['user_name'])
        return resp
    else:
        return apply_vars(render(request, 'auth_failed.html'), {
            '%reason': (SERVER_PROVIDED_REASON + res[1]) if res[1] != '' else SERVER_PROVIDED_NO_REASON
        })


def auth(request):
    '''
    A Django view that returns the auth page via http.
    :param request: http request
    :return:The HTTP response to be sent to the browser.
    '''
    return render(request, 'auth_s.html')


def register(request):
    '''
    A Django view that returns the register page via http.
    :param request: http request
    :return:The HTTP response to be sent to the browser.
    '''
    return render(request, 'register.html')


def group(request):
    '''
    A Django view that returns the group page if the entrance to the group was successful.
     if not,  returns an adjusted page , via HTTP.
    :param request:A HTTP request with parameters for id group.
    :return:The HTTP response to be sent to the browser.
    using functions:
    client.get_group_name(id) , apply_vars(resp, vars)
    '''
    if 'id' not in request.GET:
        return render(request, 'group_no_id.html')
    res = chatroom.client.get_group_name(request.GET['id'])
    if not res[0]:
        return apply_vars(render(request, 'group_failed.html'), {
            '%reason': res[1]
        })
    return apply_vars(render(request, 'group.html'), {
        '%group_name': res[1],
        '%group_id': request.GET['id']
    })

@xframe_options_exempt
@csrf_exempt
def chat(request):
    '''
    A Django view that returns the chat page
     if not,  returns an adjusted page , via HTTP.
    :param request:A HTTP request with parameters for id group and user name.
    :return:The HTTP response to be sent to the browser.
    using functions:
    client.get_messages(id, user_name)  , apply_vars(resp, vars)
    '''

    if 'id' not in request.GET:
        return render(request, 'group_no_id.html')
    elif 'user_name' not in request.COOKIES:
        return redirect('/home')
    else:
        return apply_vars(render(request, 'chat.html'), {
            '%chat': chatroom.client.get_messages(request.GET['id'], request.COOKIES['user_name'])[1]
        })


@xframe_options_exempt
@csrf_exempt
def users_in_group(request):
    """
    A Django view that returns the users in group page
     if not,  returns an adjusted page , via HTTP.
    :param request:A HTTP request with parameters for id group and user name.
    :return:The HTTP response to be sent to the browser.
    using functions:
    client.users_in_group(id, user_name)  , apply_vars(resp, vars)
    """
    if 'id' not in request.GET:
        return render(request, 'group_no_id.html')
    elif 'user_name' not in request.COOKIES:
        return render(request, 'home_no_user.html')
    else:
        return apply_vars(render(request, 'users_in_group.html'), {
            '%inserted_list': chatroom.client.users_in_group(request.GET['id'], request.COOKIES['user_name'])[1]
        })


@csrf_exempt
def send_message(request):
    '''
    A Django view that returns the group page after sending a message
     if not,  returns an adjusted page , via HTTP.
    :param request:A HTTP request with parameters for id group and user name.
    :return:The HTTP response to be sent to the browser.
    using functions:
     client.send_message(id, user_name, msg) , apply_vars(resp, vars)
    '''
    if 'id' not in request.GET:
        return render(request, 'group_no_id.html')
    elif 'user_name' not in request.COOKIES:
        return redirect('/home')
    else:
        result = chatroom.client.send_message(request.GET['id'], request.COOKIES['user_name'], request.POST['message'])
        if result[0]:
            return redirect('/group?id=' + request.GET['id'])
        else:
            return apply_vars(render(request, 'send_failed.html'), {
                '%reason': result[1]
            })


def add_to_group(request):
    '''
    A Django view that returns the group page after adding user to the group
     if not,  returns an adjusted page , via HTTP.
    :param request:A HTTP request with parameters for id group and user name and the user the user name want to add.
    :return:The HTTP response to be sent to the browser.
    using functions:
    client.add_to_group(id, adder, addee) , apply_vars(resp, vars)
    '''
    if 'id' not in request.GET or 'addee' not in request.GET:
        return render(request, 'group_no_id.html')
    elif 'user_name' not in request.COOKIES:
        return redirect('/home')
    else:
        result = chatroom.client.add_to_group(request.GET['id'], request.COOKIES['user_name'], request.GET['addee'])
        if result[0]:
            return redirect('/group?id=' + request.GET['id'])
        else:
            return apply_vars(render(request, 'add_failed.html'), {
                '%reason': result[1]
            })


@csrf_exempt
def log_out(request):
    '''
    A Django view that returns the home_no_user page after logging out the user
    , via HTTP.
    :param request:A HTTP request with parameters for user name
    :return:The HTTP response to be sent to the browser.
    using function:
    client.log_out(user)
    '''
    resp = redirect('/home')
    if 'user_name' in request.COOKIES:
        chatroom.client.log_out(request.COOKIES['user_name'])
        resp.delete_cookie('user_name')
    return resp


@csrf_exempt
def create_group(request):
    '''
    A Django view that returns the group page after creating new group
     if not,  returns an adjusted page , via HTTP.
    :param request:A HTTP request with parameters for user name and group name.
    :return:The HTTP response to be sent to the browser.
    using functions:
    client.create_group(user_name, group_name), apply_vars(resp, vars)
    '''
    if 'group_name' not in request.GET:
        return render(request, 'group_no_name.html')
    elif 'user_name' not in request.COOKIES:
        return redirect('/home')
    else:
        result = chatroom.client.create_group(request.COOKIES['user_name'], request.GET['group_name'])
        if result[0]:
            return redirect('/home')
        else:
            return apply_vars(render(request, 'group_create_failed.html'), {
                '%reason': result[1]
            })
