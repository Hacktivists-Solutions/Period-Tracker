# myapp/tests.py
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status


class UserRegistrationTestCase(TestCase):
    def setUp(self):
        # Set up any necessary test data (if needed)
        self.data = {
            'email': 'test@example.com',
            'password': 'securepassword',
            'username': 'testuser',
        }
        self.user = User.objects.create_user(
            username=self.data['username'],
            email=self.data['email'],
            password=self.data['password'],
        )

    def test_user_registration(self):
        """Test user registration API."""
        client = APIClient()

        # Define user registration data
        registration_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newsecurepassword",
        }

        # Make a POST request to the registration endpoint
        response = client.post("/auth/token/register/",
                               registration_data, format="json")

        # Assert that the response status code is 201 (created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the user was created successfully
        user = User.objects.get(username="newuser")
        self.assertEqual(user.email, "newuser@example.com")

        # You can add more assertions as needed based on your requirements

        # Clean up (delete the test user)
        user.delete()

    def test_user_login(self):
        """Test user login API."""
        client = APIClient()

        # Make a POST request to the login endpoint
        response = client.post("/auth/token/", self.data, format="json")

        # Assert that the response is the same user
        self.assertEqual(response.status_code, status.HTTP_200_OK)
