from django.db import transaction

from account.generators import generate_verification_code
from account.models import User, VerificationCode
from account.senders import send_verification_code


def login(phone_number: str) -> str:
    """
    Log in a user via phone number.

    This function performs the following steps atomically:
    1. Retrieves an existing user by phone number, or creates a new one.
    2. Generates a one-time verification code.
    3. Sends the verification code associated with the user.
    4. Returns the verification code to the user.
    """
    with transaction.atomic():
        code = generate_verification_code()
        user = User.objects.get_or_create_user(phone_number=phone_number)
        VerificationCode.objects.create(user=user, code=code)

    send_verification_code(code)
    return code
