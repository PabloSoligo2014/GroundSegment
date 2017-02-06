from django.views.generic import TemplateView
from django.views.generic import ListView, FormView
from GroundSegment.models.Satellite import Satellite
from GroundSegment.forms import PropagateTestForm
from django.http import HttpResponse
from GroundSegment.forms import SimulatorForm


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
    
"""
WEB SERVICE
"""

from django.shortcuts import render
from GroundSegment.models.DCPData import DCPData
from GroundSegment.serializer import DCPDataSerializer
#from rest_framework.viewsets import ModelViewSet
from rest_framework import generics
from datetime import datetime

class DCPDataList(generics.ListAPIView):
    serializer_class = DCPDataSerializer

    def get_queryset(self):
        """
        This view should return a list of all the files for
        the user as determined by the file_name portion of the URL.
        """
 #       dcp_name = self.kwargs['dcp_platform']

        start_date = self.kwargs['start_date']
        end_date = self.kwargs['end_date']
#         
        anio1=int(start_date[0:4])
        mes1=int(start_date[4:6])
        dia1=int(start_date[6:8])
         
        anio2=int(end_date[0:4])
        mes2=int(end_date[4:6])
        dia2=int(end_date[6:8])
          
        f1=datetime(anio1,mes1,dia1,0,0,0)
        f2=datetime(anio2,mes2,dia2,23,59,0)
        
        return DCPData.objects.filter(dataTime__range=(f1,f2))

# class DCPDataViewSet(ModelViewSet):
#     queryset = DCPData.objects.all()
#     serializer_class = DCPDataSerializer