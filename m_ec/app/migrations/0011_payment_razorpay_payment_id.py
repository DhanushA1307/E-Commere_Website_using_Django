# Generated by Django 5.0.2 on 2024-06-14 03:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0010_remove_payment_razorpay_order_id_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="payment",
            name="razorpay_payment_id",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]