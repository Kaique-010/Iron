from django.http import JsonResponse
from rest_framework import generics
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from . import models, forms
from .forms import EventoForm
from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import datetime, timedelta

class AgendaListView(ListView):
    model = models.Evento
    template_name = 'listar_eventos.html'
    context_object_name = 'Eventos'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().order_by('data_inicio', 'horario')  # Ordena por data e horário
        titulo = self.request.GET.get('titulo')

        if titulo:
            queryset = queryset.filter(titulo__icontains=titulo)

        return queryset

class AgendaCreateView(CreateView):
    model = models.Evento
    template_name = 'criar_evento.html'
    form_class = forms.EventoForm
    success_url = reverse_lazy('listar_eventos')

class AgendaDetailView(DetailView):
    model = models.Evento
    template_name = 'detalhe_evento.html'


class AgendaUpdateView(UpdateView):
    model = models.Evento
    template_name = 'editar_evento.html'
    form_class = forms.EventoForm
    success_url = reverse_lazy('listar_eventos')



class AgendaDeleteView(DeleteView):
    model = models.Evento
    template_name = 'excluir_evento.html'
    success_url = reverse_lazy('listar_eventos')


def listar_eventos(request):
    eventos = models.Evento.objects.all()
    now = timezone.now()

    context = {
        'Eventos': eventos,
        'now': now.isoformat(),  
    }
    return render(request, 'listar_eventos.html', context)

def eventos_futuros_json(request):
    agora = timezone.now()
    proximos_eventos = models.Evento.objects.filter(
        data_inicio__gte=agora,
        data_inicio__lte=agora + timedelta(minutes=6000) 
    ).order_by('data_inicio')
    
    eventos = list(proximos_eventos.values(
        'titulo', 'data_inicio', 'horario', 'local', 'descricao'
    ))
    
    return JsonResponse({'eventos': eventos})