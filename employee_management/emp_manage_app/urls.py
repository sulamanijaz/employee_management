from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /polls/
    url(r'^$', views.index_home, name='index'),
    url(r'^login/$', views.login_user, name='login_user'),
    url(r'^home/$', views.user_home, name='user_home'),
    url(r'^logout/$', views.user_logout, name='logout_user'),

    # ex: /polls/5/

]