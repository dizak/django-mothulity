# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-07 11:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mothulity', '0006_jobstatus_time_added'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobstatus',
            name='time_added',
        ),
    ]
