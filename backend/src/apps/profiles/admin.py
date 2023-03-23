from django.contrib import admin

from apps.profiles.models import User, Wallet, Profile


admin.site.register(User)
admin.site.register(Wallet)
@admin.register(Profile)

class ProfileAdmin(admin.ModelAdmin):
  list_display = ['user', 'bio', 'website']

