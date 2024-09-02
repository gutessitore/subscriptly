from django.db import models
from django.utils import timezone


class CircleUser(models.Model):
    user_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    member_since = models.DateTimeField(null=True, blank=True)
    active_status = models.CharField(max_length=5)
    tags = models.JSONField()  # Armazena as etiquetas como uma lista de strings
    location = models.CharField(max_length=100, null=True, blank=True)
    headline = models.CharField(max_length=200, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    profile_url = models.URLField(max_length=200, null=True, blank=True)
    website = models.URLField(max_length=200, null=True, blank=True)
    twitter_url = models.URLField(max_length=200, null=True, blank=True)
    facebook_url = models.URLField(max_length=200, null=True, blank=True)
    linkedin_url = models.URLField(max_length=200, null=True, blank=True)
    instagram_url = models.URLField(max_length=200, null=True, blank=True)
    num_posts = models.IntegerField(default=0)
    num_comments = models.IntegerField(default=0)
    num_likes_received = models.IntegerField(default=0)
    image_url = models.URLField(max_length=200, null=True, blank=True)
    last_active = models.DateTimeField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"

    class Meta:
        verbose_name = "Circle User"
        verbose_name_plural = "Circle Users"


class HotmartSubscription(models.Model):
    subscription_id = models.CharField(max_length=50, unique=True)
    user_id = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    creation_date = models.DateTimeField()
    last_update = models.DateTimeField()
    canceled = models.BooleanField(default=False)
    plan_name = models.CharField(max_length=255)
    plan_id = models.IntegerField()
    recurrency_period = models.IntegerField()
    product_name = models.CharField(max_length=255)
    product_id = models.IntegerField()
    product_ucode = models.CharField(max_length=50)
    currency_code = models.CharField(max_length=10)
    amount_value = models.DecimalField(max_digits=10, decimal_places=2)
    subscriber_name = models.CharField(max_length=255)
    subscriber_ucode = models.CharField(max_length=50)
    subscriber_email = models.EmailField()
    next_billing_date = models.DateTimeField()
    reference_code = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"Subscription {self.subscription_id} - {self.status}"

    class Meta:
        verbose_name = "Hotmart Subscription"
        verbose_name_plural = "Hotmart Subscriptions"
