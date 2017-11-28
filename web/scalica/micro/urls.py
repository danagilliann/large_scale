from django.conf.urls import include, url

from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^home/$', views.home, name='home'),
    url(r'^stream/(?P<user_id>[0-9]+)/$', views.stream, name='stream'),
    url(r'^post/$', views.post, name='post'),
    url(r'^follow/$', views.follow, name='follow'),
    url(r'^register/$', views.register, name='register'),
    url(r'^universities/$', views.universities, name='universities'),
    url(r'^university/(?P<university_id>[0-9]+)/$', views.university, name='university'),
    url(r'^question/(?P<question_id>[0-9]+)/$', views.question, name='question'),
    url(r'^answer/(?P<answer_id>[0-9]+)/$', views.answer, name='answer'),
    url(r'^user/(?P<user_id>[0-9]+)/$', views.user, name='user'),
    url('^', include('django.contrib.auth.urls'))
]
