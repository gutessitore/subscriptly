import os
from datetime import datetime, timedelta

import requests
from django.shortcuts import render, redirect
from django.utils.timezone import make_aware

from subscriptions.hotmart.subscription_form import HotmartSubscriptionForm
from subscriptions.models import HotmartSubscription


class HotmartAPI:
    def __init__(self):
        # Obtem as credenciais das variáveis de ambiente
        self.client_id = os.environ['CLIENT_ID']
        self.client_secret = os.environ['CLIENT_SECRET']
        self.basic_auth = os.environ['BASIC_AUTH']
        self.access_token = self.get_oauth_token()

    def get_oauth_token(self):
        url = "https://api-sec-vlc.hotmart.com/security/oauth/token"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Basic {self.basic_auth}'
        }
        params = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }

        response = requests.post(url, headers=headers, params=params)

        if response.status_code == 200:
            self.access_token = response.json()['access_token']
            return self.access_token
        else:
            raise Exception(f"Failed to get token: {response.status_code} {response.text}")

    def get_subscriptions(self, statuses, accession_date=None, next_page_token=None):
        if accession_date is None:
            # Calcula a data de hoje menos 365 dias e converte para milissegundos
            accession_date = int((datetime.now() - timedelta(days=365)).timestamp() * 1000)

        url = "https://developers.hotmart.com/payments/api/v1/subscriptions"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.access_token}'
        }
        params = {
            'status': statuses,
            'accession_date': accession_date
        }
        if next_page_token:
            params['page_token'] = next_page_token

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            result = response.json()
            items = result['items']
            if 'next_page_token' in result['page_info'] and result['page_info']['next_page_token']:
                # Recursivamente ou em loop, carrega mais dados se houver um next_page_token
                more_items = self.get_subscriptions(statuses, accession_date,
                                                    result['page_info']['next_page_token'])
                items.extend(more_items)
            return items
        else:
            raise Exception(f"Error fetching subscriptions: {response.status_code} {response.text}")


def convert_timestamp_to_datetime(timestamp):
    return make_aware(datetime.fromtimestamp(timestamp / 1000))


def extract_subscriptions_view(request):
    if request.method == 'POST':
        form = HotmartSubscriptionForm(request.POST)
        if form.is_valid():
            statuses = form.cleaned_data['statuses']
            api = HotmartAPI()
            subscriptions = api.get_subscriptions(statuses)

            for sub in subscriptions:
                HotmartSubscription.objects.create(
                    subscriber_code=sub['subscriber_code'],
                    subscription_id=sub['subscription_id'],
                    status=sub['status'],
                    accession_date=convert_timestamp_to_datetime(sub['accession_date']),
                    request_date=convert_timestamp_to_datetime(sub['request_date']),
                    trial=sub['trial'],
                    plan_name=sub['plan']['name'],
                    plan_id=sub['plan']['id'],
                    recurrency_period=sub['plan']['recurrency_period'],
                    product_name=sub['product']['name'],
                    product_id=sub['product']['id'],
                    product_ucode=sub['product']['ucode'],
                    price_currency_code=sub['price']['currency_code'],
                    price_value=sub['price']['value'],
                    subscriber_name=sub['subscriber']['name'],
                    subscriber_ucode=sub['subscriber']['ucode'],
                    subscriber_email=sub['subscriber']['email'],
                    date_next_charge=convert_timestamp_to_datetime(sub['date_next_charge']),
                    transaction=sub['transaction']
                )

            return redirect('success')
    else:
        form = HotmartSubscriptionForm()

    return render(request, 'extract_subscriptions.html', {'form': form})
