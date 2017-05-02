from django.conf.urls import include, url
from django.contrib import admin
admin.autodiscover()
urlpatterns = [
    # Examples:
    # url(r'^$', 'employee_management.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('employee_management.emp_manage_app.urls'))
]
