# Generated by Django 5.1.4 on 2025-01-13 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snackshop', '0022_orderitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('waiting for payment', 'Waiting for Payment'), ('shipped', 'Shipped'), ('completed', 'Completed'), ('paid', 'Paid')], default='pending', max_length=50),
        ),
    ]
