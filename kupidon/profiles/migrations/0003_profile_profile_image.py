# Generated by Django 5.1.5 on 2025-01-22 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_profile_last_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_image',
            field=models.URLField(blank=True, default=None, null=True),
        ),
    ]
