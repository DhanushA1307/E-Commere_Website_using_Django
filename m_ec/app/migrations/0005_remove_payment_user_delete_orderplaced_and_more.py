# Generated by Django 5.0.6 on 2024-05-27 20:37

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0004_payment_orderplaced"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="payment",
            name="user",
        ),
        migrations.DeleteModel(
            name="OrderPlaced",
        ),
        migrations.DeleteModel(
            name="Payment",
        ),
    ]
