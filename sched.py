#! /usr/bin/env python


import os
import sys
import schedule
import subprocess as sp
from glob import glob
from time import sleep

import django
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict

sys.path.append(os.path.abspath(sys.argv[1]))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_site.settings")
django.setup()

from mothulity.models import *
from mothulity import utils

min_ns_free = settings.MIN_NS_FREE
min_phis_free = settings.MIN_PHIS_FREE
max_retry = settings.MAX_RETRY
files_to_copy = settings.FILES_TO_COPY
interval = settings.INTERVAL
headnode_prefix = settings.HEADNODE_PREFIX_URL
media_url = settings.MEDIA_URL


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


def get_ids_with_status(status="submitted",
                        status_model=JobStatus):
    """
    Returns Job IDs of jobs with given status.

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
    return JobID.objects.get(job_id=job_id).seqsstats.seqs_count


def get_slurm_id(job_id):
    """
    Returns slurm ID retrieved from JobStatus model.

    Parameters
    -------
    job_id: str
        Job ID by which sequece count is returned.

    Returns
    -------
    int
        slurm ID.
    """
    return JobID.objects.get(job_id=job_id).jobstatus.slurm_id


def get_retry(job_id):
    """
    Returns number of retry from JobStatus model.

    Parameters
    -------
    job_id: str
        Job ID by which sequece count is returned.

    Returns
    -------
    int
        Retry number.
    """
    return JobID.objects.get(job_id=job_id).jobstatus.retry


def queue_submit(job_id,
                 headnode_prefix,
                 sbatch_success="Submitted batch job"):
    """
    Retrieves required data from models by Job ID, renders mothulity command,
    copies files to computing cluster and sends the mothulity command. Adds
    JobStatus.slurm_id after slurm.

    Parameters
    -------
    job_id: str
        Job ID by which rest of data are retrieved.

    Returns
    -------
    bool
        <True> if md5sum of the input files matches on the web-server and
        computing cluster, <False> otherwise.
    """
    job = JobID.objects.get(job_id=job_id)
    seqs_count = job.seqsstats.seqs_count
    sub_data = model_to_dict(job.submissiondata)
    job_id_dir = '{}{}/'.format(headnode_prefix, str(job_id).replace('-', '_'))
    if seqs_count > 500000:
        sub_data["resources"] = "phi"
    else:
        sub_data["resources"] = "n"
    moth_cmd = utils.render_moth_cmd(moth_files=job_id_dir,
                                     moth_opts=sub_data,
                                     pop_elems=["job_id",
                                                "amplicon_type"])
    sbatch_out = utils.ssh_cmd(moth_cmd)
    if sbatch_success in sbatch_out:
        add_slurm_id(job_id=job_id,
                     slurm_id=int(sbatch_out.split(" ")[-1]))
        return True
    else:
        return False


def remove_except(directory,
                  extension,
                  safety=True):
    """
    Remove non-recursively everything from the directory except extension.

    Parameters
    -------
    directory: str
        Directory path from which the unwanted files will be removed.
    extension: str
        Files ending with this will NOT be removed from the directory.
    """
    if not directory.endswith('/'):
        directory = directory + '/'
    files = glob('{}*'.format(directory))
    files_to_remove = [i for i in files if extension not in i]
    if safety:
        try:
            return sp.check_output(
                'ls {}'.format(' '.join(files_to_remove)),
                shell=True,
                ).decode('utf-8')
        except Exception as e:
            return False
    else:
        try:
            return sp.check_output(
                'rm {}'.format(' '.join(files_to_remove)),
                shell=True,
                ).decode('utf-8')
        except Exception as e:
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
    job = JobID.objects.get(job_id=job_id)
    job.jobstatus.job_status = new_status
    job.jobstatus.save()


def add_slurm_id(job_id,
                 slurm_id,
                 status_model=JobStatus):
    """
    Adds submission ID to the existing set in the JobStatus model.

    Parameters
    -------
    job_id: str
        Job ID of job which status should be changed.
    slurm_id: int
        Submission ID.
    status_model: django.models.Model, default JobStatus
        Django model to use.
    """
    job = JobID.objects.get(job_id=job_id)
    job.jobstatus.slurm_id = slurm_id
    job.jobstatus.save()


def add_retry(job_id,
              retry,
              status_model=JobStatus):
    """
    Adds retry existing set in the JobStatus model.

    Parameters
    -------
    job_id: str
        Job ID of job which status should be changed.
    retry: int
        Retry number.
    status_model: django.models.Model, default JobStatus
        Django model to use.
    """
    job = JobID.objects.get(job_id=job_id)
    job.jobstatus.retry = retry
    job.jobstatus.save()


def isrunning(job_id,
              status_model=JobStatus):
    """
    Check if job is actually running on the computing cluster.

    Parameters
    ------
    job_id: str
        Job ID of job which status should be changed.
    status_model: django.models.Model, default JobStatus
        Django model to use.

    Returns
    -------
    bool
        True is submitted ID has <R> state in squeue output.
    """
    slurm_id = get_slurm_id(job_id)
    if utils.parse_squeue(utils.ssh_cmd("squeue"), slurm_id, "ST") == "R":
        return True
    else:
        return False


def isdone(directory,
           filename="analysis*zip"):
    """
    Check for the zipped analysis on the computing cluster and copy it back if
    it exists or return False otherwise.

    Parameters
    -------
    upld_dir: str
        Path to files on the computing cluster.

    Returns
    -------
    bool
        True if file exists or False if it does not.
    """
    try:
        sp.check_output(
            "ls {}{}".format(directory, filename),
            check_output=True
            ).decode('utf-8')
        return True
    except Exception as e:
        return False


def get_from_cluster(filename,
                     upld_dir,
                     headnode_dir):
    """
    Copy zipped analysis file from the computing cluster back to the
    web-server and check md5sum afterwards.

    Parameters
    -------
    filename: str
        Name of file to copy. Glob is accepted.
    upld_dir: str
        Path to files on the web-service server.
    headnode_dir: str
        Path to files on the computing cluster.
    """
    sp.call("scp headnode:{}{} {}".format(headnode_dir,
                                          filename,
                                          upld_dir),
            shell=True)


def job():
    """
    Retrieve pending jobs and submit them properly to the computing cluster.
    """
    for i in get_pending_ids():
        print("\nJobID {} Status: pending\n".format(i))
        idle_ns = utils.parse_sinfo(utils.ssh_cmd("sinfo"), "long", "idle")
        idle_phis = utils.parse_sinfo(utils.ssh_cmd("sinfo"), "accel", "idle")
        if get_seqs_count(i) > 500000:
            if idle_phis > min_phis_free:
                if queue_submit(i, headnode_prefix) is True:
                    change_status(i)
                    print("JobID {} submitted".format(i))
            else:
                print("Only {} phi nodes free. {} phi must stay free".format(idle_phis,
                                                                             min_phis_free))
        if get_seqs_count(i) < 500000:
            if idle_ns > min_ns_free:
                if queue_submit(i, headnode_prefix) is True:
                    change_status(i)
                    print("JobID {} submitted".format(i))
            else:
                print("Only {} n nodes free. {} n nodes must stay free".format(idle_ns,
                                                                               min_ns_free))
    for i in get_ids_with_status("submitted"):
        print("\nJobID {} Status: submitted. Retries: {}\n".format(i,
                                                                   get_retry(i)))
        job_sshfs_dir = "{}{}/".format(media_url, str(i).replace("-", "_"))
        if isrunning(i) is False and isdone(job_sshfs_dir) is False and get_retry(i) >= max_retry:
            print("JobID above retry limit. Changing its status to <dead>")
            change_status(i, "dead")
            break
        if isrunning(i) is False and isdone(job_sshfs_dir) is False and get_retry(i) < max_retry:
            print("JobID {} is NOT done and is NOT runnning. Will be resubmitted".format(i))
            remove_except(job_sshfs_dir, 'fastq', safety=False)
            change_status(i, "pending")
            add_retry(i, get_retry(i) + 1)
            break
        if isrunning(i) is False and isdone(job_sshfs_dir, filename="*shared") is True:
            print("JobID {} is done".format(i))
            change_status(i, "done")
            break
    for i in get_ids_with_status("done"):
        print("\nJobID {} Status: done.\n".format(i))
        job_sshfs_dir = "{}{}/".format(media_url, str(i).replace("-", "_"))
        if isdone(job_sshfs_dir, filename='*zip'):
            remove_except(job_sshfs_dir, '*zip', safety=False)
            change_status(i, 'closed')


schedule.every(interval).seconds.do(job)


def main():
    while True:
        schedule.run_pending()


if __name__ == '__main__':
    main()
