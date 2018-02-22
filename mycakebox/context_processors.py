from django.conf import settings


def google_map_api(request):
	""" Returns google map api from settings """
	return {
		'GOOGLE_MAPS_API' : settings.GOOGLE_MAPS_API,
	}