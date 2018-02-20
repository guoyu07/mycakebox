# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-02-20 16:56
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rider', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rider',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='rider',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='rider',
            name='rider_id',
        ),
        migrations.AddField(
            model_name='rider',
            name='rider',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
