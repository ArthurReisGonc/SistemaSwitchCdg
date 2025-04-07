import os
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from .forms import UploadFileForm
from django.contrib import messages
import pandas as pd
from django.core.files.storage import FileSystemStorage



def get_timestamp():
    return timezone.now().strftime('%d-%m-%Y_%H-%M-%S')

def create_upload_directory(timestamp):
    upload_path = os.path.join('uploads', timestamp)
    os.makedirs(upload_path, exist_ok=True)
    return upload_path

def formulario_padrao(request):
    print("entrou aqui")
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
    return render(request, 'upload/formulario_padrao.html', {'form': form})


def formulario_rapido(request):
    print("Entrou na view formulario_rapido")

    if request.method == 'POST':
        print("Recebendo um POST request...")
        print("Dados do formulário (POST):", request.POST)
        print("Arquivos enviados (FILES):", request.FILES)

        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            print("Formulário válido:", form.cleaned_data)

            files = request.FILES.getlist('file')
            if not files:
                print("Erro: Nenhum arquivo enviado")
                return JsonResponse({'error': 'Nenhum arquivo enviado'}, status=400)

            timestamp = get_timestamp()
            upload_path = create_upload_directory(timestamp)
            os.makedirs(upload_path, exist_ok=True)  # Garante que a pasta existe

            uploaded_files = []

            for file in files:
                file_path = os.path.join(upload_path, file.name)
                with open(file_path, 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)

                uploaded_files.append(file.name)
            
                # Criar e salvar os metadados do upload em um JSON
                json_data = {
                    'nomeArquivo': file.name,
                    'caminho': file_path,
                    'numeroArquivos': len(files),
                    'qtde': int(request.POST.get('qtde', 0) or 0),
                    'nomeUnidade': {
                            'ARARUAMA': int(request.POST.get('ARARUAMA', 0) or 0),
                            'CABO_FRIO': int(request.POST.get('CABO_FRIO', 0) or 0),
                            'ITABORAI': int(request.POST.get('ITABORAI', 0) or 0),
                            'ITAIPUACU': int(request.POST.get('ITAIPUACU', 0) or 0),
                            'MARICA_I': int(request.POST.get('MARICA_I', 0) or 0),
                            'NOVA_FRIBURGO': int(request.POST.get('NOVA_FRIBURGO', 0) or 0),
                            'QUEIMADOS': int(request.POST.get('QUEIMADOS', 0) or 0),
                            'SEROPEDICA': int(request.POST.get('SEROPEDICA', 0) or 0),
                            'ALCANTARA': int(request.POST.get('ALCANTARA', 0) or 0),
                            'BANGU': int(request.POST.get('BANGU', 0) or 0),
                            'BARRA_DA_TIJUCA': int(request.POST.get('BARRA_DA_TIJUCA', 0) or 0),
                            'BELFORD_ROXO': int(request.POST.get('BELFORD_ROXO', 0) or 0),
                            'DUQUE_DE_CAXIAS': int(request.POST.get('DUQUE_DE_CAXIAS', 0) or 0),
                            'ICARAI': int(request.POST.get('ICARAI', 0) or 0),
                            'ILHA_DO_GOVERNADOR': int(request.POST.get('ILHA_DO_GOVERNADOR', 0) or 0),
                            'ITAIPU': int(request.POST.get('ITAIPU', 0) or 0),
                            'MADUREIRA': int(request.POST.get('MADUREIRA', 0) or 0),
                            'MEIER': int(request.POST.get('MEIER', 0) or 0),
                            'NILOPOLIS': int(request.POST.get('NILOPOLIS', 0) or 0),
                            'NITEROI': int(request.POST.get('NITEROI', 0) or 0),
                            'NOVA_IGUACU': int(request.POST.get('NOVA_IGUACU', 0) or 0),
                            'OLARIA': int(request.POST.get('OLARIA', 0) or 0),
                            'PRATA': int(request.POST.get('PRATA', 0) or 0),
                            'SAO_GONCALO': int(request.POST.get('SAO_GONCALO', 0) or 0),
                            'SAO_JOAO_DE_MERITI': int(request.POST.get('SAO_JOAO_DE_MERITI', 0) or 0),
                            'VILA_ISABEL': int(request.POST.get('VILA_ISABEL', 0) or 0),
                            'VILAR_DOS_TELES': int(request.POST.get('VILAR_DOS_TELES', 0) or 0),
                    },
                    'dadosFormulario': {
                        'titulo': request.POST.get('titulo'),
                        'dataEntrega': request.POST.get('dataEntrega'),
                        'observacoes': request.POST.get('observacoes'),
                        'formato': request.POST.get('formato'),
                        'corImpressao': request.POST.get('corImpressao'),
                        'impressao': request.POST.get('impressao'),
                        'gramatura': request.POST.get('gramatura'),
                        'papelAdesivo': None,
                        'tipoAdesivo': request.POST.get('tipoAdesivo') if request.POST.get('papelAdesivo') == 'sim' else None,
                        'grampos': request.POST.get('grampos'),
                        'espiral': None,
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

            print(f"Upload concluído! {len(uploaded_files)} arquivos salvos.")

            # Ajustando a resposta para garantir o formato desejado
            return JsonResponse({
                'message': 'Upload concluído com sucesso!',
                'arquivos': uploaded_files,
                'numeroArquivos': len(uploaded_files)
            })

        else:
            print("Erros no formulário:", form.errors)
            return JsonResponse({'error': 'Formulário inválido', 'details': form.errors}, status=400)

    else:
        form = UploadFileForm()

    return render(request, 'upload/formulario_rapido.html', {'form': form})

def formulario_rapido_excel(request):
    print("Entrou na view formulario_rapido_excel")
    if request.method == 'POST':
        print("Recebendo um POST request...")
        print("Dados do formulário (POST):", request.POST)
        print("Arquivos enviados (FILES):", request.FILES)

        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            print("Formulário válido:", form.cleaned_data)

            files = request.FILES.getlist('file')
            if not files:
                print("Erro: Nenhum arquivo PDF enviado")
                return JsonResponse({'error': 'Nenhum arquivo PDF enviado'}, status=400)

            timestamp = get_timestamp()
            upload_path = create_upload_directory(timestamp)
            os.makedirs(upload_path, exist_ok=True)  # Garante que a pasta existe

            excel_file = request.FILES.get("excel_file")
            print("Arquivo Excel:", excel_file)
            if not excel_file:
                print("Erro: Nenhum arquivo Excel enviado")
                return JsonResponse({'error': 'Nenhum arquivo Excel enviado'}, status=400)

            # Salvando o arquivo Excel
            excel_path = os.path.join(upload_path, excel_file.name)
            with open(excel_path, 'wb+') as destination:
                for chunk in excel_file.chunks():
                    destination.write(chunk)

            # Lendo o Excel
            df = pd.read_excel(excel_path)
            uploaded_files = []

            for file in files:
                # Salvar o PDF
                pdf_path = os.path.join(upload_path, file.name)
                with open(pdf_path, 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)

                uploaded_files.append(file.name)

                # Nome do JSON baseado no nome do PDF
                json_filename = os.path.splitext(file.name)[0] + ".json"
                json_path = os.path.join(upload_path, json_filename)

                json_data = {
                    'nomeArquivo': file.name,
                    'caminho': pdf_path,
                    'numeroArquivos': len(files),
                    'qtde': df.iloc[11:38, 1:3].sum().sum() if len(df) > 11 and df.shape[1] > 1 else None,
                    'nomeUnidade': request.POST.get('nomeUnidade'),
                    'dadosFormulario': {
                        'titulo': request.POST.get('titulo'),
                        'dataEntrega': request.POST.get('dataEntrega'),
                        'observacoes': request.POST.get('observacoes'),
                        'formato': df.iloc[1, 2] if len(df) > 1 and df.shape[1] > 2 else None,
                        'corImpressao': df.iloc[2, 2] if len(df) > 2 and df.shape[1] > 2 else None,
                        'impressao': df.iloc[3, 2] if len(df) > 3 and df.shape[1] > 2 else None,
                        'gramatura': df.iloc[4, 2] if len(df) > 4 and df.shape[1] > 2 else None,
                        'papelAdesivo': df.iloc[5, 2] if len(df) > 5 and df.shape[1] > 2 else None,
                        'tipoAdesivo': 'Não',
                        'grampos': df.iloc[6, 2] if len(df) > 6 and df.shape[1] > 2 else None,
                        'espiral': df.iloc[7, 2] if len(df) > 7 and df.shape[1] > 2 else None,
                        'capaPVC': df.iloc[8, 2] if len(df) > 8 and df.shape[1] > 2 else None,
                        'contato': {
                            'nome': request.POST.get('nome'),
                            'email': request.POST.get('email'),
                        }
                    },
                    'timestamp': timestamp
                }

                # Criando JSON correspondente ao PDF
                with open(json_path, 'w', encoding='utf-8') as json_file:
                    json.dump(json_data, json_file, ensure_ascii=False, indent=4)

            print(f"Upload concluído! {len(uploaded_files)} arquivos salvos.")

            return JsonResponse({
                'message': 'Upload concluído com sucesso!',
                'arquivos': uploaded_files,
                'numeroArquivos': len(uploaded_files)
            })

        else:
            print("Erros no formulário:", form.errors)
            return JsonResponse({'error': 'Formulário inválido', 'details': form.errors}, status=400)

    else:
        form = UploadFileForm()

    return render(request, 'upload_excel/formulario_rapido_excel.html', {'form': form})

def formulario_completo(request):
    print("Entrou na view formulario_completo")

    



