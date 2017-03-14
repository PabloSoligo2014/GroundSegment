"""GroundSegment URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from GroundSegment.views.views import AboutView, SatelliteListView, PropagationTestView, DCPDataViewSet,TlmyVarTypeView,post_Sat
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.routers import SimpleRouter
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from GroundSegment.models import TlmyVarType
from aptsources.distinfo import Template
from GroundSegment.models.TlmyVarType import TlmyVarType
from GroundSegment.views.SimplePlotView import SimplePlotView, GetChartData



#from django.contrib.auth import views as auth_views
from django.contrib.auth.views import login, logout
import GroundSegment
#from DistUpgrade.DistUpgradeViewGtk3 import view
from GroundSegment import views
from GroundSegment.views.PassView import PassView


# Text to put at the end of each page's <title>.
admin.site.site_title = 'MDIAE Ground Segment'

# Text to put in each page's <h1>.
admin.site.site_header = 'MDIAE Ground Segment'
  

# Text to put at the top of the admin index page.
admin.site.index_title = 'Control Panel'

router = SimpleRouter()
router.register(r'DCPData', DCPDataViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^login/$', login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout$', logout, {'template_name': 'login.html', }, name="logout"),
    url(r'^home/$', GroundSegment.views.views.home, name='home'),
    url(r'^home/TlmyVarType/$', TlmyVarTypeView.as_view(), name='TlmyVarType'),
    url(r'^about/$', AboutView.as_view(template_name="about.html")),
    url(r'^home/satellites/$', SatelliteListView.as_view(),name="satelliteListView"),
    url(r'^home/satellites/sat_form/$', GroundSegment.views.views.post_Sat, name="post_Sat"),
    url(r'^propagationTest/$', PropagationTestView.as_view(template_name="propagationTest.html")),
    url(r'^', include(router.urls)),
    url(r'^simplePlot/(?P<tvts>[\w-]+)', SimplePlotView.as_view(template_name="simplePlot.html"), name='SimplePlotView'), 
    url(r'^pasadas/$', PassView.as_view(), name='PassView'),
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    
