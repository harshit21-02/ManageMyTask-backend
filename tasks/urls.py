"""hackspace URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path

from django.conf.urls.static import static
from django.conf import settings
from . import views
app_name="tasks"
urlpatterns = [
    path('get-todo-list', views.get_todo_list, name="get_todo_list"),  
    path('create-todo-item', views.create_todo_item, name="create_todo_item"),  
    path('get-todo-item/<int:pk>', views.get_todo_item, name="get_todo_item"),
    path('log-deatils/<int:pk>', views.get_log_details, name="get_log_details"),
    path('update-todo-item', views.update_todo_item, name="update_todo_item"),    
    path('delete-todo-item/<int:pk>', views.delete_todo_item, name="delete_todo_item"),
]
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)