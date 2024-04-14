from django.contrib.auth import views as auth_views
from django.urls import path

from . import views


app_name = 'creator'


urlpatterns = [
    path('mypage/', views.mypage, name='mypage'),
    path('creators/', views.creators, name='creators'),
    path('creators/<int:pk>/', views.creator, name='creator'),
    path('edit/', views.edit, name='edit'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='creator/login.html'), name='login'),
]