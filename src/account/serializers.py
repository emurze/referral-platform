from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers


class VerifyCodeSerializer(serializers.Serializer):
    """Serializer for verifying a phone number with a verification code."""

    phone_number = serializers.CharField()
    verification_code = serializers.CharField()


class LoginSerializer(serializers.Serializer):
    """Serializer for login using a phone number."""

    phone_number = PhoneNumberField()
