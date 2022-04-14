# -*- coding: utf-8 -*-

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import BadRequest
from django.db import transaction
from rest_framework import serializers

from app.models import User, Product, Order, OrderProduct
from loggers.handler import get_logger

logger = get_logger(__name__)


class UserSerializer(serializers.ModelSerializer):
    """Allows serialisation and deserialisation of `User` model objects.
    Attributes:
        name (CharField): [Required, Write_only].
        password (CharField): [Required, Write_only].
    """
    name = serializers.CharField(write_only=True, required=True)

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('password', 'name')

    def create(self, validated_data):
        """
        Create and return a `User` with an username and password.
        """
        user = User.objects.create(
            name=validated_data['name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user

    def update(self, instance, validated_data):
        """
        Update and return updated `User`.
        """
        instance.name = validated_data.get('name', instance.name)

        instance.save()

        return instance


class ProductSerializer(serializers.ModelSerializer):
    """
    Allows serialisation and deserialisation of `Product` model objects.
    """
    class Meta:
        model = Product
        fields = ('name', 'price', 'stock')
        extra_kwargs = {
        }

    def to_representation(self, instance):
        """Return a serialised dict containing `Product` data"""
        data = super().to_representation(instance)
        return data


class OrderSerializer(serializers.ModelSerializer):
    """
    Allows serialisation and deserialisation of `OrderProduct` model objects.
    """
    class Meta:
        model = OrderProduct
        fields = ('product', 'quantity')
        extra_kwargs = {
            "product": {'required': False},
        }

    def to_representation(self, instance):
        """Return a serialised dict containing `OrderProducts` data"""
        if isinstance(instance, list):
            return {'status': 'created'}
        else:
            data = super().to_representation(instance)
            data['name'] = instance.product.name
            data['unit_price'] = instance.product.price
            data['total'] = instance.product.price * instance.quantity
            data['created_at'] = instance.order.created_at
            data['updated_at'] = instance.order.created_at
        return data

    @transaction.atomic
    def create(self, validated_data):
        """
        Create and return an `Order`.
        """
        pass
        user = self.context['request'].user
        validated_data['user_id'] = user
        order_obj = Order.objects.create(user_id=user)
        ordered_items = []
        update_product = []
        for item in self.context['request'].data.get('products'):
            ordered_items.append(OrderProduct(order=order_obj, product_id=item['id'], quantity=item['quantity']))
            product = Product.objects.get(id=item['id'])
            product.stock -= item['quantity']
            if product.stock < 0:
                logger.error(F'Order ID {order_obj.id} failed. Not enough item in Stock')
                raise BadRequest('Not enough item in Stock')
            update_product.append(product)

        orders_product = OrderProduct.objects.bulk_create(ordered_items)
        Product.objects.bulk_update(update_product, ['stock'])
        return orders_product
