# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-05 13:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mothulity', '0004_seqsstats'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_status', models.CharField(max_length=10)),
                ('job_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mothulity.JobID')),
            ],
        ),
    ]
