from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters

from .models import *
from .serializers import *


class WatchListApiView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = WatchSerializer
    authentication_classes = [JWTAuthentication]
    search = [filters.SearchFilter]

    def get_queryset(self):
        queryset = Watch.objects.all()

        return queryset


class CategoryListApiView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    authentication_classes = [JWTAuthentication]


class CategoryDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = CategorySerializer
    authentication_classes = [JWTAuthentication]
    queryset = Category

    # def get_queryset(self):
    #     queryset = Watch.objects.filter(categories__in=[self.kwargs['id']])
    #     return queryset


class ReviewListAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    authentication_classes = [JWTAuthentication]


class ReviewItemUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView, generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewValidateSerializer
    authentication_classes = [JWTAuthentication]

    def create(self, request, *args, **kwargs):
        if Review.objects.filter(author=request.user).exists():
            return Response({ "detail": "requesting user already created review update or delete previour review" },
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        instance = Review.objects.get(author=request.user)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = Review.objects.get(author=request.user)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = Review.objects.get(author=request.user)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = { }

        return Response(serializer.data)


class WatchViewSet(ModelViewSet):
    serializer_class = WatchSerializer
    queryset = Watch.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]



class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]



class PhotoViewSet(ModelViewSet):
    serializer_class = PhotoSerializer
    queryset = Photo.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewValidateSerializer
    queryset = Review.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]