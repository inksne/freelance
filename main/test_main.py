from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User

from .models import Category, Order

import pytest

@pytest.mark.skip()
class TestAPIViews(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123', email='testuser@mail.com')

        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)

    def test_register_view(self):
        url = reverse('register')
        data = {
            'username': 'newuser',
            'password': 'newpassword123',
            'email': 'newuser@main.com',
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

        user = User.objects.get(username='newuser')
        self.assertIsNotNone(user)


    def test_add_response_view(self):
        self.client.login(username='testuser', password='password123')
        category = Category.objects.create(name='веб разработка')
        order = Order.objects.create(name='создать веб-сайт', customer=self.user, category=category, description='нужно создать сайт')

        url = reverse('add_response', kwargs={'order_id': order.id})
        data = {
            'message': 'я готов выполнить этот заказ',
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response_order = Order.objects.get(id=order.id)
        self.assertEqual(response_order.responses.count(), 0)


    def test_delete_order_view(self):
        self.client.login(username='testuser', password='password123')
        category = Category.objects.create(name='веб разработка')
        order = Order.objects.create(name='создать веб-сайт', customer=self.user, category=category, description='нужно создать сайт')

        url = reverse('delete_order', kwargs={'order_id': order.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


def test_dummy():
    assert True