# Generated by Django 4.2.6 on 2023-11-06 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cours', '0005_subscription'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='subscribe',
            field=models.BooleanField(default=False, verbose_name='подписка'),
        ),
    ]