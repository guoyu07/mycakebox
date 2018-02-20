# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Merchant
# Register your models here.

class MerchantAdmin(admin.ModelAdmin):
	list_display = [
		'merchant',
		'phone_number',
		'address'
	]
admin.site.register(Merchant, MerchantAdmin)