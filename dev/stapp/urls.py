from django.conf.urls import url
from django.urls import path
from . import views
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('', views.index,name='index'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('login/', auth_view.LoginView.as_view(template_name='user/login.html'), name="login"),
    path('logout/', auth_view.LogoutView.as_view(template_name='user/logout.html'), name="logout"),
    path('edit_profile/', views.edit_profile,name='edit_profile'),
    url(r'^delete_user/(?P<pk>.*)', views.delete_user, name='delete_user'),
    path('pass_request/', views.pass_request,name='pass_request'),
    path('display_request/', views.display_request,name='display_request'),
    path('upload/', views.upload,name='upload'),
]