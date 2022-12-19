from django.urls import re_path as url
from admin.dlearn.iris import view as iris_view
from admin.dlearn.fashion import view as fashion_view
from admin.dlearn.mnist import view as mnist_view

urlpatterns = [
    url(r'iris', iris_view.iris),
    url(r'fashion', fashion_view.fashion),
    url(r'mnist', mnist_view.mnist)
]