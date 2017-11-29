# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from mothulity.forms import FileFieldForm, OptionsForm
from mothulity.models import JobID, SubmissionData
import utils
import uuid

# Create your views here.


def index(request):
    if request.method == "POST":
        form = FileFieldForm(request.POST,
                             request.FILES)
        if form.is_valid():
            upld_files = request.FILES.getlist("file_field")
            for upfile in upld_files:
                utils.write_file(upfile,
                                 settings.MEDIA_URL)
                utils.chmod_file("{}{}".format(settings.MEDIA_URL,
                                               upfile),
                                 mod=666)
                if utils.sniff_file("{}{}".format(settings.MEDIA_URL,
                                                  upfile),
                                    "fastq") is True:
                    pass
                else:
                    form = FileFieldForm()
                    return render(request,
                                  "mothulity/index.html.jj2",
                                  {"form": form,
                                   "upload_error": True})
            form = OptionsForm()
            return render(request,
                          "mothulity/options.html.jj2",
                          {"form": form})
    else:
        form = FileFieldForm()
    return render(request,
                  "mothulity/index.html.jj2",
                  {"form": form})


def submit(request):
    job_id = uuid.uuid4()
    job_id_link = "{}{}".format(request.build_absolute_uri(),
                                job_id)
    job = JobID(job_id=job_id)
    job.save()
    sub_data = job.submissiondata_set.create(job_name=request.POST["job_name"],
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
    return render(request,
                  "mothulity/submit.html.jj2",
                  {"notify_email": request.POST["notify_email"],
                   "job_id_link": job_id_link})
