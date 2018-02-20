from django.conf.urls import include, url
from . import views
from views import *

urlpatterns = [
		url(r'^login/$', merchant_login, name='merchant_login'),
		url(r'^logout/$', merchant_logout, name='merchant_logout'),
		url(r'^$', index, name='index'),
		url(r'^book_delivery/$', views.book_delivery, name='book_delivery'),
		url(r'^confirm_booking_details/$', views.confirm_booking_details, name='confirm_booking_details'),
		url(r'^cancel_booking/(?P<booking_id>\w+)/$', views.cancel_booking, name='cancel_booking'),
		url(r'^booking_list/$', booking_list, name='booking_list'),
		url(r'^booking_json/$', BookingListByMerchantJson.as_view(), name='booking_list_json'),
		url(r'^booking_details/(?P<booking_id>\w+)/$', views.booking_details, name='booking_details'),
		url(r'^pie_data/$', views.pie_data, name='pie_data'),
		url(r'^customer/get_data/(?P<customer_id>\w+)/$', views.fetch_customer_data, name='fetch_customer_data'),
		url(r'^account/settings/$', views.account_settings, name='account_settings'),
		url(r'^help/documentation/$', views.documentation, name='documentation'),
		url(r'^help/contact/$', views.contact, name='contact'),	
]