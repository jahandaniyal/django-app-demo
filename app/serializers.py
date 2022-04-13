# -*- coding: utf-8 -*-

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from app.models import User, Product


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
    # tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = ('name', 'price', 'stock')
        extra_kwargs = {
        }

    def to_representation(self, instance):
        """Return a serialised dict containing `UsageType` data"""
        data = super().to_representation(instance)
        return data
