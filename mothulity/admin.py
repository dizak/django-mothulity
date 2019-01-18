# -*- coding: utf-8 -*-


from django.contrib import admin
from mothulity.models import *


class SubmissionDataAdmin(admin.ModelAdmin):
    list_display = (
        'job_id',
        "job_name",
        "notify_email",
        "amplicon_type",
    )


class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title",)


class PathSettingsAdmin(admin.ModelAdmin):
    list_display = ('site',)


class WebServerSettingsAdmin(admin.ModelAdmin):
    list_display = ('site',)


class HPCSettingsAdmin(admin.ModelAdmin):
    list_display = ('site',)


admin.site.register(JobID)
admin.site.register(SubmissionData, SubmissionDataAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(PathSettings, PathSettingsAdmin)
admin.site.register(WebServerSettings, WebServerSettingsAdmin)
admin.site.register(HPCSettings, HPCSettingsAdmin)
