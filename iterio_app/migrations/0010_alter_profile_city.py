# Generated by Django 5.0.4 on 2024-06-01 06:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iterio_app', '0009_city_remove_serviceprovider_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='iterio_app.city'),
        ),
    ]