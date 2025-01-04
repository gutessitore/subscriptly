from dataclasses import dataclass
from typing import Optional


@dataclass
class CommunityMember:
    """
    CommunityMember

    Represents a member of a Circle community with optional fields for additional information.

    Attributes:
        email (str): The email address of the member. Required.
        password (str): The password for the member. Optional. Must be at least 6 characters, include 1 uppercase letter, 1 number, and 1 symbol (!, $, @, *, etc.).
        name (str): The full name of the member. Required.
        community_id (str): The ID of the community to which the member belongs. Required.
        avatar (Optional[str]): URL for the member's avatar image. Optional. Can only be set if the member does not already have an account with Circle.
        headline (Optional[str]): A short description or title for the member. Optional. Can only be set if the member does not already have an account.
        bio (Optional[str]): A short biography of the member. Optional. Max length: 250 characters. Can only be set if the member does not already have an account.
        location (Optional[str]): The city of the member. Optional.
        website_url (Optional[str]): The member's website URL. Optional.
        twitter_url (Optional[str]): The Twitter profile URL of the member. Optional.
        facebook_url (Optional[str]): The Facebook profile URL of the member. Optional.
        instagram_url (Optional[str]): The Instagram profile URL of the member. Optional.
        linkedin_url (Optional[str]): The LinkedIn profile URL of the member. Optional.
        space_ids (list[int]): IDs of spaces the member should be added to. Optional.
        space_group_ids (list[int]): IDs of space groups the member should be added to. Optional.
        member_tag_ids (list[int]): IDs of member tags assigned to the member. Optional.
        skip_invitation (bool): Whether to skip sending an invitation email. If true, no email is sent, and no password is set. Optional.
        is_flagged (bool): Indicates whether the member is flagged. Optional.
        preferences (dict): Preferences for the member, such as messaging settings. Optional.
        community_member_profile_fields (dict): Dynamic key-value pairs representing additional profile fields for the member. Optional.
    """

    email: str  # Email of the buyer from Hotmart
    password: str  # Password for the account
    name: str  # Name of the buyer from Hotmart
    community_id: str  # ID of the community -94039-
    avatar: Optional[str]  # URL of the avatar image
    headline: Optional[str]  # Headline of the member
    bio: Optional[str]  # Short bio of the member
    location: Optional[str]  # Member's location
    website_url: Optional[str]  # Personal or business website URL
    twitter_url: Optional[str]  # Twitter profile URL
    facebook_url: Optional[str]  # Facebook profile URL
    instagram_url: Optional[str]  # Instagram profile URL
    linkedin_url: Optional[str]  # LinkedIn profile URL
    space_ids: list[int]  # IDs of spaces the member belongs to
    space_group_ids: list[int]  # IDs of space groups the member belongs to
    member_tag_ids: list[int]  # IDs of member tags
    skip_invitation: bool  # Whether to skip sending an invitation
    is_flagged: bool  # Whether the member is flagged
    preferences: dict[str, bool]  # Preferences such as messaging settings
    community_member_profile_fields: dict[str, Optional[str]]  # Additional profile fields like nickname, business description, etc.

    __plan_type: PlanType  # Plan type of the member

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2)


class PlanType(Enum):
    """
    Only annual members have access to space with id 790485.
    """
    annual = "annual" # member_tag_id = 85328
    quarterly = "quarterly" # member_tag_id = 125528


