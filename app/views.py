# -*- coding: utf-8 -*-

import json

from django.db.models import Q
from rest_framework.generics import (
    CreateAPIView,
    ListCreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated
)
from rest_framework.response import Response

from app.authentication import AuthorAndAllAdmins, IsAdminOrReadOnly
from app.controller import (
    delete_user,
    get_all_users,
    get_user_name_by_id,
    update_user
)
from app.models import User, Product, OrderProduct, Order
from app.serializers import UserSerializer, ProductSerializer, OrderSerializer
from app.utils import sanitize_json_input


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer


class UsersAPIView(RetrieveAPIView):
    permission_classes = (IsAdminUser, )
    serializer_class = UserSerializer

    def get(self, request):
        users = get_all_users()
        return Response(users)


class UserAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, AuthorAndAllAdmins)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

    def get(self, request, user_id):
        user_name = get_user_name_by_id(user_id)
        content = {'user is': user_name}
        return Response(content)

    @sanitize_json_input
    def put(self, request, *args, **kwargs):

        data = json.loads(self.request.body)
        uuid = kwargs.get('user_id')
        user_name = update_user(request, data, uuid)
        content = {'user {} has been updated'.format(self.request.user.name): user_name}
        return Response(content)

    def delete(self, request, *args, **kwargs):
        user_name = get_user_name_by_id(kwargs.get('user_id'))
        delete_user(kwargs.get('user_id'))
        content = 'User {} has been deleted'.format(user_name)
        return Response(content)


class ProductsAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated, IsAdminOrReadOnly)
    serializer_class = ProductSerializer

    def get_queryset(self):
        max_price = self.request.query_params.get('max_price')
        keyword = self.request.query_params.get('keyword')

        filters = Q()
        if max_price:
            filters &= Q(price__lte=max_price)

        if keyword:
            filters &= Q(name__icontains=keyword)

        product_obj = Product.objects.filter(filters).distinct()
        return product_obj


class ProductAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, IsAdminOrReadOnly)
    serializer_class = ProductSerializer

    def get_object(self):
        product_obj = Product.objects.get(id=self.kwargs.get('product_id'))
        return product_obj


class OrdersAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializer

    def get_queryset(self):
        orders = Order.objects.filter(user_id=self.request.user.id)
        order_products = OrderProduct.objects.filter(order__in=list(orders))
        return order_products
