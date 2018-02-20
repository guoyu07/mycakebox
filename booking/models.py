# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import requests
import simplejson
from django.db import models
from merchant.models import Merchant
from customer.models import Customer
from rider.models import Rider
from django.conf import settings
from django.core.urlresolvers import reverse
# Create your models here.

DELIVERY_TYPE = (
		("Normal", "Normal"),
		("Jet", "Jet"),
		("Superjet", "Superjet"),
	)

STATUS_CHOICES = (
		("Pending", "Pending"),
		("Confirmed", "Confirmed"),
		("Shipped","Shipped"),
		("Complete", "Complete"),
		("Cancelled", "Cancelled"),
		("Ready to Pick", "Ready to Pick"),
	)
	
try:
	tax_rate = settings.DEFAULT_TAX_RATE
except Exception, e:
	print str(e)
	raise NotImplementedError(str(e))

class Booking(models.Model):
	booking_id = models.CharField(max_length=10, default='ABC', unique=True)
	merchant = models.ForeignKey(Merchant, null=True, blank=True)
	customer = models.ForeignKey(Customer, null=True, blank=True)
	rider = models.ForeignKey(Rider, null=True, blank=True)
	cake_cost = models.CharField(max_length=100)
	cake_weight = models.CharField(max_length=100)
	instructions = models.TextField(default="")
	origin = models.TextField(default="")
	origin_locality = models.CharField(max_length=100, default="")
	pickup_date = models.CharField(max_length=50, default=0)
	pickup_time = models.CharField(max_length=50, default=0)
	drop_date = models.CharField(max_length=50, default=0)
	drop_time = models.CharField(max_length=50, default=0)
	destination = models.TextField(default="")
	destination_locality = models.CharField(max_length=100, default="")
	duration = models.CharField(max_length=100)
	distance = models.CharField(max_length=100)
	approx_total = models.CharField(max_length=50, default=0)
	discount_total = models.CharField(max_length=50, default=0)
	sub_total = models.CharField(max_length=50, default=0)
	final_total = models.CharField(max_length=50)
	approve = models.BooleanField(default=False)
	delivery_type = models.CharField(max_length=120, choices=DELIVERY_TYPE, default="Normal")
	status = models.CharField(max_length=120, choices=STATUS_CHOICES, default="Pending")
	notify_merchant = models.BooleanField(default=False)
	notify_rider = models.BooleanField(default=False)

	def __unicode__(self):
		return self.booking_id

	def get_absolute_url(self):
		return reverse("merchant_dashboard:booking_details", kwargs={"booking_id": self.booking_id})

	def get_final_amount(self):
		instance = Booking.objects.get(id=self.id)
		two_places = Decimal(10) ** -2
		sub_total_dec = instance.sub_total
		discount_total_dec = instance.discount_total
		tax_total_dec = Decimal(tax_rate_dec * sub_total_dec).quantize(two_places)
		instance.tax_total = tax_total_dec
		instance.final_total = sub_total_dec - discount_total_dec + tax_total_dec
		instance.save()
		return instance.final_total
