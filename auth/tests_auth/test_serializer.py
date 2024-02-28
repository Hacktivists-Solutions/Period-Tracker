from django.test import TestCase
from auth.serializers import UserRegistrationSerializer


class UserRegistrationSerializerTestCase(TestCase):
    def setUp(self):
        # Set up any necessary test data (if needed)
        self.user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "securepassword",
        }

    def test_user_registration_serializer(self):
        """
        Test the UserRegistrationSerializer.
        """
        serializer = UserRegistrationSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid())

        # Create a user using the serializer
        user = serializer.save()

        # Assert that the user was created successfully
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")

        # Clean up (delete the test user)
        user.delete()
