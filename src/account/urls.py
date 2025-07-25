from django.urls.conf import path

from account import views

app_name = "account"

urlpatterns = [
    path("login/", views.login, name="login"),
    path("verify-code/", views.verify_code, name="verify-code"),
]
