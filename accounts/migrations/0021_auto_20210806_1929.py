# Generated by Django 3.1.5 on 2021-08-06 19:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0020_settings'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Settings',
            new_name='Setting',
        ),
    ]
