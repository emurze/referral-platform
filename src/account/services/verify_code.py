from datetime import timedelta

from django.db import transaction
from django.utils import timezone

from account.exceptions import (
    InvalidOrExpiredTokenException,
    UserNotFoundException,
    VerificationCodeNotFoundException,
)
from account.models import User
from rest_framework.authtoken.models import Token

from config.settings import VERIFICATION_CODE_EXPIRATION_MINUTES


def verify_code(phone_number: str, code: str) -> str:
    """
    Verify a user's phone number using a verification code and generate
    an auth token.

    This function performs the following steps atomically:
    1. Retrieve the user by phone number.
    2. Find the latest unblocked verification code matching the input.
    3. Check if the verification code exists and is not expired.
    4. Block the verification code to prevent reuse.
    5. Generate (or retrieve) an authentication token for the user.
    """
    with transaction.atomic():
        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            raise UserNotFoundException()

        verification_code = (
            user.verification_codes.select_for_update()
            .filter(code=code, is_blocked=False)
            .first()
        )

        if not verification_code:
            raise VerificationCodeNotFoundException()

        verification_code_is_expired = (
            timezone.now() - verification_code.created_at
            > timedelta(minutes=VERIFICATION_CODE_EXPIRATION_MINUTES)
        )
        if not verification_code or verification_code_is_expired:
            raise InvalidOrExpiredTokenException()

        verification_code.block()
        verification_code.save()

        auth_token, _ = Token.objects.get_or_create(user=user)
        return auth_token.key
