import json
import pytest

from django.urls import reverse
from rest_framework import status

from tests.helpers import (
    create_product,
    create_user,
    reverse_querystring
)


@pytest.mark.django_db
class TestProducts:

    def test_create_products_admin(self, api_client_admin):
        url = reverse('products')
        data = json.dumps({"name": "Redbull Purple",
                           "price": 2.6,
                           "stock": 100
                           })
        response = api_client_admin.post(url, data=data, content_type="application/json")
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_products_non_admin_user_fails(self):
        api_client, user_id = create_user('Penny')
        url = reverse('products')
        data = json.dumps({"name": "Redbull Purple",
                           "price": 2.6,
                           "stock": 100
                           })
        response = api_client.post(url, data=data, content_type="application/json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_all_products(self):
        api_client, user_id = create_user('Penny')

        create_product(name="Redbull Purple", price=2.6, stock=100)
        create_product(name="Dr. Peppers", price=1.3, stock=50)

        url = reverse_querystring('products')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 2

    def test_get_products_filter(self):
        api_client, user_id = create_user('Penny')

        create_product(name="Redbull Purple", price=2.6, stock=100)
        create_product(name="Dr. Peppers", price=1.3, stock=50)

        url = reverse_querystring('products', query_kwargs={'keyword': 'Redbull'})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['name'] == 'Redbull Purple'

        url = reverse_querystring('products', query_kwargs={'max_price': 1.8})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['name'] == 'Dr. Peppers'
        assert float(response.data['results'][0]['price']) <= 1.8

    def test_get_product_by_id(self):
        api_client, user_id = create_user('Penny')

        product = create_product(name="Redbull Purple", price=2.6, stock=100)
        create_product(name="Dr. Peppers", price=1.3, stock=50)

        url = reverse('product', args=[product.id])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Redbull Purple'

    def test_update_note_admin(self, api_client_admin):
        product = create_product(name="Redbull Purple", price=2.6, stock=100)

        url = reverse('product', args=[product.id])

        data = json.dumps({"name": "Redbull Yellow"})
        response = api_client_admin.put(url, data=data, content_type="application/json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == "Redbull Yellow"

    def test_delete_note(self, api_client_admin):
        product = create_product(name="Redbull Purple", price=2.6, stock=100)

        url = reverse('product', args=[product.id])

        response = api_client_admin.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT

        response = api_client_admin.get(reverse('products'))

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 0
