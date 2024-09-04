from django.shortcuts import redirect, render
from django.contrib import messages

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

            # Verifica se existe uma função associada ao modelo escolhido
            handle_function = HANDLE_FUNCTIONS.get(model_choice)
            if handle_function:
                try:
                    # Chama a função associada para processar o arquivo
                    handle_function(file)
                    messages.success(request, 'Upload realizado com sucesso!')
                    return redirect('success')
                except Exception as e:
                    # Trata erros que possam ocorrer ao processar o arquivo
                    messages.error(request, f"Erro ao processar o arquivo: {str(e)}")
            else:
                messages.error(request, "Opção de modelo inválida.")
        else:
            messages.error(request, "Formulário inválido. Verifique os dados.")
    else:
        form = ModelChoiceUploadForm()

    return render(request, 'upload.html', {'form': form})