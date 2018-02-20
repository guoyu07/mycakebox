# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-02-05 17:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('rider', '0001_initial'),
        ('customer', '0001_initial'),
        ('merchant', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_id', models.CharField(default='ABC', max_length=10, unique=True)),
                ('cake_cost', models.CharField(max_length=100)),
                ('cake_weight', models.CharField(max_length=100)),
                ('instructions', models.TextField(default='')),
                ('origin', models.TextField(default='')),
                ('origin_locality', models.CharField(default='', max_length=100)),
                ('pickup_date', models.CharField(default=0, max_length=50)),
                ('pickup_time', models.CharField(default=0, max_length=50)),
                ('drop_date', models.CharField(default=0, max_length=50)),
                ('drop_time', models.CharField(default=0, max_length=50)),
                ('destination', models.TextField(default='')),
                ('destination_locality', models.CharField(default='', max_length=100)),
                ('duration', models.CharField(max_length=100)),
                ('distance', models.CharField(max_length=100)),
                ('approx_total', models.CharField(default=0, max_length=50)),
                ('discount_total', models.CharField(default=0, max_length=50)),
                ('sub_total', models.CharField(default=0, max_length=50)),
                ('final_total', models.CharField(max_length=50)),
                ('approve', models.BooleanField(default=False)),
                ('delivery_type', models.CharField(choices=[('Normal', 'Normal'), ('Jet', 'Jet'), ('Superjet', 'Superjet')], default='Normal', max_length=120)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Shipped', 'Shipped'), ('Complete', 'Complete'), ('Cancelled', 'Cancelled'), ('Ready to Pick', 'Ready to Pick')], default='Pending', max_length=120)),
                ('notify_merchant', models.BooleanField(default=False)),
                ('notify_rider', models.BooleanField(default=False)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='customer.Customer')),
                ('merchant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='merchant.Merchant')),
                ('rider', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rider.Rider')),
            ],
        ),
    ]