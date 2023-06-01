from django.shortcuts import render

# Create your views here.

# views.py
from django.shortcuts import render
from django.views.generic import TemplateView
import requests

class ModelListView(TemplateView):
    template_name = 'model-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        response = requests.get('http://127.0.0.1:8000/producto/')  # Reemplaza la URL con la de tu API REST
        context['productos'] = response.json()
        return context