from typing import NoReturn

from rest_framework import serializers


class SetReferrerSerializer(serializers.Serializer):
    """
    Serializer for validating the referral code input when setting a referrer.
    """

    referral_code = serializers.CharField(required=True)

    @staticmethod
    def validate_referral_code(value: str) -> str | NoReturn:
        """Validate the format of the referral code."""
        if len(value) != 6:
            raise serializers.ValidationError("Invalid referral code format.")
        return value


class UserProfileSerializer(serializers.Serializer):
    """
    Serializer for representing a user's profile data including referrals.
    """

    phone_number = serializers.CharField()
    my_referral_code = serializers.CharField()
    used_referral_code = serializers.CharField(allow_null=True)
    referrals = serializers.ListField(child=serializers.CharField())
