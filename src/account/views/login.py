from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from account import services
from account.serializers import LoginSerializer


@swagger_auto_schema(
    method="POST",
    request_body=LoginSerializer,
    responses={
        200: openapi.Response(
            description="Verification code sent successfully",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "message": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example="Verification code sent",
                    ),
                    "verification_code": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example="123456",
                    ),
                },
            ),
        ),
        400: openapi.Response(
            description="Bad Request (invalid phone number or "
            "other validation errors)",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "phone_number": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_STRING),
                        example=["Enter a valid phone number."],
                    )
                },
            ),
        ),
    },
    operation_summary="Login",
    operation_description=(
        "Accepts a phone number and sends a verification code. "
        "**Note:** For this simple application, "
        "the verification code is returned "
        "directly in the JSON response for testing/demo purposes. "
        "In production, this would typically be sent via SMS or email."
    ),
    tags=["Authentication"],
)
@api_view(["POST"])
def login(request: Request) -> Response:
    """
    Handle user login by phone number.

    Validates the incoming phone number, creates or retrieves a user,
    generates a verification code, and sends it to the user.

    For demonstration and testing, the verification code is returned in the
    response JSON. In a production environment, the code would be sent
    via SMS or another secure method instead of returning it directly.
    """
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    code = services.login(serializer.validated_data["phone_number"])
    return Response(
        {
            "message": f"Verification code sent",
            "verification_code": code,
        },
        status=status.HTTP_200_OK,
    )
