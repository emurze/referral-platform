from django.db import transaction

from account.models import User


def get_profile(user: User) -> dict:
    """
    Retrieve the profile data for a given user, including referral
    information.

    This function executes within an atomic transaction to ensure
    data consistency. It fetches the user's phone number, their referral code,
    the referral code used by the user (if any), and a list of phone numbers
    for users they have referred.
    """
    with transaction.atomic():
        referrals = user.referrals.only("phone_number").values_list(
            "phone_number",
            flat=True,
        )
        return {
            "phone_number": str(user.phone_number),
            "my_referral_code": user.referral_code,
            "used_referral_code": (
                user.referrer.referral_code if user.referrer_id else None
            ),
            "referrals": [str(phone_number) for phone_number in referrals],
        }
