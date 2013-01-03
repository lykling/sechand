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
import Image
import pytz
import time
import re
import os

class Page:
	curr = 1 
	head = 1 
	tail = 1 
	def range(self):
		return range(self.head, self.tail + 1)
	def prev(self):
		if self.curr - 1 > self.tail:
			return self.tail
		return self.curr - 1
	def next(self):
		if self.curr + 1 < self.head:
			return self.head
		return self.curr + 1
	def __unicode__(self):
		return self.curr

def IsLogin(request) :
    return bool(request.session.get('user'))

def LoginRequired(view):
    def new_view(request, *args, **kwargs):
        if not IsLogin(request):
            return HttpResponseRedirect('/login/')
        return view(request, *args, **kwargs)
    return new_view

def checkContent(content, errors):
    string_tmp = content
    strinfo = re.compile(u'(?: |\n)')
    string_tmp = strinfo.sub(u'', string_tmp)
    if len(string_tmp) < 10 :
        errors.append(u'字数不得少于10')
    return (not errors)

def commentFilter(comments):
	for comment in comments :
		strinfo = re.compile(u'(?:\\bC\W*a\W*o\\b|(C\W*a\W*o){2,}|(f\W*u\W*c\W*k){2,})|\\bf\W*u\W*c\W*k\\b', re.I)
		comment.content = strinfo.sub(u'-=我不该说脏话=-', comment.content)
		strinfo = re.compile(u'(?:傻\W*逼|S\W*B)', re.I)
		comment.content = strinfo.sub(u'**', comment.content)

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

def Thumbnail(file, width, height, path):
	image = Image.open(file)
	image.convert('RGB')
	image.thumbnail((width,height),Image.ANTIALIAS)
	image.save(path,image.format)

def GetPic(request):
	pid = request.GET.get('pid', 0)
	uid = request.GET.get('uid', 0)
	size = request.GET.get('size', 'small')
	path = '/var/www/se/secondhand/media'
	if size == "big":
		filename = "%s_%s" % (uid, pid)
	else:
		filename = "%s_%s_s" % (uid, pid)
	if os.path.exists(u'%s/%s' % (path, filename)):
		image = open(u'%s/%s' % (path, filename), 'r')
		Cimage = Image.open(u'%s/%s' % (path, filename))
		return HttpResponse(image, mimetype=Cimage.format)
	else:
		image = open(u'%s/%s' % (path, 'default_s.png'), 'r')
		Cimage = Image.open(u'%s/%s' % (path, 'default.png'))
		return HttpResponse(image, mimetype=Cimage.format)

def GetComments(request):
	number_per_page = 5
	page = Page()
	page.head = 1
	page.curr = int(request.POST.get('page',1))
	if request.POST.get('flag', '') == 'user':
		tuid = int(request.POST.get('tuid'))
		cuid = int(request.POST.get('cuid'))
		comments = CommentUser.objects.filter(commenter_uid=cuid, targetuser=User.objects.get(id=tuid))
		page.tail = (len(comments) - 1) / number_per_page + 1
	elif request.POST.get('flag', '') == 'product':
		tpid = int(request.POST.get('tpid'))
		cuid = int(request.POST.get('cuid'))
		comments = CommentProduct.objects.filter(commenter_uid=cuid, targetproduct=Product.objects.get(id=tpid))
		page.tail = (len(comments) - 1) / number_per_page + 1
	if not page.tail:
		return render_to_response('comments.html', {
			'page': page,
		},context_instance=RequestContext(request))
	commentFilter(comments)
	return render_to_response('comments.html', {
		'comments': comments[(page.curr - 1) * number_per_page: page.curr * number_per_page],
		'comments_all': comments,
		'page': page,
	},context_instance=RequestContext(request))
