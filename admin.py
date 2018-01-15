# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from mothulity.models import *


class SeqsStatsAdmin(admin.ModelAdmin):
    list_display = ("seqs_count",)


class SubmissionDataAdmin(admin.ModelAdmin):
    list_display = ("job_name",
                    "notify_email",
                    "amplicon_type")


class JobStatusAdmin(admin.ModelAdmin):
    list_display = ("job_id",
                    "job_status",
                    "slurm_id",
                    "retry",
                    "submission_time")


class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title",)


admin.site.register(JobID)
admin.site.register(SeqsStats, SeqsStatsAdmin)
admin.site.register(SubmissionData, SubmissionDataAdmin)
admin.site.register(JobStatus, JobStatusAdmin)
admin.site.register(Article, ArticleAdmin)
