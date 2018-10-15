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
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "{}.settings".format(
        [i for i in os.path.abspath(sys.argv[1]).split('/') if len(i) > 0][-1]
        ),
    )
django.setup()

from mothulity import utils

min_ns_free = settings.MIN_NS_FREE
min_phis_free = settings.MIN_PHIS_FREE
max_retry = settings.MAX_RETRY
files_to_copy = settings.FILES_TO_COPY
interval = settings.INTERVAL
headnode_prefix = settings.HEADNODE_PREFIX_URL
media_url = settings.MEDIA_URL


def job():
    """
    Retrieve pending jobs and submit them properly to the computing cluster.
    """
    for i in utils.get_pending_ids():
        print("\nJobID {} Status: pending\n".format(i))
        idle_ns = utils.parse_sinfo(utils.ssh_cmd("sinfo"), "long", "idle")
        idle_phis = utils.parse_sinfo(utils.ssh_cmd("sinfo"), "accel", "idle")
        if utils.get_seqs_count(i) > 500000:
            if idle_phis > min_phis_free:
                if utils.queue_submit(i, headnode_prefix) is True:
                    utils.change_status(i)
                    print("JobID {} submitted".format(i))
            else:
                print("Only {} phi nodes free. {} phi must stay free".format(idle_phis,
                                                                             min_phis_free))
        if utils.get_seqs_count(i) < 500000:
            if idle_ns > min_ns_free:
                if utils.queue_submit(i, headnode_prefix) is True:
                    utils.change_status(i)
                    print("JobID {} submitted".format(i))
            else:
                print("Only {} n nodes free. {} n nodes must stay free".format(idle_ns,
                                                                               min_ns_free))
    for i in utils.get_ids_with_status("submitted"):
        print("\nJobID {} Status: submitted. Retries: {}\n".format(i,
                                                                   utils.get_retry(i)))
        job_sshfs_dir = "{}{}/".format(media_url, str(i).replace("-", "_"))
        if utils.isrunning(i) is False and utils.isdone(job_sshfs_dir) is False and utils.get_retry(i) >= max_retry:
            print("JobID above retry limit. Changing its status to <dead>")
            utils.change_status(i, "dead")
            break
        if utils.isrunning(i) is False and utils.isdone(job_sshfs_dir) is False and utils.get_retry(i) < max_retry:
            print("JobID {} is NOT done and is NOT runnning. Will be resubmitted".format(i))
            utils.remove_except(job_sshfs_dir, 'fastq', safety=False)
            utils.change_status(i, "pending")
            utils.add_retry(i, utils.get_retry(i) + 1)
            break
        if utils.isrunning(i) is False and utils.isdone(job_sshfs_dir, filename="*shared") is True:
            print("JobID {} is done".format(i))
            utils.change_status(i, "done")
            break
    for i in utils.get_ids_with_status("done"):
        print("\nJobID {} Status: done.\n".format(i))
        job_sshfs_dir = "{}{}/".format(media_url, str(i).replace("-", "_"))
        if utils.isdone(job_sshfs_dir, filename='*zip'):
            utils.remove_except(job_sshfs_dir, '*zip', safety=False)
            utils.change_status(i, 'closed')


schedule.every(interval).seconds.do(job)


def main():
    while True:
        schedule.run_pending()


if __name__ == '__main__':
    main()
