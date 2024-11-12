from datetime import datetime
from django.utils import timezone
from django import forms
from django.conf import settings
import environ
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.db import connections, transaction
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied
from django.utils.functional import cached_property
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Sum, F
from Empresas.models import CustomUser, Empresa, Licenca
from Produtos.models import Produtos
from Entradas_Produtos.models import Entrada_Produtos
from Saidas_Produtos.models import Saida_Produtos
from Agenda.models import Evento
import logging
from django.db.utils import OperationalError
import django.db
from django.db import connections
from django.core.exceptions import ImproperlyConfigured


logger = logging.getLogger(__name__)

from django.db import connections
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from django.contrib.auth import get_user_model, authenticate, login
from django.db import connections, OperationalError


def login_view(request):
    if request.method == 'POST':
        document = request.POST.get('document')
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            empresa = Empresa.objects.using('default').get(document=document)
        except Empresa.DoesNotExist:
            messages.error(request, "Empresa não encontrada.")
            return render(request, 'login.html')

        empresa_banco = empresa.database  

        try:
            with connections[empresa_banco].cursor() as cursor:
                User = get_user_model()
                try:
                    user = User.objects.using(empresa_banco).get(username=username, empresa_id=empresa.id)
                    if user.check_password(password):
                        login(request, user)

                        # Salvar informações na sessão
                        request.session['empresa_id'] = empresa.id
                        request.session['empresa_name'] = empresa.name  
                        request.session['usuario_nome'] = user.username
                        request.session['empresa_database'] = empresa_banco

                        messages.success(request, "Login realizado com sucesso.")
                        print("Sessão após login:", request.session.items())
                        return redirect('home')  # Nome da URL de redirecionamento após o login
                    else:
                        messages.error(request, "Credenciais inválidas ou empresa incorreta.")
                except User.DoesNotExist:
                    messages.error(request, "Usuário não encontrado na empresa especificada.")
        
        except OperationalError:
            messages.error(request, "Erro de conexão com o banco de dados da empresa.")
    
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect('login')


'''def calcular_metricas_produtos(request):
    
    empresa_banco = request.session.get("empresa_database", None)
    
    if not empresa_banco:
        # Retorna ou lança um erro caso o banco de dados da empresa não esteja definido
        raise ValueError("Nenhuma empresa associada ao usuário.")
    
    # Verifica se a conexão com o banco de dados da empresa existe
    if empresa_banco not in connections:
        # Caso a conexão não exista, retorna ou lança um erro
        raise ValueError(f"A conexão com o banco de dados '{empresa_banco}' não existe.")
    
    # Realiza as consultas no banco de dados associado à empresa
    total_produtos = Produtos.objects.using(empresa_banco).count()
    total_produtos_ativos = Produtos.objects.using(empresa_banco).filter(ativo=True).count()
    total_produtos_inativos = Produtos.objects.using(empresa_banco).filter(ativo=False).count()
    total_saldo_produtos = Produtos.objects.using(empresa_banco).aggregate(total_quantidade=Sum('quantidade'))['total_quantidade'] or 0
    valor_estoque = Produtos.objects.using(empresa_banco).annotate(
        valor_total=Sum(F('quantidade') * F('precos__preco_compra'))
    ).aggregate(total_valor_estoque=Sum('valor_total'))['total_valor_estoque'] or 0
    total_entradas = Entrada_Produtos.objects.using(empresa_banco).count()
    total_saidas = Saida_Produtos.objects.using(empresa_banco).count()
    total_quantidade_entradas = Entrada_Produtos.objects.using(empresa_banco).aggregate(total=Sum('quantidade'))['total'] or 0
    total_quantidade_saidas = Saida_Produtos.objects.using(empresa_banco).aggregate(total=Sum('quantidade'))['total'] or 0
    total_movimentacoes = total_quantidade_entradas + total_quantidade_saidas

    return {
        'total_produtos': total_produtos,
        'total_produtos_ativos': total_produtos_ativos,
        'total_produtos_inativos': total_produtos_inativos,
        'total_saldo_produtos': total_saldo_produtos,
        'valor_estoque': valor_estoque,
        'total_entradas': total_entradas,
        'total_saidas': total_saidas,
        'total_quantidade_entradas': total_quantidade_entradas,
        'total_quantidade_saidas': total_quantidade_saidas,
        'total_movimentacoes': total_movimentacoes,
    }'''

class HomeView(View):
    def get(self, request, *args, **kwargs):
        #metricas = calcular_metricas_produtos(request)
        usuario_nome = request.session.get('usuario_nome', 'Usuário não encontrado')
        empresa_nome = request.session.get('empresa_name', 'Empresa não definida')  
        context = {
            #'produtos_metricas': metricas,
            'mostrar_modal': True,
            'usuario_nome': usuario_nome,
            'empresa_nome': empresa_nome,
        }
        return render(request, 'home.html', context)


@login_required
class ListarEventos(View):
    def get(self, request, *args, **kwargs):
        empresa_db = request.session.get("empresa_db", "default")
        eventos = Evento.objects.using(empresa_db).filter(user=request.user)
        return render(request, 'listar_eventos.html', {'eventos': eventos})


@user_passes_test(lambda u: u.is_superuser)
def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
           
            empresa = form.cleaned_data.get("empresa")
            if empresa:
                connection_name = empresa.database  
            else:
                connection_name = 'default'

            # Salva o usuário na base da empresa selecionada
            with transaction.atomic(using=connection_name):
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password1'])
                user.empresa = empresa
                user.save(using=connection_name) 
            
            success_message = f"Usuário criado com sucesso na empresa '{empresa}' e salvo no banco '{connection_name}'."
            return render(request, 'register_user.html', {'form': form, 'success_message': success_message})
        
        else:
            return render(request, 'register_user.html', {'form': form, 'errors': form.errors})
    else:
        form = CustomUserCreationForm()
        
    return render(request, 'register_user.html', {'form': form})


def empresa_inativa(request):
    # Retorne uma resposta informando que a empresa não está ativa
    return render(request, 'empresa_inativa.html')
