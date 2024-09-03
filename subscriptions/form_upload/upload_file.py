from django.shortcuts import redirect, render

from subscriptions.form_upload.model_handlers.circle_user import handle_circle_user_form_upload
from subscriptions.form_upload.model_handlers.hotmart_user import \
    handle_hotmart_subscription_form_upload
from subscriptions.form_upload.upload_file_form import ModelChoiceUploadForm


HANDLE_FUNCTIONS = {
    'circle_user': handle_circle_user_form_upload,
    'hotmart_subscriptions': handle_hotmart_subscription_form_upload
}


def upload_file(request):
    if request.method == 'POST':
        form = ModelChoiceUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            model_choice = form.cleaned_data['model_choice']

            # Use o mapa para chamar a função correta
            handle_function = HANDLE_FUNCTIONS.get(model_choice)
            if handle_function:
                handle_function(file)
            else:
                # Tratar o caso onde a escolha não é válida (opcional)
                pass

            return redirect('success')
    else:
        form = ModelChoiceUploadForm()
    return render(request, 'upload.html', {'form': form})
