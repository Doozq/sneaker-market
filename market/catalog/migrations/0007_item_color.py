# Generated by Django 4.2.3 on 2024-05-27 19:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0006_orderhistory"),
    ]

    operations = [
        migrations.AddField(
            model_name="item",
            name="color",
            field=models.CharField(
                default="",
                help_text="Перечислите цвета",
                max_length=150,
                verbose_name="Цвет",
            ),
        ),
    ]