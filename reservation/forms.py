from django.forms import ModelForm




from .models import *

class ReservationFrom(ModelForm):
	class Meta:
			model=Reservation	
			fields=['profile']
	