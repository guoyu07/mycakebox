from django.http import JsonResponse
from django.shortcuts import render, HttpResponseRedirect, HttpResponse, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from booking.models import Booking
from .models import Merchant
from customer.models import Customer
from .forms import LoginForm
# Create your views here.
