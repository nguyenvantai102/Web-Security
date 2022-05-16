from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.loginUser, name='login'),
    path('register/', views.registerPage, name='register'),
    path('logout/', views.logoutUser, name='logout'),
    path('admin_page', views.admin, name='manage'),
    path('profile/', views.user_page, name='profile'),
    path('user-settings/', views.account_setting, name='settings'),
    
    # About, Service
    path('about', views.about_view, name='about'),
    path('propose', views.propose, name='propose'),
    path('service', views.get_info, name='service'),

]
