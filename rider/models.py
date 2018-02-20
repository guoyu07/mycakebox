# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from .utils import rider_id_generator
# Create your models here.

FLAGS = (
		("GREEN", "GREEN"),
		("GREEN", "GREEN"),
		("RED", "RED"),
	)

class Rider(models.Model):
	rider = models.ForeignKey(User, blank=True, null=True)
	address = models.CharField(max_length=100)
	locality = models.CharField(max_length=100)
	phone_number = models.CharField(max_length=15)
	alt_phone_number = models.CharField(max_length=15, blank=True, null=True)
	flag = models.CharField(max_length=100, choices=FLAGS, default="RED")
	slug = models.SlugField(unique=True, default="")

	def __unicode__(self):
		return "%s %s" %(self.first_name, self.last_name)

	def save(self, *args, **kwargs):
		self.rider_id = rider_id_generator(self)
		self.slug = self.rider_id
		super(Rider, self).save(*args, **kwargs)
