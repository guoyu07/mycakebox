# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-02-05 17:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Rider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rider_id', models.CharField(default='ABC', max_length=10, unique=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('locality', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=15)),
                ('alt_phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('flag', models.CharField(choices=[('GREEN', 'GREEN'), ('GREEN', 'GREEN'), ('RED', 'RED')], default='RED', max_length=100)),
                ('slug', models.SlugField(default='', unique=True)),
            ],
        ),
    ]