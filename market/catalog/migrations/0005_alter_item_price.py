# Generated by Django 4.2.3 on 2024-05-27 14:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0004_item_price"),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="price",
            field=models.PositiveIntegerField(default=1),
        ),
    ]
