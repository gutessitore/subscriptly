import requests

from objects.circle.community_member import CommunityMember
from pydantic_core import ValidationError


class CircleAPI:
    def __init__(self, api_key: str):
        self.circle_url = "https://app.circle.so"
        self.auth_headers = {
            "Authorization": f"Token {api_key}"
        }

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
            'password': password, # at least 6 characters, 1 uppercase letter, 1 number, and 1 symbol
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
            return  response_json

        try:
            community_member = CommunityMember(**response_json)
        except ValidationError as e:
            raise ValueError(f"Failed to parse community member: {e}")

        return community_member
