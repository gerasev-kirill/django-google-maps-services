# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-09-06 03:09
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GMapDirectionCache',
            fields=[
                ('id', models.CharField(max_length=337, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('data', jsonfield.fields.JSONField(default=[])),
            ],
        ),
        migrations.CreateModel(
            name='GMapPointCache',
            fields=[
                ('id', models.CharField(max_length=300, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('lat', models.DecimalField(decimal_places=7, max_digits=9)),
                ('lng', models.DecimalField(decimal_places=7, max_digits=9)),
                ('data', jsonfield.fields.JSONField(default=[])),
            ],
        ),
    ]
