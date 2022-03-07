from datetime import date
from django.db import models
from accounts.models import *


class Reservation(models.Model):
    unique_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)    
    profile=models.ForeignKey(Profile,related_name='reservation',max_length=150,on_delete=models.CASCADE)
    date_reservation=models.DateField(default='',null=False,blank=False)
    time_reservation=models.TimeField(default='',null=True,blank=True)
    active=models.BooleanField(default=True,null=False,blank=False)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    def __str__(self):
            return "name : "+str(self.profile)+" time :"+str(self.time_reservation)
    
    class Meta:
          ordering = ['time_reservation']

class time_reservations(models.Model):
      unique_id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
      time_reservation_part=models.TimeField(default='',null=True,blank=True)
      created=models.DateTimeField(auto_now_add=True)
      updated=models.DateTimeField(auto_now=True)
      def __str__(self):
                return str(self.time_reservation_part)
    
      class Meta:
          ordering = ['time_reservation_part']