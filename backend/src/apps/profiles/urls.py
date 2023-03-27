from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views

from apps.profiles import views as profile_views
from apps.profiles.router import router_profile
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Documentacion API",
      default_version='v1',
      description="Documentacion de api ",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
)

urlpatterns = [
    path('auth/otp/verify/', profile_views.VerifyOTPView.as_view(), name='verify_otp'),
    path('auth/otp/qr/', profile_views.OTPQrView.as_view(), name='otp_qr'),
    path('auth/register/', profile_views.RegisterView.as_view(), name='register'),
    path('auth/logout/', profile_views.LogoutView.as_view(), name='logout'),
    path('auth/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    path('user/', profile_views.UserView.as_view(), name='user_detail'),
    path('user/wallet/', profile_views.WalletView.as_view(), name='user_wallet'),
    path('user/profile/all/', profile_views.ProfileListView.as_view(), name='user_profiles'),
    path('user/profile/', include(router_profile.urls)),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
