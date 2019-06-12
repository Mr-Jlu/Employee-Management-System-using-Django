from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from employees.views import homepage

urlpatterns = [
    path('home/', include('employees.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^employees/', include('employees.urls', namespace='employees')),
    url(r'^$', homepage, name='main_home'),
    url(r'^payslip/', include('payslip.urls')),
    # url(r'^payslip/', include('payslip.urls', namespace='pay')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

