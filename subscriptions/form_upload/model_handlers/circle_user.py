import csv
import json
import logging
from dateutil.parser import parse
from subscriptions.models import CircleUser
from django.core.exceptions import ValidationError

# Inicializa o logger para registrar erros
logger = logging.getLogger(__name__)

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
    """Função principal para processar o upload de usuários Circle."""
    try:
        reader = csv.DictReader(file.read().decode('utf-8').splitlines())
    except Exception as e:
        logger.error(f"Erro ao ler o arquivo CSV: {e}")
        raise ValidationError("O arquivo não está no formato CSV correto.")

    for row_number, row in enumerate(reader, start=1):
        try:
            data = {
                map_column_to_field(column): parse_field(map_column_to_field(column), value)
                for column, value in row.items() if map_column_to_field(column)
            }

            # Validação extra para garantir que os campos obrigatórios existam
            validate_required_fields(data)

            # Salva ou atualiza o usuário Circle
            CircleUser.objects.update_or_create(
                email=data['email'],
                defaults=data
            )
        except ValidationError as e:
            logger.error(f"Erro de validação na linha {row_number}: {e}")
        except Exception as e:
            logger.error(f"Erro inesperado ao processar a linha {row_number}: {e}")
            raise ValidationError(f"Erro ao processar a linha {row_number}: {e}")


def validate_required_fields(data):
    """Verifica se os campos obrigatórios estão presentes e são válidos."""
    required_fields = ['email', 'user_id', 'first_name', 'last_name']

    for field in required_fields:
        if not data.get(field):
            raise ValidationError(f"O campo obrigatório {field} está ausente ou vazio.")

    # Validação do formato do e-mail
    if 'email' in data and '@' not in data['email']:
        raise ValidationError(f"E-mail inválido: {data['email']}")


def parse_date_field(value):
    """Converte a string de data para datetime ou retorna None se estiver vazia."""
    try:
        return parse(value) if value else None
    except ValueError:
        raise ValidationError(f"Data inválida: {value}")


def parse_tags_field(value):
    """Converte o campo tags de JSON para uma lista ou retorna uma lista vazia."""
    try:
        return json.loads(value) if value else []
    except json.JSONDecodeError:
        raise ValidationError(f"Erro ao decodificar o campo de tags: {value}")


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
