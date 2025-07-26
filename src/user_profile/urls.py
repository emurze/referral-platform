from django.urls import path

from user_profile.views import set_referrer, get_profile

app_name = "user_profile"

urlpatterns = [
    path("", get_profile, name="profile"),
    path("referrer/", set_referrer, name="set-referrer"),
]
