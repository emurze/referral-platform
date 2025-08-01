# Generated by Django 5.2.4 on 2025-07-24 07:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0004_user_referral_code"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="referrer",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="referrals",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
