# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from mothulity.forms import FileFieldForm, OptionsForm
from mothulity.models import *
from mothulity.sched import max_retry, isdone
import utils
import uuid
import subprocess as sp

# Create your views here.


def index(request,
          seqs_limit=900000):
    """
    Evaluates file upload form, uploaded files, total number of reads, creates
    Job ID and renders appropriate template.

    Parameters
    -------
    request: HTTP.request
    seqs_limit: int, default <900000>
        Number of maximum reads per job allowed.

    Return
    ------
    django.template
        Template rendered to HTML.
    """
    if request.method == "POST":
        form = FileFieldForm(request.POST,
                             request.FILES)
        if form.is_valid():
            job_id = uuid.uuid4()
            upld_dir = "{}{}/".format(settings.MEDIA_URL,
                                      str(job_id).replace("-", "_"))
            sp.check_output("mkdir {}".format(upld_dir), shell=True)
            upld_files = request.FILES.getlist("file_field")
            for upfile in upld_files:
                utils.write_file(upfile,
                                 upld_dir)
                utils.chmod_file("{}{}".format(upld_dir,
                                               upfile),
                                 mod=666)
                if utils.sniff_file("{}{}".format(upld_dir,
                                                  upfile),
                                    "fastq") is not True:
                    sp.check_output("rm -r {}".format(upld_dir), shell=True)
                    form = FileFieldForm()
                    return render(request,
                                  "mothulity/index.html.jj2",
                                  {"form": form,
                                   "upload_error": True})
            seqs_count = utils.count_seqs("{}*fastq".format(upld_dir))
            if seqs_count > seqs_limit:
                sp.check_output("rm -r {}".format(upld_dir), shell=True)
                form = FileFieldForm()
                return render(request,
                              "mothulity/index.html.jj2",
                              {"form": form,
                               "too_many_error": True,
                               "seqs_count": seqs_count,
                               "seqs_limit": seqs_limit})
            job = JobID(job_id=job_id)
            job.save()
            seqsstats = SeqsStats(job_id=job, seqs_count=seqs_count)
            seqsstats.save()
            form = OptionsForm()
            return render(request,
                          "mothulity/options.html.jj2",
                          {"form": form,
                           "job": job_id})
    else:
        form = FileFieldForm()
    return render(request,
                  "mothulity/index.html.jj2",
                  {"form": form})


def submit(request,
           job):
    """
    Evaluates options form retrieves Job ID and its properties, renders
    appropriate template.

    Parameters
    -------
    request: HTTP.request
    job: str
        Job ID

    Return
    ------
    django.template
        Template rendered to HTML.
    """
    if request.method == "POST":
        form = OptionsForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            job = get_object_or_404(JobID, job_id=job)
            submissiondata = SubmissionData(job_id=job, **form_data)
            submissiondata.save()
            jobstatus = JobStatus(job_id=job, job_status="pending")
            jobstatus.save()
            return render(request,
                          "mothulity/submit.html.jj2",
                          {"notify_email": request.POST["notify_email"],
                           "job_id": job.job_id})
        else:
            return render(request,
                          "mothulity/options.html.jj2",
                          {"form": form,
                           "job": job})


def status(request,
           job):
    job = get_object_or_404(JobID, job_id=job)
    return render(request,
                  "mothulity/status.html.jj2",
                  {"submissiondata": job.submissiondata,
                   "jobstatus": job.jobstatus,
                   "max_retry": max_retry})
