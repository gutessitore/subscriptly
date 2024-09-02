from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

import pandas as pd

from subscriptions.form_upload.upload_file import upload_file


def index(par):
    return HttpResponse('Process completed successfully')


def upload_page(request):
    return upload_file(request)
