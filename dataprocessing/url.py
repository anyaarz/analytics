from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^domain/$', views.DomainListView.as_view(), name = 'domains'),
    url(r'^itemss/$', views.ItemsListView.as_view(), name = 'items'),
]