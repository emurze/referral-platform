import uuid
from unittest.mock import patch

import pytest
from faker import Faker
from rest_framework.reverse import reverse
from rest_framework.test import APIClient


@pytest.fixture
def api_client() -> APIClient:
    """Fixture that provides a fresh instance of APIClient for testing."""
    return APIClient()


def register_user(
    faker: Faker,
    api_client: APIClient | None = None,
) -> APIClient:
    """
    Register and authenticate a user through the API.

    Simulates user login by posting a phone number, verifying the code,
    and setting the token in the APIClient credentials for authenticated
    requests.
    """
    if api_client is None:
        api_client = APIClient()

    phone_number = fake_phone_number(faker)
    response = api_client.post(
        path=reverse("account:login"),
        data={"phone_number": phone_number},
    )
    code = response.data["verification_code"]

    response = api_client.post(
        path=reverse("account:verify-code"),
        data={"phone_number": phone_number, "verification_code": code},
    )
    token = response.data["token"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {token}")

    return api_client


@pytest.fixture
@patch("account.senders.time.sleep", return_value=None)
def aclient(_, api_client: APIClient, faker: Faker) -> APIClient:
    """Pytest fixture that provides an authenticated API client."""
    return register_user(faker, api_client)


def fake_phone_number(faker: Faker) -> str:
    """Generate a fake phone number in a specific format."""
    return f"+91 {faker.msisdn()[3:]}"


def generate_code() -> str:
    """Generate a short verification code using UUID."""
    return str(uuid.uuid4())[:4]
