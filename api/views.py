from rest_framework import viewsets, permissions, generics, mixins
from .serializers import *
from bot_service.models import *
import math
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.decorators import api_view


class AlbumView(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permisson_class = [permissions.IsAdminUser]


class ProductView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class =  ProductSerializer
    permisson_class = [permissions.IsAdminUser]


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerilizer
    permisson_class = [permissions.IsAdminUser]


class OrderView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permisson_class = [permissions.IsAdminUser]
