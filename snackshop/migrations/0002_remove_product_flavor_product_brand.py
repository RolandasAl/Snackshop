# Generated by Django 5.1.4 on 2024-12-29 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snackshop', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='flavor',
        ),
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
