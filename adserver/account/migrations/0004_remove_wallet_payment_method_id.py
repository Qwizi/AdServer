# Generated by Django 3.2.5 on 2021-07-05 17:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20210705_1830'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wallet',
            name='payment_method_id',
        ),
    ]
