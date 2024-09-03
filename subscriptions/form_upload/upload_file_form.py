from django import forms


class ModelChoiceUploadForm(forms.Form):
    MODEL_CHOICES = (
        ('circle_user', 'Circle'),
        ('hotmart_subscriptions', 'HotMart'),
    )
    model_choice = forms.ChoiceField(choices=MODEL_CHOICES, label='Escolha o modelo')
    file = forms.FileField()