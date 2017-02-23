from django.views.generic import TemplateView
from django.views.generic import ListView, FormView
from GroundSegment.models.Satellite import Satellite
from GroundSegment.forms import PropagateTestForm
from django.http import HttpResponse
from GroundSegment.forms import SimulatorForm
from django.template.context_processors import request
from django.contrib.messages.api import success
from django.core.urlresolvers import reverse_lazy
from django.db.models.query import QuerySet
from django.template.base import kwarg_re

"""
Autorefresh para vistas de telemetria en tiempo real...
http://www.b-list.org/weblog/2006/jul/31/django-tips-simple-ajax-example-part-1/
"""

class AboutView(TemplateView):
    template_name = "about.html"
    
  
    
    
    
class SimulatorView(FormView):
    template_name = 'simulators.html'
    form_class = SimulatorForm
    success_url = '/thanks/'
    
    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.alarmSimulator()
        return super(PropagationTestView, self).form_valid(form)
    
    
class SatelliteListView(ListView):
    
    model = Satellite
    template_name = "satelliteListView.html"
    paginate_by = '5'
    queryset = Satellite.objects.all()
    context_object_name = "satellites"
    
    
class PropagationTestView(FormView):
    
    template_name = 'propagationTest.html'
    form_class = PropagateTestForm
    success_url = '/thanks/'
    
    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.propagate()
        return super(PropagationTestView, self).form_valid(form)
    
    
  

    """
    def head(self, *args, **kwargs):
        
        last_sat = self.get_queryset().latest('publication_date')
        
        response = HttpResponse('')
        # RFC 1123 date format
        response['Last-sat'] = last_book.publication_date.strftime('%a, %d %b %Y %H:%M:%S GMT')
        return response
    """
# #Importamos el formulario de autenticación de django
# from django.contrib.auth.forms import AuthenticationForm
# from django.contrib.auth import login
# #autent de usuarioss
#     
# class LoginView(FormView):
#     template_name   = "login.html"
#     form_class  = AuthenticationForm
#     success_url = reverse_lazy("Principal")##
#     
#     def ingreso(self, form):
#         login(self.request, form.get_user())
#         return super(LoginView, self).form_valid(form)
#         
    
"""
WEB SERVICE
"""

from django.shortcuts import render
from GroundSegment.models.DCPData import DCPData
from GroundSegment.serializer import DCPDataSerializer
from rest_framework.viewsets import ModelViewSet


class DCPDataViewSet(ModelViewSet):
    queryset = DCPData.objects.all()
    serializer_class = DCPDataSerializer
  

from GroundSegment.models.TlmyVarType import TlmyVarType


class TlmyVarTypeView(ListView):
    model = TlmyVarType
    template_name = "TlmyVarType.html"
    QuerySet = TlmyVarType.objects.all()[:5]
    context_object_name = "TlmyVarTypes"
    
    


