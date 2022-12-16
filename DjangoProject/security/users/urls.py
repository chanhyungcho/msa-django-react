from django.urls import re_path as url
from security.users import views

urlpatterns = [
    url(r'users', views.users),
    url(r'login', views.users)
]