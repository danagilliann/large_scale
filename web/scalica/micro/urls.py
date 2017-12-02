from django.conf.urls import include, url

from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^home/$', views.home, name='home'),
    url(r'^register/$', views.register, name='register'),
    url(r'^universities/$', views.universities, name='universities'),
    url(r'^university/(?P<university_id>[0-9]+)/$', views.university, name='university'),
    url(r'^question/(?P<question_id>[0-9]+)/$', views.question, name='question'),
    url(r'^answer/(?P<answer_id>[0-9]+)/$', views.answer, name='answer'),
    url(r'^user/(?P<user_id>[0-9]+)/$', views.user, name='user'),
    url(r'^post_university/$', views.post_university, name='post_university'),    
    url(r'^post_question/(?P<university_id>[0-9]+)/$', views.post_question, name='post_question'),
    url(r'^post_answer/(?P<question_id>[0-9]+)/$', views.post_answer, name='post_answer'),
    url('^', include('django.contrib.auth.urls'))
]
