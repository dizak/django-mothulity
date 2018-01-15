# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from froala_editor.fields import FroalaField
from django.utils import timezone
import pytz

# Create your models here.


class JobID(models.Model):
    job_id = models.CharField(max_length=50)

    def __str__(self):
        return self.job_id


class SeqsStats(models.Model):
    job_id = models.OneToOneField(JobID,
                                  on_delete=models.CASCADE,
                                  primary_key=True)
    seqs_count = models.IntegerField()

    def __int__(self):
        return self.seqs_count


class SubmissionData(models.Model):
    job_id = models.OneToOneField(JobID,
                                  on_delete=models.CASCADE,
                                  primary_key=True)
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


class JobStatus(models.Model):
    """
    Model for job status description.

    Parameters
    -------
    added_time: int
        Number of times a job has been submitted.
    """
    job_id = models.OneToOneField(JobID,
                                  on_delete=models.CASCADE,
                                  primary_key=True)
    job_status = models.CharField(max_length=10)
    slurm_id = models.IntegerField(null=True)
    retry = models.IntegerField(default=0)
    submission_time = models.DateTimeField("submission time",
                                           default=timezone.now)

    def __str__(self):
        return self.job_status


class Article(models.Model):
    """
    Model for small wiki articles.
    """
    title = models.CharField(max_length=100)
    content = FroalaField()
