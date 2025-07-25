import random
import string
from unittest.mock import patch

import pytest
from django.urls import reverse
from faker import Faker
from rest_framework import status

from rest_framework.test import APIClient

from conftest import register_user


@pytest.mark.django_db
@patch("account.senders.time.sleep", return_value=None)
def test_can_set_referrer(
    _,
    aclient: APIClient,
    faker: Faker,
) -> None:
    # arrange
    api_client = register_user(faker)
    response = api_client.get(reverse("user_profile:profile"))
    user1_referral_code = response.json()["my_referral_code"]

    # act
    url = reverse("user_profile:set-referrer")
    response = aclient.put(url, data={"referral_code": user1_referral_code})

    # assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == "Referral code successfully set"


@pytest.mark.django_db
@patch("account.senders.time.sleep", return_value=None)
def test_cannot_set_referrer_when_client_already_have_referrer(
    _,
    aclient: APIClient,
    faker: Faker,
) -> None:
    # arrange
    client2 = register_user(faker)
    client2_response = client2.get(reverse("user_profile:profile"))
    client2_referral_code = client2_response.json()["my_referral_code"]

    client3 = register_user(faker)
    client3_response = client3.get(reverse("user_profile:profile"))
    client3_referral_code = client3_response.json()["my_referral_code"]

    url = reverse("user_profile:set-referrer")
    aclient.put(url, data={"referral_code": client2_referral_code})

    # act
    url = reverse("user_profile:set-referrer")
    response = aclient.put(url, data={"referral_code": client3_referral_code})

    # assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["referral_code"] == ["You already have a referrer."]


@pytest.mark.django_db
def test_cannot_set_referrer_when_referral_code_mine(
    aclient: APIClient,
) -> None:
    # arrange
    url = reverse("user_profile:profile")
    response = aclient.get(url)
    my_referral_code = response.json()["my_referral_code"]

    # act
    url = reverse("user_profile:set-referrer")
    response = aclient.put(url, data={"referral_code": my_referral_code})

    # assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["referral_code"] == [
        "You cannot use your own referral code."
    ]


@pytest.mark.django_db
def test_cannot_set_referrer_when_referral_code_does_not_exist(
    aclient: APIClient,
) -> None:
    # arrange by generate a completely new 6-character alphanumeric code
    new_referral_code = "".join(
        random.choices(string.ascii_uppercase + string.digits, k=6)
    )

    # act
    url = reverse("user_profile:set-referrer")
    response = aclient.put(url, data={"referral_code": new_referral_code})

    # assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["referral_code"] == [
        "This referral code does not exist."
    ]


@pytest.mark.django_db
def test_cannot_set_referrer_when_referral_code_empty(
    aclient: APIClient,
) -> None:
    # act
    url = reverse("user_profile:set-referrer")
    response = aclient.put(url, data={"referral_code": ""})

    # assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["referral_code"] == ["This field may not be blank."]


@pytest.mark.django_db
def test_cannot_set_referrer_when_referral_code_invalid(
    aclient: APIClient,
) -> None:
    # act
    url = reverse("user_profile:set-referrer")
    response = aclient.put(url, data={"referral_code": "S" * 7})

    # assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["referral_code"] == [
        "Invalid referral code format."
    ]
