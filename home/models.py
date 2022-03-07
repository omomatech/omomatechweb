from django import forms
from django.db import models
from datetime import datetime
import uuid
from accounts.models import *
from django.utils.timezone import now
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token



@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)   
class Visiting(models.Model):
      '''
      model visiting that contain profile uuid 
      '''
      unique_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
      profile=models.ForeignKey(Profile,max_length=100,related_name="visiting",on_delete=models.CASCADE)
      created=models.DateTimeField(default=now, editable=True)
      
      updated=models.DateTimeField(auto_now=True)
      def __str__(self):
            return self.profile.name
      class Meta:
            ordering = ['created']



def impage_upload(instance,filename):
      '''
      function that save image in folder named by [username/year/month/day/name.ext]
      django speed search by number
      '''
      imagename,extension=filename.split(".")
      year=datetime.datetime.now().year
      month=datetime.datetime.now().month
      day=datetime.datetime.now().day

      return '%s/%s/%s/%s/%s.%s'%(str(instance.visiting.profile.mobile),str(year),str(month),str(day),str(imagename),str(extension))
      


class Image_visiting(models.Model):
      '''
      model images that contain visit uuid 
      when delete image from database remove file from forlder

      '''
      unique_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
      visiting=models.ForeignKey(Visiting,max_length=100,related_name="image_visting",on_delete=models.CASCADE)
      img_visiting= models.ImageField(upload_to=impage_upload)
      created=models.DateTimeField(auto_now_add=True, editable=True)
      updated=models.DateTimeField(auto_now=True)
      def __str__(self):
            return self.visiting.profile.name
      class Meta:
            ordering = ['created']
      
      def delete(self, using=None, keep_parents=False):
            self.img_visiting.storage.delete(self.img_visiting.name)
           
            super().delete()


@receiver(pre_save, sender=Image_visiting)
def upload_file_pre_save(sender, instance, **kwargs):
      '''
        signals =>you can upload max 4 images in one visiting
        
      '''
      if Image_visiting.objects.filter(visiting_id=instance.visiting_id).count() >= 10:
          raise forms.ValidationErro('sorry cant upload more than 4')  

  