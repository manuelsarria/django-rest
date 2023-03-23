from rest_framework.routers import DefaultRouter
from apps.profiles.views import ProfileviewSet

router_profile = DefaultRouter()

router_profile.register(prefix='profiles', basename='profiles', viewset=ProfileviewSet)

