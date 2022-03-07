import uuid
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from django.db.models.fields.related import OneToOneField
import datetime
import uuid

from django.db import models

'''
profile model uuid pk
relation to user one to one 
ispregnant false create profile after user create User.username=profile.mobile,

'''


class Profile(models.Model):
    unique_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user=OneToOneField(User,null=True,on_delete=models.CASCADE)
    email = models.EmailField(max_length=100,unique=False,null=True)
    mobile = models.CharField(max_length=11, unique=True)
    password=models.CharField(max_length=10,null=True,blank=True)
    name = models.CharField(max_length=100, blank=True,null=True)
    #is_pregnant=models.BooleanField(default=False,blank=True,null=True)
    #date_pregnant=models.DateField(null=True,editable=True,blank=True)
    #number_week_pregnant=models.IntegerField(default=0,null=True,blank=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    about = models.TextField(max_length=50, blank=True,null=True)
    token_notifcation=models.CharField(max_length=200,null=True,blank=True)
    class meta:
          ordering = ('created')
    def __str__(self):
        return self.name 

