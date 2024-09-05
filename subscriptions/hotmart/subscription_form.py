from django import forms


class HotmartSubscriptionForm(forms.Form):
    STATUS_CHOICES = [
        ('ACTIVE', 'Ativa'),
        ('INACTIVE', 'Inativa'),
        ('DELAYED', 'Atrasada'),
        ('CANCELLED_BY_CUSTOMER', 'Cancelada pelo Cliente'),
        ('CANCELLED_BY_SELLER', 'Cancelada pelo Vendedor'),
        ('CANCELLED_BY_ADMIN', 'Cancelada pelo Admin'),
        ('STARTED', 'Iniciada'),
        ('OVERDUE', 'Vencida'),
    ]

    statuses = forms.MultipleChoiceField(
        choices=STATUS_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Subscription Status",
        initial=['ACTIVE', 'CANCELLED_BY_CUSTOMER', 'CANCELLED_BY_SELLER', 'CANCELLED_BY_ADMIN']
    )
