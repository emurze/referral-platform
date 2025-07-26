import pytest
from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.test import APIClient
from account.models import User, VerificationCode
from rest_framework.authtoken.models import Token
from django.utils import timezone
from datetime import timedelta

from config.settings import VERIFICATION_CODE_EXPIRATION_MINUTES
from conftest import generate_code, fake_phone_number


@pytest.mark.django_db
def test_can_verify(
    api_client: APIClient,
    faker: Faker,
) -> None:
    # arrange by creating a user and valid code
    user = User.objects.create(phone_number=fake_phone_number(faker))
    code = VerificationCode.objects.create(user=user, code="1234")
    VerificationCode.objects.create(user=user, code="1234")

    # act
    url = reverse("account:verify-code")
    response = api_client.post(
        url,
        {
            "phone_number": user.phone_number,
            "verification_code": code.code,
        },
    )

    # assert
    assert response.status_code == status.HTTP_200_OK
    assert "token" in response.data

    # token is created and linked to the user
    token = Token.objects.get(user=user)
    assert response.data["token"] == token.key


@pytest.mark.django_db
def test_cannot_verify_when_verification_code_empty(
    api_client: APIClient,
    faker: Faker,
) -> None:
    # act
    url = reverse("account:verify-code")
    response = api_client.post(
        path=url,
        data={
            "phone_number": fake_phone_number(faker),
            "verification_code": "",
        },
        format="json",
    )

    # assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["verification_code"] == [
        "This field may not be blank."
    ]


@pytest.mark.django_db
def test_cannot_verify_when_phone_number_empty(api_client: APIClient) -> None:
    # act
    url = reverse("account:verify-code")
    response = api_client.post(
        path=url,
        data={
            "phone_number": "",
            "verification_code": "1234",
        },
        format="json",
    )

    # assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["phone_number"] == ["This field may not be blank."]


@pytest.mark.django_db
def test_cannot_verify_when_verification_code_not_found(
    api_client: APIClient,
    faker: Faker,
) -> None:
    # arrange
    phone_number = fake_phone_number(faker)
    User.objects.create(phone_number=phone_number)

    # act
    url = reverse("account:verify-code")
    response = api_client.post(
        path=url,
        data={
            "phone_number": phone_number,
            "verification_code": "wrong-code",
        },
        format="json",
    )

    # assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Verification code not found"


@pytest.mark.django_db
def test_cannot_verify_verification_code_expired(
    api_client: APIClient,
    faker: Faker,
) -> None:
    # arrange
    phone_number = fake_phone_number(faker)
    code = generate_code()
    user = User.objects.create(phone_number=phone_number)
    VerificationCode.objects.create(
        user=user,
        code=code,
        created_at=timezone.now()
        - timedelta(minutes=VERIFICATION_CODE_EXPIRATION_MINUTES + 1),
    )

    # act
    url = reverse("account:verify-code")
    response = api_client.post(
        path=url,
        data={"phone_number": phone_number, "verification_code": code},
        format="json",
    )

    # assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Invalid or expired code"


@pytest.mark.django_db
def test_cannot_verify_when_user_not_found(
    api_client: APIClient,
    faker: Faker,
) -> None:
    # act
    url = reverse("account:verify-code")
    response = api_client.post(
        path=url,
        data={
            "phone_number": fake_phone_number(faker),
            "verification_code": "1234",
        },
        format="json",
    )

    # assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "User not found"
