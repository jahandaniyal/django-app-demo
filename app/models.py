import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.timezone import now


class UserManager(BaseUserManager):
    """
    Manager class for User Model.
    """
    def create_user(self, name, password=None):
        """
        Create and return a `User` with an username and password.
        """
        if not name:
            raise ValueError('Users Must Have a name')

        user = self.model(
            name=name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, password):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(name, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser):
    """
    The class representing the User Model.
    :param name (Characters): Name of the user.
    :param password (Characters): Password of the user.
    :param is_staff (Number): 1 if the user has admin access else 0.
    :param is_superuser (Number): 1 if the user has admin access else 0.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    last_login = None

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.name

    def has_perm(self):
        return self.is_superuser

    def has_module_perms(self):
        return self.is_superuser


class Product(models.Model):
    """
    The class representing the Product model.
    :param name (Characters): Name of the product.
    :param price (Decimal): Unit price of this product.
    :param stock (Integer): Quantity in stock.
    :param created_at (DateTime): Time of creation.
    :param updated_at (DateTime): Time of update.
    """
    name = models.CharField(max_length=200, unique=True)     # max_length not enforced at db level
    price = models.DecimalField(default=0.0, max_digits=10, decimal_places=3)
    stock = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)


class Order(models.Model):
    """
    The class representing the Order model.
    :param user_id (f_key): ID of the user who creates this Order.
    :param created_at (DateTime): Time of creation.
    :param updated_at (DateTime): Time of update.
    """
    user_id = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)


class OrderProduct(models.Model):
    """
    The class representing the OrderProduct model.
    :param order (f_key): ID of the Order.
    :param product (f_key): ID of the product.
    :param quantity (Integer): Total number of product requested.
    """
    class Meta:
        unique_together = ('order', 'product')

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

