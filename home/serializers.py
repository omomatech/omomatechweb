from django.db.models import fields
from rest_framework import serializers
from .models import *

class VisitingSerializers(serializers.ModelSerializer):
      class Meta:
          model=Visiting
          fields='__all__'          
class Img_visitingSerializers(serializers.ModelSerializer):
      class Meta:
          model=Image_visiting
          fields='__all__'                    