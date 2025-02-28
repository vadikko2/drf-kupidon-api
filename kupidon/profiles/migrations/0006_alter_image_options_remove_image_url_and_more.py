# Generated by Django 5.1.5 on 2025-01-27 11:11

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_remove_profile_age_profile_birthdate_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='image',
            options={'ordering': ['profile_order', '-created_at']},
        ),
        migrations.RemoveField(
            model_name='image',
            name='url',
        ),
        migrations.AddField(
            model_name='image',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='image',
            name='file',
            field=models.ImageField(default=django.utils.timezone.now, upload_to='profile_images/'),
            preserve_default=False,
        ),
    ]
