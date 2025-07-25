from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from user_profile import services
from user_profile.exceptions import ReferralCodeValidationError
from user_profile.serializers import SetReferrerSerializer


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def set_referrer(request: Request) -> Response:
    """
    Set a referral code for the authenticated user.

    Validates the provided referral code and assigns it as the user's referrer
    if it is valid and not already used by the user. Returns a success message
    on completion.
    """
    serializer = SetReferrerSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    try:
        services.set_referrer(
            request.user,
            serializer.validated_data["referral_code"],
        )
    except ReferralCodeValidationError as e:
        raise ValidationError({"referral_code": [e.message]})

    return Response(
        {"status": "Referral code successfully set"},
        status=status.HTTP_200_OK,
    )
