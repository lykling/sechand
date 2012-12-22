#-*- coding=utf-8 -*-
from secondhand.BasicViews import *
from secondhand.models import User,PhoneNumber

def ShowUser(request,user_id):
	loginuser = request.session.get('user')
	user=User.objects.get(id=user_id)
	errors = []
	if request.method == "GET" and request.GET.get('form_name') == "comment":
		return render_to_response('dialogform/comment_form.html', {
			'errors': [''],
			'loginuser': loginuser,
		},context_instance=RequestContext(request))
	if request.method == "POST" and request.POST.get('form_name') == 'comment':
		now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
		CommentUser.objects.create(
			commenttime = now,
			commenter_uid = loginuser.id,
			targetuser = user,
			content = request.POST.get('comment')
		)
		return render_to_response('dialogform/comment_form.html', {
			'errors': [],
			'loginuser': loginuser,
		},context_instance=RequestContext(request))
	#if request.method == 'GET' :
		#productid = request.GET.get('productid')
		#if productid :
			#try :
				#productid = int(productid)
			#except ValueError :
				#pass
				##logpack['reason'] += 'Invalid product_id.'
			#else :
				#pass
				##logpack['tbid'] = productid
		#key = request.GET.get('form_name')
		#if key == 'lend' :
			#return lend(request, flag='dialog')
	products = user.product_set.filter(valid=True).order_by('-addtime')[0:6]
	products1 = products[0:3]
	products2 = products[3:6]
	comments = user.commentuser_set.order_by('-commenttime')
	return render_to_response('user.html', {
		'isLogin': IsLogin(request),
		'reg_or_login': False,
		'loginuser': loginuser,
		'errors': errors,
		'tuser': user,
		'products1': products1,
		'products2': products2,
		'comments': comments,
	},context_instance=RequestContext(request))

def Login(request):
	if IsLogin(request):
		return HttpResponseRedirect('/index/')
	errors = []
	if request.method == "POST":
		loginform = {}
		loginform['username'] = request.POST.get('username')
		loginform['password'] = request.POST.get('password')
		try:
			user = User.objects.get(name=loginform['username'])
		except User.DoesNotExist:
			errors.append(u'user %s is not exist' % (loginform['username']))
		else:
			if user.pwd == md5(loginform['password']).hexdigest():
				request.session['user'] = user
				return HttpResponseRedirect('/index/')
			else:
				errors.append(u'password error!')
	return render_to_response('login.html', {
		'isLogin': IsLogin(request),
		'reg_or_login': True,
		'errors': errors,
	},context_instance=RequestContext(request))

def Register(request):
	if IsLogin(request):
		return HttpResponseRedirect('/index/')
	errors = []
	regform = {}
	if request.method == "POST":
		regform['username'] = request.POST.get('username')
		regform['password'] = request.POST.get('password')
		regform['conform'] = request.POST.get('conform')
		if checkRegister(regform, errors):
			user = User.objects.create(
				name=regform['username'],
				nick=regform['username'],
				pwd=md5(regform['password']).hexdigest(),
				address="",
				valid=True
			)
			return render_to_response('msg_redirect.html', {
				'message': u'注册成功',
			},context_instance=RequestContext(request))
	return render_to_response('register.html', {
		'isLogin': IsLogin(request),
		'reg_or_login': True,
		'errors': errors,
		'regform': regform,
	},context_instance=RequestContext(request))

def Logout(request):
	try :
		tpuser = request.session['user']
		del request.session['user']
		message = u"注销成功"
	except KeyError :
		message = u"你还没有登录"
	else :
		pass
	return render_to_response('msg_redirect.html', {
		'message': message,
	},context_instance=RequestContext(request))

def EditPro(request):
	loginuser = request.session.get('user')
	uid = request.POST.get('uid', 0)
	if loginuser.id != int(uid):
		return HttpResponseRedirect("/")
	elif request.POST.get('submit') == 'Save':
		address = request.POST.get('address')
		nick = request.POST.get('nick')
		loginuser.address = address
		loginuser.nick = nick
		loginuser.save()
		phones_old = loginuser.phonenumber_set.all()
		phones_new = list(set(request.POST.getlist('phone')))
		try:
			phones_new.remove("")
		except ValueError:
			pass
		mails_old = loginuser.mail_set.all()
		mails_new = list(set(request.POST.getlist('mail')))
		try:
			mails_new.remove("")
		except ValueError:
			pass
	 	phone_len_old = len(phones_old)
		phone_len_new = len(phones_new)
		mail_len_old = len(mails_old)
		mail_len_new = len(mails_new)
		if phone_len_old <= phone_len_new:
			for i in range(0, phone_len_old):
				phones_old[i].num = phones_new[i]
				phones_old[i].save()
			for i in range(phone_len_old, phone_len_new):
				PhoneNumber.objects.create(num = phones_new[i], user=loginuser)
		else:
			for i in range(0, phone_len_new):
				phones_old[i].num = phones_new[i]
				phones_old[i].save()
			for i in range(phone_len_new, phone_len_old):
				phones_old[i].num = ""
				phones_old[i].save()
		if mail_len_old <= mail_len_new:
			for i in range(0, mail_len_old):
				mails_old[i].num = mails_new[i]
				mails_old[i].save()
			for i in range(mail_len_old, mail_len_new):
				Mail.objects.create(address = mails_new[i], user=loginuser)
		else:
			for i in range(0, mail_len_new):
				mails_old[i].num = mails_new[i]
				mails_old[i].save()
			for i in range(mail_len_new, mail_len_old):
				mails_old[i].num = ""
				mails_old[i].save()
	return render_to_response('editpro.html', {
		'loginuser': loginuser,
		'reg_or_login': False,
		'tuser': loginuser,
	},context_instance=RequestContext(request))
