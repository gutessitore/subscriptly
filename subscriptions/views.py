import hashlib
import hmac
import json

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

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


HOTMART_SECRET_KEY = getattr(settings, "HOTMART_SECRET_KEY", "sua-chave-secreta-hotmart")

def validate_signature(request):
    """
    Valida a assinatura HMAC-SHA256 enviada pela Hotmart.
    """
    signature = request.headers.get("x-hotmart-hmac-sha256")
    if not signature:
        return False

    computed_signature = hmac.new(
        HOTMART_SECRET_KEY.encode(),
        request.body,
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(signature, computed_signature)

def parse_webhook_payload(request):
    """
    Faz o parsing do corpo da requisição JSON.
    """
    try:
        return json.loads(request.body), None
    except json.JSONDecodeError:
        return None, JsonResponse({"error": "Invalid JSON"}, status=400)

@csrf_exempt
def invite_circle_user(request):
    """
    Endpoint para receber e processar webhooks da Hotmart.
    """
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    # Valida a assinatura do webhook
    if not validate_signature(request):
        return JsonResponse({"error": "Invalid signature"}, status=403)

    # Faz o parsing do payload
    payload, error_response = parse_webhook_payload(request)
    if error_response:
        return error_response

    # Processa os dados do webhook
    try:
        # Exemplo de processamento
        buyer_name = payload.get("buyer", {}).get("name", "N/A")
        product_name = payload.get("product", {}).get("name", "N/A")
        print(f"Compra recebida: {buyer_name} comprou {product_name}")

        # Salvar no banco de dados, chamar outro serviço, etc.
        # Exemplo:
        # Compra.objects.create(
        #     nome_cliente=buyer_name,
        #     produto=product_name,
        #     email=payload.get("buyer", {}).get("email", "N/A")
        # )

        return JsonResponse({"status": "success"}, status=200)

    except Exception as e:
        # Log do erro para depuração
        print(f"Erro ao processar webhook: {str(e)}")
        return JsonResponse({"error": "Internal server error"}, status=500)