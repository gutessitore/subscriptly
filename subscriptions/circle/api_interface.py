import requests

from objects.circle.community_member import CommunityMember
from pydantic_core import ValidationError

from subscriptions.models import CircleUser


class CircleAPI:
    def __init__(self, api_key: str):
        self.circle_url = "https://app.circle.so"
        self.auth_headers = {
            "Authorization": f"Token {api_key}"
        }

    def get_space_ids(self, community_id: int) -> list[int]:
        endpoint = "/api/v1/spaces"
        url = f"{self.circle_url}{endpoint}?community_id={community_id}"
        response = requests.get(url, headers=self.auth_headers)

        if not response.ok:
            raise ValueError(f"Failed to get space IDs: {response.status_code} - {response.text}")

        return [space['id'] for space in response.json()]

    def remove_member_from_spaces(self, member_email: str, community_id: int) -> requests.Response:

        spaces = self.get_space_ids(community_id)

        endpoint = "/api/v1/space_members"
        url_params = f"?community_id={community_id}&email={member_email}"
        url = f"{self.circle_url}{endpoint}{url_params}"

        for space_id in spaces:
            response = requests.delete(url + f"&space_id={space_id}", headers=self.auth_headers)

            if not response.ok:
                raise ValueError(
                    f"Failed to remove member from space group: {response.status_code} - {response.text}"
                )

        return response

    def remove_member_from_community(self, member_email: str, community_id: int) -> requests.Response:
        endpoint = "/api/v1/community_members"
        url_params = f"?community_id={community_id}&email={member_email}"
        url = f"{self.circle_url}{endpoint}{url_params}"

        response = requests.delete(url, headers=self.auth_headers)

        if not response.ok:
            raise ValueError(
                f"Failed to remove member from community: {response.status_code} - {response.text}"
            )

        return response

    def invite_community_member(
            self,
            member_email: str,
            member_name: str,
            community_id: int,
            member_tag_ids: list[int],
            space_ids: list[int],
            password: str
    ) -> requests.Response:

        endpoint = "/api/v1/community_members"
        url = f"{self.circle_url}{endpoint}"

        payload = {
            'email': member_email,
            'name': member_name,
            'community_id': community_id,
            'member_tag_ids': member_tag_ids,
            'space_ids': space_ids,
            'password': password,  # at least 6 characters, 1 uppercase letter, 1 number, and 1 symbol
            'skip_invitation': True
        }

        response = requests.post(url, headers=self.auth_headers, data=payload)

        if not response.ok:
            raise ValueError(
                f"Failed to invite community member: {response.status_code} - {response.text}")

        return response

    def get_community_member(self, community_member_email: str, community_id: int) -> CommunityMember | dict:
        endpoint = f"/api/v1/community_members/search"
        url_params = f"?community_id={community_id}&email={community_member_email}"
        url = f"{self.circle_url}{endpoint}{url_params}"
        response = requests.get(url, headers=self.auth_headers)

        if not response.ok:
            raise ValueError(f"Failed to get community member: {response.status_code} - {response.text}")

        response_json = response.json()
        if response_json.get("success") is False:
            return response_json

        try:
            community_member = CommunityMember(**response_json)
        except ValidationError as e:
            raise ValueError(f"Failed to parse community member: {e}")

        return community_member

    def fetch_community_members(self) -> list[dict]:
        """
        Itera sobre as páginas da API e retorna todos os membros da comunidade.
        """
        endpoint = "/api/v1/community_members"
        url = f"{self.circle_url}{endpoint}?sort=latest&per_page=100&page={{}}"

        page = 1
        members = []
        is_last_page = False

        while not is_last_page:
            try:
                response = requests.get(url.format(page), headers=self.auth_headers)
                response.raise_for_status()
                data = response.json()

                if not data:
                    is_last_page = True

                members.extend(data)
                page += 1

            except requests.exceptions.RequestException as e:
                raise ValueError(f"Error fetching community members on page {page}: {e}")

        return members

    def process_and_save_community_members(self, members: list[dict]):
        """
        Processa e salva os membros da comunidade no banco de dados.
        """
        for member_number, member_data in enumerate(members, start=1):
            try:
                self._save_community_member(member_data)
            except ValidationError as e:
                print(f"Validation error for member #{member_number}: {e}")
            except Exception as e:
                raise ValueError(f"Unexpected error for member #{member_number}: {e}")

    @staticmethod
    def _save_community_member(data: dict):
        """
        Salva ou atualiza um membro da comunidade no banco de dados.
        """
        CircleUser.objects.update_or_create(
            email=data['email'],
            defaults={
                'user_id': data.get('id'),
                'first_name': data.get('first_name'),
                'last_name': data.get('last_name') or ' ',
                'member_since': data.get('profile_confirmed_at'),
                'active_status': 'active' if data.get('active') else 'inactive',
                # Define status padrão
                'tags': [tag['name'] for tag in data.get('member_tags', [])],
                # Extrai nomes das tags
                'location': data.get('location') or '',
                'headline': data.get('headline'),
                'bio': data.get('bio') or '',
                'profile_url': data.get('profile_url'),
                'website': data.get('website_url') or '',
                'twitter_url': data.get('twitter_url') or '',
                'facebook_url': data.get('facebook_url') or '',
                'linkedin_url': data.get('linkedin_url') or '',
                'instagram_url': data.get('instagram_url') or '',
                'num_posts': data.get('posts_count', 0),
                'num_comments': data.get('comments_count', 0),
                'num_likes_received': data.get('activity_score', {}).get('likes', 0),
                'image_url': data.get('avatar_url'),
                'last_active': data.get('last_seen_at')
            }
        )

