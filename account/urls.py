from django.urls import path,include
from .views import *
from rest_framework import routers

route =routers.SimpleRouter()

route.register('register',UserRegister,basename='user')


urlpatterns =[

    
    path('',include(route.urls)),


    path('login/',UserLogin.as_view(),name='login'),
    path('logout/<id>',Logout.as_view(),name='logout'),
]