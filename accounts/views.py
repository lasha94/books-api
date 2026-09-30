from django.contrib.auth import get_user_model
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.serializers import (
    ChangePasswordSerializer,
    CustomTokenObtainPairSerializer,
    DeleteAccountSerializer,
    LogoutSerializer,
    RegisterSerializer,
    UserSerializer,
)

User = get_user_model()


@extend_schema(tags=["Auth"], responses={201: UserSerializer})
class RegisterView(generics.CreateAPIView):
    """Create a new user account. Response shape comes from RegisterSerializer.to_representation."""

    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


@extend_schema(tags=["Auth"], summary="Log in and obtain a JWT access/refresh token pair.")
class LoginView(TokenObtainPairView):
    """Log in with email + password. Returns access/refresh tokens and the user's profile."""

    permission_classes = [AllowAny]
    serializer_class = CustomTokenObtainPairSerializer


@extend_schema(
    tags=["Auth"],
    request=LogoutSerializer,
    responses={205: OpenApiResponse(description="Logged out."), 400: OpenApiResponse(description="Invalid token.")},
)
class LogoutView(generics.GenericAPIView):
    """Blacklist the given refresh token, effectively logging the user out."""

    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            RefreshToken(serializer.validated_data["refresh"]).blacklist()
        except TokenError:
            return Response({"detail": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_205_RESET_CONTENT)


@extend_schema(tags=["Account"])
class ProfileView(generics.RetrieveUpdateAPIView):
    """Retrieve or partially/fully update the authenticated user's own profile."""

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


@extend_schema(tags=["Account"], request=ChangePasswordSerializer)
class ChangePasswordView(generics.GenericAPIView):
    """Change the authenticated user's password."""

    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Password updated successfully."}, status=status.HTTP_200_OK)


@extend_schema(tags=["Account"], request=DeleteAccountSerializer)
class DeleteAccountView(generics.DestroyAPIView):
    """Permanently delete the authenticated user's account after password confirmation."""

    serializer_class = DeleteAccountSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def destroy(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return super().destroy(request, *args, **kwargs)
