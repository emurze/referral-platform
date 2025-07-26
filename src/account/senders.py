import time


def send_verification_code(code: str) -> None:
    """Simulate sending a verification code to the user."""
    time.sleep(2)
    print(f"Verification code sent: {code}")
