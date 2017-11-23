# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404

# Create your views here.


def index(request):
    return render(request,
                  "mothulity/index.html.jj2",
                  {"msg": "rendered by index view"})


def options(request):
    return render(request,
                  "mothulity/options.html.jj2",
                  {"methods": request.method})
