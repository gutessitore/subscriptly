from django.shortcuts import render

from subscriptions.circle.upload_file import upload_file
from subscriptions.hotmart.api_extractor import extract_subscriptions_view
from subscriptions.integrations.circle_hotmart_integration import update_non_subscribed_users
from subscriptions.integrations.excel_download import export_non_subscribed_users_to_excel
from subscriptions.models import CircleUser, HotmartSubscription, NonSubscribedCircleUser


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


def list_non_subscribed_circle_users(request):
    update_non_subscribed_users()
    users = NonSubscribedCircleUser.objects.all()
    return render(request, 'compare_users.html', {'users': users})


def export_users_to_excel(request):
    response = export_non_subscribed_users_to_excel()
    return response
