from django.db import transaction

from account.models import User
from user_profile.exceptions import ReferralCodeValidationError


def set_referrer(current_user: User, referral_code: str) -> None:
    """
    Assign a referrer to the current user based on a given referral code.

    This function ensures that:
    - The current user does not already have a referrer.
    - The user cannot use their own referral code.
    - The provided referral code exists and corresponds to a valid user.

    The operation is executed inside a database transaction for atomicity.
    """
    with transaction.atomic():
        if current_user.referrer_id is not None:
            raise ReferralCodeValidationError("You already have a referrer.")

        if current_user.referral_code == referral_code:
            raise ReferralCodeValidationError(
                "You cannot use your own referral code."
            )

        try:
            current_user.referrer = User.objects.get(
                referral_code=referral_code,
            )
        except User.DoesNotExist:
            raise ReferralCodeValidationError(
                "This referral code does not exist."
            )

        current_user.save()
