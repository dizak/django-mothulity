# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from mothulity.forms import FileFieldForm, OptionsForm
from mothulity.models import *
import utils
import uuid
import subprocess as sp

# Create your views here.


def index(request,
          seqs_limit=900000):
    if request.method == "POST":
        form = FileFieldForm(request.POST,
                             request.FILES)
        if form.is_valid():
            job_id = uuid.uuid4()
            upld_dir = "{}{}/".format(settings.MEDIA_URL,
                                      job_id)
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
                                    "fastq") is True:
                    pass
                else:
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
            seqs_stats = job.seqsstats_set.create(seqs_count=seqs_count)
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
    job = get_object_or_404(JobID, job_id=job)
    job.submissiondata_set.create(job_name=request.POST["job_name"],
                                  notify_email=request.POST["notify_email"],
                                  max_ambig=request.POST["max_ambig"],
                                  max_homop=request.POST["max_homop"],
                                  min_length=request.POST["min_length"],
                                  max_length=request.POST["max_length"],
                                  min_overlap=request.POST["min_overlap"],
                                  screen_criteria=request.POST["screen_criteria"],
                                  chop_length=request.POST["chop_length"],
                                  precluster_diffs=request.POST["precluster_diffs"],
                                  classify_seqs_cutoff=request.POST["classify_seqs_cutoff"],
                                  amplicon_type=request.POST["amplicon_type"])
    job.jobstatus_set.create(job_status="pending")
    return render(request,
                  "mothulity/submit.html.jj2",
                  {"notify_email": request.POST["notify_email"],
                   "job_id": job.job_id})


def status(request,
           job):
    job = get_object_or_404(JobID, job_id=job)
    return render(request,
                  "mothulity/status.html.jj2",
                  {"job_id": job.job_id})
