from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render

from subscriptions.circle.upload_file import upload_file
from subscriptions.hotmart.api_extractor import extract_subscriptions_view
from subscriptions.integrations.circle_hotmart_integration import update_non_subscribed_users
from subscriptions.integrations.excel_download import export_non_subscribed_users_to_excel
from subscriptions.models import CircleUser, HotmartSubscription, NonSubscribedCircleUser


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # redireciona para a página principal
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def index(request):
    return render(request, 'index.html')


@login_required
def upload_page(request):
    return upload_file(request)


def success_view(request):
    return render(request, 'success.html')


def home_view(request):
    return render(request, 'home.html')


@login_required
def circle_user_list_view(request):
    users = CircleUser.objects.all()
    return render(request, 'circle_user_list.html', {'users': users})


@login_required
def list_hotmart_users_view(request):
    subscriptions = HotmartSubscription.objects.all()
    return render(request, 'list_hotmart_users.html', {'subscriptions': subscriptions})


@login_required
def extract_hotmart_data(request):
    return extract_subscriptions_view(request)


@login_required
def list_non_subscribed_circle_users(request):
    update_non_subscribed_users()
    users = NonSubscribedCircleUser.objects.all()
    return render(request, 'compare_users.html', {'users': users})


@login_required
def export_users_to_excel(request):
    response = export_non_subscribed_users_to_excel()
    return response
