# Generated by Django 5.0.4 on 2024-05-28 00:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iterio_app', '0006_profile_user_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pictures'),
        ),
    ]