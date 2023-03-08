from django.contrib import admin

from apps.profiles.models import User, Wallet


admin.site.register(User)
admin.site.register(Wallet)
