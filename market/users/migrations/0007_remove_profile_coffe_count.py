# Generated by Django 4.2.3 on 2024-04-22 22:42

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0006_alter_profile_image"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="profile",
            name="coffe_count",
        ),
    ]
