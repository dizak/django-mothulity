# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from mothulity.forms import FileFieldForm, OptionsForm
import utils

# Create your views here.


def index(request):
    if request.method == "POST":
        form = FileFieldForm(request.POST,
                             request.FILES)
        if form.is_valid():
            upld_files = request.FILES.getlist("file_field")
            for upfile in upld_files:
                utils.write_file(upfile,
                                 settings.MEDIA_URL)
            return render(request,
                          "mothulity/options.html.jj2",
                          {"methods": request.FILES.getlist("file_field")})
    else:
        form = FileFieldForm()
    return render(request,
                  "mothulity/index.html.jj2",
                  {"form": form})


def options(request):
    if request.method == "POST":
        form = OptionsForm(request.POST)
        if form.is_valid():
            return render(request,
                          "mothulity/submit.html.jj2")
    else:
        form = OptionsForm()
    return render(request,
                  "mothulity/options.html.jj2",
                  {"form": form})


def submit(request):
    return render(request,
                  "mothulity/submit.html.jj2",
                  {"results": request.POST})
