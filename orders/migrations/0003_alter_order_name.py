# Generated by Django 3.2.5 on 2021-07-03 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_order_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='name',
            field=models.CharField(default='Doładowanie portfela', max_length=64),
        ),
    ]
