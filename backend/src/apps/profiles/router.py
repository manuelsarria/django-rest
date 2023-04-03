from rest_framework.routers import DefaultRouter
from apps.profiles.views import ProfileviewSet

router_profile = DefaultRouter()

router_profile.register(prefix='', basename='', viewset=ProfileviewSet)

