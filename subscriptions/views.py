import hashlib
import hmac
import json
import logging
import os

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt

from objects.hotmart.purchase_approved_webhook import PurchaseApprovedResponse
from subscriptions.circle.api_interface import CircleAPI
from subscriptions.circle.upload_file import upload_file
from subscriptions.hotmart.api_extractor import extract_subscriptions_view
from subscriptions.integrations.circle_hotmart_integration import update_non_subscribed_users
from subscriptions.integrations.email import EmailSender
from subscriptions.integrations.excel_download import export_non_subscribed_users_to_excel
from subscriptions.models import CircleUser, HotmartSubscription, NonSubscribedCircleUser
from subscriptions.utils.password_gen import PasswordGenerator

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


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


def validate_signature(request):
    # https://developers.hotmart.com/docs/en/2.0.0/webhook/purchase-webhook/
    try:
        secret_token = os.environ.get("HOTMART_SECRET_KEY")
        if not secret_token:
            logging.error("HOTMART_SECRET_KEY is not set in the environment.")
            return False

        received_token = request.headers.get("X-HOTMART-HOTTOK")
        if not received_token:
            logging.warning("Missing 'X-HOTMART-HOTTOK' in the request headers.")
            return False

        if received_token != secret_token:
            logging.warning("Invalid 'X-HOTMART-HOTTOK' token.")
            return False

        return True

    except Exception as e:
        logging.exception(f"Error validating 'X-HOTMART-HOTTOK': {e}")
        return False


def parse_webhook_payload(request):
    try:
        return json.loads(request.body), None
    except json.JSONDecodeError:
        return None, JsonResponse({"error": "Invalid JSON"}, status=400)


@csrf_exempt
def invite_circle_user(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    if not validate_signature(request):
        return JsonResponse({"error": "Invalid signature"}, status=403)

    payload, error_response = parse_webhook_payload(request)
    if error_response:
        return error_response

    try:
        response_payload = PurchaseApprovedResponse(**payload)

        buyer_name = response_payload.data.buyer.name
        buyer_email = response_payload.data.buyer.email
        subscription_name = response_payload.data.subscription.plan.name
        is_quarterly_plan = response_payload.data.subscription.plan.is_quarterly
        buyer_password = PasswordGenerator().generate()
        community_id = 94039

        data = {
            'name': buyer_name,
            'email': buyer_email,
            'subscription_name': subscription_name,
            'is_quarterly_plan': is_quarterly_plan
        }

        if not is_quarterly_plan:
            member_tag_ids = [85328]
            space_ids = [790485]

        elif is_quarterly_plan:
            member_tag_ids = [125528]
            space_ids = []

        else:
            raise ValueError("Invalid plan type")

        CircleAPI(api_key=os.environ['CIRCLE_API_V1_KEY']).invite_community_member(
            member_email=buyer_email,
            member_name=buyer_name,
            community_id=community_id,
            password=buyer_password,
            member_tag_ids=member_tag_ids,
            space_ids=space_ids
        )

        email_sender = EmailSender(
            sender_email=os.environ['CIRCLE_SENDER_EMAIL'],
            sender_password=os.environ['CIRCLE_SENDER_EMAIL_SECRET'],
            sender_alias="Rotina Perfeita"
        )


        logging.info(f"Gerando senha para {buyer_email}")

        email_html_body = render_to_string(
            'circle_invite_email.html',
            {'password': buyer_password, 'buyer_email': buyer_email}
        )

        logging.info(f"Enviando email para {buyer_email}")

        email_sender.send_email(
            recipient_email=buyer_email,
            body=email_html_body,
            subject="Seu acesso ao Clube chegou! 🎉"
        )

        logging.info(f"Email enviado para {buyer_email} com sucesso")

        return JsonResponse(
            {"message": "Webhook processed successfully", "content": data},
            status=200
        )

    except Exception as e:
        logging.error(f"Erro ao processar webhook: {str(e)}")
        return JsonResponse({"error": "Internal server error"}, status=500)
