# Generated by Django 3.2.5 on 2021-07-03 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0002_alter_ad_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='banner',
            field=models.ImageField(null=True, upload_to='uploads/'),
        ),
    ]
