"""OPSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.views.static import serve
from django.conf.urls.static import static
from DashBoard import views
from django.conf.urls import handler404, handler500


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_URL}),
    url(r'^user_access/', include('UserAccess.urls')),
    url(r'^weekly_report/', include('WeeklyReport.urls')),
    url(r'^dashboard/', include('DashBoard.urls')),
    url(r'^cobbler/', include('Cobbler.urls')),
    url(r'^asset/', include('Asset.urls')),
    url(r'^$', views.index, name="index"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "DashBoard.views.page_not_found"
handler500 = "DashBoard.views.page_error"
