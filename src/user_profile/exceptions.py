from dataclasses import dataclass


@dataclass(eq=False)
class ReferralCodeValidationError(Exception):
    """Exception raised for errors related to invalid referral codes."""

    message: str
