from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from account import services
from account.serializers import LoginSerializer


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
