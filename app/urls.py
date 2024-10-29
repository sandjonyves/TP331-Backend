from django.urls import path,include
from .views import *
from rest_framework import routers

route =routers.SimpleRouter()



urlpatterns =[

    
    path('',include(route.urls)),


]