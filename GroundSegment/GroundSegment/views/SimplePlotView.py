'''
Created on Feb 23, 2017

@author: ubuntumate
'''

from django.views.generic import TemplateView
from GroundSegment.models.TlmyVarType import TlmyVarType


#url(r'ajax/getchartdata/$', GetChartData.as_view(), name='getchartdata'), 

class GetChartData(TemplateView):
    def get(self, request, *args, **kwargs):
        pass
        
class SimplePlotView(TemplateView):
    #http://127.0.0.1:8000/simplePlot/100001-100002-100003-100010
    template_name = 'simplePlot.html'
    #queryset = TmlyVar.objects.filter(code='obcT1').order_by('-created')[:50] 
    #context_object_name = "objects"
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        from graphos.sources.simple import SimpleDataSource
        from graphos.renderers.gchart import LineChart
        from GroundSegment.models.TmlyVar import TmlyVar
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