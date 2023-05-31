from django.urls import path
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import views as auth_views
from home import views

urlpatterns = [
    path('', views.home, name='home'),
    path('user_login/', views.login_user, name='login'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('logout/', views.logoutUser, name='logout'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('change_password/', views.change_password, name='change_password'),
    path('profile/', views.profile, name='profile'),
    path('update_profile/', views.update_profile, name='update_profile'),

]