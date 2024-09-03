from django import forms


class ModelChoiceUploadForm(forms.Form):
    MODEL_CHOICES = (
        ('circle_user', 'Circle Users'),
        ('hotmart_subscriptions', 'HotMart Subscriptions'),
    )
    model_choice = forms.ChoiceField(choices=MODEL_CHOICES)
    file = forms.FileField()