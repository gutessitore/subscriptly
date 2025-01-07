from typing import List, Optional, Dict
from pydantic import BaseModel, HttpUrl, field_validator
from datetime import datetime


class BaseModelWithDatetime(BaseModel):
    """
    Base model with a validator for datetime fields handling 'UTC' suffix.
    """

    @field_validator("*", mode="before")
    def parse_datetime_fields(cls, value, info):
        """
        Parse datetime fields with 'UTC' suffix into valid datetime objects.
        """
        if isinstance(value, str) and "UTC" in value:
            value = value.replace("UTC", "").strip()
            try:
                return datetime.fromisoformat(value)
            except ValueError:
                raise ValueError(f"Invalid datetime format: {value}")
        return value




class CommunityMemberProfileField(BaseModelWithDatetime):
    """
    Represents additional details for a specific profile field in a community member's profile.

    Attributes:
        id (int): Unique identifier for the profile field detail.
        text (Optional[str]): Text value for the field (if applicable).
        textarea (Optional[str]): Textarea value for the field (if applicable).
        created_at (datetime): Timestamp of when the field detail was created.
        updated_at (datetime): Timestamp of the last update to the field detail.
        display_value (Optional[str]): Display value of the field.
        community_member_choices (List[dict]): Choices associated with the field (if applicable).
    """
    id: int
    text: Optional[str]
    textarea: Optional[str]
    created_at: datetime
    updated_at: datetime
    display_value: Optional[str]
    community_member_choices: List[dict]


class ProfileFieldPage(BaseModelWithDatetime):
    """
    Represents a page where a specific profile field is visible or editable.

    Attributes:
        id (int): Unique identifier for the page.
        name (str): Name of the page (e.g., "edit_profile", "profile_view").
        position (int): Position of the field on the page.
        visible (bool): Indicates if the field is visible on the page.
        created_at (datetime): Timestamp of when the page configuration was created.
        updated_at (datetime): Timestamp of the last update to the page configuration.
    """
    id: int
    name: str
    position: int
    visible: bool
    created_at: datetime
    updated_at: datetime


class ProfileField(BaseModelWithDatetime):
    """
    Represents a custom profile field in a community member's profile.

    Attributes:
        id (int): Unique identifier for the profile field.
        label (str): Label of the profile field.
        field_type (str): Type of the field (e.g., "text", "textarea", "link").
        key (str): Key used to reference the field programmatically.
        placeholder (Optional[str]): Placeholder text for the field.
        description (Optional[str]): Description of the field's purpose.
        required (bool): Indicates whether the field is required.
        platform_field (bool): Indicates if the field is a platform-defined field.
        created_at (datetime): Timestamp of when the field was created.
        updated_at (datetime): Timestamp of the last update to the field.
        community_member_profile_field (Optional[CommunityMemberProfileField]): Details about the field's content.
        number_options (Optional[dict]): Number formatting options (if applicable).
        choices (List[dict]): Choices available for the field (if applicable).
        pages (List[ProfileFieldPage]): Pages where the field is visible or editable.
    """
    id: int
    label: str
    field_type: str
    key: str
    placeholder: Optional[str]
    description: Optional[str]
    required: bool
    platform_field: bool
    created_at: datetime
    updated_at: datetime
    community_member_profile_field: Optional[CommunityMemberProfileField]
    number_options: Optional[dict]
    choices: List[dict]
    pages: List[ProfileFieldPage]


class MemberTag(BaseModelWithDatetime):
    """
    Represents a tag associated with a community member's profile.

    Attributes:
        name (str): Name of the tag.
        id (int): Unique identifier for the tag.
    """
    name: str
    id: int


class CommunityMember(BaseModelWithDatetime):
    """
    Represents a member of a community on the Circle.so platform.

    Attributes:
        id (int): Unique identifier for the community member's profile.
        first_name (str): First name of the member.
        last_name (str): Last name of the member.
        headline (Optional[str]): Member's headline or short description (e.g., job title or tagline).
        bio (Optional[str]): A brief biography or description about the member.
        created_at (datetime): Timestamp of when the profile was created.
        updated_at (datetime): Timestamp of the last update to the profile.
        community_id (int): Identifier for the community the member belongs to.
        last_seen_at (datetime): Timestamp of the member's last activity in the platform.
        profile_url (HttpUrl | str): Public URL to the member's profile.
        public_uid (str): Public unique identifier for the member's profile.
        profile_fields (List[ProfileField]): Custom fields in the member's profile, including their structure, values, and metadata.
        flattened_profile_fields (Dict[str, Optional[str]]): A simplified dictionary view of profile fields with key-value pairs.
        avatar_url (Optional[HttpUrl | str]): URL to the member's avatar image.
        user_id (int): Unique identifier for the user associated with the profile.
        name (str): Full name of the member.
        email (str): Email address associated with the member.
        topics_count (int): Number of topics created by the member.
        posts_count (int): Number of posts made by the member.
        comments_count (int): Number of comments made by the member.
        location (Optional[str]): The member's location.
        website_url (Optional[HttpUrl | str]): URL to the member's personal website or portfolio.
        instagram_url (Optional[HttpUrl | str]): URL to the member's Instagram profile.
        twitter_url (Optional[HttpUrl | str]): URL to the member's Twitter profile.
        linkedin_url (Optional[HttpUrl | str]): URL to the member's LinkedIn profile.
        facebook_url (Optional[HttpUrl | str]): URL to the member's Facebook profile.
        accepted_invitation (datetime): Timestamp of when the member accepted their invitation to join the platform.
        active (bool): Indicates whether the member's profile is currently active.
        sso_provider_user_id (Optional[str]): Single Sign-On (SSO) provider user ID, if applicable.
        member_tags (List[MemberTag]): List of tags associated with the member's profile.
        activity_score (Dict[str, int]): Dictionary containing the activity scores of the member.
    """
    id: int
    first_name: str
    last_name: str
    headline: Optional[str]
    bio: Optional[str]
    created_at: datetime
    updated_at: datetime
    community_id: int
    last_seen_at: datetime
    profile_url: HttpUrl | str
    public_uid: str
    profile_fields: List[ProfileField]
    flattened_profile_fields: Dict[str, Optional[str]]
    avatar_url: Optional[HttpUrl | str]
    user_id: int
    name: str
    email: str
    topics_count: int
    posts_count: int
    comments_count: int
    location: Optional[str]
    website_url: Optional[HttpUrl | str]
    instagram_url: Optional[HttpUrl | str]
    twitter_url: Optional[HttpUrl | str]
    linkedin_url: Optional[HttpUrl | str]
    facebook_url: Optional[HttpUrl | str]
    accepted_invitation: datetime
    active: bool
    sso_provider_user_id: Optional[str]
    member_tags: List[MemberTag]
    activity_score: Dict[str, int]
