from django.db.models import fields
from rest_framework import serializers
from .models import *
class ReservationSerializers(serializers.ModelSerializer):
      class Meta:
          model=time_reservations
          fields=['time_reservation_part'] 

