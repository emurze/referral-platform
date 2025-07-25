import uuid


def generate_referral_code() -> str:
    """Generate a short referral code using UUID."""
    return str(uuid.uuid4())[:6]
