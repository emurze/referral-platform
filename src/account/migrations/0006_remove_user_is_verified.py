# Generated by Django 5.2.4 on 2025-07-24 12:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0005_user_referrer"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="is_verified",
        ),
    ]
