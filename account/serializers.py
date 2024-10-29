
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate,get_user_model,login
from django.contrib.auth.models import Permission,Group


from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.status import HTTP_404_NOT_FOUND

from .models import *

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username','email','password')




class UserLoginSerializer(TokenObtainPairSerializer):
  
    pass


