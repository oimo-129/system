# -*- coding: utf-8 -*-

from django.urls import path, include

from .views import *


app_name = 'user'
urlpatterns = [

    path('userinfo/', UserInfoView.as_view(), name='userinfo'),

    path('list/', ShowDep.as_view(), name='list'),

    path('need/', UserInfoNeed.as_view(), name='need'),


]