from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.validators import RegexValidator

class DeviceAndClientIp(models.Model):
	reader_ip = models.GenericIPAddressField(default=None)
	reader_port = models.IntegerField(default=None)
	client_ip = models.GenericIPAddressField(default=None)
	def __str__(self):
		return str("Device IP : "+ self.client_ip + "   Reader IP : "+self.reader_ip)
	def __unicode__(self):
		return str("Device IP : "+ self.client_ip + "   Reader IP : "+self.reader_ip)
	class Meta:
		 verbose_name_plural = "Device IPs and ReaderIPs"

class MyUserManager(BaseUserManager):
	def create_user(self, username ,email, password=None):
		if not email:
			raise ValueError('Users must have an email address')
		user = self.model(
			username = username,
			email=self.normalize_email(email),
		)
		user.set_password(password)
		user.save(using=self._db)
		return user
	def create_superuser(self, email, username, password):
		user = self.create_user(
			username,
			email,
			password=password,
		)
		user.is_admin = True
		user.is_staff = True
		user.save(using=self._db)
		return user
username_regex = '^[a-zA-Z0-9.@+-]*$'
class MyUser(AbstractBaseUser):
	username = models.CharField(max_length=20, validators=[
		RegexValidator(
			regex=username_regex,
			message='Username must be alphanumberic containing +-*.',
			code= 'Invalid Username'
		)],
								unique=True
	)
	email = models.EmailField(verbose_name="Email Address",
							  max_length=100,
							  unique=True)
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)
	objects = MyUserManager()
	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['username']
	def get_full_name(self):
		return self.email
	def get_short_name(self):
		return self.email
	def __str__(self):
		return self.username
	def __unicode__(self):
		return self.username
	def has_perm(self, perm, obj=None):
		return True
	def has_module_perms(self, app_label):
		return True
	class Meta:
		verbose_name_plural = "Users"