# Generated by Django 3.1.3 on 2020-11-27 16:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bot_service', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='album',
            old_name='videos',
            new_name='video',
        ),
    ]
