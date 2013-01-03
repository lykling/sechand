from django.db import models

# Create your models here.
class User(models.Model):
	name	= models.CharField(max_length=30)
	nick	= models.CharField(max_length=10)
	address	= models.CharField(max_length=100)
	pwd		= models.CharField(max_length=50)
	visits	= models.IntegerField(default=0)
	valid	= models.BooleanField(default=True)	
	def __unicode__(self):
		return '%s %s' %(self.nick,self.name)
	
	def FNNP(self):
		for i in self.phonenumber_set.all():
			if i.num:
				return i
		return None

	def FNNM(self):
		for i in self.mail_set.all():
			if i.address:
				return i
		return None

	class Admin:
		pass
#		list_display=('id','name','nick','valid')
#		ordering=('-id',)
#		search_fields=('id','name','nick',)


class PhoneNumber(models.Model):
	user	= models.ForeignKey(User)
	num		= models.CharField(max_length=12)
	def __unicode__(self):
		return self.num

	class Admin:
		pass
#		list_display=('user','num')
#		ordering=('user',)
#		search_fields=('user','num',)

class Mail(models.Model):
	user	= models.ForeignKey(User)
	address	= models.CharField(max_length=50)
	
	def __unicode__(self):
		return self.address
	class Admin:
		pass
#		list_display=('user','address')
#		ordering=('user',)
#		search_fields=('user','address',)

class Product(models.Model):
	addtime		= models.DateTimeField()
	closetime	= models.DateTimeField(null=True)
	title		= models.CharField(max_length=50)
	descrip		= models.CharField(max_length=1000)
	visits		= models.IntegerField(default=0)
	user		= models.ForeignKey(User)
	valid		= models.BooleanField(default=True)	
	def __unicode__(self):
		return self.title
	class Admin:
		pass
#		list_display=('user','title','valid')
#		ordering=('user',)
#		search_fields=('user','title',)

class CommentUser(models.Model):
	commenttime		= models.DateTimeField()
	commenter_uid	= models.IntegerField(null=False)
	targetuser		= models.ForeignKey(User)
	content			= models.CharField(max_length=1000)
	def getCommenter(self):
		try:
			user = User.objects.get(id = self.commenter_uid)
		except User.DoesNotExist:
			return None
		return user
	class Meta:
		ordering = ['-commenttime']
	class Admin:
		pass

class CommentProduct(models.Model):
	commenttime		= models.DateTimeField()
	commenter_uid	= models.IntegerField(null=False)
	targetproduct	= models.ForeignKey(Product)
	content			= models.CharField(max_length=1000)
	def getCommenter(self):
		try:
			user = User.objects.get(id = self.commenter_uid)
		except User.DoesNotExist:
			return None
		return user
	class Meta:
		ordering = ['-commenttime']
	class Admin:
		pass
