# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class JobID(models.Model):
    job_id = models.CharField(max_length=50)

    def __str__(self):
        return self.job_id


class SubmissionData(models.Model):
    job_id = models.ForeignKey(JobID,
                               on_delete=models.CASCADE)
    job_name = models.CharField(max_length=20)
    notify_email = models.CharField(max_length=40)
    max_ambig = models.IntegerField()
    max_homop = models.IntegerField()
    min_length = models.IntegerField()
    max_length = models.IntegerField()
    min_overlap = models.IntegerField()
    screen_criteria = models.IntegerField()
    chop_length = models.IntegerField()
    precluster_diffs = models.IntegerField()
    classify_seqs_cutoff = models.IntegerField()
    amplicon_type = models.CharField(max_length=3)

    def __str__(self):
        return self.job_name
