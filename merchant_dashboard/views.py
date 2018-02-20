# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# imports
import urllib
import requests
import simplejson
import googlemaps
import math
# 
from datetime import datetime, date
from django.http import JsonResponse, Http404
from django.shortcuts import render, get_object_or_404, HttpResponse, HttpResponseRedirect
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
# models
from merchant.models import Merchant
from customer.models import Customer
from booking.models import Booking
# Forms
from merchant.forms import LoginForm
# utils
from customer.utils import customer_id_generator
from booking.utils import booking_id_generator
# 3rd party
from googlemaps import convert
from django_datatables_view.base_datatable_view import BaseDatatableView
# Create your views here.
gmaps = googlemaps.Client(key='AIzaSyBqutK-8jg1lEcs9_AFCKDMsLYUWA9QYag')


def merchant_logout(request):
	logout(request)
	return HttpResponseRedirect("/dashboard/merchant/login/")

def merchant_login(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect("/dashboard/merchant")
	
	form = LoginForm(request.POST or None)
	btn = "Login"
	if form.is_valid():
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		user = authenticate(username=username, password=password)
		login(request, user)
		messages.success(request, "Successfully Logged In. Welcome Back!")
		return HttpResponseRedirect("/dashboard/merchant/")
	context = {
		"form": form,
		"submit_btn": btn,
	}
	return render(request, "merchant_dashboard/login.html", context)


@login_required(login_url='/dashboard/merchant/login/')
def index(request):
	merchant = get_object_or_404(Merchant, merchant=request.user, status="Enabled")
	bookings = Booking.objects.filter(merchant=merchant)
	upcoming_bookings = bookings.exclude(status="Complete")
	template = "merchant_dashboard/index.html"
	context = {
		"page_title" : "Dashboard - Book Cake Delivery in minutes",
		"merchant": merchant,
		"bookings": bookings,
		"total_bookings_count": bookings.count(),
		"upcoming_bookings" : upcoming_bookings,
		"upcoming_bookings_count": upcoming_bookings.count(),
		"recent_customer_list": merchant.customer.all()[:8],
		"total_confirmed_count": bookings.filter(status="Confirmed").count(),
		"total_cancelled_count": bookings.filter(status="Cancelled").count(),
		"total_complete_count": bookings.filter(status="Complete").count(),
		"total_pending_count": bookings.filter(status="Pending").count(),
		"total_shipped_count": bookings.filter(status="Shipped").count(),
		"total_ready_to_pick_count": bookings.filter(status="Ready to Pick").count(),

	}
	return render(request, template, context)

@login_required(login_url='/dashboard/merchant/login/')
def fetch_customer_data(request, customer_id):
	
	""" This will return individual customer data based on customer_id """

	customer_data = {}
	if request.is_ajax:
		get_customer = get_object_or_404(Customer, customer_id=customer_id)
		customer_data['customer_first_name'] = get_customer.first_name
		customer_data['customer_last_name'] = get_customer.last_name
		customer_data['customer_phone'] = get_customer.phone_number
		customer_data['customer_address'] = get_customer.address
		customer_data['customer_locality'] = get_customer.locality
	return JsonResponse(customer_data)


@login_required(login_url='/dashboard/merchant/login/')
def book_delivery(request):
	
	""" This method will create booking and customer instances """

	merchant = get_object_or_404(Merchant, merchant=request.user)
	distance_data = {}
	if request.method == "POST" and request.is_ajax:
		if 'cost_of_cake' not in request.POST:
			cost_of_cake = 0
		else:
			cost_of_cake = request.POST['cost_of_cake']

		if 'weight_of_cake' not in request.POST:
			weight_of_cake = 0
		else:
			weight_of_cake = request.POST['weight_of_cake']

		if 'customer_first_name' not in request.POST:
			customer_first_name = 0
		else:
			customer_first_name = request.POST['customer_first_name']

		if 'customer_last_name' not in request.POST:
			customer_last_name = 0
		else:
			customer_last_name = request.POST['customer_last_name']

		if 'customer_address' not in request.POST:
			customer_address = 0
		else:
			customer_address = request.POST['customer_address']

		if 'customer_locality' not in request.POST:
			customer_locality = 0
		else:
			customer_locality = request.POST['customer_locality']

		if 'customer_phone' not in request.POST:
			customer_phone = 0
		else:
			customer_phone = request.POST['customer_phone']

		if 'customer_alt_phone' not in request.POST:
			customer_alt_phone = 0
		else:
			customer_alt_phone = request.POST['customer_alt_phone']

		if 'instruction' not in request.POST:
			instruction = 0
		else:
			instruction = request.POST['instruction']

		if 'booking_id' not in request.POST:
			booking_id = "ASDFFEKKDS"
		else:
			booking_id = request.POST['booking_id']

		if 'pickup_date' not in request.POST:
			pickup_date = "EKKDS"
		else:
			pickup_date = request.POST['pickup_date']

		if 'pickup_time' not in request.POST:
			pickup_time = "EKKDS"
		else:
			pickup_time = request.POST['pickup_time']

		if 'drop_date' not in request.POST:
			drop_date = "EKKDS"
		else:
			drop_date = request.POST['drop_date']

		if 'drop_time' not in request.POST:
			drop_time = "EKKDS"
		else:
			drop_time = request.POST['drop_time']

		distancematrix_result = gmaps.distance_matrix(merchant.address, customer_locality)
		
		# try to find existing customer, if not then create new.
		try:
			customer = get_object_or_404(Customer, phone_number=customer_phone)
		except:
			customer = Customer.objects.create(merchant=merchant, customer_id=customer_id_generator())
			customer.first_name = customer_first_name
			customer.last_name = customer_last_name
			customer.address = customer_address
			customer.locality = customer_locality
			customer.phone_number = customer_phone
			customer.alt_phone_number = customer_alt_phone
			customer.save()

		# Add customer instance to merchant model
		merchant.customer.add(customer)
		merchant.save()

		# try to find existing booking, if not then create new.
		try:
			booking = get_object_or_404(Booking, booking_id=booking_id)
		except:
			booking = Booking.objects.create(merchant=merchant, booking_id=booking_id_generator())
			booking.customer = customer
			booking.cake_cost = cost_of_cake
			booking.cake_weight = weight_of_cake
			booking.instruction = instruction
			booking.origin = merchant.address
			booking.destination = customer.address
			booking.destination_locality = distancematrix_result['destination_addresses'][0]
			booking.duration = distancematrix_result['rows'][0]['elements'][0]['duration']['text']
			booking.distance = distancematrix_result['rows'][0]['elements'][0]['distance']['text']
			booking.pickup_date = pickup_date
			booking.drop_date = drop_date
			booking.save()

		# create variables to calculate various approx delivery cost.
		approx_total_normal = 0
		approx_total_jet = 0
		approx_total_superjet = 0
		rate_normal = 0
		rate_jet = 0
		rate_superjet = 0
		first = booking.distance.split()
		# if the distance is less than 10km. then choose delivery option as hyperlocal /
		# else choose the delivery option as long distance
		if float(first[0]) <= 10.0:
			delivery_type = "Hyperlocal"
			if float(first[0]) < 3.0:
				approx_total_normal = 60
			else:
				approx_total_normal = 60+((float(first[0])-3.0)*12)
			rate_normal = "Rs. 60.0 for 3.0 km, Rs. 12.0/km afterthat upto 10.0 km."
		elif float(first[0]) > 10.0:
			delivery_type = "Long distance"
			approx_total_jet = 200
			# for distance upto 5km flat Rs. 250 post 5km add Rs.15/km
			if float(first[0]) < 5.0:
				approx_total_superjet = 250
			else:
				approx_total_superjet = 250+((float(first[0])-5.0)*15)
			rate_jet = "Rs. 200.0 flat (Public means of transport will be used)."
			rate_superjet = "Rs. 250.0 for 5.0 km, Rs. 15.0/km afterthat."

		distance_data['booking_id'] = booking.booking_id
		distance_data['cake_cost'] = booking.cake_cost
		distance_data['cake_weight'] = booking.cake_weight
		distance_data['customer'] = "%s %s" %(booking.customer.first_name, booking.customer.last_name)
		distance_data['customer_phone'] = "%s / %s" %(booking.customer.phone_number, booking.customer.alt_phone_number)
		distance_data['origin'] = booking.origin
		distance_data['destination'] = "%s, %s" %(booking.destination, booking.destination_locality)
		distance_data['pickupDateTime'] = booking.pickup_date
		distance_data['dropDateTime'] = booking.drop_date
		distance_data['distance'] = booking.distance
		distance_data['duration'] = booking.duration
		distance_data['instruction'] = booking.instruction
		distance_data['delivery_type'] = delivery_type
		distance_data['rate_normal'] = rate_normal
		distance_data['rate_jet'] = rate_jet
		distance_data['rate_superjet'] = rate_superjet
		distance_data['approx_total_normal'] = math.ceil(approx_total_normal)
		distance_data['approx_total_jet'] = math.ceil(approx_total_jet)
		distance_data['approx_total_superjet'] = math.ceil(approx_total_superjet)
	
	return JsonResponse(distance_data)


@login_required(login_url='/dashboard/merchant/login/')
def confirm_booking_details(request):
	
	""" This method will confirm the booking """

	confirmation_data = {}
	if request.POST and request.is_ajax:
		if 'booking_id' not in request.POST:
			booking_id = "Normal"
		else:
			booking_id = request.POST['booking_id']

		if 'delivery_type' not in request.POST:
			delivery_type = "Normal"
		else:
			delivery_type = request.POST['delivery_type']

		if 'approx_total' not in request.POST:
			approx_total = "60"
		else:
			approx_total = request.POST['approx_total']

		booking = get_object_or_404(Booking, booking_id=booking_id)
		booking.delivery_type = delivery_type
		booking.approx_total = approx_total
		booking.save()
		confirmation_data['success'] = "True"
		messages.success(request, "Your booking id " +
						 booking_id + " is submitted successfully.")
		print confirmation_data
		return JsonResponse(confirmation_data)
	confirmation_data['success'] = "False"
	print confirmation_data
	return JsonResponse(confirmation_data)


def cancel_booking(request, booking_id):
	
	""" this method will cancel the booking """

	booking = get_object_or_404(Booking, booking_id=booking_id)
	cancellation_data = {}
	if request.is_ajax:
		booking.instruction = "Booking cancelled by merchant"
		booking.status = "Cancelled"
		booking.save()
		cancellation_data['success'] = "True"
		return JsonResponse(cancellation_data)
	cancellation_data['success'] = "False"
	return JsonResponse(cancellation_data)

@login_required(login_url='/dashboard/merchant/login/')
def booking_list(request):
	template = "merchant_dashboard/booking/booking_list.html"
	context = {
		"page_title": "Merchant Booking List",
	}
	return render(request, template, context)

class BookingListByMerchantJson(BaseDatatableView):
	columns = ['booking_id', 'customer', 'customer phone', 'drop address', 'rider', 'pickup date', 'drop date', 'status', 'action']
	order_columns = ['booking_id', 'customer', 'customer phone', 'drop address', 'rider', 'status', 'action']
	max_display_length = 500

	def get_initial_queryset(self):
		merchant = get_object_or_404(Merchant, merchant=self.request.user)
		return Booking.objects.filter(merchant=merchant)

	def render_column(self, row, column):
		if column == 'booking_id':
			return row.booking_id
		elif column == 'customer':
			return row.customer.get_full_name()
		elif column == 'customer phone':
			return row.customer.phone_number
		elif column == 'drop address':
			return '%s , %s' %(row.destination, row.destination_locality)
		elif column == 'pickup date':
			return row.pickup_date
		elif column == 'drop date':
			return row.drop_date
		elif column == 'status':
			return row.status
		elif column == 'action':
			booking_id = row.booking_id
			return '<a href="/dashboard/merchant/booking_details/'+booking_id+'"> View More</a>'
		else:
			return super(BookingListByMerchantJson, self).render_column(row, column)

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super(BookingListByMerchantJson, self).dispatch(request, *args, **kwargs)

@login_required(login_url='/merchant/login')
def booking_details(request, booking_id):
	
	""" this method will return individual booking details """

	booking = get_object_or_404(Booking, booking_id=booking_id)
	now = datetime.now
	distancematrix_result = gmaps.directions(booking.origin_locality, booking.destination_locality)
	print distancematrix_result
	steps = []
	# for item in distancematrix_result['routes'][0]['legs'][0]['steps']:
	# 	steps.append("via:enc:" + item['polyline']['points'] + ":|")

	template = "merchant_dashboard/booking/booking_details.html"
	context = {
		"page_title": "Booking Details for " + str(booking_id),
		"booking_id": booking_id,
		"booking": booking,
		"steps": steps
	}
	return render(request, template, context)

def pie_data(request):
	
	""" This method is to return order_status_count in jsonResponse """

	pie_data = []
	pie_items = {"Complete", "Cancelled", "Pending", "Shipped", "Confirmed", "Ready to Pick"}
	total_confirmed_count = Booking.objects.filter(status="Confirmed").count()
	total_cancelled_count = Booking.objects.filter(status="Cancelled").count()
	total_complete_count = Booking.objects.filter(status="Complete").count()
	total_pending_count = Booking.objects.filter(status="Pending").count()
	total_shipped_count = Booking.objects.filter(status="Shipped").count()
	total_ready_to_pick_count = Booking.objects.filter(status="Ready to Pick").count()

	for item in pie_items:
		if item == "Complete":
			pie_data.append(
					{
						'name': 'Complete',
						'y': total_complete_count,
						'sliced':'true',
						'selected':'true',
						'color': '#00a65a',
					}
				)
		elif item == "Cancelled":
			pie_data.append(
					{
						'name': 'Cancelled',
						'y': total_cancelled_count,
						'color': '#dd4b39',
					}
				)
		elif item == "Pending":
			pie_data.append(
					{
						'name': 'Pending',
						'y': total_pending_count,
						'color': '#d2d6de',
					}
				)
		elif item == "Shipped":
			pie_data.append(
					{
						'name': 'Shipped',
						'y': total_shipped_count,
						'color': '#3c8dbc',
					}
				)
		elif item == "Confirmed":
			pie_data.append(
					{
						'name': 'Confirmed',
						'y': total_confirmed_count,
						'color': '#00c0ef',
					}
				)
		elif item == "Ready to Pick":
			pie_data.append(
					{
						'name': 'Ready to Pick',
						'y': total_ready_to_pick_count,
						'color': '#f39c12',
					}
				)
	return JsonResponse(pie_data, safe=False)


@login_required(login_url='/dashboard/merchant/login/')
def account_settings(request):
	template = "merchant_dashboard/coming_soon.html"
	context = {

	}
	return render(request, template, context)
	
@login_required(login_url='/dashboard/merchant/login/')
def documentation(request):
	template = "merchant_dashboard/coming_soon.html"
	context = {

	}
	return render(request, template, context)

@login_required(login_url='/dashboard/merchant/login/')
def contact(request):
	template = "merchant_dashboard/coming_soon.html"
	context = {

	}
	return render(request, template, context)
	
	