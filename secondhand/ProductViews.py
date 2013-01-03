#-*- coding=utf-8 -*-
from secondhand.BasicViews import *

def index(request):
	errors = []
	loginform = {}
	loginuser = request.session.get('user')
	if request.method == "POST":
		loginform['username'] = u'%s' % (request.POST.get('username'))
		loginform['password'] = request.POST.get('password')
		try:
			user = User.objects.get(name=loginform['username'])
		except User.DoesNotExist:
			errors.append(u'user %s is not exist' % (loginform['username']))
		else:
			if user.pwd == md5(loginform['password']).hexdigest():
				request.session['user'] = user
				return render_to_response('msg_redirect.html', {
					'turl': '/index/',
					'timeout': '1000',
					'isLogin': IsLogin(request),
					'reg_or_login': False,
					'loginuser': loginuser,
					'message': u'登录成功',
				},context_instance=RequestContext(request))
			else:
				errors.append(u'password error!')
	products = Product.objects.filter(valid=True).order_by('-addtime')[0:6]
	products1 = products[0:3]
	products2 = products[3:6]
	comments = CommentProduct.objects.all().order_by('-commenttime')[0:6]
	commentFilter(comments)
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
	errors = []
	try:
		product = Product.objects.get(id=productid)
	except Product.DoesNotExist:
		return render_to_response('msg_redirect.html', {
			'turl': '/index/',
			'timeout': '1000',
			'isLogin': IsLogin(request),
			'reg_or_login': False,
			'loginuser': loginuser,
			'message': u'该商品不存在',
		},context_instance=RequestContext(request))
	if request.method == "GET" and request.GET.get('form_name') == "comment":
		return render_to_response('dialogform/comment_form.html', {
			'errors': [''],
			'loginuser': loginuser,
		},context_instance=RequestContext(request))
	if request.method == "POST" and request.POST.get('form_name') == 'comment':
		content = u'%s' % (request.POST.get('comment', ''))
		now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
		CommentProduct.objects.create(
			commenttime = now,
			commenter_uid = loginuser.id,
			targetproduct = product,
			content = content,
		)
		return render_to_response('dialogform/comment_form.html', {
			'errors': errors,
			'loginuser': loginuser,
		},context_instance=RequestContext(request))
	if request.method == "POST":
		title = u'%s' % (request.POST.get('title'))
		descrip = u'%s' % (request.POST.get('descrip'))
		valid = request.POST.get('checkbox') == "True"
		now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
		product.valid = valid
		if not valid:
			product.closetime = now
		product.title = title
		product.descrip = descrip
		product.save()
		image = request.FILES.get('image', None)
		if image:
			path = "/var/www/se/secondhand/media"
			destination = open("%s/%d_%d" % (path, loginuser.id, product.id), 'wb+')
			for chunk in image.chunks():
				destination.write(chunk)
			destination.close()
			thumb_name = "%s/%d_%d_s" % (path, loginuser.id, product.id)
			Thumbnail("%s/%d_%d" % (path, loginuser.id, product.id), 300, 200, thumb_name)
	product.visits += 1
	product.save()
	comments = product.commentproduct_set.order_by('-commenttime')
	commentFilter(comments)
	number_per_page = 5
	page = Page()
	page.head = 1
	page.curr = int(request.POST.get('page',1))
	page.tail = (len(comments) - 1) / number_per_page + 1
	return render_to_response('productinfo.html', {
		'isLogin': IsLogin(request),
		'reg_or_login': False,
		'loginuser': loginuser,
		'product': product,
		'comments': comments,
		'page': page,
	},context_instance=RequestContext(request))

def Search(request):
	loginuser = request.session.get('user')
	query = request.GET.get('query', '')
	name = request.GET.get('user_name', '')
	errors = []
	if not name:
		products = Product.objects.filter(Q(title__icontains = query)).order_by('-visits')
	else:
		try:
			tuser = User.objects.get(name=name)
		except User.DoesNotExist:
			errors.append(u"无此用户")
			return render_to_response('search.html', {
				'isLogin': IsLogin(request),
				'reg_or_login': False,
				'loginuser': loginuser,
				'query': query,
				'user_name': name,
				'products': [],
			},context_instance=RequestContext(request))
		else:
			products = Product.objects.filter(Q(title__icontains = query) & Q(user = tuser)).order_by('-visits')
	number_per_page = 6
	page = Page()
	page.head = 1
	page.tail = (len(products) - 1) / number_per_page + 1
	page.curr = request.GET.get('page', 1)
	page.curr = int(page.curr)
	return render_to_response('search.html', {
		'isLogin': IsLogin(request),
		'reg_or_login': False,
		'loginuser': loginuser,
		'products': products[(page.curr - 1) * number_per_page: page.curr * number_per_page],
		'products_all': products,
		'user_name': name,
		'query': query,
		'page': page
	},context_instance=RequestContext(request))

def AddProduct(request):
	loginuser = request.session.get('user')
	errors = []
	if request.method == "POST":
		title = u'%s' % (request.POST.get('title'))
		descrip = u'%s' % (request.POST.get('descrip'))
		now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
		product = Product.objects.create(
			valid = True,
			addtime = now,
			title = title,
			descrip = descrip,
			visits = 0,
			user = loginuser
		)
		image = request.FILES.get('image', None)
		if image:
			path = "/var/www/se/secondhand/media"
			destination = open("%s/%d_%d" % (path, loginuser.id, product.id), 'wb+')
			for chunk in image.chunks():
				destination.write(chunk)
			destination.close()
			thumb_name = "%s/%d_%d_s" % (path, loginuser.id, product.id)
			Thumbnail("%s/%d_%d" % (path, loginuser.id, product.id), 200, 139, thumb_name)
		return HttpResponseRedirect("/profile/%d/" % (loginuser.id))
	return render_to_response('addproduct.html', {
		'isLogin': IsLogin(request),
		'reg_or_login': False,
		'errors': errors,
		'loginuser': loginuser,
	},context_instance=RequestContext(request))
