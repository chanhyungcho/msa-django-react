from django.urls import re_path as url
from admin.dlearn import fashion_view

urlpatterns = [
    url(r'fashion', fashion_view.fashion),
    # url(r'fashion/(?P<test_num>)$', fashion_views.fashion),
]