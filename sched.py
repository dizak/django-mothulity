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


def get_pending_ids(ids_quantity=20,
                    status="pending",
                    status_model=JobStatus):
    """
    Returns Job IDs of oldest pending jobs within given limit retrieved from
    JobStatus model.

    Parameters
    -------
    ids_quantity: int, default <20>
        Maximium number of Job IDs to return.
    status: str, default <pending>
        Status of job in JobStatus model.
    status_model: django.models.Model, default JobStatus
        Django model to use.

    Returns
    -------
    list of str
        job_id with <pending> status.
    """
    ids = [i.job_id for i in status_model.objects.filter(job_status=status).
           order_by("-submission_time")]
    if len(ids) < ids_quantity:
        return ids
    else:
        return ids[:ids_quantity]


def get_submitted_ids(status="submitted",
                      status_model=JobStatus):
    """
    Returns Job IDs of submitted jobs

    Parameters
    -------
    status: str, default <submitted>
        Status of job in JobStatus model.
    status_model: django.models.Model, default JobStatus
        Django model to use.

    Returns
    -------
    list of str
        job_id with <submitted> status.
    """
    return [i.job_id for i in status_model.objects.filter(job_status=status)]


def get_seqs_count(job_id):
    """
    Returns total sequence count retrieved from SeqsStats model.

    Parameters
    -------
    job_id: str
        Job ID by which sequece count is returned.

    Returns
    -------
    int
        Sequence count.
    """
    job = get_object_or_404(JobID, job_id=job_id)
    return job.seqsstats_set.values()[0]["seqs_count"]


def queue_submit(job_id,
                 upld_dir,
                 headnode_dir,
                 sbatch_success="Submitted batch job"):
    """
    Retrieves required data from models by Job ID, renders mothulity command,
    copies files to computing cluster and send the command.

    Parameters
    -------
    job_id: str
        Job ID by which rest of data are retrieved.
    upld_dir: str
        Path to input files on the web-service server.
    headnode_dir: str
        Path to input files on the computing cluster.

    Returns
    -------
    bool
        <True> if md5sum of the input files matches on the web-server and
        computing cluster, <False> otherwise.
    """
    job = get_object_or_404(JobID, job_id=job_id)
    seqs_count = job.seqsstats_set.values()[0]["seqs_count"]
    sub_data = job.submissiondata_set.values()[0]
    if seqs_count > 500000:
        sub_data["resources"] = "phi"
    moth_cmd = utils.render_moth_cmd(moth_files=headnode_dir,
                                     moth_opts=sub_data)
    sp.check_output("scp -r {} headnode:{}".format(upld_dir,
                                                   settings.HEADNODE_PREFIX_URL),
                    shell=True)
    upld_md5 = utils.md5sum("{}*".format(upld_dir))
    headnode_md5 = utils.md5sum("{}*".format(headnode_dir), remote=True)
    if sorted(upld_md5) == sorted(headnode_md5):
        sbatch_out = utils.ssh_cmd(moth_cmd)
        if sbatch_success in sbatch_out:
            return True
    else:
        return False


def change_status(job_id,
                  new_status="submitted",
                  status_model=JobStatus):
    """
    Changes status from pending to submitted in the JobStatus model.

    Parameters
    -------
    job_id: str
        Job ID of job which status should be changed.
    new_status: str
        Content of new status.
    status_model: django.models.Model, default JobStatus
        Django model to use.
    """
    job = status_model.objects.filter(job_id=job_id)[0]
    job.job_status = new_status
    job.save()


def isdone(job_id,
           headnode_dir):
    """
    Check for the zipped analysis on the computing cluster and copy it back if
    it exists or return False otherwise.

    Parameters
    -------
    job_id: str
        Job ID of which check is made.
    headnode_dir: str
        Path to files on the computing cluster.

    Returns
    -------
    bool
        True if file exists or False if it does not.
    """
    try:
        utils.ssh_cmd("ls {}/{}/analysis*zip".format(headnode_dir, job_id))
        return True
    except Exception as e:
        return False


def get_from_cluster(job_id,
                     upld_dir,
                     headnode_dir):
    """
    Copy zipped analysis file from the computing cluster back to the
    web-server and check md5sum afterwards.

    Parameters
    -------
    job_id: str
        Job ID of which check is made.
    upld_dir: str
        Path to files on the web-service server.
    headnode_dir: str
        Path to files on the computing cluster.
    """
    sp.check_output("scp headnode:{}{}/analysis*zip {}/job_id".format(headnode_dir,
                                                                      job_id,
                                                                      upld_dir),
                    shell=True)


def job():
    """
    Retrieve pending jobs and submit them properly to the computing cluster.
    """
    pending_ids = get_pending_ids()
    submitted_ids = get_submitted_ids()
    for i in pending_ids:
        idle_ns = utils.parse_sinfo(utils.ssh_cmd("sinfo"), "long", "idle")
        idle_phis = utils.parse_sinfo(utils.ssh_cmd("sinfo"), "accel", "idle")
        upld_dir = "{}{}/".format(settings.MEDIA_URL, i)
        headnode_dir = "{}{}/".format(settings.HEADNODE_PREFIX_URL, i)
        if get_seqs_count(i) > 500000 and idle_phis > 5:
            if queue_submit(i, upld_dir, headnode_dir) is True:
                change_status(i)
        if get_seqs_count(i) < 500000 and idle_ns > 30:
            if queue_submit(i, upld_dir, headnode_dir) is True:
                change_status(i)
    for i in submitted_ids:
        upld_dir = "{}{}/".format(settings.MEDIA_URL, i)
        headnode_dir = "{}{}/".format(settings.HEADNODE_PREFIX_URL, i)
        if isdone(i) is True:
            get_from_cluster(i, upld_dir, headnode_dir)


schedule.every(1).seconds.do(job)


def main():
    while True:
        schedule.run_pending()


if __name__ == '__main__':
    main()
