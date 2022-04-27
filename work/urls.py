from django.conf.urls import url
from work import views

urlpatterns = [
    url(r'^$', views.work_index),
]
