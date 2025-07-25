from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from account import services
from account.exceptions import (
    InvalidOrExpiredTokenException,
    UserNotFoundException,
    VerificationCodeNotFoundException,
)
from account.serializers import VerifyCodeSerializer


@api_view(["POST"])
def verify_code(request: Request) -> Response:
    """
    Verify a user's phone number with a verification code and return
    an authentication token.

    Validates the input data, attempts to verify the provided code against
    the user's stored verification codes, and returns a token if successful.
    """
    serializer = VerifyCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    try:
        token = services.verify_code(
            phone_number=serializer.validated_data["phone_number"],
            code=serializer.validated_data["verification_code"],
        )
        return Response({"token": token}, status=status.HTTP_200_OK)

    except (
        VerificationCodeNotFoundException,
        InvalidOrExpiredTokenException,
    ) as e:
        return Response(
            {"error": e.message},
            status=status.HTTP_400_BAD_REQUEST,
        )

    except UserNotFoundException as e:
        return Response(
            {"error": e.message},
            status=status.HTTP_404_NOT_FOUND,
        )
