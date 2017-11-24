# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from django.urls import reverse
from . import views


class ViewsResponseTests(TestCase):
    """
    Tests for the index view
    """
    def setUp(self):
        """
        Sets up class level attributes for the tests.

        Parameters
        -------
        urls_list: list of str
            List urls postfixes to be tested by django's test client.
        """
        self.urls_list = ["index",
                          "options"]

    def test_response_code(self):
        """
        Tests whether response code of available urls equals <200>.
        """
        for url in self.urls_list:
            response = self.client.get(reverse("mothulity:{}".format(url)))
            self.assertIs(response.status_code, 200)
