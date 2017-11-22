# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

# Create your views here.


def index(request):
    return HttpResponse("Hello from index view")
