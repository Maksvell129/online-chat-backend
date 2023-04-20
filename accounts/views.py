from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from accounts.serializers import CustomTokenObtainPairSerializer, UserSerializer

User = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    # Uses the CustomTokenObtainPairSerializer to obtain a token pair.
    serializer_class = CustomTokenObtainPairSerializer


class RegisterView(CreateAPIView):
    # Retrieves all User objects and uses the UserSerializer to serialize the data for the response.
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, **kwargs):
        # Deserializes the request data with the UserSerializer.
        serializer = self.serializer_class(data=request.data)
        # Validates the data and raises an exception if it is not valid.
        serializer.is_valid(raise_exception=True)
        # Saves the User object to the database.
        user = serializer.save()
        # Generates a token pair for the new User object.
        refresh = RefreshToken.for_user(user)
        # Creates a dictionary with the token pair.
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        # Returns a Response object with the token pair and a status code indicating a successful creation.
        return Response(data, status=status.HTTP_201_CREATED)
