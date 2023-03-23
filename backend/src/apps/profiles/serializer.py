import pyotp

from rest_framework import  serializers
from django.contrib.auth.hashers import make_password

from apps.profiles.models import User, Wallet, Profile


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','password', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.otp_secret = pyotp.random_base32()
        user.save()
        return user


class OTPSerializer(serializers.Serializer):
    otp = serializers.IntegerField(required=True)


class OTPQrSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['secret_url', 'has_mfa_configured']


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['user', 'address', 'chain']

    def create(self, validated_data):
        wallet = Wallet(**validated_data)
        wallet.save()
        return wallet


class UserSerializer(serializers.ModelSerializer):
    wallets = WalletSerializer(many=True, read_only=True)

    class Meta:
        model = User
        # fields = ['id', 'first_name', 'last_name', 'email', 'wallets',
        #           'coincover_password', 'has_coincover_password']
        fields = ['id', 'first_name', 'last_name', 'email', 'wallets']

    def update(self, instance, validated_data):
        validated_data.pop('password', None)
        # if validated_data.get('coincover_password'):
        #     validated_data['coincover_password'] = make_password(
        #         validated_data['coincover_password'])
        for key, arg in validated_data.items():
            setattr(instance, key, arg)
        instance.save()
        return instance

    def to_representation(self, instance):
        data = super(UserSerializer, self).to_representation(instance)
        # data.pop('coincover_password', None)
        return data

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'bio', 'website']
