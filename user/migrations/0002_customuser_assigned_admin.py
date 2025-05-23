# Generated by Django 5.2.1 on 2025-05-16 03:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='assigned_admin',
            field=models.ForeignKey(blank=True, limit_choices_to={'role': 'ADMIN'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_users', to=settings.AUTH_USER_MODEL),
        ),
    ]
