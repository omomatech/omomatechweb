from django.db.models import fields
from rest_framework import serializers
from .models import *


class ProfileSerializers(serializers.ModelSerializer):
      class Meta:
          model=Profile
          fields='__all__'
class UserSerializers(serializers.ModelSerializer):
      class Meta:
          model=User
          fields='__all__'
          exclude = ('password')         