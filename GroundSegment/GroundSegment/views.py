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
    
class SimplePlotView(TemplateView):
    #http://127.0.0.1:8000/simplePlot/100001-100002-100003-100010
    template_name = 'simplePlot.html'
    #queryset = TmlyVar.objects.filter(code='obcT1').order_by('-created')[:50] 
    #context_object_name = "objects"
    
    
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        
        from graphos.sources.simple import SimpleDataSource
        from graphos.renderers.gchart import LineChart
        tvtVector = []
        
        
        
        tvts = self.kwargs['tvts']
        
        tvts = tvts.split('-')
        
        for pk in tvts:        
            tvt = TlmyVarType.objects.get(pk=pk)
            tvtVector.append(tvt)
        
        context = super(SimplePlotView, self).get_context_data(**kwargs)
        
        valuesVector = []
        
        for tvt in tvtVector:
            valuesVector.append(TmlyVar.objects.filter(tmlyVarType=tvt).order_by('created')[:50]) 
        
        
        
        i = 0
        context['charts'] = []
        for values in valuesVector:
            data = []
            data.append(['Fecha', tvtVector[i].code])
            for v in values:
                data.append( [v.created.strftime("%H:%M:%-S"), v.getValue()]   )
            
            data_source = SimpleDataSource(data=data)
            # Chart object
            chart = LineChart(data_source)
            chart.options['title']      = tvtVector[i].description+ " (Ultimos 50 valores)"  
            chart.options['subtitle']   = "Ultimos 50 valores"  
            #chart.options['width']      = 200
            chart.options['height']     = 300
            chart.options['isStacked']     = 'relative'
            
            #chart.options['lineWidth']  = 5 
            chart.options['smooth']     = False
            
            
            chart.options['series'] =    { 
                                          '0': { 'color': '#DB3411' }
                                         }
                                        
            """
            series: {
            0: { color: '#e2431e' },
            1: { color: '#e7711b' },
            2: { color: '#f1ca3a' },
            3: { color: '#6f9654' },
            4: { color: '#1c91c0' },
            5: { color: '#43459d' },
                    }
            """
            
            #chart.options['curveType']  = 'function'
            
            
            chart.options['legend']  = { 'position': 'bottom' }
            
            #legend: { position: 'bottom' }
            
            
            
            i=i+1
            context['charts'].append(chart)
            
        
        
        return context
    
    #return render(request, 'yourtemplate.html', context)
  
    
    
    
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
    
    



