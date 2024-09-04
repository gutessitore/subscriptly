from datetime import datetime, timedelta

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


def compare_users_view(request):

    emails_diversity_program = [
        "kelly.sts17@gmail.com", "alanisesteffanysilvaa@gmail.com",
        "beatriz.ngonc@gmail.com", "stephmmeireles@gmail.com",
        "marcellafariasid@gmail.com", "amandabarbozacontato@gmail.com",
        "heloisa.chs@gmail.com", "dressa.lops@gmail.com",
        "camylagcelestino@gmail.com", "depaula.stephanny@gmail.com",
        "juuhcmartins@gmail.com", "alannacarla@outlook.com.br",
        "oliveiramara0987@gmail.com", "thaisv.franca@gmail.com",
        "bialaris17@gmail.com", "aanabia033@gmail.com",
        "angelborges@hotmail.com", "annanaan304@gmail.com",
        "brunaluisasantos07@gmail.com", "estelamscoelho@gmail.com",
        "iasmyn.almeida78@gmail.com", "julia.nyte@hotmail.com",
        "kedmabarroso15@gmail.com", "laurarosa299@gmail.com",
        "castromayara@outlook.com", "saramirandacontato@hotmail.com",
        "scoelho684@gmail.com", "valsortiz@yahoo.com.br",
        "vic.dames@gmail.com"
    ]

    tags_to_exclude = ['Equipe do Clube', 'Embaixadora']

    hotmart_emails = HotmartSubscription.objects.values_list('subscriber_email', flat=True)
    circle_users = (
        CircleUser.objects
        .exclude(email__in=hotmart_emails)
        .exclude(email__in=emails_diversity_program)
    )

    circle_users = [
        user for user in circle_users if
        not any(tag in tags_to_exclude for tag in user.tags)
    ]

    all_tags = set()
    for user in circle_users:
        all_tags.update(user.tags)

    accession_date = int((datetime.now() - timedelta(days=365 * 5)).timestamp() * 1000)
    end_accession_date = int(datetime.now().timestamp() * 1000)
    status = 'ACTIVE'

    context = {
        'circle_users': circle_users,
        'unique_tags': sorted(all_tags),
        'hotmart_url_data': {
            'accession_date': accession_date,
            'end_accession_date': end_accession_date,
            'status': status
        }
    }

    return render(request, 'compare_users.html', context)
