# Generated by Django 5.1.4 on 2024-12-29 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snackshop', '0006_alter_product_weight'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sub_category',
            field=models.CharField(blank=True, choices=[('chips', 'Chips'), ('cookies', 'Cookies'), ('jerky', 'Jerky'), ('bars', 'Bars'), ('nuts', 'Nuts & Trail Mix')], max_length=50, null=True),
        ),
    ]
