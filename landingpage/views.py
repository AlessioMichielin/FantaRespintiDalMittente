from django.shortcuts import render
from accounts.models import Sfide
from django.views.generic.base import TemplateView

# Create your views here.

def index(request):
    return render(request, 'landingpage/index.html')

def regole(request):
    return render(request, 'landingpage/regole.html')

class ListaSfideView(TemplateView):
    
    template_name = 'landingpage/lista-sfide.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sfide'] = Sfide.objects.all().order_by('punti')
        return context
