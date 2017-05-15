from django.conf.urls import url


from . import views
from employee_management.emp_manage_app.views import ContactWizard
from employee_management.emp_manage_app.forms import signupform1, signupform2

urlpatterns = [
    # ex: /polls/
    url(r'^$', views.index_home, name='index'),
    url(r'^login/$', views.login_user, name='login_user'),
    url(r'^home/$', views.user_home, name='user_home'),
    url(r'^logout/$', views.user_logout, name='logout_user'),
    url(r'^add_user/$', views.add_sub_user, name='add_sub_user'),
    url(r'^upload_avatar/$', views.upload_image, name='upload_avatar'),
    url(r'^add_user/(?P<msg>[\w\-]+)/$', views.add_sub_user),
    url(r'^schedule/$', views.emp_schedule, name='emp_schedule'),
    url(r'^schedule_detail/(?P<id>[\d\-]+)/$$', views.emp_detail_shift, name='emp_schedule_detail'),
    url(r'^signup/$', ContactWizard.as_view([signupform1, signupform2]), name='signup_user'),

    # ex: /polls/5/

]
