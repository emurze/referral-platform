from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from user_profile import services
from user_profile.serializers import UserProfileSerializer


@swagger_auto_schema(
    method="GET",
    responses={
        200: UserProfileSerializer,
        401: openapi.Response(
            description="Unauthorized",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "detail": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example="Authentication credentials "
                        "were not provided.",
                    )
                },
            ),
        ),
    },
    operation_summary="Get Profile",
    operation_description="Retrieves the authenticated user's profile "
    "information.",
    tags=["User Profile"],
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_profile(request: Request) -> Response:
    """
    Retrieve the profile of the currently authenticated user.

    Requires the user to be authenticated. Calls the profile service to get
    the user’s profile data and returns it serialized.
    """
    profile = services.get_profile(request.user)
    return Response(data=profile, status=status.HTTP_200_OK)
