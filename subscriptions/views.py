from django.http import HttpResponse
from django.shortcuts import render

from subscriptions.form_upload.upload_file import upload_file
from subscriptions.hotmart.api_extractor import extract_subscriptions_view
from subscriptions.models import CircleUser, HotmartSubscription


def index(request):
    return render(request, 'index.html')


def upload_page(request):
    return upload_file(request)


def success_view(request):
    return render(request, 'success.html')


def home_view(request):
    return render(request, 'home.html')


def circle_user_list_view(request):
    users = CircleUser.objects.all()
    return render(request, 'circle_user_list.html', {'users': users})


def list_hotmart_users_view(request):
    subscriptions = HotmartSubscription.objects.all()
    return render(request, 'list_hotmart_users.html', {'subscriptions': subscriptions})


def extract_hotmart_data(request):
    return extract_subscriptions_view(request)
