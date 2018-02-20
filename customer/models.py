# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.
class Customer(models.Model):
	customer_id = models.CharField(max_length=10, default='ABC', unique=True)
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	address = models.CharField(max_length=100)
	locality = models.CharField(max_length=100)
	phone_number = models.CharField(max_length=15, default='9766526943', unique=True)
	alt_phone_number = models.CharField(max_length=15, blank=True, null=True)

	def __unicode__(self):
		return "%s %s - %s" %(self.first_name, self.last_name, self.phone_number)

	def get_full_name(self):
		return "%s %s"%(self.first_name, self.last_name)

