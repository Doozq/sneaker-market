# Generated by Django 4.2.3 on 2023-11-21 14:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0003_delete_myuser_person"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="image",
            field=models.ImageField(null=True, upload_to=""),
        ),
    ]
