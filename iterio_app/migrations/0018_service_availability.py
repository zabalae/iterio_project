# Generated by Django 5.0.4 on 2024-06-02 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iterio_app', '0017_remove_service_availability'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='availability',
            field=models.TextField(blank=True),
        ),
    ]
