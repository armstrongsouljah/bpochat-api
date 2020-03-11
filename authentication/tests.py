from .models import User
from .test_.base_test_case import BaseTest
from rest_framework import status
import json

class TestUserModel(BaseTest):
    
    def test_create_user(self):
        user = User.objects.create_user(
            self.user_data['user']['username'],
            self.user_data['user']['email'],
            self.user_data['user']['password'])
        self.assertEqual(2, User.objects.count())

    def test_create_staff_user(self):
        user = User.objects.create_staffuser(
            username='sampleuser',
            email='sampleemail@server.com',
            password='Paseedere12d'
        )
        self.assertEqual(user.is_staff, True)

    def test_create_super_user_succeeds(self):
        user = User.objects.create_superuser(
            username='sampleuser',
            email='sampleemail@server.com',
            password='Paseedere12d'
        )
        self.assertIs(user.admin, True)

    def test_creating_a_user_without_username_fails(self):
        """
           failure to provide a username raises an error
        """
        with self.assertRaises(TypeError):
            user = User.objects.create_user(
            username=None,
            email='ededefefeef',
            password='ssassaasas'
        )

    def test_creating_a_user_without_password_fails(self):
        """
          failure to provide a password raises an
           exception
        """
        with self.assertRaises(TypeError):
            user = User.objects.create_user(
            username='dedededede',
            email='aswewe@asas.cdcdc',
            password=None
        )

    def test_creating_a_user_without_email_fails(self):
        """
           failure to provide an email raises an
           exception
        """
        with self.assertRaises(TypeError):
            user = User.objects.create_user(
            username='dedededede',
            email=None,
            password='ssassaasas'
        )

"""
  Module views tests
"""

class TestViews(BaseTest):
    def test_signup_with_valid_data(self):
        response = self.client.post(
            f"{self.baseUrl}/auth/signup",
            content_type='application/json',
            data=json.dumps(self.user_data)
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_signup_without_user_data_fails(self):
        response = self.client.post(
            f"{self.baseUrl}/auth/signup",
            content_type='application/json',
            data=json.dumps({}),
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_with_a_weak_password_fails(self):
        self.user_data['user']['password'] = '1232324'
        response = self.client.post(
            f"{self.baseUrl}/auth/signup",
            content_type='application/json',
            data=json.dumps(self.user_data),
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_with_valid_data_succeeds(self):
        response = self.client.post(f'{self.baseUrl}/auth/login',
               content_type='application/json',
               data=json.dumps(self.valid_user_login))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_with_invalid_data_fails(self):
        response = self.client.post(
            f"{self.baseUrl}/auth/login",
            content_type="application/json",
            data=json.dumps(self.invalid_user_login)
        )
        
