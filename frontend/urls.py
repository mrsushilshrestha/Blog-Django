from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    # Creation URL should come before slug URL patterns
    path('post/create/', views.create_post, name='create_post'),
    
    # Other specific URLs with slugs
    path('post/<slug:slug>/edit/', views.edit_post, name='edit_post'),
    path('post/<slug:slug>/delete/', views.delete_post, name='delete_post'),
    path('post/<slug:slug>/like/', views.like_post, name='like_post'),
    
    # Generic post detail URL should come after more specific post URLs
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    
    # User URLs
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='frontend/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
] 