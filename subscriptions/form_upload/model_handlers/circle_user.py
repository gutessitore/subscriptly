import csv
import json
from dateutil.parser import parse
from subscriptions.models import CircleUser

COLUMN_TO_FIELD_MAP = {
    'User ID': 'user_id',
    'First Name': 'first_name',
    'Last Name': 'last_name',
    'Email': 'email',
    'Join Date': 'member_since',
    'Active (Signed In Last 30 Days)': 'active_status',
    'Member Tags': 'tags',
    'Location': 'location',
    'Headline': 'headline',
    'Bio': 'bio',
    'Profile URL': 'profile_url',
    'Website': 'website',
    'Twitter URL': 'twitter_url',
    'Facebook URL': 'facebook_url',
    'LinkedIn URL': 'linkedin_url',
    'Instagram URL': 'instagram_url',
    'No. of Posts': 'num_posts',
    'No. of Comments': 'num_comments',
    'No. of Likes Received': 'num_likes_received',
    'Avatar URL': 'image_url',
    'Last Active': 'last_active'
}


def handle_circle_user_form_upload(file):
    reader = csv.DictReader(file.read().decode('utf-8').splitlines())

    for row in reader:
        data = {
            map_column_to_field(column): parse_field(map_column_to_field(column), value)
            for column, value in row.items() if map_column_to_field(column)
        }

        CircleUser.objects.update_or_create(
            email=data['email'],
            defaults=data
        )


def parse_date_field(value):
    """Converte a string de data para datetime ou retorna None se estiver vazia."""
    return parse(value) if value else None


def parse_tags_field(value):
    """Converte o campo tags de JSON para uma lista ou retorna uma lista vazia."""
    return json.loads(value) if value else []


def map_column_to_field(column):
    """Retorna o nome do campo correspondente para a coluna dada ou None se não for encontrado."""
    return COLUMN_TO_FIELD_MAP.get(column)


def parse_field(field_name, value):
    """Converte o valor conforme o tipo de campo."""
    if field_name in ['member_since', 'last_active']:
        return parse_date_field(value)
    elif field_name == 'tags':
        return parse_tags_field(value)
    return value
