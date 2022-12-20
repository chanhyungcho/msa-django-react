from django.urls import re_path as url
from webcrawler import views as view_crawler

urlpatterns = [
    url(r'crawler', view_crawler.crawler)
]