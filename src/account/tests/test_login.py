from unittest.mock import patch

import pytest
from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.test import APIClient
from account.models import User, VerificationCode
from conftest import fake_phone_number


@pytest.mark.django_db
@patch("account.senders.time.sleep", return_value=None)
def test_can_login(
    _,
    api_client: APIClient,
    faker: Faker,
) -> None:
    # arrange
    phone_number = fake_phone_number(faker)

    # act
    url = reverse("account:login")
    response = api_client.post(
        path=url,
        data={"phone_number": phone_number},
        ormat="json",
    )

    # assert
    assert response.status_code == status.HTTP_200_OK
    assert response.data["message"] == "Verification code sent"

    # Verify user and code are created
    user = User.objects.get(phone_number=phone_number)
    code = VerificationCode.objects.filter(user=user).last()
    assert code is not None
    assert user.referral_code


@pytest.mark.django_db
@patch("account.senders.time.sleep", return_value=None)
def test_cannot_login_when_phone_number_empty(
    _,
    api_client: APIClient,
) -> None:
    # act
    url = reverse("account:login")
    response = api_client.post(
        path=url,
        data={"phone_number": None},
        format="json",
    )

    # assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["phone_number"] == ["This field may not be null."]


@pytest.mark.django_db
@patch("account.senders.time.sleep", return_value=None)
def test_cannot_login_when_phone_number_invalid(
    _,
    api_client: APIClient,
) -> None:
    # act
    url = reverse("account:login")
    response = api_client.post(
        path=url,
        data={"phone_number": "invalid_phone_number"},
        format="json",
    )

    # assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["phone_number"] == ["Enter a valid phone number."]
