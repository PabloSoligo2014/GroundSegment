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
from django.conf.urls import url
from django.contrib import admin
from GroundSegment.views import AboutView, SatelliteListView, PropagationTestView

# Text to put at the end of each page's <title>.
admin.site.site_title = 'MDIAE Ground Segment'

# Text to put in each page's <h1>.
admin.site.site_header = 'MDIAE Ground Segment'

# Text to put at the top of the admin index page.
admin.site.index_title = 'Control Panel'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^about/$', AboutView.as_view(template_name="about.html")),
    url(r'^satellites/$', SatelliteListView.as_view(template_name="satelliteListView.html")),
    url(r'^propagationTest/$', PropagationTestView.as_view(template_name="propagationTest.html")),
]
