# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from io import BytesIO
import os
import uuid
from mothulity import views, models, utils, sched


class UtilsTests(TestCase):
    """
    Tests for uploaded files validator.
    """
    def setUp(self):
        """
        Sets up class level attributes for the tests.

        Parameters
        -------
        fastq_file: str
            Path to test fastq file.
        summ_file: str
            Path to test non-fastq file.
        """
        fastq_file = "mothulity/tests/Mock_S280_L001_R1_001.fastq"
        summ_file = "mothulity/tests/mothur.job.trim.contigs.summary"
        self.remote_machine = "headnode"
        self.fastq_file_remote = "/home/dizak/misc/mothulity_django_tests/Mock_S280_L001_R1_001.fastq"
        self.fastq_file = "{}/{}".format(settings.BASE_DIR,
                                         fastq_file)
        self.summ_file = "{}/{}".format(settings.BASE_DIR,
                                        summ_file)
        self.mock_md5sum = "7e4f54362bd0f030a623a6aaba27ddba"

    def test_sniff_true(self):
        """
        Tests whether utils.sniff returns <True> on fastq file.
        """
        self.assertIs(utils.sniff_file(self.fastq_file), True)

    def test_sniff_false(self):
        """
        Tests whether utils.sniff returns <False> on fastq file.
        """
        self.assertIs(utils.sniff_file(self.summ_file), False)

    def test_count_seqs(self):
        self.assertEqual(utils.count_seqs(self.fastq_file), 4779)

    def test_md5sum(self):
        self.assertEqual(utils.md5sum(self.fastq_file),
                         self.mock_md5sum)

    def test_md5sum_remote(self):
        self.assertEqual(utils.md5sum(self.fastq_file_remote,
                                      remote=True,
                                      machine=self.remote_machine),
                         self.mock_md5sum)


class ViewsResponseTests(TestCase):
    """
    Tests for the response codes.
    """
    def setUp(self):
        """
        Sets up class level attributes for the tests.

        Parameters
        -------
        urls_list: list of str
            List urls postfixes to be tested by django's test client.
        """
        self.urls_list = ["index"]

    def test_response_code(self):
        """
        Tests whether response code of available urls equals <200>.
        """
        for url in self.urls_list:
            response = self.client.get(reverse("mothulity:{}".format(url)))
            self.assertIs(response.status_code, 200)


class ModelsTest(TestCase):
    """
    Tests for the models database API.
    """
    def setUp(self):
        """
        Sets up class level attrubutes for the tests.

        Parameters
        -------
        test_job_id: str
            UUID created ad hoc and converted into str.
        """
        self.test_job_id = str(uuid.uuid4())
        self.test_seqs_count = 17

    def test_job_id(self):
        """
        Tests whether job_id is properly saved and retrieved into and from the\
        model.
        """
        j_id = models.JobID(job_id=self.test_job_id)
        j_id.save()
        self.assertIs(j_id.job_id, self.test_job_id)

    def test_seqsstats(self):
        j_id = models.JobID(job_id=self.test_job_id)
        j_id.save()
        stats = j_id.seqsstats_set.create(seqs_count=self.test_seqs_count)
        self.assertIs(stats.seqs_count, self.test_seqs_count)


class SchedulerTests(TestCase):
    """
    Tests for the scheduler actions.
    """
    def setUp(self):
        """
        Sets up class level attributes for the tests.

        Parameters
        -------
        sinfo_raw: str
            Path to test sinfo log file.
        long_idle_nodes: int, <61>
            Number of nodes idle in queue long.
        """
        self.sinfo_file = "mothulity/tests/sinfo.log"
        self.long_idle_nodes = 61
        self.accel_idle_nodes = 12
        self.accel_alloc_nodes = 3

    def test_parse_sinfo(self):
        """
        Tests whether sinfo log file returns expected values.
        """
        with open(self.sinfo_file) as fin:
            sinfo_str = fin.read()
        self.assertEqual(sched.parse_sinfo(sinfo_str,
                                           partition="long",
                                           state="idle"),
                         self.long_idle_nodes)
        self.assertEqual(sched.parse_sinfo(sinfo_str,
                                           partition="accel",
                                           state="idle"),
                         self.accel_idle_nodes)
        self.assertEqual(sched.parse_sinfo(sinfo_str,
                                           partition="accel",
                                           state="alloc"),
                         self.accel_alloc_nodes)
