# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import os
import sys
import schedule
import subprocess as sp
from glob import glob

import django
from django.conf import settings
from django.shortcuts import get_object_or_404

sys.path.append("/home/darek/git_repos/django_site/")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_site.settings")
django.setup()

from mothulity.models import *
from mothulity import utils


def get_pending_ids(ids_quantity=5,
                    status="pending",
                    status_model=JobStatus):
        ids = [i.job_id for i in status_model.objects.filter(job_status=status).order_by("-submission_time")]
        if len(ids) < ids_quantity:
            return ids
        else:
            return ids[:ids_quantity]


def get_seqs_count(job_id):
    job = get_object_or_404(JobID, job_id=job_id)
    return job.seqsstats_set.values()[0]["seqs_count"]


def queue_submit(job_id,
                 upld_dir,
                 headnode_dir):
    job = get_object_or_404(JobID, job_id=job_id)
    seqs_count = job.seqsstats_set.values()[0]["seqs_count"]
    sub_data = job.submissiondata_set.values()[0]
    if seqs_count > 500000:
        sub_data["resources"] = "phi"
    moth_cmd = utils.render_moth_cmd(moth_files=headnode_dir,
                                     moth_opts=sub_data)
    os.system("scp -r {} headnode:{}".format(upld_dir,
                                             settings.HEADNODE_PREFIX_URL))
    upld_md5 = utils.md5sum("{}*".format(upld_dir))
    headnode_md5 = utils.md5sum("{}*".format(headnode_dir), remote=True)
    if sorted(upld_md5) == sorted(headnode_md5):
        os.system("ssh headnode {}".format(moth_cmd))


def change_status(job_id,
                  new_status="submitted",
                  status_model=JobStatus):
    job = status_model.objects.filter(job_id=job_id)[0]
    job.job_status = new_status
    job.save()


def job():
    pending_ids = get_pending_ids()
    for i in pending_ids:
        idle_ns = utils.parse_sinfo(utils.ssh_cmd("sinfo"), "long", "idle")
        idle_phis = utils.parse_sinfo(utils.ssh_cmd("sinfo"), "accel", "idle")
        upld_dir = "{}{}/".format(settings.MEDIA_URL, i)
        headnode_dir = "{}{}/".format(settings.HEADNODE_PREFIX_URL, i)
        if get_seqs_count(i) > 500000 and idle_phis > 5:
            queue_submit(i, upld_dir, headnode_dir)
            change_status(i)
        if get_seqs_count(i) < 500000 and idle_ns > 30:
            queue_submit(i, upld_dir, headnode_dir)
            change_status(i)

schedule.every(1).seconds.do(job)


def main():
    while True:
        schedule.run_pending()


if __name__ == '__main__':
    main()
