from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'community'

urlpatterns = [
    # community/
    path('', views.home, name='home'),

    # community/write/
    path('write/', views.write, name='write'),

    # community/list/
    path('list/', views.list, name='list'),

    # community/<num>/
    url('view/(?P<article_id>[0-9]+)/$', views.view, name='view'),

    # community/login/
    path('login/', views.login, name='login'),

    # community/login/signup/
    path('login/signup', views.signup, name='signup'),

    # community/logout/
    path('logout/', views.logout, name='logout'),
]
