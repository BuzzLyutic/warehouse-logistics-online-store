from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User, Role, Permission


class AuthenticationTests(APITestCase):
    def setUp(self):
        # Create a default role and permissions for testing
        self.permission = Permission.objects.create(name="read_data")
        self.role = Role.objects.create(name="User")
        self.role.permissions.add(self.permission)

        # Test user credentials
        self.user_data = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User'
        }

    def test_user_registration(self):
        """
        Test user registration endpoint
        """
        url = reverse('register')
        response = self.client.post(url, self.user_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'test@example.com')

    def test_user_registration_invalid_email(self):
        """
        Test registration with invalid email
        """
        url = reverse('register')
        invalid_user_data = self.user_data.copy()
        invalid_user_data['email'] = 'invalid-email'

        response = self.client.post(url, invalid_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login(self):
        """
        Test user login endpoint
        """
        url = reverse('register')
        self.client.post(url, self.user_data, format='json')

        url = reverse('login')
        login_data = {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }
        response = self.client.post(url, login_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user', response.data)

    def test_user_login_invalid_credentials(self):
        """
        Test login with invalid credentials
        """
        url = reverse('login')
        invalid_login_data = {
            'email': 'wrong@example.com',
            'password': 'wrongpass'
        }
        response = self.client.post(url, invalid_login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)



    def test_current_user(self):
        """
        Test getting current user information
        """
        # First register and login
        self.client.post(reverse('register'), self.user_data, format='json')
        login_response = self.client.post(reverse('login'), {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }, format='json')

        # Set the access token in the header
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # Get current user info
        url = reverse('current_user')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user_data['email'])

    def test_health_check(self):
        """
        Test health check endpoint
        """
        url = reverse('health')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'ok')