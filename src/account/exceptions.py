class VerificationCodeNotFoundException(Exception):
    """
    Exception raised when a verification code matching the criteria
    (e.g., code value, not blocked) cannot be found for a user.
    """

    message: str = "Verification code not found"


class InvalidOrExpiredTokenException(Exception):
    """
    Exception raised when a provided verification code is either invalid
    or has expired based on the configured expiration time.
    """

    message: str = "Invalid or expired code"


class UserNotFoundException(Exception):
    """Exception raised when no user exists for the given phone number."""

    message: str = "User not found"
