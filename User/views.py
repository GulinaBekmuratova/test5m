from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login

from .models import User
from .serializer import SignUpSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import permissions
from .tokens import create_jwt_pair_for_user
from rest_framework import filters



class SignUpView(generics.GenericAPIView):
    serializer_class = SignUpSerializer
    # permission_classes = (permissions.AllowAny,)

    def post(self, request: Request):
        data = request.data

        serializer = SignUpSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

            context = {
                "message": "user created successfully",
                "user": serializer.data
            }
            return Response(data=context, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request: Request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(email=email, password=password)

        if user is not None:
            tokens = create_jwt_pair_for_user(user)
            response = {
                "message": "Login Successfully",
                "tokens": tokens
            }
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            return Response(data={ 'message': "Invalid email or password" })

    def get(self, request: Request):
        context = {
            "user": str(request.user),
            "auth": str(request.auth)
        }
        return Response(data=context, status=status.HTTP_200_OK)