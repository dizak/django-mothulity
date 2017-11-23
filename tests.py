# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from django.urls import reverse
from . import views

# Create your tests here.


class setUp(TestCase):
    """
    Sets up class level attributes for the tests.

    Parameters
    -------
    urls_list: list of str
        List urls postfixes to be tested by django's test client.
    """
    urls_list = ["index",
                 "options"]


class ViewsResponseTests(setUp):
    """
    Tests for the index view
    """
    def test_response_code(self):
        for url in self.urls_list:
            response = self.client.get(reverse("mothulity:{}".format(url)))
            self.assertIs(response.status_code, 200)
