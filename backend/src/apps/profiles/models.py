import pyotp

from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_superuser(self, email, password):
        if password is None:
            raise TypeError("provide password please")
        user = self.model(email=email, password=password)
        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save()

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    otp_secret = models.CharField(max_length = 40, blank=True)
    has_mfa_configured = models.BooleanField(default=False)
    # coincover_password = models.CharField(max_length = 100, blank=True)
    # kyc = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
    
    def get_profile(self):
        return Profile.objects.get(user=self)

    # @property
    # def has_coincover_password(self):
    #     return True if self.coincover_password else False

    @property
    def secret_url(self):
        secret_url = ''
        if self.otp_secret:
            secret_url = pyotp.TOTP(self.otp_secret) \
                .provisioning_uri(self.email, issuer_name="Stakesauce")
        return secret_url

class Wallet(models.Model):
    POKT = 'POKT'
    CHAIN_CHOICES = [
        (POKT, 'Pocket Network'),
    ]

    user = models.ForeignKey(User, related_name='wallets', on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    chain = models.CharField(max_length=4, choices=CHAIN_CHOICES, default=POKT)

class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profiles', on_delete=models.CASCADE)
    bio = models.CharField(max_length=500, blank=True)
    website =  models.URLField(blank=True)
    
    def __str__(self):
        return self.user.first_name
    
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
      if created:
        Profile.objects.create(user=instance)
        
class UserProfiles(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name
