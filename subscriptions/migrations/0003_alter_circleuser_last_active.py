# Generated by Django 5.1 on 2024-09-02 22:12

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0002_alter_circleuser_active_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='circleuser',
            name='last_active',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
    ]
