import pandas as pd
from django.http import HttpResponse

from subscriptions.models import NonSubscribedCircleUser


def export_non_subscribed_users_to_excel():
    users = NonSubscribedCircleUser.objects.all().values(
        'first_name', 'last_name', 'email', 'profile_url',
        'active_status', 'member_since', 'hotmart_search_link'
    )

    df = pd.DataFrame(users)

    if 'member_since' in df.columns and pd.api.types.is_datetime64_any_dtype(df['member_since']):
        df['member_since'] = df['member_since'].dt.tz_localize(None)

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="potentially_non_subscribed_circle_users.xlsx"'

    df.to_excel(response, index=False)  # type: ignore
    return response