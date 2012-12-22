#-*- coding=utf-8 -*-
from django.core.serializers import serialize,deserialize
from django.shortcuts import render_to_response
from django.template import loader, Context, RequestContext
from django.contrib import admin
from django.utils import simplejson
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.db import connections
from secondhand.models import *
from random import randint
from md5 import md5
import datetime
import MySQLdb
import string
import random
import pytz
import time
import re
import os

def IsLogin(request) :
    return bool(request.session.get('user'))

def LoginRequired(view):
    def new_view(request, *args, **kwargs):
        if not IsLogin(request):
            return HttpResponseRedirect('/login/')
        return view(request, *args, **kwargs)
    return new_view

def checkRegister(regform, errors):
	invalidchar = "`,./?\\|\'\";:{[<(]}*&^%$@!~+=-"
	if not regform['username']:
		errors.append(u'请输入帐号。')
	else :
		for c in regform['username']:
			if c in invalidchar :
				errors.append(u'用户名包含非法字符')
				break
		try:
			tpuser = User.objects.get(name=regform['username'])
		except User.DoesNotExist:
			pass
		else:
			errors.append(u'user %s existed!' % (tpuser.name))
	if not regform['password']:
		errors.append(u'请输入密码。')
	if not regform['conform']:
		errors.append(u'请输入校验密码。')
	if regform['password'] != regform['conform']:
		errors.append(u'两次输入的密码不相同')
	return (not errors)
