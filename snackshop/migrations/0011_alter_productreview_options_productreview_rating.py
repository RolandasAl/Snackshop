# Generated by Django 5.1.4 on 2025-01-04 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snackshop', '0010_alter_product_category_alter_product_sub_category_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productreview',
            options={'ordering': ['-date_created'], 'verbose_name': 'Review', 'verbose_name_plural': 'Reviews'},
        ),
        migrations.AddField(
            model_name='productreview',
            name='rating',
            field=models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], null=True),
        ),
    ]
