from django.contrib import admin

from apps.profiles.models import User, Wallet, Profile, UserProfiles


admin.site.register(User)
admin.site.register(Wallet)
admin.site.register(Profile)
admin.site.register(UserProfiles)

