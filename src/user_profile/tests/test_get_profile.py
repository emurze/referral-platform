from unittest.mock import patch

import pytest
from faker import Faker
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse

from conftest import register_user


@pytest.mark.django_db
def test_can_get_profile(aclient: APIClient) -> None:
    # act
    url = reverse("user_profile:profile")
    response = aclient.get(url)

    # assert
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_can_get_generated_referral_code(aclient: APIClient) -> None:
    # act
    url = reverse("user_profile:profile")
    response = aclient.get(url)

    # assert
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["my_referral_code"]) == 6


@pytest.mark.django_db
@patch("account.senders.time.sleep", return_value=None)
def test_can_get_referrals(
    _,
    aclient: APIClient,
    faker: Faker,
) -> None:
    # arrange by retrieving invite code from current user
    client1_response = aclient.get(reverse("user_profile:profile"))

    # and by assigning referrer to this invite code
    client2 = register_user(faker)
    client2.put(
        reverse("user_profile:set-referrer"),
        data={"referral_code": client1_response.json()["my_referral_code"]},
    )

    # act
    client1_response = aclient.get(reverse("user_profile:profile"))

    # assert
    client2_response = client2.get(reverse("user_profile:profile"))
    client2_phone_number = client2_response.json()["phone_number"]

    assert client1_response.json()["referrals"] == [client2_phone_number]


@pytest.mark.django_db
@patch("account.senders.time.sleep", return_value=None)
def test_user_can_see_used_referral_code(
    _,
    aclient: APIClient,
    faker: Faker,
) -> None:
    # arrange by retrieving invite code from current user
    client1_response = aclient.get(reverse("user_profile:profile"))
    client1_referral_code = client1_response.json()["my_referral_code"]

    # and by assigning referrer to this invite code
    client2 = register_user(faker)
    client2.put(
        reverse("user_profile:set-referrer"),
        data={"referral_code": client1_referral_code},
    )

    # act
    client2_response = client2.get(reverse("user_profile:profile"))

    # assert
    assert (
        client2_response.json()["used_referral_code"] == client1_referral_code
    )


@pytest.mark.django_db
def test_cannot_get_profile_when_user_not_authenticated(
    api_client: APIClient,
) -> None:
    # act
    url = reverse("user_profile:profile")
    response = api_client.get(url)

    # assert
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
