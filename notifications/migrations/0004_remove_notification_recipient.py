# Generated by Django 4.0.3 on 2022-04-08 08:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0003_notification_to_adviser_notification_to_ktto_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='recipient',
        ),
    ]