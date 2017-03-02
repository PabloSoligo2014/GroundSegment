from django.views.generic import TemplateView
from django.views.generic import ListView, FormView
from GroundSegment.models.Satellite import Satellite
from GroundSegment.forms import PropagateTestForm
from django.http import HttpResponse,HttpResponseRedirect
from GroundSegment.forms import SimulatorForm
from django.template.context_processors import request
from django.contrib.messages.api import success
from django.core.urlresolvers import reverse_lazy
from django.db.models.query import QuerySet
from django.template.base import kwarg_re



from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.core.urlresolvers import reverse #para error reverse c
from django.views.generic.base import View
from django import views
from lxml.html._diffcommand import description
import code
from django.contrib.admin.utils import help_text_for_field
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
from braces.views import LoginRequiredMixin
from GroundSegment.models.Satellite import FormViewSat

@login_required()
def home(request):
    return render_to_response('home.html', {'user': request.user}, context_instance=RequestContext(request))

class TlmyVarTypeView(LoginRequiredMixin, ListView):
    template_name   = "TlmyVarType.html"
    model           = TlmyVarType
    QuerySet        = TlmyVarType.objects.all()
    context_object_name = "TlmyVarTypes"


class SatelliteListView(LoginRequiredMixin,ListView):
    model = Satellite
    template_name = "satelliteListView.html"
    paginate_by = '5'
    queryset = Satellite.objects.all()
    context_object_name = "satellites"

@login_required()
def post_Sat(request):
        form = FormViewSat()
        return render(request, 'sat_form.html', {'form': form})


