# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import os
import sys
import schedule
import subprocess as sp

import django
from django.conf import settings
from django.shortcuts import get_object_or_404

sys.path.append("/home/dizak/Software/django_site/")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_site.settings")
django.setup()

from mothulity.models import *
from mothulity import utils


def get_pending_ids():
    return [i.job_id for i in JobStatus.objects.filter(job_status="pending")]


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
    os.system("ssh headnode {}".format(moth_cmd))


def change_status(job_id,
                  new_status="submitted"):
    job = JobStatus.objects.filter(job_id=job_id)[0]
    job.job_status = new_status
    job.save()


def job():
    idle_ns = utils.parse_sinfo(utils.ssh_cmd("sinfo"),
                                "long",
                                "idle")
    if idle_ns > 30:
        pending_ids = get_pending_ids()
        for i in pending_ids:
            upld_dir = "{}{}".format(settings.MEDIA_URL, i)
            headnode_dir = "{}{}".format(settings.HEADNODE_PREFIX_URL,
                                         i)
            queue_submit(i, upld_dir, headnode_dir)
            change_status(i)


schedule.every(1).seconds.do(job)


def main():
    while True:
        schedule.run_pending()


if __name__ == '__main__':
    main()
