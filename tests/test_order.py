import json
import pytest

from django.urls import reverse
from rest_framework import status

from tests.helpers import (
    create_product,
    create_user,
)


@pytest.mark.django_db
class TestOrders:

    def test_create_orders(self):
        api_client, _ = create_user('Penny')
        product_1 = create_product(name="Redbull Purple", price=2.6, stock=100)
        product_2 = create_product(name="Dr. Peppers", price=1.3, stock=50)
        url = reverse('orders')
        data = json.dumps({
                            "products": [
                                {"id": product_1.id, "quantity": 15},
                                {"id": product_2.id, "quantity": 13}
                            ]
                        })
        response = api_client.post(url, data=data, content_type="application/json")
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_orders_insufficient_stock_fails(self):
        api_client, _ = create_user('Penny')
        product_1 = create_product(name="Redbull Purple", price=2.6, stock=100)
        product_2 = create_product(name="Dr. Peppers", price=1.3, stock=50)
        url = reverse('orders')
        data = json.dumps({
            "products": [
                {"id": product_1.id, "quantity": 150},
                {"id": product_2.id, "quantity": 13}
            ]
        })
        response = api_client.post(url, data=data, content_type="application/json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_get_orders(self):
        api_client, _ = create_user('Penny')
        product_1 = create_product(name="Redbull Purple", price=2.6, stock=100)
        product_2 = create_product(name="Dr. Peppers", price=1.3, stock=50)
        url = reverse('orders')
        data = json.dumps({
            "products": [
                {"id": product_1.id, "quantity": 15},
                {"id": product_2.id, "quantity": 13}
            ]
        })
        api_client.post(url, data=data, content_type="application/json")
        response = api_client.get(url, content_type="application/json")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 2
