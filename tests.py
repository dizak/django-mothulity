# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from django.urls import reverse
from . import views

# Create your tests here.


class IndexViewTests(TestCase):
    """
    Tests for the index view
    """
    def test_response_code(self):
        response = self.client.get(reverse("mothulity:index"))
        self.assertIs(response.status_code, 200)
