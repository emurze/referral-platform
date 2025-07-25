import uuid


def generate_verification_code() -> str:
    """Generate a short verification code using UUID."""
    return str(uuid.uuid4())[:4]


def generate_referral_code() -> str:
    """Generate a short referral code using UUID."""
    return str(uuid.uuid4())[:6]
