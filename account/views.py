from django.shortcuts import render

# Create your views here.
from django.db import transaction
from django.shortcuts import render
from django.contrib.auth import authenticate ,login,logout
# from django.core.mail import send_mail

from .serializers import *
from.models import *

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated,IsAdminUser
from rest_framework.decorators import action
from rest_framework import generics,viewsets,mixins
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status



class PersonnalModelViewSet(
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """
    pass





class UserRegister(viewsets.ModelViewSet):

    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()

    def create(self, request, *args, **kwargs):
        serializers = self.get_serializer(data=request.data)
     
        if serializers.is_valid():
        
            password = serializers.validated_data.get('password')
            email = serializers.validated_data.get('email')
         
            serializers.validated_data['password']  =  make_password(password)
            
            user = CustomUser.objects.create(**serializers.validated_data)
           
         
            if user is  None:
                return Response({'message':'error this user can not create '},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
               

            user = authenticate(email = email, password=password)
            if not user:
                raise serializers.ValidationError('data is not valid')
            if not user.is_active:
                raise serializers.ValidationError('user is not activated ')

            login(request, user)
            token = RefreshToken.for_user(user)
         
            token['id'] = user.id
            token['email']  = user.email
            token['username'] = user.username

            response_data = {
             
                'refresh': str(token),
                'access': str(token.access_token),
                'message':'user create succesfuly'

            }
            return Response(response_data, status=status.HTTP_200_OK)
        
        else:
            return Response({"message":"data is not valid "},status=status.HTTP_400_BAD_REQUEST)









class UserLogin(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Login a user with their email/email and password.

        Parameters:
        email_or_email (str): The email for students/marchands or email for admins.
        password (str): The password of the user.

        Returns:
        Response: A JSON response containing the access and refresh tokens.
        """
        email_or_email = request.data.get('email')
        password = request.data.get('password')

        # Try to authenticate the user with email or email
        try: 
            user_login = CustomUser.objects.get(username = email_or_email)
        except:
            try:
                user_login = CustomUser.objects.get(email = email_or_email)
            except:
                return Response({"message": "user can't exist"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(email=user_login.email, password=password)
        if not user:
            # If authentication fails, try to authenticate with email
            user = authenticate(email=email_or_email, password=password)

            if not user:
                return Response({"message": "Les données ne sont pas valides"}, status=status.HTTP_400_BAD_REQUEST)

        if not user.is_active:
            return Response({"message": "L'utilisateur n'est pas actif"}, status=status.HTTP_400_BAD_REQUEST)

        login(request, user)
        
        token = RefreshToken.for_user(user)
        token['id'] = user.id
        token['email']  = user.email
        token['username'] = user.username
        response_data = {
            'id': user.id,
            'refresh': str(token),
            'access': str(token.access_token),
            'message': 'Connexion réussie',
        }

        return Response(response_data, status=status.HTTP_200_OK)
      




class Logout(APIView):
    permission_classes=[AllowAny]
    def post(self, request,id):
        user =  CustomUser.objects.filter(id=id).first
        request.user = user
        # print(request.user)
        logout(request)
        if not request.user.is_authenticated:

            return Response({
            'message': 'logout succesfull'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
            'message': 'logout failed'
            })
  
# fonction d'envoi des email
