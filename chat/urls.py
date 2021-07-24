"""chat URL Configuration
The `urlpatterns` list routes URLs to views.

Django lets you design URLs however you want, with no framework limitations.
To design URLs for an app, you create a Python module informally called a URLconf (URL configuration).
This module is pure Python code and is a mapping between URL path expressions to Python functions (views).
"""
from django.conf.urls import url
from django.contrib import admin
import chatroom.views# to use all the functions in the views script


urlpatterns = [
    url(r'^admin$', admin.site.urls),
    url(r'^$', chatroom.views.home),
    url(r'^home$', chatroom.views.home),
    url(r'^auth$', chatroom.views.auth),
    url(r'^register$', chatroom.views.register),
    url(r'^userauth$', chatroom.views.userauth),
    url(r'^group$', chatroom.views.group),
    url(r'^chat$', chatroom.views.chat),
    url(r'^users_in_group$', chatroom.views.users_in_group),
    url(r'^send_message', chatroom.views.send_message),
    url(r'^add_to_group', chatroom.views.add_to_group),
    url(r'^log_out', chatroom.views.log_out),
    url(r'^create_group', chatroom.views.create_group)
]
