from django.contrib.auth.hashers import make_password
from django.http import JsonResponse, response
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny

from authenticate.serializer import UserLoginSerializer, UserRegistraitionSerializer, UserSerializer


class UserRegisterView(CreateAPIView):
    serializer_class = UserRegistraitionSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse({
            'message': 'Register successful!'
        }, status=status.HTTP_201_CREATED)


class UserLoginView(RetrieveAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = {
            'succcess': 'True',
            'message': 'Login successful!',
            'status_code': status.HTTP_200_OK,
            'token': serializer.data['token']
        } 
        status_code= status.HTTP_200_OK
        return JsonResponse(response, status=status_code)
