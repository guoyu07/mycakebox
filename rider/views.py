# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
def rider_details(request, rider_id):
	rider = get_object_or_404(Rider, rider_id=rider_id)
	context = {

	}
	template = "rider/rider_details.html"
	return render(request, context)