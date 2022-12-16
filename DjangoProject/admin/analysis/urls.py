from django.urls import re_path as url

from admin.analysis import views

urlpatterns = [
    url(r'stroke', views.stroke)
]