from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .serializers import Registerserializer
# # Create your views here.
# @api_view(['POST'])
# def register(request):
#     username = request.data.get('username')
#     password = request.data.get('password')


#     user = User.objects.create_user(username=username,password=password)
#     return Response({"message":"user created"})


class HelloView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        content = {'message': 'Hello, i am auth'}
        return Response(content)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = Registerserializer

