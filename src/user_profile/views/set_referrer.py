from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from user_profile import services
from user_profile.exceptions import ReferralCodeValidationError
from user_profile.serializers import SetReferrerSerializer


@swagger_auto_schema(
    method="PUT",
    request_body=SetReferrerSerializer,
    responses={
        200: openapi.Response(
            description="Referral code set successfully",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "status": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example="Referral code successfully set",
                    )
                },
            ),
        ),
        400: openapi.Response(
            description="Invalid referral code or bad request",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "referral_code": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_STRING),
                        example=["This referral code is invalid or expired."],
                    )
                },
            ),
        ),
        401: openapi.Response(
            description="Unauthorized",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "detail": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example="Authentication credentials were not provided.",
                    )
                },
            ),
        ),
    },
    operation_summary="Set Referrer Code",
    operation_description=(
        "Sets a referral code for the authenticated user. "
        "The code must be valid and not previously used."
    ),
    tags=["User Profile"],
)
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
