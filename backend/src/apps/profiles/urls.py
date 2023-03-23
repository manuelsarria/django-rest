from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views

from apps.profiles import views as profile_views
from apps.profiles.router import router_profile


urlpatterns = [
    path('auth/otp/verify/', profile_views.VerifyOTPView.as_view(), name='verify_otp'),
    path('auth/otp/qr/', profile_views.OTPQrView.as_view(), name='otp_qr'),
    path('auth/register/', profile_views.RegisterView.as_view(), name='register'),
    path('auth/logout/', profile_views.LogoutView.as_view(), name='logout'),
    path('auth/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    path('user/', profile_views.UserView.as_view(), name='user_detail'),
    path('user/wallet/', profile_views.WalletView.as_view(), name='user_wallet'),
    path('user/profiles/', profile_views.ProfileListView.as_view(), name='user_profiles'),
    path('user/profile/', include(router_profile.urls)),
]
