from datetime import datetime, timedelta
from subscriptions.models import CircleUser, HotmartSubscription, NonSubscribedCircleUser


def get_filtered_circle_users(hotmart_emails, diversity_emails, tags_to_exclude):
    circle_users = (
        CircleUser.objects
        .exclude(email__in=hotmart_emails)
        .exclude(email__in=diversity_emails)
    )

    return [
        user for user in circle_users
        if not any(tag in tags_to_exclude for tag in user.tags)
    ]

def populate_non_subscribed_users(circle_users):
    for user in circle_users:
        NonSubscribedCircleUser.objects.update_or_create(
            email=user.email,
            defaults={
                'first_name': user.first_name,
                'last_name': user.last_name,
                'profile_url': user.profile_url,
                'active_status': user.active_status,
                'member_since': user.member_since,
                'hotmart_search_link': get_hotmart_url_data(user.email)
            }
        )


def get_hotmart_url_data(email):
    accession_date = int((datetime.now() - timedelta(days=365 * 5)).timestamp() * 1000)
    end_accession_date = int(datetime.now().timestamp() * 1000)
    return (f"https://app.hotmart.com/subscriptions?accessionDate={ accession_date }"
            f"&endAccessionDate={ end_accession_date }&status%5B0%5D=ACTIVE&status%5B1%5D=DELAYED"
            f"&status%5B2%5D=CANCELLED_BY_ADMIN&status%5B3%5D=CANCELLED_BY_CUSTOMER"
            f"&status%5B4%5D=CANCELLED_BY_SELLER&status%5B5%5D=INACTIVE&status%5B6%5D=STARTED"
            f"&status%5B7%5D=OVERDUE&email={ email }")


def update_non_subscribed_users():
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
    circle_users = get_filtered_circle_users(hotmart_emails, emails_diversity_program,tags_to_exclude)
    populate_non_subscribed_users(circle_users)
