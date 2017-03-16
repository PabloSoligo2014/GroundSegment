'''
Created on Mar 13, 2017

@author: ubuntumate
'''
from django.views.generic.list import ListView
from GroundSegment.models.Pasada import Pasada
from django.db.models import Q
from GroundSegment.models.Satellite import Satellite
from GroundSegment.models.Sitio import Sitio
from datetime import datetime
import dateutil.parser

class PassView(ListView):
    model = Pasada
    
    template_name = "pasadas.html"
    paginate_by = 50
    
    def get_queryset(self):
        
        try:
            filter_desde    =    dateutil.parser.parse(self.request.GET.get('tbdesde', 'fecha desde'))
        except:
            filter_desde = datetime.now()
            
        try:
            filter_hasta    =    dateutil.parser.parse(self.request.GET.get('tbhasta', 'fecha hasta'))
        except:
            filter_hasta   = datetime.now()
            
        try:
            filter_sat      =    int(self.request.GET.get('tbsatellite', 'seleccione satelite'))
        except:
            filter_sat = -1
            
        try:
            filter_site  =    int(self.request.GET.get('tbsitio', 'seleccione sitio'))
        except:
            filter_site = -1
            
        #order = self.request.GET.get('orderby', 'give-default-value')
        
        self.current_sat_id    = filter_sat
        self.current_site_id   = filter_site
        
        try:
            sat = Satellite.objects.get(pk=filter_sat)
            
        except:
            sat=None
        try:
            site = Sitio.objects.get(pk=filter_site)
            
        except:
            site = None
           
        self.satellite = sat 
        self.sitio = site 
            
        if sat!=None and site!=None:
            new_context = site.getPasses(sat, filter_desde, filter_hasta)
        else:
            new_context = []
            
        
        #TODO TERMINAR ESTO Deberia funcionar ya    
        #new_context = Pasada.objects.filter(Q(passGeneration__satellite__pk=filter_sat) & Q(passGeneration__sitio__pk=filter_site) ).order_by('startTime')
        
        return new_context

    def get_context_data(self, **kwargs):
        context = super(PassView, self).get_context_data(**kwargs)
        
        context['sat_list']         = Satellite.objects.all()  
        context['site_list']        = Sitio.objects.all()  
        
        
        context['tbsatellite']      = self.request.GET.get('tbsatellite', 'give-default-value')
        context['tbsitio']          = self.request.GET.get('tbsitio', 'give-default-value')
        context['tbdesde']          = self.request.GET.get('tbdesde', 'give-default-value')
        context['tbhasta']          = self.request.GET.get('tbhasta', 'give-default-value')
        
        context['current_sat_id']   = self.current_sat_id
        context['current_site_id']  = self.current_site_id
        context['satellite']        = self.satellite
        context['sitio']            = self.sitio
        
        
        #context['orderby'] = self.request.GET.get('orderby', 'give-default-value')
        
        return context