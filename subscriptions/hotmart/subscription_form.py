from django import forms


class HotmartSubscriptionForm(forms.Form):
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('DELAYED', 'Delayed'),
        ('CANCELLED_BY_CUSTOMER', 'Cancelled by Customer'),
        ('CANCELLED_BY_SELLER', 'Cancelled by Seller'),
        ('CANCELLED_BY_ADMIN', 'Cancelled by Admin'),
        ('STARTED', 'Started'),
        ('OVERDUE', 'Overdue'),
    ]

    statuses = forms.MultipleChoiceField(
        choices=STATUS_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Subscription Status"
    )
