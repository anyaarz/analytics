from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^domain/$', views.DomainListView.as_view(), name = 'domain'),
    url(r'^domain/new/$', views.post_domain, name='post_domain'),
    url(r'^domain/(?P<pk>\d+)/edit/$', views.edit_domain, name='edit_domain'),
    url(r'^items/$', views.ItemsListView.as_view(), name = 'items'),
    url(r'^relation/$', views.RelationListView.as_view(), name = 'relation'),
    url(r'^evaluate/$', views.post_value, name = 'value'),
    url(r'^upload/$', views.upload, name = 'upload'),
    url(r'^relation/new/$', views.post_relation, name='post_relation'),
    url(r'^relation/(?P<pk>\d+)/edit/$', views.edit_relation, name='edit_relation'),
    url(r'^items/new/$', views.post_item, name='post_items'),
    url(r'^items/(?P<pk>\d+)/edit/$', views.ItemUpdateView.as_view(), name='edit_items'),
    url(r'^items/(?P<pk>\d+)/delete/$', views.item_delete, name='items_delete'),
    url(r'^data/$', views.DataListView.as_view(), name = 'data'),

]
