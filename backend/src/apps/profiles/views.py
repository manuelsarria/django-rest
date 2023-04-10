import pyotp

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.tokens import OutstandingToken, BlacklistedToken
from apps.profiles.models import Profile

from apps.profiles.serializer import (RegisterSerializer, UserSerializer,
                                      OTPSerializer, OTPQrSerializer, WalletSerializer,
                                      ProfileSerializer)


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "message": "User created successfully."},
                    status=status.HTTP_201_CREATED)
            else:
                return Response({
                    "error": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({
                "error" : "Error encountered"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LogoutView(APIView):
    permission_class = (IsAuthenticated,)

    def post(self, request):
        try:
            tokens = OutstandingToken.objects.filter(user_id=request.user.id)
            for token in tokens:
                BlacklistedToken.objects.get_or_create(token=token)
            return Response({
                "message": "User logged out successfully"},
                status=status.HTTP_200_OK)
        except Exception:
            return Response({
                "error" : "Error encountered"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OTPQrView(generics.GenericAPIView):
    permission_class = (IsAuthenticated,)
    serializer_class = OTPQrSerializer

    def get(self, request):
        try:
            serializer = self.get_serializer(request.user)
            return Response({
                "otp": serializer.data},
                status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "error" : "Error encountered"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VerifyOTPView(generics.GenericAPIView):
    permission_class = (IsAuthenticated,)
    serializer_class = OTPSerializer

    def post(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                user = request.user
                totp = pyotp.TOTP(user.otp_secret)
                token_valid = totp.verify(serializer.validated_data['otp'], valid_window=2)

                if not token_valid:
                    return Response({
                        "valid": False},
                        status=status.HTTP_200_OK)

                if not user.has_mfa_configured:
                    user.has_mfa_configured = True
                    user.save()

                return Response({
                    "valid": True},
                    status=status.HTTP_200_OK)
            else:
                return Response({
                    "error": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({
                "error" : "Error encountered"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserView(generics.GenericAPIView):
    permission_class = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request):
        try:
            serializer = self.get_serializer(request.user)
            return Response({
                "user": serializer.data},
                status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "error" : "Error encountered"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request):
        try:
            user_data = request.data
            user_data['email'] = request.user.email
            serializer = self.get_serializer(request.user, data=user_data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "user": serializer.data},
                    status=status.HTTP_200_OK)
            else:
                return Response({
                    "error": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({
                "error" : "Error encountered"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class WalletView(generics.GenericAPIView):
    permission_class = (IsAuthenticated,)
    serializer_class = WalletSerializer

    def post(self, request):
        try:
            wallet_data = request.data
            wallet_data['user'] = request.user.id
            serializer = self.get_serializer(data=wallet_data)
            if serializer.is_valid():
                serializer.save()
                user_data = UserSerializer(request.user).data
                wallets = user_data.get('wallets', [])
                return Response({
                    "wallets": wallets},
                    status=status.HTTP_201_CREATED)
            else:
                return Response({
                    "error": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({
                "error" : "Error encountered"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
class ProfileviewSet(ModelViewSet):
#   permission_classes = [IsAuthenticatedOrReadOnly]
  serializer_class = ProfileSerializer
  queryset = Profile.objects.all()
  
class LargeResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50
  
class ProfileListView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    pagination_class = LargeResultsSetPagination