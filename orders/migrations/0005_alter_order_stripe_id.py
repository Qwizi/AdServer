# Generated by Django 3.2.5 on 2021-07-06 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_alter_order_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='stripe_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
