from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'community'

urlpatterns = [
    # community/
    path('', views.home, name='home'),

    # community/write/
    # path('write/', views.write, name='write'),
    path('write/', views.PostCreateView.as_view(), name='post_new'),

    # community/list/
    path('list/', views.list, name='list'),

    # community/<num>/
    path('detail/<int:article_id>/', views.detail, name='detail'),

    # community/login/
    path('login/', views.login, name='login'),

    # community/login/signup/
    path('login/signup', views.signup, name='signup'),

    # community/logout/
    path('logout/', views.logout, name='logout'),

    path('index/', views.index, name='index'),


]
