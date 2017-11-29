# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from io import BytesIO
import os
import uuid
from mothulity import views, models, utils


class FileSniffTests(TestCase):
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
        self.fastq_file = "{}/{}".format(settings.BASE_DIR,
                                         fastq_file)
        self.summ_file = "{}/{}".format(settings.BASE_DIR,
                                        summ_file)

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

    def test_job_id(self):
        """
        Tests whether job_id is properly saved and retrieved into and from the\
        model.
        """
        j_id = models.JobID(job_id=self.test_job_id)
        j_id.save()
        self.assertIs(j_id.job_id, self.test_job_id)


class MultipleFilesFormTest(TestCase):
    """
    Tests for the multiple files upload on the index view.
    """
    def setUp(self):
        """
        Sets up class level attributes for the tests.

        Parameters
        -------
        upload_dir: str
            Directory from django.conf.settings.MEDIA_URL which servers as
            the file upload directory.
        test_content: int, 1
            Content of the uploaded test file. Due to potential problems with
            str encoding it is simply <1>.
        test_file: BytesIO object.
            Mimics the file that would be normally saved on the drive.
        test_file.name: str
            Name of the test_file artificial object.
        """
        self.upload_dir = settings.MEDIA_URL
        self.test_content = 1
        self.test_file = BytesIO(b"{}".format(self.test_content))
        self.test_file.name = "artificial_file.dat"

    def test_form(self):
        """
        Tests whether uploading file into a form using POST method is
        succesful.
        """
        self.client.post("/mothulity/", {"file_field": self.test_file})
        with open("{}/{}".format(self.upload_dir,
                                 self.test_file.name)) as fin:
            self.assertIs(int(fin.read()),
                          self.test_content)
        os.remove("{}/{}".format(self.upload_dir, self.test_file.name))
