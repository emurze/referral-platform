from typing import NoReturn

from django.contrib.auth.models import AbstractUser
from django.db import models, transaction, IntegrityError
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

from account.generators import generate_referral_code


class UserManager(models.Manager):
    """Custom manager for the User model that provides utility methods."""

    def get_or_create_user(self, phone_number: str) -> "User" | NoReturn:
        """
        Creates or retrieves a user by phone number with a unique
        referral code using a retry loop.
        """
        for attempt in range(10):
            try:
                with transaction.atomic():
                    referral_code = generate_referral_code()

                    if self.model.objects.filter(
                        referral_code=referral_code
                    ).exists():
                        continue

                    user, created = self.get_or_create(
                        phone_number=phone_number,
                        defaults={"referral_code": referral_code},
                    )
                    return user
            except IntegrityError:
                continue

        raise RuntimeError(
            "Failed to create user with a unique referral code."
        )


class User(AbstractUser):
    """Custom user model identified by phone number."""

    phone_number = PhoneNumberField(unique=True)
    referral_code = models.CharField(max_length=6, unique=True)
    referrer = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="referrals",
    )

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    objects = UserManager()

    username = None
    password = None

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-id"]
        indexes = [
            models.Index(fields=["phone_number"]),
            models.Index(fields=["referral_code"]),
            models.Index(fields=["referrer"]),
        ]

    def __str__(self) -> str:
        return str(self.phone_number)


class VerificationCode(models.Model):
    """
    Class responsible for storing a temporary verification code
    linked to a user.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="verification_codes",
    )
    code = models.CharField(max_length=4)
    created_at = models.DateTimeField(default=timezone.now)
    is_blocked = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Verification Code"
        verbose_name_plural = "Verification Codes"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["created_at"]),
        ]

    def block(self) -> None:
        """Marks the verification code as blocked."""
        self.is_blocked = True

    def __str__(self) -> str:
        return str(self.code)
