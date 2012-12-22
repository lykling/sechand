#-*- coding=utf-8 -*-
from secondhand.BasicViews import *

def index(request):
	errors = []
	loginform = {}
	loginuser = request.session.get('user')
	if request.method == "POST":
		loginform['username'] = request.POST.get('username')
		loginform['password'] = request.POST.get('password')
		try:
			user = User.objects.get(name=loginform['username'])
		except User.DoesNotExist:
			errors.append(u'user %s is not exist' % (loginform['username']))
		else:
			if user.pwd == md5(loginform['password']).hexdigest():
				request.session['user'] = user
				return render_to_response('msg_redirect.html', {
					'message': u'登录成功',
				},context_instance=RequestContext(request))
			else:
				errors.append(u'password error!')
	products = Product.objects.filter(valid=True).order_by('-addtime')[0:6]
	products1 = products[0:3]
	products2 = products[3:6]
	comments = CommentProduct.objects.all().order_by('-commenttime')[0:3]
	return render_to_response('index.html', {
		'isLogin': IsLogin(request),
		'reg_or_login': False,
		'errors': errors,
		'loginuser': loginuser,
		'tuser': loginuser,
		'products1': products1,
		'products2': products2,
		'comments': comments,
	},context_instance=RequestContext(request))

def ProductInfo(request, productid):
	loginuser = request.session.get('user')
	try:
		product = Product.objects.get(id=productid)
	except Product.DoesNotExist:
		return render_to_response('msg_redirect.html', {
			'isLogin': IsLogin(request),
			'reg_or_login': False,
			'loginuser': loginuser,
			'message': u'该产品不存在',
		},context_instance=RequestContext(request))
	if request.method == "GET" and request.GET.get('form_name') == "comment":
		return render_to_response('dialogform/comment_form.html', {
			'errors': [''],
			'loginuser': loginuser,
		},context_instance=RequestContext(request))
	if request.method == "POST" and request.POST.get('form_name') == 'comment':
		now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
		CommentProduct.objects.create(
			commenttime = now,
			commenter_uid = loginuser.id,
			targetproduct = product,
			content = request.POST.get('comment')
		)
		return render_to_response('dialogform/comment_form.html', {
			'errors': [],
			'loginuser': loginuser,
		},context_instance=RequestContext(request))
	if request.method == "POST":
		title = request.POST.get('title')
		descrip = request.POST.get('descrip')
		valid = request.POST.get('checkbox') == "True"
		now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
		product.valid = valid
		if not valid:
			product.closetime = now
		product.title = title
		product.descrip = descrip
		product.save()
	return render_to_response('productinfo.html', {
		'isLogin': IsLogin(request),
		'reg_or_login': False,
		'loginuser': loginuser,
		'product': product,
	},context_instance=RequestContext(request))

def Search(request):
	return HttpResponse("hello")

def AddProduct(request):
	loginuser = request.session.get('user')
	errors = []
	if request.method == "POST":
		title = request.POST.get('title')
		descrip = request.POST.get('descrip')
		now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
		Product.objects.create(
			valid = True,
			addtime = now,
			title = title,
			descrip = descrip,
			visits = 0,
			user = loginuser
		)
		return HttpResponseRedirect("/profile/%d" % (loginuser.id))
	return render_to_response('addproduct.html', {
		'isLogin': IsLogin(request),
		'reg_or_login': False,
		'errors': errors,
		'loginuser': loginuser,
	},context_instance=RequestContext(request))
