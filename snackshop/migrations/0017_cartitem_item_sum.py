# Generated by Django 5.1.4 on 2025-01-08 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snackshop', '0016_order_final_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='item_sum',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
