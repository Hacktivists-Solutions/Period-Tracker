from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView

from auth.serializers import MyTokenObtainPairSerializer
from .serializers import UserRegistrationSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


class MyTokenObtainPairView(TokenObtainPairView):
    """
    Custom view for obtaining JWT token pairs.
    Uses a custom serializer for token generation.
    """
    serializer_class = MyTokenObtainPairSerializer


@api_view(['POST'])
def register_user(request):
    """
    Function-based view for user registration.
    Accepts POST requests with user registration data.
    Returns JSON response with user details and access token on successful registration.
    """
    serializer = UserRegistrationSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()

        # Generate access and refresh tokens
        refresh_token = RefreshToken.for_user(user)
        access_token = str(refresh_token)

        # Prepare response data
        response_data = {
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
            "access_token": access_token,
        }

        return Response(response_data, status=status.HTTP_201_CREATED)
    else:
        # Return validation errors if registration data is invalid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
