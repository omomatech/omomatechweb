from django.db.models import fields
from rest_framework import serializers
from .models import *

        
class Note_Serializers(serializers.ModelSerializer):
      class Meta:
          model=notefication
          fields='__all__'                    
class Catogreys_serializer(serializers.ModelSerializer) :
     class Meta:
         model=catgorys
         fields=['category_name']

