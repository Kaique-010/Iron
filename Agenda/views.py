from django.db import connections
from django.db import IntegrityError
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from Agenda.models import Evento
from Empresas.models import Empresa, CustomUser
from Agenda.forms import EventoForm
from datetime import timedelta, datetime
import logging
import json

logger = logging.getLogger(__name__)

def set_empresa_database(empresa):
    db_alias = empresa.database  
    if db_alias not in connections:
        raise IntegrityError(f"Banco de dados {db_alias} não configurado.")
    connections['default'] = connections[db_alias]

class AgendaListView(ListView):
    model = Evento
    template_name = 'listar_eventos.html'
    context_object_name = 'Eventos'

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            raise Http404("Usuário não autenticado")
        
        if not self.request.user.empresa:
            raise Http404("Usuário não associado a uma empresa")

        # A partir daqui, garantimos que o usuário está autenticado e possui uma empresa associada
        set_empresa_database(self.request.user.empresa)

        queryset = Evento.objects.filter(user=self.request.user)
        titulo = self.request.GET.get('titulo')
        if titulo:
            queryset = queryset.filter(titulo__icontains=titulo)
        return queryset



class AgendaCreateView(CreateView):
    model = Evento
    template_name = 'criar_evento.html'
    form_class = EventoForm
    success_url = reverse_lazy('listar_eventos')

    def form_valid(self, form):
        if not self.request.user.is_authenticated:
            raise Http404("Usuário não autenticado")
        
        if not self.request.user.empresa:
            raise Http404("Usuário não associado a uma empresa")

        # Definindo a conexão antes de salvar o evento
        set_empresa_database(self.request.user.empresa)
        
        evento = form.save(commit=False)
        evento.user = self.request.user
        evento.empresa = self.request.user.empresa
        
        evento.save()
        return super().form_valid(form)
        
    

class AgendaUpdateView(UpdateView):
    model = Evento
    template_name = 'editar_evento.html'
    form_class = EventoForm
    success_url = reverse_lazy('listar_eventos')
    
    def form_valid(self, form):
        # Antes de salvar, garantimos que a conexão esteja configurada corretamente
        set_empresa_database(self.request.user.empresa)
        
        evento = form.save(commit=False)
        evento.user = self.request.user
        evento.save()
        return super().form_valid(form)

   

class AgendaDetailView(DetailView):
    model = Evento
    template_name = 'detalhe_evento.html'

    def get_object(self):
        # Defina a conexão aqui antes de consultar o banco
        set_empresa_database(self.request.user.empresa)
        return super().get_object()

   


class AgendaDeleteView(DeleteView):
    model = Evento
    template_name = 'excluir_evento.html'
    success_url = reverse_lazy('listar_eventos')

    def get_object(self):
        # Defina a conexão aqui antes de consultar o banco
        set_empresa_database(self.request.user.empresa)
        return super().get_object()

    


@login_required
def eventos_json(request):
    if not request.user.empresa:
        logger.error("Tentativa de acesso a eventos sem empresa associada.")
        return JsonResponse({'error': 'Empresa não encontrada.'}, status=404)

    agora = timezone.now()
    proximos_eventos = Evento.objects.filter(
        user=request.user,
        data_inicio__gte=agora,
        data_inicio__lte=agora + timedelta(days=30)
    ).order_by('data_inicio')
    
    eventos = [
        {
            'id': evento.id,
            'title': evento.titulo,
            'start': datetime.combine(evento.data_inicio, evento.horario).isoformat(),
            'end': (datetime.combine(evento.data_inicio, evento.horario) + timedelta(hours=1)).isoformat(),
            'location': evento.local,
            'description': evento.descricao,
        }
        for evento in proximos_eventos
    ]
    
    return JsonResponse({'events': eventos}, encoder=CustomJSONEncoder)


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()  
        return super().default(obj)

    
    

@login_required
def eventos_futuros_json(request):
    if not request.user.empresa:
        return JsonResponse({'error': 'Usuário não associado a nenhuma empresa.'}, status=404)
    
    try:
        eventos_futuros = Evento.objects.filter(
            data_inicio__gte=timezone.now(),
            data_inicio__lte=timezone.now() + timedelta(days=30)
        ).order_by('data_inicio')

        eventos = [
            {
                'id': evento.id,
                'titulo': evento.titulo,
                'inicio': evento.data_inicio.isoformat(),
                'fim': (evento.data_inicio + timedelta(hours=1)).isoformat(),
                'local': evento.local,
                'descricao': evento.descricao,
            }
            for evento in eventos_futuros
        ]
        return JsonResponse({'eventos': eventos}, status=200)

    except Exception as e:
        return JsonResponse({'error': f'Erro ao recuperar eventos: {str(e)}'}, status=500)


@login_required 
def eventos_futuros(request):
    if request.user.is_authenticated:
        
        eventos_futuros = Evento.objects.filter(
            data_inicio__gte=timezone.now(),
            data_inicio__lte=timezone.now() + timedelta(days=30)
        ).order_by('data_inicio')
        
        return render(request, 'eventos_futuros.html', {'eventos': eventos_futuros})
    else:
        # Caso o usuário não tenha uma empresa associada
        logger.warning(f"Usuário {request.user.username} não tem empresa associada.")
        return redirect('sem_empresa')  # Redireciona para uma página que pode informar sobre a ausência de empresa
    