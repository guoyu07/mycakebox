# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from customer.models import Customer
# Create your models here.
STATUS = (
		("Enabled", "Enabled"),
		("Disabled", "Disabled"),
	)

# Create your models here.
class Merchant(models.Model):
	"""docstring for Merchant"""
	merchant = models.ForeignKey(User, blank=True, null=True)
	phone_number = models.CharField(max_length=15, default="")
	image = models.ImageField(upload_to='baker/images/', default="baker/default.jpg")
	customer = models.ManyToManyField(Customer, blank=True)
	address = models.CharField(max_length=100, blank=True, null=True)
	locality = models.CharField(max_length=100, blank=True, null=True)
	mou_signed_on = models.DateField('Date', default="2017-06-06")
	status = models.CharField(max_length=100, choices=STATUS, default="Disabled")
	slug = models.SlugField(unique=True, default="")
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __unicode__(self):
		return "Merchant - %s" %(self.merchant)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.merchant)
		super(Merchant, self).save(*args, **kwargs)


