# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import string
import random

def rider_id_generator(self, size=5, chars=string.ascii_uppercase + string.digits):
	the_id = "".join(random.choice(chars) for x in range(size))
	try:
		rider_id = self.objects.get(rider_id=the_id)
		rider_id_generator()
	except self.DoesNotExist:
		return the_id