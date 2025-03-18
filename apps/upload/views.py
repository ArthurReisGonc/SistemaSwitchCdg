import os
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from .forms import UploadFileForm

def get_timestamp():
    return timezone.now().strftime('%d-%m-%Y_%H-%M-%S')

def create_upload_directory(timestamp):
    upload_path = os.path.join('uploads', timestamp)
    os.makedirs(upload_path, exist_ok=True)
    return upload_path

def upload_file(request):
    if request.method == 'POST':
        # Depuração: Exibir os dados do request.POST e request.FILES
        print("Dados do formulário (POST):", request.POST)
        print("Arquivos enviados (FILES):", request.FILES)

        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Depuração: Exibir os dados do formulário validados
            print("Dados do formulário validados:", form.cleaned_data)

            timestamp = get_timestamp()
            upload_path = create_upload_directory(timestamp)

            uploaded_files = []
            files = request.FILES.getlist('file')
            if not files:
                return JsonResponse({'error': 'Nenhum arquivo enviado'}, status=400)

            for file in files:
                file_path = os.path.join(upload_path, file.name)
                with open(file_path, 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)
                uploaded_files.append(file.name)

                json_data = {
                    'nomeArquivo': file.name,
                    'caminho': file_path,
                    'numeroArquivos': len(uploaded_files),
                    'dadosFormulario': {
                        'titulo': request.POST.get('titulo'),
                        'dataEntrega': request.POST.get('dataEntrega'),
                        'observacoes': request.POST.get('observacoes'),
                        'formato': request.POST.get('formato'),
                        'corImpressao': request.POST.get('corImpressao'),
                        'impressao': request.POST.get('impressao'),
                        'gramatura': request.POST.get('gramatura'),
                        'papelAdesivo': request.POST.get('papelAdesivo'),
                        'tipoAdesivo': request.POST.get('tipoAdesivo') if request.POST.get('papelAdesivo') == 'sim' else None,
                        'grampos': request.POST.get('grampos'),
                        'espiral': request.POST.get('espiral'),
                        'capaPVC': request.POST.get('capaPVC'),
                        'contato': {
                            'nome': request.POST.get('nome'),
                            'email': request.POST.get('email'),
                        }
                    },
                    'timestamp': timestamp
                }

                json_file_path = os.path.join(upload_path, f"{os.path.splitext(file.name)[0]}.json")
                with open(json_file_path, 'w', encoding='utf-8') as json_file:
                    json.dump(json_data, json_file, ensure_ascii=False, indent=4)

            return JsonResponse({
                'message': 'Upload concluído com sucesso!',
                'arquivos': uploaded_files,
                'numeroArquivos': len(uploaded_files)
            })
        else:
            # Depuração: Exibir erros de validação do formulário
            print("Erros no formulário:", form.errors)
            return JsonResponse({'error': 'Formulário inválido', 'details': form.errors}, status=400)
    else:
        form = UploadFileForm()
    return render(request, 'upload/upload_file.html', {'form': form})