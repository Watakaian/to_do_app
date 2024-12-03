"""
URL configuration for main app.

The `urlpatterns` list routes URLs to views. 
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from main import views
from django.contrib.auth import views as auth_views
from .views import CustomPasswordChangeView

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path('logout/', views.custom_logout, name='logout'),
    path('add/', views.add_todo, name='add_todo'),
    path('todo/', views.todo_list, name="todo"),
    path('<int:pk>/update/', views.update_todo, name='update_todo'),
    path('<int:pk>/delete/', views.delete_todo, name='delete_todo'),
    path('<int:pk>/', views.todo_detail, name='todo_detail'),
    path('complete/<int:pk>/', views.mark_as_complete, name='mark_as_complete'),
    path('completed/', views.completed_todos, name='completed_todos'),
    path('password-change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('password-change-success/', views.password_change_success, name='custom_success_page'),
    path('profile/', views.profile, name='profile'),
    path('delete_profile/', views.delete_profile, name='delete_profile'),
]
