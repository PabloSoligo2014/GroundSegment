'''
Created on Feb 23, 2017

@author: ubuntumate
'''

from django.views.generic import TemplateView
from GroundSegment.models.TlmyVarType import TlmyVarType
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta


#url(r'ajax/getchartdata/$', GetChartData.as_view(), name='getchartdata'), 

class GetChartData(TemplateView):
    def get(self, request, *args, **kwargs):
        pass
        
class SimplePlotView(TemplateView):
    #http://127.0.0.1:8000/simplePlot/100001-100002-100003-100010
    template_name = 'simplePlot.html'
    #queryset = TlmyVar.objects.filter(code='obcT1').order_by('-created')[:50] 
    #context_object_name = "objects"
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        from graphos.sources.simple import SimpleDataSource
        from graphos.renderers.gchart import LineChart
        from GroundSegment.models.TmlyVar import TlmyVar
        tvtVector = []

        tvts = self.kwargs['tvts']
        
        tvts = tvts.split('-')
        
        for pk in tvts:        
            tvt = TlmyVarType.objects.get(pk=pk)
            tvtVector.append(tvt)
        
        context = super(SimplePlotView, self).get_context_data(**kwargs)
        
        valuesVector = []
        
        minutes = int(self.kwargs['minutes'])
         
        now = timezone.now()
        for tvt in tvtVector:
            if minutes==-1:
                valuesVector.append(TlmyVar.objects.filter(tmlyVarType=tvt).order_by('created')[:50]) 
            else:
                vars = TlmyVar.objects.filter(Q(tmlyVarType=tvt) & Q(created__gte=now-timedelta(minutes=minutes) ) ).order_by('created') 
                valuesVector.append(vars)
            
        
        i = 0
        context['charts'] = []
        
        for values in valuesVector:
            data = []
            data.append(['Fecha', tvtVector[i].code])
            if values.count()==0:
                data.append([0,0])
            else:
                for v in values:
                    data.append( [v.created.strftime("%H:%M:%-S"), v.getValue()]   )
                
            data_source = SimpleDataSource(data=data)
            # Chart object
            chart = LineChart(data_source)
            chart.options['title']      = tvtVector[i].description+ " (Ultimos valores)"  
            chart.options['subtitle']   = "Ultimos valores"  
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
