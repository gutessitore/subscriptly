from django.shortcuts import redirect, render
from django.contrib import messages

from subscriptions.circle.handle_circle_user_upload import handle_circle_user_form_upload
from subscriptions.circle.upload_file_form import ModelChoiceUploadForm


HANDLE_FUNCTIONS = {
    'circle_user': handle_circle_user_form_upload
}


def upload_file(request):
    if request.method != 'POST':
        form = ModelChoiceUploadForm()
        return render(request, 'upload.html', {'form': form})

    form = ModelChoiceUploadForm(request.POST, request.FILES)
    if not form.is_valid():
        messages.error(request, "Formulário inválido. Verifique os dados.")
        return render(request, 'upload.html', {'form': form})

    file = request.FILES['file']
    model_choice = form.cleaned_data['model_choice']

    handle_function = HANDLE_FUNCTIONS.get(model_choice)
    if not handle_function:
        messages.error(request, "Opção de modelo inválida.")
        return render(request, 'upload.html', {'form': form})

    try:
        handle_function(file)
    except Exception as e:
        messages.error(request, f"Erro ao processar o arquivo: {str(e)}")
        return render(request, 'upload.html', {'form': form})

    messages.success(request, 'Upload realizado com sucesso!')
    return redirect('hotmart/extract')
