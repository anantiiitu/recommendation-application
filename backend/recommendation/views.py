from django.core.cache import cache
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework import generics, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta

from django.contrib.auth.models import User
from rest_framework import status

from .serializers import UserSerializer


class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)
    allowed_methods = ["POST"]


class UserLoginView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)
    allowed_methods = ["POST"]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        )


class UserLogoutView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    allowed_methods = ["POST"]

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def get_recommendations(request):
    data = cache.get("recommendations")
    if data is None:
        # If data is not in cache, fetch it from an external source or perform calculations.
        # For simplicity, we'll assume the recommendations are a list of dictionaries.
        recommendations = [
            {"title": "Recommendation 1", "description": "This is recommendation 1"},
            {"title": "Recommendation 2", "description": "This is recommendation 2"},
        ]

        # Store the recommendations in the cache for future requests.
        cache.set("recommendations", recommendations)

        data = recommendations

    return Response(data)
